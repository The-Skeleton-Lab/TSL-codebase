import pymel.core as pm
from common import controls_mod, transforms_mod, utils_mod, attributes_mod
import importlib as imp
imp.reload(transforms_mod)
imp.reload(controls_mod)

class fk_module():
    '''
    TODO write doc
    TODO add tweak
    '''

    def create_fk_chain(self,base_rig_group = None, count = 1,curveType = 'Square', basename = 'temp', sub_controls =1,parent_to =None,pos = None,shape_scale = 1):
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
        base_grp = tr.create_transform(Trname='%s_fk'%basename,make_local=False)
        
        #createNetwork_grps
        network = tr.create_transform(Trname='%s_fk_network'%basename,make_local=False,parent = base_grp)
        input_ntw = tr.create_transform(Trname= '%s_fk_input'%basename, parent=network)
        output_ntw = tr.create_transform(Trname= '%s_fk_output'%basename, parent=network)
        utz.object_tag(input_ntw,'input_network')
        utz.object_tag(output_ntw,'output_network')
 
     
        #create guides
        guide_grp = tr.create_transform(Trname='%s_fk_guide'%basename,make_local=False,parent=base_grp,inheritTransform =0)
        
        #create controls
        main_ctrl_grp = tr.create_transform(Trname='%s_fk_ctrl'%basename,make_local=False,parent=base_grp,inheritTransform =0)


        #createskeleton
        skeleton_grp = tr.create_transform(Trname='%s_fk_jnt'%basename, make_local=False,parent = base_grp,inheritTransform =0)
        
        #create inputs for parent
        atz.add_matrix_attr(input_ntw,atrName= 'parent_control_mtx')
        atz.add_matrix_attr(input_ntw,atrName= 'parent_guide_mtx')


        #creating guides, controls and skel
            #guides
        gd_grps = []
        gds = []
       
        if count > 0:
            
            for i in range(1,count+1):
                gd_grp =  tr.create_transform(Trname='%s_0%d_fk_guide'%(basename,i), make_local=False)
                gd = tr.create_transform(Trname = '%s_0%d_fk'%(basename,i), typ = 'guide',make_local=False,parent = gd_grp,guide_scale=shape_scale)
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
            
            #controls
        ctrl_grps = []
        ctrls = []
            
        if count > 0:
            
            for i in range(1,count+1):
                ctrl_grp =  pm.PyNode(tr.create_transform(Trname='%s_0%d_fk_base_ctrl'%(basename,i), make_local=False))
                
                ctl = cm.create_control(basename='%s_0%d_fk'%(basename,i),curveType = curveType,sub_controls=1,zgrps=0,parent_to=ctrl_grp,control_scale=shape_scale)[1]
                utz.add_world_mtxs_to_output(output_ntw,ctl)
                ctrl_grps.append(ctrl_grp)
                ctrls.append(ctl)
                utz.object_tag(ctl,'guide')
                
                if i == 1:
                    pm.parent(ctrl_grp,main_ctrl_grp)
                    multMtx = pm.createNode('multMatrix',n = '%s_0%d_multMtx'%(basename,i))
                    invMtx = pm.createNode('inverseMatrix',n = '%s_0%d_invMtx'%(basename,i))
                    pm.connectAttr(gds[0].worldMatrix[0],multMtx.matrixIn[0])
                    pm.connectAttr(input_ntw.parent_guide_mtx,invMtx.inputMatrix)
                    pm.connectAttr(invMtx.outputMatrix,multMtx.matrixIn[1])
                    pm.connectAttr(input_ntw.parent_control_mtx,multMtx.matrixIn[2])  
                    pm.connectAttr(multMtx.matrixSum,ctrl_grp.offsetParentMatrix)

                else:
                    multMtx = pm.createNode('multMatrix',n = '%s_0%d_multMtx'%(basename,i))
                    pm.connectAttr(gds[i-1].worldMatrix[0],multMtx.matrixIn[0])
                    pm.connectAttr(gds[i-2].worldInverseMatrix[0],multMtx.matrixIn[1])
                    pm.connectAttr(ctrls[i-2].worldMatrix[0],multMtx.matrixIn[2])
                    pm.connectAttr(multMtx.matrixSum,ctrl_grp.offsetParentMatrix)

                    pm.parent(ctrl_grp,main_ctrl_grp)
                
            #skeleton

        skl = []
       
        if count > 0:
            
            for i in range(1,count+1):
                jnt = tr.create_transform(Trname = '%s_0%d_fk'%(basename,i), typ = 'joint',make_local=False,parent = skeleton_grp)
                skl.append(jnt)
                utz.object_tag(jnt,'joint')
                pm.connectAttr(ctrls[i-1].worldMatrix[0],jnt.offsetParentMatrix)
                
        
        #adding outputs
        
        utz.add_world_mtxs_to_output(output_ntw,ctrls[-1],custom_name='end_ctrl_out')
        utz.add_world_mtxs_to_output(output_ntw,gds[-1],custom_name='end_guide_out')
        
        #returns
        return base_grp,input_ntw,output_ntw