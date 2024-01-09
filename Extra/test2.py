cmds.file(new=1, f=1)


class createIKFK:
    def __init__(self, side, name):
        self.name = name
        self.side = side
        self.jntTypes = ["_main_jnt", "_Ik_jnt", "_Fk_jnt"]
        self.ctrl = "_ctrl"
        self.ikCtrl = "_ik_ctrl"
        self.IkHandle = "_ikHandle"
        self.guide = "Guide"
        self.polVector = "_PolVecter_ctrl"
        self.pref = ""

        if name == "bipedArm":
            self.guidsNam = ["shoulder", "elbow", "wrist"]
            self.guidstans = [(2.2, 12.0, 0), (5.9, 12.0, -0.7), (9.6, 12.0, 0.0)]
            self.ctrlRot = (0, 90, 0)

        if name == "bipedLeg":
            self.guidsNam = ["hip", "knee", "ankle"]
            self.guidstans = [(1.5, 6.0, 0.0), (1.5, 3.5, 0.5), (1.5, 1.0, 0.0)]
            self.ctrlRot = (90, 90, 0)

    #   Creating Guides -----
    def bipedGuide(self):
        print("{} bipedGuide {} started".format(self.side, self.name))

        cmds.select(cl=1)

        if self.side == "L":
            LftGuide = [
                cmds.joint(n=self.side + "_" + i[0] + self.guide, p=i[1])
                for i in list(zip(self.guidsNam, self.guidstans))
            ]

        if self.side == "R":
            LftGuide = [
                cmds.joint(n=self.side + "_" + i[0] + self.guide, p=i[1])
                for i in list(zip(self.guidsNam, self.guidstans))
            ]
            startjnt = cmds.mirrorJoint(
                LftGuide[0], myz=1, searchReplace=("L_", "R_"), mb=1
            )
            cmds.delete(LftGuide[0])
            cmds.rename(startjnt[0], self.side + "_" + self.guidsNam[0] + self.guide)

        print("{} bipedGuide {} done".format(self.side, self.name))

    #   Creating jnts -----
    def createIkFkJnt(self):
        print("{} createJnt {} started".format(self.side, self.name))

        cmds.select(cl=1)

        guidsNewTans = [
            cmds.xform(self.side + "_" + self.guidsNam[i] + self.guide, q=1, t=1, ws=1)
            for i in range(len(self.guidsNam))
        ]

        for d in self.jntTypes:
            LftGuide = [
                cmds.joint(n=self.side + "_" + i[0] + d, p=i[1])
                for i in list(zip(self.guidsNam, guidsNewTans))
            ]
            cmds.select(cl=1)

        print("{} createJnt {} done".format(self.side, self.name))

    #   Creating Ctrls -----
    def createCtrl(self):
        print("{} side createCtrl {} started".format(self.side, self.name))

        LftGuide = [
            cmds.circle(n=self.side + "_" + i[0] + self.ctrl)
            for i in list(zip(self.guidsNam, self.guidstans))
        ]
        cmds.select(cl=1)

        guidsNewTans = [
            cmds.xform(self.side + "_" + self.guidsNam[i] + self.guide, q=1, t=1, ws=1)
            for i in range(len(self.guidsNam))
        ]

        for n in range(len(self.guidsNam)):
            [
                cmds.xform(self.side + "_" + i[0] + self.ctrl, t=i[1], ro=self.ctrlRot)
                for i in list(zip(self.guidsNam, guidsNewTans))
            ]

        print("{} side createCtrl {} done".format(self.side, self.name))

    #   Creating IK -----
    def createIK(self):
        print("{} side createIK {} started".format(self.side, self.name))

        cmds.select(
            self.side + "_" + self.guidsNam[0] + self.jntTypes[1],
            self.side + "_" + self.guidsNam[2] + self.jntTypes[1],
        )
        cmds.ikHandle(n=self.side + "_" + self.name + self.IkHandle)

        cmds.circle(n=self.side + "_" + self.name + self.ikCtrl, r=0.5)
        cmds.circle(n=self.side + "_" + self.name + self.polVector, r=0.2)

        guidsNewTans = [
            cmds.xform(self.side + "_" + self.guidsNam[i] + self.guide, q=1, t=1, ws=1)
            for i in range(len(self.guidsNam))
        ]

        cmds.xform(
            self.side + "_" + self.name + self.ikCtrl,
            t=guidsNewTans[2],
            ro=self.ctrlRot,
        )
        cmds.xform(self.side + "_" + self.name + self.polVector, t=guidsNewTans[1])

        cmds.parentConstraint(
            self.side + "_" + self.name + self.ikCtrl,
            self.side + "_" + self.name + self.IkHandle,
            mo=1,
        )

        cmds.poleVectorConstraint(
            self.side + "_" + self.name + self.polVector,
            self.side + "_" + self.name + self.IkHandle,
            w=1,
        )
        print("{} side createIK {} done".format(self.side, self.name))

    #   Creating FK -----
    def createfK(self):
        print("{} side createfK {} started".format(self.side, self.name))

        for i in self.guidsNam:
            cmds.parentConstraint(
                self.side + "_" + i + self.ctrl,
                self.side + "_" + i + self.jntTypes[2],
                mo=1,
            )

        for i in range(len(self.guidsNam) - 1):
            cmds.parentConstraint(
                self.side + "_" + self.guidsNam[i] + self.ctrl,
                self.side + "_" + self.guidsNam[i + 1] + self.ctrl,
                mo=1,
            )
        print("{} side createfK {} done".format(self.side, self.name))

    def prefrncCtrl(self):
        if cmds.objExists("preference") == False:
            self.pref = cmds.circle(n="preference", r=5, nr=(0, 1, 0))
            cmds.addAttr("preference", ln="IKFK", at="float", min=0, max=1, dv=0, k=1)
        else:
            self.pref = ["preference"]

        # switch finelizing----

    def switch(self):
        print("Ik/Fk switch started")

        for i in self.guidsNam:
            cmds.parentConstraint(
                self.side + "_" + i + self.jntTypes[2],
                self.side + "_" + i + self.jntTypes[1],
                self.side + "_" + i + self.jntTypes[0],
                mo=1,
            )

        for i in range(len(self.guidsNam)):
            cmds.connectAttr(
                self.pref[0] + ".IKFK",
                self.side
                + "_"
                + self.guidsNam[i]
                + self.jntTypes[0]
                + "_parentConstraint1."
                + self.side
                + "_"
                + self.guidsNam[i]
                + self.jntTypes[2]
                + "W0",
            )

            cmds.setAttr(self.pref[0] + ".IKFK", 0)
            cmds.setAttr(
                self.side
                + "_"
                + self.guidsNam[i]
                + self.jntTypes[0]
                + "_parentConstraint1."
                + self.side
                + "_"
                + self.guidsNam[i]
                + self.jntTypes[1]
                + "W1",
                1,
            )
            cmds.setDrivenKeyframe(
                self.side
                + "_"
                + self.guidsNam[i]
                + self.jntTypes[0]
                + "_parentConstraint1."
                + self.side
                + "_"
                + self.guidsNam[i]
                + self.jntTypes[1]
                + "W1",
                cd="preference.IKFK",
            )

            cmds.setAttr(self.pref[0] + ".IKFK", 1)
            cmds.setAttr(
                self.side
                + "_"
                + self.guidsNam[i]
                + self.jntTypes[0]
                + "_parentConstraint1."
                + self.side
                + "_"
                + self.guidsNam[i]
                + self.jntTypes[1]
                + "W1",
                0,
            )
            cmds.setDrivenKeyframe(
                self.side
                + "_"
                + self.guidsNam[i]
                + self.jntTypes[0]
                + "_parentConstraint1."
                + self.side
                + "_"
                + self.guidsNam[i]
                + self.jntTypes[1]
                + "W1",
                cd="preference.IKFK",
            )

        print("Ik/Fk switch done")

    #   Creating Guides -------------------------
    def finelize(self):
        print("finelizing and grouping started")

        # grouping----
        if cmds.ls("preference", assemblies=1) != []:
            cmds.group((cmds.ls("*Guide", assemblies=1)), n="guideGrp")
            cmds.group((cmds.ls("*_main_jnt", assemblies=1)), n="mainJntGrp")
            cmds.group((cmds.ls("*_Ik_jnt", assemblies=1)), n="IkJntGrp")
            cmds.group((cmds.ls("*_Fk_jnt", assemblies=1)), n="FkJntGrp")

            cmds.group((cmds.ls("*JntGrp", assemblies=1)), n="jntGrp")
            cmds.group((cmds.ls("*ctrl", assemblies=1)), n="ctrlGrp")
            cmds.group((cmds.ls("*ikHandle", assemblies=1)), n="IkHandleGrp")
            cmds.setAttr("guideGrp.visibility", 0)
            cmds.setAttr("IkHandleGrp.visibility", 0)

            cmds.parentConstraint(self.pref[0], "ctrlGrp", mo=1)
            cmds.group(
                (
                    cmds.ls(
                        "jntGrp",
                        "guideGrp",
                        "ctrlGrp",
                        "IkHandleGrp",
                        "preference",
                        assemblies=1,
                    )
                ),
                n="main",
            )

        else:
            cmds.parent((cmds.ls("*Guide", assemblies=1)), "guideGrp")
            cmds.parent((cmds.ls("*_main_jnt", assemblies=1)), "mainJntGrp")
            cmds.parent((cmds.ls("*_Ik_jnt", assemblies=1)), "IkJntGrp")
            cmds.parent((cmds.ls("*_Fk_jnt", assemblies=1)), "FkJntGrp")
            cmds.parent((cmds.ls("*ctrl", assemblies=1)), "ctrlGrp")
            cmds.parent((cmds.ls("*ikHandle", assemblies=1)), "IkHandleGrp")

        print("finelizing and grouping done")


SetupType = createIKFK(VSide, VName)
SetupType.bipedGuide()


def CreateFkIksetup(VSide, VName):
    SetupType = createIKFK(VSide, VName)
    SetupType.createIkFkJnt()
    SetupType.createCtrl()
    SetupType.createIK()
    SetupType.createfK()


def finelIt(VSide, VName):
    SetupType = createIKFK(VSide, VName)
    SetupType.prefrncCtrl()
    SetupType.switch()
    SetupType.finelize()


#        print (f"{self.side} side createCtrl {self.name} done")
