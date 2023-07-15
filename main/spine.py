import pymel.core as pm
from common import controls_mod, transforms_mod, utils_mod, attributes_mod
import importlib as imp
imp.reload(transforms_mod)
imp.reload(controls_mod)

class spine_module():
    '''
    TODO write doc
    TODO add tweak
    '''

    def create_spine(self,base_rig_group = None, count = 1,curveType = 'Square', basename = 'spine', sub_controls =1,parent_to =None,pos = None,shape_scale = 1):
        """
        TODO write doc

        """
        # classes intialize

        tr = transforms_mod.tf_class()
        cm = controls_mod.controls()
        utz = utils_mod.utilites()
        atz = attributes_mod.attributes()
        
        # createing all groups and transforms first, connections will be made later
        #create maingrp
        base_grp = tr.create_transform(Trname='%s_'%basename,make_local=False)
        
        #createNetwork_grps
        network = tr.create_transform(Trname='%s_network'%basename,make_local=False,parent = base_grp)
        input_ntw = tr.create_transform(Trname= '%s_input'%basename, parent=network)
        output_ntw = tr.create_transform(Trname= '%s_output'%basename, parent=network)
        utz.object_tag(input_ntw,'input_network')
        utz.object_tag(output_ntw,'output_network')
 
     
        #create guides
        guide_grp = tr.create_transform(Trname='%s_guide'%basename,make_local=False,parent=base_grp,inheritTransform =0)
        
        #create controls
        main_ctrl_grp = tr.create_transform(Trname='%s_ctrl'%basename,make_local=False,parent=base_grp,inheritTransform =0)


        #createskeleton
        skeleton_grp = tr.create_transform(Trname='%s_jnt'%basename, make_local=False,parent = base_grp,inheritTransform =0)
        
        #create inputs for parent
        atz.add_matrix_attr(input_ntw,atrName= 'parent_control_mtx')
        atz.add_matrix_attr(input_ntw,atrName= 'parent_guide_mtx')
        
        #creating guides, controls and skel
            #guides
        gd_grps = []
        gds = []
       
        if count > 0:
            
            for i in range(1,count+1):
                gd_grp =  tr.create_transform(Trname='%s_0%d_guide'%(basename,i), make_local=False)
                gd = tr.create_transform(Trname = '%s_0%d'%(basename,i), typ = 'guide',make_local=False,parent = gd_grp,guide_scale=shape_scale)
                gd_grps.append(gd_grp)
                gds.append(gd)
                utz.add_world_mtxs_to_output(output_ntw,gd)
                utz.object_tag(gd,'guide')
                
                if i == 1:
                    pm.connectAttr(input_ntw.parent_guide_mtx,gd_grp.offsetParentMatrix)
                    
                else:
                    gd_grp.translateY.set((i-1)*(2))
                    pm.parent(gd_grp,gds[i-2])
                
            pm.parent(gd_grps[0],guide_grp)       
















        #adding outputs
        
        #utz.add_world_mtxs_to_output(output_ntw,ctrls[-1],custom_name='end_ctrl_out')
        utz.add_world_mtxs_to_output(output_ntw,gds[-1],custom_name='end_guide_out')
        
        #returns
        return base_grp,input_ntw,output_ntw