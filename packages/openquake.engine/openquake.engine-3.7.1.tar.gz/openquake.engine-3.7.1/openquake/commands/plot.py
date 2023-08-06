# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (C) 2015-2019 GEM Foundation
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
# along with OpenQuake. If not, see <http://www.gnu.org/licenses/>.
import logging
from openquake.baselib import sap
from openquake.hazardlib import mfd
from openquake.hazardlib.geo.utils import get_bounding_box
from openquake.calculators.extract import Extractor, WebExtractor


def basemap(projection, sitecol):
    from mpl_toolkits.basemap import Basemap  # costly import
    minlon, minlat, maxlon, maxlat = get_bounding_box(sitecol, maxdist=10)
    bmap = Basemap(projection=projection,
                   llcrnrlon=minlon, llcrnrlat=minlat,
                   urcrnrlon=maxlon, urcrnrlat=maxlat,
                   lat_0=sitecol['lat'].mean(), lon_0=sitecol['lon'].mean())
    bmap.drawcoastlines()
    return bmap


def make_figure_hcurves(extractors, what):
    """
    $ oq plot 'hcurves?kind=mean&imt=PGA&site_id=0'
    """
    import matplotlib.pyplot as plt
    fig = plt.figure()
    got = {}  # (calc_id, kind) -> curves
    for i, ex in enumerate(extractors):
        hcurves = ex.get(what)
        for kind in hcurves.kind:
            got[ex.calc_id, kind] = hcurves[kind]
    oq = ex.oqparam
    n_imts = len(hcurves.imt)
    [site] = hcurves.site_id
    for j, imt in enumerate(hcurves.imt):
        imls = oq.imtls[imt]
        imt_slice = oq.imtls(imt)
        ax = fig.add_subplot(n_imts, 1, j + 1)
        ax.set_xlabel('%s, site %s, inv_time=%dy' %
                      (imt, site, oq.investigation_time))
        ax.set_ylabel('PoE')
        for ck, arr in got.items():
            if (arr == 0).all():
                logging.warning('There is a zero curve %s_%s', *ck)
            ax.loglog(imls, arr[0, imt_slice], '-', label='%s_%s' % ck)
            ax.loglog(imls, arr[0, imt_slice], '.')
        ax.grid(True)
        ax.legend()
    return plt


def make_figure_hmaps(extractors, what):
    """
    $ oq plot 'hmaps?kind=mean&imt=PGA'
    """
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ncalcs = len(extractors)
    for i, ex in enumerate(extractors):
        oq = ex.oqparam
        n_poes = len(oq.poes)
        sitecol = ex.get('sitecol')
        hmaps = ex.get(what)
        [imt] = hmaps.imt
        [kind] = hmaps.kind
        for j, poe in enumerate(oq.poes):
            ax = fig.add_subplot(n_poes, ncalcs, j * ncalcs + i + 1)
            ax.grid(True)
            ax.set_xlabel('hmap for IMT=%s, kind=%s, poe=%s\ncalculation %d, '
                          'inv_time=%dy' %
                          (imt, kind, poe, ex.calc_id, oq.investigation_time))
            bmap = basemap('cyl', sitecol)
            bmap.scatter(sitecol['lon'], sitecol['lat'],
                         c=hmaps[kind][:, 0, j], cmap='jet')
    return plt


def make_figure_uhs(extractors, what):
    """
    $ oq plot 'uhs?kind=mean&site_id=0'
    """
    import matplotlib.pyplot as plt
    fig = plt.figure()
    got = {}  # (calc_id, kind) -> curves
    for i, ex in enumerate(extractors):
        uhs = ex.get(what)
        for kind in uhs.kind:
            got[ex.calc_id, kind] = uhs[kind]
    oq = ex.oqparam
    n_poes = len(oq.poes)
    periods = [imt.period for imt in oq.imt_periods()]
    [site] = uhs.site_id
    for j, poe in enumerate(oq.poes):
        ax = fig.add_subplot(n_poes, 1, j + 1)
        ax.set_xlabel('UHS on site %s, poe=%s, inv_time=%dy' %
                      (site, poe, oq.investigation_time))
        ax.set_ylabel('SA')
        for ck, arr in got.items():
            ax.plot(periods, arr[0, :, j], '-', label='%s_%s' % ck)
            ax.plot(periods, arr[0, :, j], '.')
        ax.grid(True)
        ax.legend()
    return plt


def make_figure_disagg(extractors, what):
    """
    $ oq plot 'disagg?by=Dist&imt=PGA'
    """
    assert len(extractors) == 1
    import matplotlib.pyplot as plt
    fig = plt.figure()
    disagg = extractors[0].get(what)
    [sid] = disagg.site_id
    [poe_id] = disagg.poe_id
    oq = extractors[0].oqparam
    poe = oq.poes_disagg[poe_id]
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel('Disagg%s on site %s, poe=%s, inv_time=%dy' %
                  (disagg.by, sid, poe, oq.investigation_time))
    ax.plot(disagg.array)
    ax.legend()
    return plt


def make_figure_source_geom(extractors, what):
    """
    Extract the geometry of a given sources
    Example:
    http://127.0.0.1:8800/v1/calc/30/extract/source_geom/1,2,3
    """
    import matplotlib.pyplot as plt
    fig = plt.figure()
    [ex] = extractors
    sitecol = ex.get('sitecol')
    geom_by_src = vars(ex.get(what))
    ax = fig.add_subplot(1, 1, 1)
    ax.grid(True)
    ax.set_xlabel('Source')
    bmap = basemap('cyl', sitecol)
    for src, geom in geom_by_src.items():
        if src != 'array':
            bmap.plot(geom['lon'], geom['lat'], label=src)
    bmap.plot(sitecol['lon'], sitecol['lat'], 'x')
    ax.legend()
    return plt


def make_figure_task_info(extractors, what):
    """
    Plot an histogram with the task distribution. Example:
    http://127.0.0.1:8800/v1/calc/30/extract/task_info?kind=classical
    """
    import matplotlib.pyplot as plt
    fig = plt.figure()
    [ex] = extractors
    [(task_name, task_info)] = ex.get(what).to_dict().items()
    x = task_info['duration']
    ax = fig.add_subplot(1, 1, 1)
    mean, std = x.mean(), x.std(ddof=1)
    ax.hist(x, bins=50, rwidth=0.9)
    ax.set_xlabel("mean=%d+-%d seconds" % (mean, std))
    ax.set_ylabel("tasks=%d" % len(x))
    #from scipy.stats import linregress
    #ax = fig.add_subplot(2, 1, 2)
    #arr = numpy.sort(task_info, order='duration')
    #x, y = arr['duration'], arr['weight']
    #reg = linregress(x, y)
    #ax.plot(x, reg.intercept + reg.slope * x)
    #ax.plot(x, y)
    #ax.set_ylabel("weight")
    #ax.set_xlabel("duration")
    return plt


def make_figure_memory(extractors, what):
    """
    :param plots: list of pairs (task_name, memory array)
    """
    # NB: matplotlib is imported inside since it is a costly import
    import matplotlib.pyplot as plt

    [ex] = extractors
    task_info = ex.get('task_info').to_dict()
    fig, ax = plt.subplots()
    ax.grid(True)
    ax.set_xlabel('tasks')
    ax.set_ylabel('GB')
    start = 0
    for task_name in task_info:
        mem = task_info[task_name]['mem_gb']
        ax.plot(range(start, start + len(mem)), mem, label=task_name)
        start += len(mem)
    ax.legend()
    return plt


def make_figure_event_based_mfd(extractors, what):
    """
    :param plots: list of pairs (task_name, memory array)
    """
    # NB: matplotlib is imported inside since it is a costly import
    import matplotlib.pyplot as plt

    num_plots = len(extractors)
    fig = plt.figure()
    for i, ex in enumerate(extractors):
        mfd_dict = ex.get(what).to_dict()
        mags = mfd_dict.pop('magnitudes')
        duration = mfd_dict.pop('duration')
        ax = fig.add_subplot(1, num_plots, i + 1)
        ax.grid(True)
        ax.set_xlabel('magnitude')
        ax.set_ylabel('annual frequency [on %dy]' % duration)
        for label, freqs in mfd_dict.items():
            ax.plot(mags, freqs, label=label)
        mfds = ex.get('source_mfds').array
        if len(mfds) == 1:
            expected = mfd.from_toml(mfds[0], ex.oqparam.width_of_mfd_bin)
            magnitudes, frequencies = zip(
                *expected.get_annual_occurrence_rates())
            ax.plot(magnitudes, frequencies, label='expected')
        ax.legend()
    return plt


@sap.script
def plot(what, calc_id=-1, other_id=None, webapi=False):
    """
    Generic plotter for local and remote calculations.
    """
    if '?' not in what:
        raise SystemExit('Missing ? in %r' % what)
    prefix, rest = what.split('?', 1)
    if prefix in 'hcurves hmaps' and 'imt=' not in rest:
        raise SystemExit('Missing imt= in %r' % what)
    elif prefix == 'uhs' and 'imt=' in rest:
        raise SystemExit('Invalid IMT in %r' % what)
    elif prefix in 'hcurves uhs disagg' and 'site_id=' not in rest:
        what += '&site_id=0'
    if prefix == 'disagg' and 'poe=' not in rest:
        what += '&poe_id=0'
    if webapi:
        xs = [WebExtractor(calc_id)]
        if other_id:
            xs.append(WebExtractor(other_id))
    else:
        xs = [Extractor(calc_id)]
        if other_id:
            xs.append(Extractor(other_id))
    make_figure = globals()['make_figure_' + prefix]
    plt = make_figure(xs, what)
    plt.show()


plot.arg('what', 'what to extract')
plot.arg('calc_id', 'computation ID', type=int)
plot.arg('other_id', 'ID of another computation', type=int)
plot.flg('webapi', 'if given, pass through the WebAPI')
