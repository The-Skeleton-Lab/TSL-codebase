
import maya.cmds as cmds
import pymel.core as pm


class attributes():
    def add_matrix_attr(self,Trname = None,atrName = None):
        if Trname!=None:
            pass
        else:
            raise RuntimeError('Transform not given or not an applicable obj')
            
        if atrName!=None:
            pass
        else:
            raise RuntimeError('Attribute name not given')
            
            
        trf = pm.PyNode(Trname)
        
        dataAtr = pm.addAttr(trf,dt = 'matrix',ln = '%s'%atrName)
    
    def add_data_attr(self,Trname = None,Data = ''):
        if Trname!=None:
            pass
        else:
            raise RuntimeError('Transform not given or not an applicable obj')

        trf = pm.PyNode(Trname)
        try:
            dataAtr = pm.addAttr(trf,dt = 'string',ln = 'data')
            trf.data.set(Data)
        except:
            try:
                trf.data.set(Data)
            except:
                raise RuntimeError('Failed to add/set Data Attribute')