import bpy
from bpy.types import Operator,PropertyGroup
from bpy.props import FloatProperty, PointerProperty,StringProperty

from . BL_Panel import * #
from . BL_EdgesGen import EdgesGen



class GenLine(bpy.types.Operator):
    bl_idname = "object.bl_genline"
    bl_label = "Do Edges Gen"
    bl_description = "根据参数随机生成线段并添加到场景中" #Just do Edges line generate~Operator
    bl_options = {'REGISTER'}

    def execute(self, context):
        sampleProperty = context.scene.AMOldPropertyGroup
        amProperty = context.scene.amProperties

        #初始化生成位置
        if sampleProperty.LocEdgeBool == True:
            edgeLocation = sampleProperty.edgeLoc
        else:
            sampleProperty.edgeLoc = (0,0,0)
            edgeLocation = sampleProperty.edgeLoc
        
        if amProperty.GenLineEnum =='GenLineOnly':

            edgeName= "1GenLine" #sampleProperty.edgeName
            edgeMin = sampleProperty.edgeMin
            edgeMax = sampleProperty.edgeMax
            edgeVNumber = sampleProperty.edgeVNumber

            myedges = EdgesGen(edgeName,edgeMin,edgeMax,edgeVNumber,edgeLocation)
            myedges.add_EdgeMesh()#组成头部等身体各部位

        elif amProperty.GenLineEnum =='GenLineMechBody':#可以删掉不要的物体根据没有的名字重新生成

            sampleProperty.edgeMin = 0
            sampleProperty.edgeMax = 0
            sampleProperty.edgeVNumber = 10
            #生成腿部l
            thigh_rName= "thigh_l"
            

            sampleProperty.edgeLoc = (0.5,0.05,2.4)
            

            edgeMin = sampleProperty.edgeMin
            edgeMax = sampleProperty.edgeMax
            edgeVNumber = sampleProperty.edgeVNumber
            edgeLocation = sampleProperty.edgeLoc

            sampleProperty.edgeXYZ =True
            sampleProperty.xuMin = 0
            sampleProperty.yuMin = -0.3
            sampleProperty.zuMin = -1
            sampleProperty.xvMax = 0.2
            sampleProperty.yvMax = 0
            sampleProperty.zvMax = 2.5

            thigh_r = EdgesGen(thigh_rName,edgeMin,edgeMax,edgeVNumber,edgeLocation)
            thigh_r.add_EdgeMesh()

            calf_lName = "calf_l"

            sampleProperty.edgeLoc = (0.5,0,0.8)

            sampleProperty.edgeXYZ =True
            sampleProperty.xuMin = 0
            sampleProperty.yuMin = -0.3
            sampleProperty.zuMin = -0.5
            sampleProperty.xvMax = 0.2
            sampleProperty.yvMax = 0
            sampleProperty.zvMax = 2.7

            calf_l = EdgesGen(calf_lName,edgeMin,edgeMax,edgeVNumber,edgeLocation)
            calf_l.add_EdgeMesh()

            foot_lName = "foot_l"

            sampleProperty.edgeLoc = (0.5,0,0.1)

            sampleProperty.edgeXYZ =True
            sampleProperty.xuMin = 0.05
            sampleProperty.yuMin = -1.4
            sampleProperty.zuMin = 0.05
            sampleProperty.xvMax = 0.6
            sampleProperty.yvMax = 0.6
            sampleProperty.zvMax = 0.5

            foot_l = EdgesGen(foot_lName,edgeMin,edgeMax,edgeVNumber,edgeLocation)
            foot_l.add_EdgeMesh()

            sampleProperty.edgeXYZ =False

            pelvisName = "pelvis"

            sampleProperty.edgeLoc = (0,0.2,3.5)

            sampleProperty.edgeXYZ =True
            sampleProperty.xuMin = -0.7
            sampleProperty.yuMin = -0.5
            sampleProperty.zuMin = -0.1
            sampleProperty.xvMax = 0.8
            sampleProperty.yvMax = 0.5
            sampleProperty.zvMax = 1.6

            pelvis = EdgesGen(pelvisName,edgeMin,edgeMax,edgeVNumber,edgeLocation)
            pelvis.add_EdgeMesh()


            spine_01Name = "spine_01"

            sampleProperty.edgeLoc = (0,0.1,4.1)

            sampleProperty.edgeXYZ =True
            sampleProperty.xuMin = -0.4
            sampleProperty.yuMin = -0.3
            sampleProperty.zuMin = -0.1
            sampleProperty.xvMax = 0.5
            sampleProperty.yvMax = 0.4
            sampleProperty.zvMax = 1.3

            spine_01 = EdgesGen(spine_01Name,edgeMin,edgeMax,edgeVNumber,edgeLocation)
            spine_01.add_EdgeMesh()

            spine_02Name = "spine_02"

            sampleProperty.edgeLoc = (0,0.1,4.7)

            sampleProperty.edgeXYZ =True
            sampleProperty.xuMin = -0.6
            sampleProperty.yuMin = -0.5
            sampleProperty.zuMin = -0.1
            sampleProperty.xvMax = 0.8
            sampleProperty.yvMax = 0.5
            sampleProperty.zvMax = 1.2

            spine_02 = EdgesGen(spine_02Name,edgeMin,edgeMax,edgeVNumber,edgeLocation)
            spine_02.add_EdgeMesh()

            spine_03Name = "spine_03"

            sampleProperty.edgeLoc = (0,0,5.3)

            sampleProperty.edgeXYZ =True
            sampleProperty.xuMin = -0.7
            sampleProperty.yuMin = -0.5
            sampleProperty.zuMin = -0.1
            sampleProperty.xvMax = 1
            sampleProperty.yvMax = 0.5
            sampleProperty.zvMax = 1.3

            spine_03 = EdgesGen(spine_03Name,edgeMin,edgeMax,edgeVNumber,edgeLocation)
            spine_03.add_EdgeMesh()

            neck_01Name = "neck_01"

            sampleProperty.edgeLoc = (0,0,5.7)

            sampleProperty.edgeXYZ =True
            sampleProperty.xuMin = -0.02
            sampleProperty.yuMin = -0.1
            sampleProperty.zuMin = -1.2
            sampleProperty.xvMax = 0.03
            sampleProperty.yvMax = 0.1
            sampleProperty.zvMax = 1

            neck_01 = EdgesGen(neck_01Name,edgeMin,edgeMax,edgeVNumber,edgeLocation)
            neck_01.add_EdgeMesh()

            headName = "head"

            sampleProperty.edgeLoc = (0,-0.3,6.6)

            sampleProperty.edgeXYZ =True
            sampleProperty.xuMin = -0.3
            sampleProperty.yuMin = -0.5
            sampleProperty.zuMin = 0
            sampleProperty.xvMax = 0.3
            sampleProperty.yvMax = 0.8
            sampleProperty.zvMax = 0.55

            head = EdgesGen(headName,edgeMin,edgeMax,edgeVNumber,edgeLocation)
            head.add_EdgeMesh()



            clavicle_lName = "clavicle_l"

            sampleProperty.edgeLoc = (0.65,0.2,5.6)

            sampleProperty.edgeXYZ =True
            sampleProperty.xuMin = -1
            sampleProperty.yuMin = -0.2
            sampleProperty.zuMin = -0.1
            sampleProperty.xvMax = 1
            sampleProperty.yvMax = 0.2
            sampleProperty.zvMax = 0.1

            clavicle_l = EdgesGen(clavicle_lName,edgeMin,edgeMax,edgeVNumber,edgeLocation)
            clavicle_l.add_EdgeMesh()

            upperarm_lName = "upperarm_l"

            sampleProperty.edgeLoc = (1.8,0.15,5.65)

            sampleProperty.edgeXYZ =True        
            sampleProperty.xuMin = -1.4
            sampleProperty.yuMin = -0.1
            sampleProperty.zuMin = -0.2
            sampleProperty.xvMax = 1.4
            sampleProperty.yvMax = 0.2
            sampleProperty.zvMax = 0.1

            upperarm_l = EdgesGen(upperarm_lName,edgeMin,edgeMax,edgeVNumber,edgeLocation)
            upperarm_l.add_EdgeMesh()

            lowerarm_lName = "lowerarm_l"

            sampleProperty.edgeLoc = (2.7,0.2,5.63)

            sampleProperty.edgeXYZ =True        
            sampleProperty.xuMin = -1.4
            sampleProperty.yuMin = -0.1
            sampleProperty.zuMin = -0.3
            sampleProperty.xvMax = 1.4
            sampleProperty.yvMax = 0.2
            sampleProperty.zvMax = 0.3

            lowerarm_l = EdgesGen(lowerarm_lName,edgeMin,edgeMax,edgeVNumber,edgeLocation)
            lowerarm_l.add_EdgeMesh()

            hand_lName = "hand_l"

            sampleProperty.edgeLoc = (3.9,0.2,5.6)

            sampleProperty.edgeXYZ =True        
            sampleProperty.xuMin = -1
            sampleProperty.yuMin = -0.1
            sampleProperty.zuMin = -0.3
            sampleProperty.xvMax = 1
            sampleProperty.yvMax = 0.2
            sampleProperty.zvMax = 0.3

            hand_l = EdgesGen(hand_lName,edgeMin,edgeMax,edgeVNumber,edgeLocation)
            hand_l.add_EdgeMesh()


        elif amProperty.GenLineEnum =='GenLineStruct':
            edgeName= "1GenLineStruct"
            sampleProperty.edgeMin = -5
            sampleProperty.edgeMax = 5
            sampleProperty.edgeVNumber = 10
            sampleProperty.edgeLoc = (0,0,0)

            edgeMin = sampleProperty.edgeMin
            edgeMax = sampleProperty.edgeMax
            edgeVNumber = sampleProperty.edgeVNumber
            edgeLocation = sampleProperty.edgeLoc

            genStruct = EdgesGen(edgeName,edgeMin,edgeMax,edgeVNumber,edgeLocation)
            genStruct.add_EdgeMesh()
        
        elif amProperty.GenLineEnum =='GenLineKit':
            edgeName= "1GenLineKit"
            sampleProperty.edgeMin = 0
            sampleProperty.edgeMax = 0
            sampleProperty.edgeVNumber = 8
            sampleProperty.edgeLoc = (0,0,0)

            edgeMin = sampleProperty.edgeMin
            edgeMax = sampleProperty.edgeMax
            edgeVNumber = sampleProperty.edgeVNumber
            edgeLocation = sampleProperty.edgeLoc

            sampleProperty.edgeXYZ =True
            sampleProperty.xuMin = -0.3
            sampleProperty.yuMin = -1
            sampleProperty.zuMin = 0.2
            sampleProperty.xvMax = 0.3
            sampleProperty.yvMax = 1
            sampleProperty.zvMax = 0.55

            genKit = EdgesGen(edgeName,edgeMin,edgeMax,edgeVNumber,edgeLocation)
            genKit.add_EdgeMesh()

        elif amProperty.GenLineEnum =='GenLineWeapon':
            edgeName= "1GenLineWeapon"
            sampleProperty.edgeMin = 0
            sampleProperty.edgeMax = 0
            sampleProperty.edgeVNumber = 20
            sampleProperty.edgeLoc = (0,0,0)

            edgeMin = sampleProperty.edgeMin
            edgeMax = sampleProperty.edgeMax
            edgeVNumber = sampleProperty.edgeVNumber
            edgeLocation = sampleProperty.edgeLoc

            sampleProperty.edgeXYZ =True
            sampleProperty.xuMin = -0.1
            sampleProperty.yuMin = -15
            sampleProperty.zuMin = -1
            sampleProperty.xvMax = 0.1
            sampleProperty.yvMax = 30
            sampleProperty.zvMax = 3

            genWeapon = EdgesGen(edgeName,edgeMin,edgeMax,edgeVNumber,edgeLocation)
            genWeapon.add_EdgeMesh()


        if sampleProperty.LocEditBool == True:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.context.active_object
            bpy.context.scene.cursor.location = sampleProperty.LocEdit
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
            

        self.report({'INFO'}, "Gen Line")
        return {'FINISHED'}