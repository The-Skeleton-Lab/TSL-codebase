import importlib 
import pymel.core as pm
from common import controls_mod, transforms_mod, utils_mod, attributes_mod
from main import master_mod as master
from main import fk_mod as fk1

#importlib.reload(master)
#importlib.reload(fk1)

#creating the base rig_grp
def build_rig():
    tr = transforms_mod.tf_class()
    cm = controls_mod.controls()
    utz = utils_mod.utilites()
    atz = attributes_mod.attributes()
    if pm.objExists('base_rig_grp'):
        base_grp = pm.PyNode('base_rig_grp')
    else:
        base_grp = tr.create_transform(Trname='rig_grp',make_local=False)
            

    #creating master class
    m_class = master.master_module()
    master_objs = m_class.createMaster()	

    #creating the fk chain
    fkchain = fk1.fk_module()
    fk1_objs = fkchain.create_fk_chain(count =5,basename = 'Sid')

    #connecting the modules
    master_objs[2].master_gd_worldMatrix>>fk1_objs[1].parent_guide_mtx
    master_objs[2].master_ctrl_output_worldMatrix>>fk1_objs[1].parent_control_mtx

    #parenting the modules
    pm.parent(master_objs[0],base_grp)
    pm.parent(fk1_objs[0],base_grp)