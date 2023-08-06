# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (C) 2018-2019 GEM Foundation
#
# OpenQuake is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OpenQuake is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with OpenQuake.  If not, see <http://www.gnu.org/licenses/>.
import collections
import itertools
import operator
import unittest.mock as mock
import numpy
from openquake.baselib import hdf5, datastore, general
from openquake.hazardlib.gsim.base import ContextMaker, FarAwayRupture
from openquake.hazardlib import calc, geo, probability_map
from openquake.hazardlib.geo.mesh import Mesh, RectangularMesh
from openquake.hazardlib.source.rupture import (
    EBRupture, BaseRupture, events_dt)
from openquake.risklib.riskinput import rsi2str
from openquake.commonlib.calc import _gmvs_to_haz_curve

U16 = numpy.uint16
U32 = numpy.uint32
F32 = numpy.float32
by_taxonomy = operator.attrgetter('taxonomy')
code2cls = BaseRupture.init()


def sig_eps_dt(imts):
    """
    :returns: a composite data type for the sig_eps output
    """
    lst = [('eid', U32), ('rlzi', U16)]
    for imt in imts:
        lst.append(('sig_' + imt, F32))
    for imt in imts:
        lst.append(('eps_' + imt, F32))
    return numpy.dtype(lst)


class PmapGetter(object):
    """
    Read hazard curves from the datastore for all realizations or for a
    specific realization.

    :param dstore: a DataStore instance or file system path to it
    :param sids: the subset of sites to consider (if None, all sites)
    :param rlzs_assoc: a RlzsAssoc instance (if None, infers it)
    """
    def __init__(self, dstore, weights, sids=None, poes=()):
        self.dstore = dstore
        self.sids = dstore['sitecol'].sids if sids is None else sids
        if len(weights[0].dic) == 1:  # no weights by IMT
            self.weights = numpy.array([w['weight'] for w in weights])
        else:
            self.weights = weights
        self.poes = poes
        self.num_rlzs = len(weights)
        self.eids = None
        self.nbytes = 0
        self.sids = sids

    @property
    def imts(self):
        return list(self.imtls)

    def init(self):
        """
        Read the poes and set the .data attribute with the hazard curves
        """
        if hasattr(self, '_pmap_by_grp'):  # already initialized
            return self._pmap_by_grp
        if isinstance(self.dstore, str):
            self.dstore = hdf5.File(self.dstore, 'r')
        else:
            self.dstore.open('r')  # if not
        if self.sids is None:
            self.sids = self.dstore['sitecol'].sids
        oq = self.dstore['oqparam']
        self.imtls = oq.imtls
        self.poes = self.poes or oq.poes
        rlzs_by_grp = self.dstore['rlzs_by_grp']
        self.rlzs_by_grp = {k: dset[()] for k, dset in rlzs_by_grp.items()}

        # populate _pmap_by_grp
        self._pmap_by_grp = {}
        if 'poes' in self.dstore:
            # build probability maps restricted to the given sids
            ok_sids = set(self.sids)
            for grp, dset in self.dstore['poes'].items():
                ds = dset['array']
                L, G = ds.shape[1:]
                pmap = probability_map.ProbabilityMap(L, G)
                for idx, sid in enumerate(dset['sids'][()]):
                    if sid in ok_sids:
                        pmap[sid] = probability_map.ProbabilityCurve(ds[idx])
                self._pmap_by_grp[grp] = pmap
                self.nbytes += pmap.nbytes
        return self._pmap_by_grp

    def get_hazard(self, gsim=None):
        """
        :param gsim: ignored
        :returns: R probability curves for the given site
        """
        return self.get_pcurves(self.sids[0])

    def get(self, rlzi, grp=None):
        """
        :param rlzi: a realization index
        :param grp: None (all groups) or a string of the form "grp-XX"
        :returns: the hazard curves for the given realization
        """
        self.init()
        assert self.sids is not None
        pmap = probability_map.ProbabilityMap(len(self.imtls.array), 1)
        grps = [grp] if grp is not None else sorted(self._pmap_by_grp)
        for grp in grps:
            for gsim_idx, rlzis in enumerate(self.rlzs_by_grp[grp]):
                for r in rlzis:
                    if r == rlzi:
                        pmap |= self._pmap_by_grp[grp].extract(gsim_idx)
                        break
        return pmap

    def get_pcurves(self, sid):  # used in classical
        """
        :returns: a list of R probability curves with shape L
        """
        pmap_by_grp = self.init()
        L = len(self.imtls.array)
        pcurves = [probability_map.ProbabilityCurve(numpy.zeros((L, 1)))
                   for _ in range(self.num_rlzs)]
        for grp, pmap in pmap_by_grp.items():
            try:
                pc = pmap[sid]
            except KeyError:  # no hazard for sid
                continue
            for gsim_idx, rlzis in enumerate(self.rlzs_by_grp[grp]):
                c = probability_map.ProbabilityCurve(pc.array[:, [gsim_idx]])
                for rlzi in rlzis:
                    pcurves[rlzi] |= c
        return pcurves

    def get_pcurve(self, s, r, g):  # used in disaggregation
        """
        :param s: site ID
        :param r: realization ID
        :param g: group ID
        :returns: a probability curves with shape L (or None, if missing)
        """
        grp = 'grp-%02d' % g
        pmap = self.init()[grp]
        try:
            pc = pmap[s]
        except KeyError:
            return
        L = len(self.imtls.array)
        pcurve = probability_map.ProbabilityCurve(numpy.zeros((L, 1)))
        for gsim_idx, rlzis in enumerate(self.rlzs_by_grp[grp]):
            for rlzi in rlzis:
                if rlzi == r:
                    pcurve |= probability_map.ProbabilityCurve(
                        pc.array[:, [gsim_idx]])
        return pcurve

    def items(self, kind=''):
        """
        Extract probability maps from the datastore, possibly generating
        on the fly the ones corresponding to the individual realizations.
        Yields pairs (tag, pmap).

        :param kind:
            the kind of PoEs to extract; if not given, returns the realization
            if there is only one or the statistics otherwise.
        """
        num_rlzs = len(self.weights)
        if not kind or kind == 'all':  # use default
            if 'hcurves' in self.dstore:
                for k in sorted(self.dstore['hcurves']):
                    yield k, self.dstore['hcurves/' + k][()]
            elif num_rlzs == 1:
                yield 'mean', self.get(0)
            return
        if 'poes' in self.dstore and kind in ('rlzs', 'all'):
            for rlzi in range(num_rlzs):
                hcurves = self.get(rlzi)
                yield 'rlz-%03d' % rlzi, hcurves
        elif 'poes' in self.dstore and kind.startswith('rlz-'):
            yield kind, self.get(int(kind[4:]))
        if 'hcurves' in self.dstore and kind == 'stats':
            for k in sorted(self.dstore['hcurves']):
                if not k.startswith('rlz'):
                    yield k, self.dstore['hcurves/' + k][()]

    def get_mean(self, grp=None):
        """
        Compute the mean curve as a ProbabilityMap

        :param grp:
            if not None must be a string of the form "grp-XX"; in that case
            returns the mean considering only the contribution for group XX
        """
        self.init()
        if len(self.weights) == 1:  # one realization
            # the standard deviation is zero
            pmap = self.get(0, grp)
            for sid, pcurve in pmap.items():
                array = numpy.zeros(pcurve.array.shape)
                array[:, 0] = pcurve.array[:, 0]
                pcurve.array = array
            return pmap
        else:
            raise NotImplementedError('multiple realizations')


class GmfDataGetter(collections.abc.Mapping):
    """
    A dictionary-like object {sid: dictionary by realization index}
    """
    def __init__(self, dstore, sids, num_rlzs):
        self.dstore = dstore
        self.sids = sids
        self.num_rlzs = num_rlzs
        assert len(sids) == 1, sids

    def init(self):
        if hasattr(self, 'data'):  # already initialized
            return
        self.dstore.open('r')  # if not already open
        try:
            self.imts = self.dstore['gmf_data/imts'][()].split()
        except KeyError:  # engine < 3.3
            self.imts = list(self.dstore['oqparam'].imtls)
        self.rlzs = self.dstore['events']['rlz_id']
        self.data = self[self.sids[0]]
        if not self.data:  # no GMVs, return 0, counted in no_damage
            self.data = {rlzi: 0 for rlzi in range(self.num_rlzs)}
        # now some attributes set for API compatibility with the GmfGetter
        # number of ground motion fields
        # dictionary rlzi -> array(imts, events, nbytes)
        self.E = len(self.rlzs)

    def get_hazard(self, gsim=None):
        """
        :param gsim: ignored
        :returns: an dict rlzi -> datadict
        """
        return self.data

    def __getitem__(self, sid):
        dset = self.dstore['gmf_data/data']
        idxs = self.dstore['gmf_data/indices'][sid]
        if idxs.dtype.name == 'uint32':  # scenario
            idxs = [idxs]
        elif not idxs.dtype.names:  # engine >= 3.2
            idxs = zip(*idxs)
        data = [dset[start:stop] for start, stop in idxs]
        if len(data) == 0:  # site ID with no data
            return {}
        return group_by_rlz(numpy.concatenate(data), self.rlzs)

    def __iter__(self):
        return iter(self.sids)

    def __len__(self):
        return len(self.sids)


class GmfGetter(object):
    """
    An hazard getter with methods .get_gmfdata and .get_hazard returning
    ground motion values.
    """
    def __init__(self, rupgetter, srcfilter, oqparam):
        self.rlzs_by_gsim = rupgetter.rlzs_by_gsim
        self.rupgetter = rupgetter
        self.srcfilter = srcfilter
        self.sitecol = srcfilter.sitecol.complete
        self.oqparam = oqparam
        self.min_iml = oqparam.min_iml
        self.N = len(self.sitecol)
        self.num_rlzs = sum(len(rlzs) for rlzs in self.rlzs_by_gsim.values())
        self.sig_eps_dt = sig_eps_dt(oqparam.imtls)
        M32 = (F32, len(oqparam.imtls))
        self.gmv_eid_dt = numpy.dtype([('gmv', M32), ('eid', U32)])
        md = (calc.filters.IntegrationDistance(oqparam.maximum_distance)
              if isinstance(oqparam.maximum_distance, dict)
              else oqparam.maximum_distance)
        param = {'filter_distance': oqparam.filter_distance,
                 'imtls': oqparam.imtls, 'maximum_distance': md}
        self.cmaker = ContextMaker(
            rupgetter.trt, rupgetter.rlzs_by_gsim, param)
        self.correl_model = oqparam.correl_model

    @property
    def sids(self):
        return self.sitecol.sids

    @property
    def imtls(self):
        return self.oqparam.imtls

    @property
    def imts(self):
        return list(self.oqparam.imtls)

    def init(self):
        """
        Initialize the computers. Should be called on the workers
        """
        if hasattr(self, 'computers'):  # init already called
            return
        self.computers = []
        for ebr in self.rupgetter.get_ruptures(self.srcfilter):
            sitecol = self.sitecol.filtered(ebr.sids)
            try:
                computer = calc.gmf.GmfComputer(
                    ebr, sitecol, self.oqparam.imtls, self.cmaker,
                    self.oqparam.truncation_level, self.correl_model)
            except FarAwayRupture:
                # due to numeric errors, ruptures within the maximum_distance
                # when written, can be outside when read; I found a case with
                # a distance of 99.9996936 km over a maximum distance of 100 km
                continue
            self.computers.append(computer)

    def get_gmfdata(self):
        """
        :returns: an array of the dtype (sid, eid, gmv)
        """
        alldata = []
        self.sig_eps = []
        for computer in self.computers:
            data = computer.compute_all(
                self.min_iml, self.rlzs_by_gsim, self.sig_eps)
            alldata.append(data)
        if not alldata:
            return []
        return numpy.concatenate(alldata)

    def get_hazard_by_sid(self, data=None):
        """
        :param data: if given, an iterator of records of dtype gmf_dt
        :returns: sid -> records
        """
        if data is None:
            data = self.get_gmfdata()
        if len(data) == 0:
            return {}
        return general.group_array(data, 'sid')

    def compute_gmfs_curves(self, rlzs, monitor):
        """
        :param rlzs: an array of shapeE
        :returns: a dict with keys gmfdata, indices, hcurves
        """
        oq = self.oqparam
        with monitor('getting ruptures', measuremem=True):
            self.init()
        hcurves = {}  # key -> poes
        if oq.hazard_curves_from_gmfs:
            hc_mon = monitor('building hazard curves', measuremem=False)
            with monitor('building hazard', measuremem=True):
                gmfdata = self.get_gmfdata()  # returned later
                hazard = self.get_hazard_by_sid(data=gmfdata)
            for sid, hazardr in hazard.items():
                dic = group_by_rlz(hazardr, rlzs)
                for rlzi, array in dic.items():
                    with hc_mon:
                        gmvs = array['gmv']
                        for imti, imt in enumerate(oq.imtls):
                            poes = _gmvs_to_haz_curve(
                                gmvs[:, imti], oq.imtls[imt],
                                oq.ses_per_logic_tree_path)
                            hcurves[rsi2str(rlzi, sid, imt)] = poes
        elif oq.ground_motion_fields:  # fast lane
            with monitor('building hazard', measuremem=True):
                gmfdata = self.get_gmfdata()
        else:
            return dict(gmfdata=(), hcurves=hcurves)
        if len(gmfdata) == 0:
            return dict(gmfdata=[])
        indices = []
        gmfdata.sort(order=('sid', 'eid'))
        start = stop = 0
        for sid, rows in itertools.groupby(gmfdata['sid']):
            for row in rows:
                stop += 1
            indices.append((sid, start, stop))
            start = stop
        res = dict(gmfdata=gmfdata, hcurves=hcurves,
                   sig_eps=numpy.array(self.sig_eps, self.sig_eps_dt),
                   indices=numpy.array(indices, (U32, 3)))
        return res


def group_by_rlz(data, rlzs):
    """
    :param data: a composite array of D elements with a field `eid`
    :param rlzs: an array of E >= D elements
    :returns: a dictionary rlzi -> data for each realization
    """
    acc = general.AccumDict(accum=[])
    for rec in data:
        acc[rlzs[rec['eid']]].append(rec)
    return {rlzi: numpy.array(recs) for rlzi, recs in acc.items()}


def gen_rupture_getters(dstore, slc=slice(None), concurrent_tasks=1,
                        filename=None):
    """
    :yields: RuptureGetters
    """
    try:
        e0s = dstore['eslices'][:, 0]
    except KeyError:
        e0s = None
    if dstore.parent:
        dstore = dstore.parent
    csm_info = dstore['csm_info']
    trt_by_grp = csm_info.grp_by("trt")
    samples = csm_info.get_samples_by_grp()
    rlzs_by_gsim = csm_info.get_rlzs_by_gsim_grp()
    rup_array = dstore['ruptures'][slc]
    maxweight = numpy.ceil(len(rup_array) / (concurrent_tasks or 1))
    nr, ne = 0, 0
    for grp_id, arr in general.group_array(rup_array, 'grp_id').items():
        if not rlzs_by_gsim[grp_id]:
            # this may happen if a source model has no sources, like
            # in event_based_risk/case_3
            continue
        for block in general.block_splitter(arr, maxweight):
            if e0s is None:
                e0 = numpy.zeros(len(block), U32)
            else:
                e0 = e0s[nr: nr + len(block)]
            rgetter = RuptureGetter(
                numpy.array(block), filename or dstore.filename, grp_id,
                trt_by_grp[grp_id], samples[grp_id], rlzs_by_gsim[grp_id], e0)
            yield rgetter
            nr += len(block)
            ne += rgetter.num_events


# this is never called directly; gen_rupture_getters is used instead
class RuptureGetter(object):
    """
    :param rup_array:
        an array of ruptures of the same group
    :param filename:
        path to the HDF5 file containing a 'rupgeoms' dataset
    :param grp_id:
        source group index
    :param trt:
        tectonic region type string
    :param samples:
        number of samples of the group
    :param rlzs_by_gsim:
        dictionary gsim -> rlzs for the group
    """
    def __init__(self, rup_array, filename, grp_id, trt, samples,
                 rlzs_by_gsim, e0=None):
        self.rup_array = rup_array
        self.filename = filename
        self.grp_id = grp_id
        self.trt = trt
        self.samples = samples
        self.rlzs_by_gsim = rlzs_by_gsim
        self.e0 = e0
        n_occ = int(rup_array['n_occ'].sum())
        self.num_events = n_occ if samples > 1 else n_occ * sum(
            len(rlzs) for rlzs in rlzs_by_gsim.values())

    def split(self, srcfilter):
        """
        :returns: a list of RuptureGetters with 1 rupture each
        """
        out = []
        array = self.rup_array
        for i, ridx in enumerate(array['id']):
            rg = object.__new__(self.__class__)
            rg.rup_array = array[i: i+1]
            rg.filename = self.filename
            rg.grp_id = self.grp_id
            rg.trt = self.trt
            rg.samples = self.samples
            rg.rlzs_by_gsim = self.rlzs_by_gsim
            rg.e0 = numpy.array([self.e0[i]])
            n_occ = array[i]['n_occ']
            sids = srcfilter.close_sids(array[i], self.trt)
            rg.weight = len(sids) * n_occ
            if rg.weight:
                out.append(rg)
        return out

    @property
    def num_ruptures(self):
        return len(self.rup_array)

    def get_eid_rlz(self):
        """
        :returns: a composite array with the associations eid->rlz
        """
        eid_rlz = []
        for e0, rup in zip(self.e0, self.rup_array):
            ebr = EBRupture(mock.Mock(rup_id=rup['serial']), rup['srcidx'],
                            self.grp_id, rup['n_occ'], self.samples)
            for rlz_id, eids in ebr.get_eids_by_rlz(self.rlzs_by_gsim).items():
                for eid in eids:
                    eid_rlz.append((eid + e0, rup['id'], rlz_id))
        return numpy.array(eid_rlz, events_dt)

    def get_rupdict(self):
        """
        :returns: a dictionary with the parameters of the rupture
        """
        assert len(self.rup_array) == 1, 'Please specify a slice of length 1'
        dic = {'trt': self.trt, 'samples': self.samples}
        with datastore.read(self.filename) as dstore:
            rupgeoms = dstore['rupgeoms']
            source_ids = dstore['source_info']['source_id']
            rec = self.rup_array[0]
            geom = rupgeoms[rec['gidx1']:rec['gidx2']].reshape(
                rec['sy'], rec['sz'])
            dic['lons'] = geom['lon']
            dic['lats'] = geom['lat']
            dic['deps'] = geom['depth']
            rupclass, surclass = code2cls[rec['code']]
            dic['rupture_class'] = rupclass.__name__
            dic['surface_class'] = surclass.__name__
            dic['hypo'] = rec['hypo']
            dic['occurrence_rate'] = rec['occurrence_rate']
            dic['grp_id'] = rec['grp_id']
            dic['n_occ'] = rec['n_occ']
            dic['serial'] = rec['serial']
            dic['mag'] = rec['mag']
            dic['srcid'] = source_ids[rec['srcidx']]
        return dic

    def get_ruptures(self, srcfilter):
        """
        :returns: a list of EBRuptures filtered by bounding box
        """
        ebrs = []
        with datastore.read(self.filename) as dstore:
            rupgeoms = dstore['rupgeoms']
            for e0, rec in zip(self.e0, self.rup_array):
                if srcfilter.integration_distance:
                    sids = srcfilter.close_sids(rec, self.trt)
                    if len(sids) == 0:  # the rupture is far away
                        continue
                else:
                    sids = None
                mesh = numpy.zeros((3, rec['sy'], rec['sz']), F32)
                geom = rupgeoms[rec['gidx1']:rec['gidx2']].reshape(
                    rec['sy'], rec['sz'])
                mesh[0] = geom['lon']
                mesh[1] = geom['lat']
                mesh[2] = geom['depth']
                rupture_cls, surface_cls = code2cls[rec['code']]
                rupture = object.__new__(rupture_cls)
                rupture.rup_id = rec['serial']
                rupture.surface = object.__new__(surface_cls)
                rupture.mag = rec['mag']
                rupture.rake = rec['rake']
                rupture.hypocenter = geo.Point(*rec['hypo'])
                rupture.occurrence_rate = rec['occurrence_rate']
                rupture.tectonic_region_type = self.trt
                if surface_cls is geo.PlanarSurface:
                    rupture.surface = geo.PlanarSurface.from_array(
                        mesh[:, 0, :])
                elif surface_cls is geo.MultiSurface:
                    # mesh has shape (3, n, 4)
                    rupture.surface.__init__([
                        geo.PlanarSurface.from_array(mesh[:, i, :])
                        for i in range(mesh.shape[1])])
                elif surface_cls is geo.GriddedSurface:
                    # fault surface, strike and dip will be computed
                    rupture.surface.strike = rupture.surface.dip = None
                    rupture.surface.mesh = Mesh(*mesh)
                else:
                    # fault surface, strike and dip will be computed
                    rupture.surface.strike = rupture.surface.dip = None
                    rupture.surface.__init__(RectangularMesh(*mesh))
                grp_id = rec['grp_id']
                ebr = EBRupture(rupture, rec['srcidx'], grp_id,
                                rec['n_occ'], self.samples)
                # not implemented: rupture_slip_direction
                ebr.sids = sids
                ebr.ridx = rec['id']
                ebr.e0 = 0 if self.e0 is None else e0
                ebr.id = rec['id']  # rup_id  in the datastore
                ebrs.append(ebr)
        return ebrs

    def __len__(self):
        return len(self.rup_array)

    def __repr__(self):
        wei = ' [w=%d]' % self.weight if hasattr(self, 'weight') else ''
        return '<%s grp_id=%d, %d rupture(s)%s>' % (
            self.__class__.__name__, self.grp_id, len(self), wei)
