import pymel.core as pm
from common import controls_mod, transforms_mod, utils_mod, attributes_mod
import importlib as imp
imp.reload(transforms_mod)
imp.reload(controls_mod)

class fk_module():
    '''
    TODO write doc
    '''

    def create_fk_chain(self,base_rig_group = None, count = 1,curveType = 'Square', basename = 'temp', sub_controls =1,parent_to =None,pos = None):
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
        #pm.parent(master_sk,base_grp)
        input_ntw = tr.create_transform(Trname= '%s_fk_input'%basename, parent=network)
        output_ntw = tr.create_transform(Trname= '%s_fk_output'%basename, parent=network)
 
     
        #create guides
        guide_grp = tr.create_transform(Trname='%s_fk_guide'%basename,make_local=False,parent=base_grp)
        
        #guide_01 = tr.create_transform(Trname = 'master', typ = 'guide',make_local=False,parent = guide_grp)
 
        #create controls
        main_ctrl_grp = tr.create_transform(Trname='%s_fk_ctrl'%basename,make_local=False,parent=base_grp)


        #createskeleton
        skeleton_grp = tr.create_transform(Trname='%s_fk_jnt'%basename, make_local=False,parent = base_grp)
  
        #creating guides, controls and skel
            #guides
        gd_grps = []
        gds = []
       
        if count > 0:
            
            for i in range(1,count+1):
                gd_grp =  tr.create_transform(Trname='%s_0%d_fk_guide'%(basename,i), make_local=False)
                gd = tr.create_transform(Trname = '%s_0%d_fk'%(basename,i), typ = 'guide',make_local=False,parent = gd_grp)
                gd_grps.append(gd_grp)
                gds.append(gd)
                utz.object_tag(gd,'guide')
                
                if i == 1:
                    pass
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
                
                ctl = cm.create_control(basename='%s_0%d_fk'%(basename,i),curveType = curveType,sub_controls=1,zgrps=0,parent_to=ctrl_grp)[1]
                utz.add_world_mtxs_to_output(output_ntw,ctl)
                ctrl_grps.append(ctrl_grp)
                ctrls.append(ctl)
                utz.object_tag(ctl,'guide')
                
                if i == 1:
                    pm.parent(ctrl_grp,main_ctrl_grp)
                    pm.connectAttr(gds[0].worldMatrix[0],ctrl_grp.offsetParentMatrix)
                    
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
                
        

            

        pass