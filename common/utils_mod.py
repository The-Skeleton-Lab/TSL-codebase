import maya.cmds as cmds
import pymel.core as pm
import common.utils_mod as ut
import common.attributes_mod as at


class utilites():
    '''
    TODO write doc
    '''
    
    def object_tag(self,obj = None,Data = 'transform' ):
        
        if obj != None:
            PyObj = pm.PyNode(obj)
            if pm.attributeQuery('obj_type',node = PyObj,ex=1):
                    
                    PyObj.obj_type.set(Data)
            else:
                dataAtr = pm.addAttr(PyObj,dt = 'string',ln = 'obj_type')
                PyObj.obj_type.set(Data)




    def add_world_mtxs_to_output(self,output_ntw='',object=''):
        attr_class = at.attributes()
        if output_ntw !='':
            pass
        else:
            raise RuntimeError('%s output network node not found'%output_ntw)
        if object !='':
            pass
        else:
            raise RuntimeError('%s object network node not found'%object)
            
        attr_class.add_matrix_attr(output_ntw,atrName='%s_worldMatrix'%object)
        pm.connectAttr(object+'.worldMatrix[0]',output_ntw+'.%s_worldMatrix'%object)
        attr_class.add_matrix_attr(output_ntw,atrName='%s_worldInverseMatrix'%object)
        pm.connectAttr(object+'.worldInverseMatrix[0]',output_ntw+'.%s_worldInverseMatrix'%object)
        


    def match_network_attrs(self,ntw_from='',ntw_to=''):
        attr_class = at.attributes()
        if ntw_from !='':
            pass
        else:
            raise RuntimeError('%s network node not found'%ntw_from)
        if ntw_to !='':
            pass
        else:
            raise RuntimeError('%s network node not found'%ntw_to)
            
        Attributes = pm.listAttr('%s'%ntw_from,ud=1)
        Out_Attributes = pm.listAttr('%s'%ntw_to,ud=1)
        for i in Attributes:
            at_type = pm.getAttr('%s.%s'%(ntw_from,i),type=1)
            if at_type == 'message':
                Attributes.remove(i)
            
        for i in Attributes:
            at_type = pm.getAttr('%s.%s'%(ntw_from,i),type=1)
                
            if at_type == 'matrix':
                if i in Out_Attributes:
                    try:pm.connectAttr(ntw_from+'.%s'%i,ntw_to+'.%s'%i)
                    except:pass
                    
                else:
                    attr_class.add_matrix_attr(ntw_to,atrName=i)
                    pm.connectAttr(ntw_from+'.%s'%i,ntw_to+'.%s'%i)
            elif at_type == 'enum' or 'float' or 'double' or 'bool':
                print ('%s_%s'%(i,at_type))

