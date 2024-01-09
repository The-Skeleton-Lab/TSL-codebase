import importlib 
import pymel.core as pm
from common import controls_mod, transforms_mod, utils_mod, attributes_mod, save_load_guides
from main import master_mod as master
from main import fk_mod, fk_ribbon
importlib.reload(save_load_guides)

def build_rig(asset_name = 'cape_rig',guide_path= None):
    tr = transforms_mod.tf_class()
    cm = controls_mod.controls()
    utz = utils_mod.utilites()
    atz = attributes_mod.attributes()
    fk_rib = fk_ribbon.fk_ribbon_mod()

    if pm.objExists('%s_rig_grp'%asset_name):
        base_grp = pm.PyNode('%s_rig_grp'%asset_name)
    else:
        base_grp = tr.create_transform(Trname='%s_rig_grp'%asset_name,make_local=False)
    

    #creating master class
    m_class = master.master_module()
    master_objs = m_class.createMaster(asset_name=asset_name,shape_scale = 30)	



    fkchain = fk_mod.fk_module()
    fk_base = fkchain.create_fk_chain(count =1,basename = '%s_neck_base'%asset_name,shape_scale = 6,curveType ='Circle')
    fk1_objs = fkchain.create_fk_chain(count =1,basename = '%s_fk_01'%asset_name,shape_scale = 1.5,curveType ='Sphere')
    fk2_objs = fkchain.create_fk_chain(count =1,basename = '%s_fk_02'%asset_name,shape_scale = 1.5,curveType ='Sphere')
    fk3_objs = fkchain.create_fk_chain(count =1,basename = '%s_fk_03'%asset_name,shape_scale = 1.5,curveType ='Sphere')
    fk4_objs = fkchain.create_fk_chain(count =1,basename = '%s_fk_04'%asset_name,shape_scale = 1.5,curveType ='Sphere')
    fk5_objs = fkchain.create_fk_chain(count =1,basename = '%s_fk_05'%asset_name,shape_scale = 1.5,curveType ='Sphere')

    fk_cape_base = fkchain.create_fk_chain(count =1,basename = '%s_back_base'%asset_name,shape_scale = 6,curveType ='Square')
    fk_asset_base = fkchain.create_fk_chain(count =1,basename = '%s_main'%asset_name,shape_scale = 7,curveType ='Box')


    lf_cape = fk_rib.create_chain(basename = 'lf_cape',count = 13,shape_scale = 3)
    rt_cape = fk_rib.create_chain(basename = 'rt_cape',count = 13,shape_scale = 3)
    cn_cape = fk_rib.create_chain(basename = 'cn_cape',count = 13,shape_scale = 3)

    #connecting the modules
    master_objs[2].end_guide_out>>fk_asset_base[1].parent_guide_mtx
    master_objs[2].end_ctrl_out>>fk_asset_base[1].parent_control_mtx
    
    fk_asset_base[2].end_guide_out>>fk_base[1].parent_guide_mtx
    fk_asset_base[2].end_ctrl_out>>fk_base[1].parent_control_mtx

    fk_asset_base[2].end_guide_out>>fk_cape_base[1].parent_guide_mtx
    fk_asset_base[2].end_ctrl_out>>fk_cape_base[1].parent_control_mtx
        
    fk_base[2].end_guide_out>>fk1_objs[1].parent_guide_mtx
    fk_base[2].end_ctrl_out>>fk1_objs[1].parent_control_mtx

    fk_base[2].end_guide_out>>fk2_objs[1].parent_guide_mtx
    fk_base[2].end_ctrl_out>>fk2_objs[1].parent_control_mtx

    fk_base[2].end_guide_out>>fk3_objs[1].parent_guide_mtx
    fk_base[2].end_ctrl_out>>fk3_objs[1].parent_control_mtx

    fk_base[2].end_guide_out>>fk4_objs[1].parent_guide_mtx
    fk_base[2].end_ctrl_out>>fk4_objs[1].parent_control_mtx
    
    fk_base[2].end_guide_out>>fk5_objs[1].parent_guide_mtx
    fk_base[2].end_ctrl_out>>fk5_objs[1].parent_control_mtx
    
    fk_base[2].end_guide_out>>fk5_objs[1].parent_guide_mtx
    fk_base[2].end_ctrl_out>>fk5_objs[1].parent_control_mtx

    fk_cape_base[2].end_guide_out>>lf_cape[1].parent_guide_mtx
    fk_cape_base[2].end_ctrl_out>>lf_cape[1].parent_control_mtx

    fk_cape_base[2].end_guide_out>>rt_cape[1].parent_guide_mtx
    fk_cape_base[2].end_ctrl_out>>rt_cape[1].parent_control_mtx

    fk_cape_base[2].end_guide_out>>cn_cape[1].parent_guide_mtx
    fk_cape_base[2].end_ctrl_out>>cn_cape[1].parent_control_mtx



    #parenting the modules
    pm.parent(master_objs[0],base_grp)
    pm.parent(fk_base[0],base_grp)
    pm.parent(fk1_objs[0],base_grp)
    pm.parent(fk2_objs[0],base_grp)
    pm.parent(fk3_objs[0],base_grp)
    pm.parent(fk4_objs[0],base_grp)
    pm.parent(fk5_objs[0],base_grp)

    pm.parent(fk_cape_base[0],base_grp)
    pm.parent(fk_asset_base[0],base_grp)
    

    pm.parent(lf_cape[0],base_grp)
    pm.parent(rt_cape[0],base_grp)
    pm.parent(cn_cape[0],base_grp)
    
    

def guide_functions(save_guides=False,load_guides=True):
    #save_load_guides
    gdz = save_load_guides.guides()

    fileName = '/Users/siddarthmehraajm/Documents/GitHub/AutoRiggingFramework/TSL-codebase/Extra/cape.json'

    if load_guides:
        gdz.load_guides(fileName)
    if save_guides:
        gdz.save_guides_data(fileName)