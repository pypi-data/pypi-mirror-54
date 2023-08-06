Event Based Risk from GMF
=========================

============== ===================
checksum32     1,821,360,684      
date           2019-09-24T15:20:55
engine_version 3.7.0-git749bb363b3
============== ===================

num_sites = 3, num_levels = 10, num_rlzs = 1

Parameters
----------
=============================== ==================
calculation_mode                'event_based_risk'
number_of_logic_tree_samples    0                 
maximum_distance                None              
investigation_time              1.0               
ses_per_logic_tree_path         1                 
truncation_level                None              
rupture_mesh_spacing            None              
complex_fault_mesh_spacing      None              
width_of_mfd_bin                None              
area_source_discretization      None              
ground_motion_correlation_model None              
minimum_intensity               {}                
random_seed                     42                
master_seed                     0                 
ses_seed                        42                
avg_losses                      True              
=============================== ==================

Input files
-----------
======================== ================================================
Name                     File                                            
======================== ================================================
exposure                 `exposure_model_2.xml <exposure_model_2.xml>`_  
gmfs                     `gmfs_3_2IM.csv <gmfs_3_2IM.csv>`_              
job_ini                  `job.ini <job.ini>`_                            
sites                    `sitemesh.csv <sitemesh.csv>`_                  
structural_vulnerability `vulnerability_2IM.xml <vulnerability_2IM.xml>`_
======================== ================================================

Composite source model
----------------------
========= ======= =============== ================
smlt_path weight  gsim_logic_tree num_realizations
========= ======= =============== ================
b_1       1.00000 trivial(1)      1               
========= ======= =============== ================

Realizations per (GRP, GSIM)
----------------------------

::

  <RlzsAssoc(size=1, rlzs=1)>

Number of ruptures per tectonic region type
-------------------------------------------
============ ====== === ============ ============
source_model grp_id trt eff_ruptures tot_ruptures
============ ====== === ============ ============
scenario     0      *   1            0           
============ ====== === ============ ============

Estimated data transfer for the avglosses
-----------------------------------------
3 asset(s) x 1 realization(s) x 1 loss type(s) losses x 8 bytes x 20 tasks = 480 B

Exposure model
--------------
=========== =
#assets     3
#taxonomies 2
=========== =

======== ======= ====== === === ========= ==========
taxonomy mean    stddev min max num_sites num_assets
RM       1.00000 0.0    1   1   2         2         
RC       1.00000 NaN    1   1   1         1         
*ALL*    1.00000 0.0    1   1   3         3         
======== ======= ====== === === ========= ==========

Information about the tasks
---------------------------
Not available

Data transfer
-------------
==== ==== ========
task sent received
==== ==== ========

Slowest operations
------------------
================ ========= ========= ======
calc_1709        time_sec  memory_mb counts
================ ========= ========= ======
reading exposure 6.979E-04 0.0       1     
================ ========= ========= ======