import pymel.core as pm
from common import controls_mod, transforms_mod, utils_mod, attributes_mod
import importlib as imp
imp.reload(transforms_mod)
imp.reload(controls_mod)
imp.reload(utils_mod)

class cape_mod():
    '''
    TODO write doc
    TODO add tweak
    '''

    def create_chain(self,base_rig_group = None, count = 1,curveType = 'Square', basename = 'spine', sub_controls =1,parent_to =None,pos = None,shape_scale = 1):
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
        base_grp = tr.create_transform(Trname='%s'%basename,make_local=False)
        
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
        
        #misc_grp

        misc_grp = tr.create_transform(Trname='%s_misc'%basename,make_local=False,parent=base_grp,inheritTransform =0)

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
            
            for i in range(1,count):
                gd_grp =  tr.create_transform(Trname='%s_0%d_guide'%(basename,i), make_local=False)
                gd = tr.create_transform(Trname = '%s_0%d'%(basename,i), typ = 'guide',make_local=False,parent = gd_grp,guide_scale=shape_scale)
                gd_grps.append(gd_grp)
                gds.append(gd)
                utz.add_world_mtxs_to_output(output_ntw,gd)
                utz.object_tag(gd,'guide')
                
                if i == 1:
                    pm.connectAttr(input_ntw.parent_guide_mtx,gd_grp.offsetParentMatrix)
                    
                else:
                    gd.translateY.set((i-1)*(2))
                    pm.parent(gd_grp,gds[i-2])


            pm.parent(gd_grps[0],guide_grp)       

        #controls
        ctrl_grps = []
        tweak_ctrls =[]
        ctrls = []
            
        if count > 0:
            
            for i in range(1,count):
                ctrl_grp =  pm.PyNode(tr.create_transform(Trname='%s_0%d_base_ctrl'%(basename,i), make_local=False))              
                ctl = cm.create_control(basename='%s_0%d'%(basename,i),curveType = curveType,sub_controls=1,zgrps=0,parent_to=ctrl_grp,control_scale=shape_scale)[1]
 
                tweak_ctrl_grp =  pm.PyNode(tr.create_transform(Trname='%s_0%d_base_tweak'%(basename,i), make_local=False))              
                tweak_ctl = cm.create_control(basename='%s_0%d_tweak'%(basename,i),curveType = 'Two Arrows',sub_controls=1,zgrps=0,parent_to=tweak_ctrl_grp,control_scale=(shape_scale - .22),color=[.7,1,.2])[1]
                
                pm.connectAttr(ctl.worldMatrix[0],tweak_ctrl_grp.offsetParentMatrix)


                utz.add_world_mtxs_to_output(output_ntw,ctl)
                ctrl_grps.append(ctrl_grp)
                ctrls.append(ctl)
                tweak_ctrls.append(tweak_ctl)
                utz.object_tag(ctl,'ctrl')

                
                if i == 1:
                    pm.parent(ctrl_grp,main_ctrl_grp)
                    multMtx = pm.createNode('multMatrix',n = '%s_0%d_multMtx'%(basename,i))
                    invMtx = pm.createNode('inverseMatrix',n = '%s_0%d_invMtx'%(basename,i))
                    pm.connectAttr(gds[0].worldMatrix[0],multMtx.matrixIn[0])
                    pm.connectAttr(input_ntw.parent_guide_mtx,invMtx.inputMatrix)
                    pm.connectAttr(invMtx.outputMatrix,multMtx.matrixIn[1])
                    pm.connectAttr(input_ntw.parent_control_mtx,multMtx.matrixIn[2])  
                    pm.connectAttr(multMtx.matrixSum,ctrl_grp.offsetParentMatrix)
                    pm.parent(tweak_ctrl_grp,main_ctrl_grp)

                else:
                    multMtx = pm.createNode('multMatrix',n = '%s_0%d_multMtx'%(basename,i))
                    pm.connectAttr(gds[i-1].worldMatrix[0],multMtx.matrixIn[0])
                    pm.connectAttr(gds[i-2].worldInverseMatrix[0],multMtx.matrixIn[1])
                    pm.connectAttr(ctrls[i-2].worldMatrix[0],multMtx.matrixIn[2])
                    pm.connectAttr(multMtx.matrixSum,ctrl_grp.offsetParentMatrix)

                    pm.parent(ctrl_grp,main_ctrl_grp)
                    pm.parent(tweak_ctrl_grp,main_ctrl_grp)

   
        

        #create joints
        skl = []
       
        if count > 0:
            
            for idx,i in enumerate(tweak_ctrls):
                jnt = tr.create_transform(Trname = '%s_0%d'%(i,idx+1), typ = 'joint',make_local=False,parent = misc_grp)
                skl.append(jnt)
                utz.object_tag(jnt,'joint')
                pm.connectAttr(i.worldMatrix[0],jnt.offsetParentMatrix)

        
        #create_plane

        dist =((gds[-1].worldMatrix.get()).translate-(gds[0].worldMatrix.get()).translate).length()

        v_patches = ((((count)-2)*2)+2)
        nb = pm.nurbsPlane(lr = dist, v = v_patches,ch =0,d =3,ax = [0,0,1],n = basename+'_plane')
        nbShp = pm.listRelatives(nb, s=1)[0]
        pm.delete(pm.parentConstraint([gds[0],gds[-1]],nb))
        pm.makeIdentity(nb,a=1)
        pm.parent(nb,misc_grp)
        #skin plane
        joints = skl

        sknPlane = pm.polyPlane(h = dist,w =1,ax = [0,0,1],sw = 1,sh =v_patches,ch =0,name=basename+'skn_plane')
        pm.delete(pm.parentConstraint([gds[0],gds[-1]],sknPlane))

        newSkn = pm.skinCluster(joints, sknPlane, sm =0, bm = 0, omi = False, tsb = True, mi=2,wd=0,normalizeWeights = 1,weightDistribution =0,dr =4,rui = 0)

        pm.parent(sknPlane,misc_grp)
        utz.copy_skn(sknPlane[0],nb[0])
        pm.delete(sknPlane)


        #sub_controls on plane
        sub_ctrl_grp = tr.create_transform(Trname='%s_sub'%basename,make_local=False,parent=main_ctrl_grp,inheritTransform =0)

        subctrl_no = (count-1)*2
        print (sub_controls)
        sub_ctrls = []
        uvPin = pm.createNode('uvPin',n = '%s_uvpin'%basename)
        nbShp.worldSpace[0]>>uvPin.deformedGeometry
        incriment = 1/(subctrl_no-2)

        v = incriment

        for i in range(0,subctrl_no-3):
            sub_csize = shape_scale - (shape_scale*50/100)
            subc = cm.create_control(basename='%s_0%d_sub'%(basename,i),curveType = curveType,sub_controls=1,zgrps=0,parent_to=sub_ctrl_grp,control_scale=sub_csize,color=[.2,.6,.6])
            sub_ctrls.append(subc[1])
            if i  == 0:
                vC = v
            else:
                v = v+incriment
                vC = v
                
            uvPin.coordinate[i].set(0.5,vC)
            uvPin.outputMatrix[i]>>subc[0].offsetParentMatrix

        out_skel = []
       
        if count > 0:
            
            for idx,i in enumerate(sub_ctrls):
                jnt = tr.create_transform(Trname = '%s_0%d_out'%(i,idx+1), typ = 'joint',make_local=False,parent = skeleton_grp)
                out_skel.append(jnt)
                utz.object_tag(jnt,'joint')
                pm.connectAttr(i.worldMatrix[0],jnt.offsetParentMatrix)
            

        #first and last out joints 

        jnts = [skl[0],skl[-1],skl[-2]]
        for i in jnts:
            jnt = tr.create_transform(Trname = '%sout'%(i.replace('jnt','')), typ = 'joint',make_local=False,parent = skeleton_grp)
            out_skel.append(jnt)
            utz.object_tag(jnt,'joint')
            pm.connectAttr(i.worldMatrix[0],jnt.offsetParentMatrix)

        #setting and spinerotate
        
        
        
        #adding outputs
        
        utz.add_world_mtxs_to_output(output_ntw,ctrls[-1],custom_name='end_ctrl_out')
        utz.add_world_mtxs_to_output(output_ntw,gds[-1],custom_name='end_guide_out')
        
        utz.add_world_mtxs_to_output(output_ntw,ctrls[0],custom_name='start_ctrl_out')
        utz.add_world_mtxs_to_output(output_ntw,gds[0],custom_name='start_guide_out')        
        #returns
        return base_grp,input_ntw,output_ntw