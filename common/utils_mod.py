import maya.cmds as cmds
import pymel.core as pm
import common.utils_mod as ut
import common.attributes_mod as at


class utilites:
    """
    TODO write doc
    TODO add transform lock option
    """

    def object_tag(self, obj=None, Data="transform"):
        if obj != None:
            PyObj = pm.PyNode(obj)
            if pm.attributeQuery("obj_type", node=PyObj, ex=1):
                PyObj.obj_type.set(Data)
            else:
                dataAtr = pm.addAttr(PyObj, dt="string", ln="obj_type")
                PyObj.obj_type.set(Data)

    def add_world_mtxs_to_output(
        self, output_ntw="", object="", custom_name=None, inverse_attr=False
    ):
        attr_class = at.attributes()
        if output_ntw != "":
            pass
        else:
            raise RuntimeError("%s output network node not found" % output_ntw)
        if object != "":
            pass
        else:
            raise RuntimeError("%s object network node not found" % object)
        if custom_name != None:
            attrName = custom_name
        else:
            attrName = "%s_worldMatrix" % object
        attr_class.add_matrix_attr(output_ntw, attrName)
        pm.connectAttr(object + ".worldMatrix[0]", output_ntw + ".%s" % attrName)

        if inverse_attr:
            attr_class.add_matrix_attr(
                output_ntw, atrName="%s_worldInverseMatrix" % object
            )
            pm.connectAttr(
                object + ".worldInverseMatrix[0]",
                output_ntw + ".%s_worldInverseMatrix" % object,
            )

    def match_network_attrs(self, ntw_from="", ntw_to=""):
        attr_class = at.attributes()
        if ntw_from != "":
            pass
        else:
            raise RuntimeError("%s network node not found" % ntw_from)
        if ntw_to != "":
            pass
        else:
            raise RuntimeError("%s network node not found" % ntw_to)

        Attributes = pm.listAttr("%s" % ntw_from, ud=1)
        Out_Attributes = pm.listAttr("%s" % ntw_to, ud=1)
        for i in Attributes:
            at_type = pm.getAttr("%s.%s" % (ntw_from, i), type=1)
            if at_type == "message":
                Attributes.remove(i)

        for i in Attributes:
            at_type = pm.getAttr("%s.%s" % (ntw_from, i), type=1)

            if at_type == "matrix":
                if i in Out_Attributes:
                    try:
                        pm.connectAttr(ntw_from + ".%s" % i, ntw_to + ".%s" % i)
                    except:
                        pass

                else:
                    attr_class.add_matrix_attr(ntw_to, atrName=i)
                    pm.connectAttr(ntw_from + ".%s" % i, ntw_to + ".%s" % i)
            elif at_type == "enum" or "float" or "double" or "bool":
                print("%s_%s" % (i, at_type))

    def copy_skn(self, src, tgt):
        srcMesh = src
        tgtMesh = [tgt]
        for i in tgtMesh:
            skn = pm.ls(pm.listHistory(srcMesh), typ="skinCluster")[0]
            jnts = pm.skinCluster(skn, q=1, inf=1)
            try:
                tgt_skn = pm.ls(pm.listHistory(i), typ="skinCluster")[0]
                if tgt_skn:
                    pm.skinCluster(tgt_skn, e=1, ub=1)
            except:
                pass
            nskn = pm.skinCluster(jnts, tgtMesh, tsb=1)

            pm.copySkinWeights(
                ss=skn, ds=nskn, nm=1, sa="closestPoint", ia=["label", "oneToOne"]
            )

    def curve_from_transform(trz):
        points = []
        trs = trz
        for i in trs:
            mtx = i.worldMatrix.get()
            tr = mtx.translate.get()
            points.append(tr)

        crv = pm.curve(d=3, p=points)
        pm.parent(trs, w=1)
        pm.skinCluster(trs, crv, tsb=1)
