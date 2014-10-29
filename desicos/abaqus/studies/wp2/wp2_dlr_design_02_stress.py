#
study_name_prefix = 'wp2_dlr_design_02_stress'
#
import numpy as np
import sys
import os
#
meshes =  {\
          'NUMEL_140': 140.,
         }
studies = {}
for meshname, numel_r in meshes.iteritems():
    study_name = study_name_prefix + '_' + meshname
    source_python = r'C:\Users\pfh-castro\doutorado\desicos\abaqus-conecyl-python'
    sys.path.append( source_python )
    study_dir  = os.path.join( r'C:\Temp','abaqus',study_name )
    if not os.path.isdir( study_dir ):
        os.makedirs( study_dir )
    output_dir = os.path.join( study_dir,'outputs' )
    print 'configuring folders...'
    print '\t' + output_dir
    if not os.path.isdir( output_dir ):
        os.makedirs( output_dir )
    #
    import study
    study = reload( study )
    from study import Study
    std = Study()
    std.name = study_name
    std.rebuild()
    #ploads = [ 0.,0.2,0.5,0.7,1.,2.,3.,4.,5.,10., 15. ]
    #ploads = [ 15. ]
    #ploads = [ 0.2 ]
    ploads = [ 0.2, 1. ]
    pt = 0.5
    cname = 'wp2_dlr_des_02'
    for pload in ploads:
        cc = std.add_cc_fromDB( cname )
        cc.meshname = meshname
        cc.numel_r = numel_r
        cc.elem_type = 'S8R5'
        cc.request_stress_output = True
        cc.impconf.ploads = []
        cc.impconf.add_pload(
            theta=  0.,
            pt = pt,
            pltotal = pload )
        cc.minInc2 = 1.e-6
        cc.initialInc2 = 1.e-1
        cc.maxInc2 = 1.e-1
        cc.maxNumInc2 = 10000
        cc.damping_factor2 = 1.e-7
        cc.axial_displ = 0.6
        cc.time_points = 80
    std.create_models()
    studies[ std.name ] = std