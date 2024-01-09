import importlib
import pymel.core as pm
from common import controls_mod, transforms_mod, utils_mod, attributes_mod
from main import master_mod as master
from main import fk_mod as fk1

importlib.reload(master)
importlib.reload(fk1)


# creating the base rig_grp
def build_rig(asset_name="base"):
    tr = transforms_mod.tf_class()
    cm = controls_mod.controls()
    utz = utils_mod.utilites()
    atz = attributes_mod.attributes()
    if pm.objExists("%s_rig_grp" % asset_name):
        base_grp = pm.PyNode("%s_rig_grp" % asset_name)
    else:
        base_grp = tr.create_transform(
            Trname="%s_rig_grp" % asset_name, make_local=False
        )

    # creating master class
    m_class = master.master_module()
    master_objs = m_class.createMaster(asset_name=asset_name)

    # creating the fk chain
    fkchain = fk1.fk_module()
    fk1_objs = fkchain.create_fk_chain(
        count=5, basename="%s_fk_01" % asset_name, shape_scale=0.5
    )

    # connecting the modules
    master_objs[2].end_guide_out >> fk1_objs[1].parent_guide_mtx
    master_objs[2].end_ctrl_out >> fk1_objs[1].parent_control_mtx

    # parenting the modules
    pm.parent(master_objs[0], base_grp)
    pm.parent(fk1_objs[0], base_grp)
