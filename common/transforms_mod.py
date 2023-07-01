import pymel.core as pm
import common.controls_mod as ctls
import common.utils_mod as ut
class tf_class(object):
    def create_transform(self,Trname = 'temp',pos = None, parent= None,typ = 'transform',root_joint = None,inheritTransform = 1,child = None, make_local =False):
        """
        create_transform
        Args:
            TODO update doc
            
            
            Trname: Name of the transform : String
                makeLocal

            parent: Parent of the given transform : Optional arg 
        Returns:
            Returns Transform Name
        Raises:
            Raises Runtime error if parent string is given and that is not found in the scene
        example: 
            var = tf_class()
            var.create_transform(Trname = 'Test',parent= 'rig_global',Data = 'Test Data')
        """
        baseMtx = pm.datatypes.Matrix()
        utz = ut.utilites()
        ct = ctls.controls()
        shape = ctls.BSControlsUtils()
        
        if typ == 'joint':
            trf = pm.createNode('joint', n = Trname+'_jnt')
            trf.jox.setKeyable(1)
            trf.joy.setKeyable(1)
            trf.joz.setKeyable(1)
            utz.object_tag(trf, 'joint')
            if root_joint:
                root_attr = pm.addAttr(trf,dt = 'string',ln = 'rootJoint')
                trf.rootJoint.set('root_joint')
        elif typ == 'guide':
            #TODO scale the guides smaller
            trf = pm.PyNode(shape.bsDrawCurve(curve = 'Locator',name = Trname+'_gd'))
            shapes = pm.listRelatives(trf,shapes=True)
            for sh in shapes:
                    sh.overrideEnabled.set(1)
                    sh.overrideRGBColors.set(1)
                    sh.overrideColorR.set(.35)
                    sh.overrideColorG.set(.9)
                    sh.overrideColorB.set(.6)
                    sh.lineWidth.set(1.1)
            trf.v.setLocked(1)
            trf.v.setKeyable(0)   
            
            utz.object_tag(trf,'guide')
            
            
            

            

        else:
            trf = pm.createNode('transform', n = Trname+'_group')
            utz.object_tag(trf)
        
        
        
    
        if pos == None:
            Posmtx = pm.datatypes.Matrix()
            trf.setMatrix(Posmtx)
        else:
            objTyp = type(baseMtx)
            posTyp = type(pos)
            if objTyp == posTyp:
                trf.setMatrix(pos)
            else:
                try:
                    mtx = pm.datatypes.Matrix(pos)
                    tr = mtx.translate
                    rt = mtx.rotate
                    sc = mtx.scale
                    trf.setTranslation(tr)
                    trf.setRotation(rt)
                    trf.setScale(sc)
                except ValueError:
                    print("Pos attribute is not a matrix, mtx example = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]")

        if parent !='':
            try:
                pm.parent(trf,parent)
            except:
                raise RuntimeError('Parent not found')

        if inheritTransform ==0:
            trf.inheritsTransform.set(0)
        if child:
            pm.parent(child,trf)
        if make_local is True:
            grp = pm.createNode('transform', n = Trname+'_zgrp')
            pm.delete(pm.parentConstraint(trf,grp))
            pm.parent(trf,grp)
            if typ == 'joint':
                trf.jointOrientX.set(0)
                trf.jointOrientY.set(0)
                trf.jointOrientZ.set(0)
                trf.rotate.set(0,0,0)
            if parent !=None:
                try:
                    pm.parent(grp,parent)
                except:
                    raise RuntimeError('Parent not found')
            
            return grp,trf
        
        if make_local is False:
            if parent !=None:
                try:
                    pm.parent(trf,parent)
                except:
                    raise RuntimeError('Parent not found')
            return trf
        

        
