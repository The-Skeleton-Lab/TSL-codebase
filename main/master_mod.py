import pymel.core as pm
from common import controls_mod, transforms_mod, utils_mod, attributes_mod
import importlib as imp
imp.reload(transforms_mod)
imp.reload(controls_mod)

class master_module():
    '''
    TODO write doc
    TODO add shape scale option
    '''

    def createMaster(self,base_rig_group = None, asset_name = '', shape_scale = 1):
        '''
        TODO write doc
        '''
        # classes intialize

        tr = transforms_mod.tf_class()
        cm = controls_mod.controls()
        utz = utils_mod.utilites()
        atz = attributes_mod.attributes()
        
        # createing all groups and transforms first, connections will be made later
        #create maingrp
        base_grp = tr.create_transform(Trname='master_main',make_local=False)
        
        #createNetwork_grps
        master_network = tr.create_transform(Trname='master_network',make_local=False,parent = base_grp)
        input_ntw = tr.create_transform(Trname= 'master_input',parent=master_network)
        output_ntw = tr.create_transform(Trname= 'master_output',parent=master_network)
        utz.object_tag(input_ntw,'input_network')
        utz.object_tag(output_ntw,'output_network')
 
     
        #create guides
        master_gd = tr.create_transform(Trname='master_guide',make_local=False,parent=base_grp,inheritTransform =0)
        guide_01 = tr.create_transform(Trname = 'master', typ = 'guide',make_local=False,parent = master_gd,inheritTransform =0)

        
        #create controls
        master_ct = tr.create_transform(Trname='master_ctrl',make_local=False,parent=base_grp,inheritTransform =0)

        main_ctrl = cm.create_control(basename='master',curveType = 'Four Arrows',sub_controls=3,zgrps=0)
        pm.parent(main_ctrl[-1],master_ct)


        #create skeleton
        master_sk = tr.create_transform(Trname='master_jnt',make_local=False,parent = base_grp,inheritTransform =0)
        
        root_skel = tr.create_transform(Trname= 'root',typ='joint',parent=master_sk,root_joint = True)
        main_skel = tr.create_transform(Trname= 'master',typ='joint',parent=root_skel)


        for i in [base_grp,master_gd,master_ct,master_sk]:
            utz.object_tag(i)

        if base_rig_group:
            pm.parent(base_grp,base_rig_group)
        
        if asset_name:
            atz.add_data_attr(base_grp,asset_name)


        #connections
        guide_01.worldMatrix[0]>>main_ctrl[0].offsetParentMatrix
        main_ctrl[1].worldMatrix[0]>>main_skel.offsetParentMatrix
        
        utz.add_world_mtxs_to_output(output_ntw,main_ctrl[1],custom_name='end_ctrl_out')
        utz.add_world_mtxs_to_output(output_ntw,guide_01,custom_name='end_guide_out')
        
        #base output which can be used for all groups 

        #returns
        return base_grp,input_ntw,output_ntw