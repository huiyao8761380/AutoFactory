import bpy
from .RIG_Tool import *
#执行顺序2 点击Armature
#脸部腮帮、脖子到头部的位置 及法令纹部位需要调整 --舌头可能需要调整 
#twist需要调整 neck01也调整吧 它只做左右旋转
# #upperarm_twist_01_l——>upperarm_l
# #lowerarm_l也——>upperarm_l

# #lowerarm_twist_01_l——>lowerarm_l
# #hand_l——>lowerarm_l

#thigh_twist_01_l——>thigh_l
#calf_l——>thigh_l

#calf_twist_01_l——>calf_l
#foot_l——>calf_l

#ik_foot_root ik_hand_root（0，0，0）指向root 记得添加空的形变

#ik_hand_gun(handr的位置)——>ik_hand_root
#ik_hand_r(handr的位置)——>ik_hand_gun
#ik_hand_l(handl的位置)——>ik_hand_gun
#ik_foot_l(footl的位置)——>ik_foot_root
#ik_foot_r(footr的位置)——> ik_foot_root
#——> 
#——> 

'''
def MakeSureSelectOneLayer(layer):#确保选中该骨骼层级
    for i in range(31):
        #bpy.ops.pose.select_all(action='SELECT')
        bpy.context.object.data.layers[i] = False
    bpy.context.object.data.layers[layer] = True

    for i in range(31):
        bpy.context.object.data.layers[i] = False
    bpy.context.object.data.layers[layer] = True


def SelectBone(bone):#选择该层级的骨骼及子级

    bpy.ops.armature.select_all(action='DESELECT')
    SelectBone=bpy.context.object.data.edit_bones[bone]

    SelectBone.select_head = True
    SelectBone.select_tail = True
    SelectBone.select = True

    bpy.context.object.data.edit_bones.active = SelectBone #GOOD!
    

def Select2Bone(SecondBone,ActiveBone):

    SelectBone(ActiveBone)
    Select2Bone=bpy.context.object.data.edit_bones[SecondBone]

    Select2Bone.select_head = True
    Select2Bone.select_tail = True
    Select2Bone.select = True

def DuplicateMove():#复制骨骼到空层级

    #bpy.ops.armature.select_all(action='DESELECT')#'SELECT'
    #SelectBone(bone)
    bpy.ops.armature.duplicate_move(ARMATURE_OT_duplicate={"do_flip_names":False}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
    bpy.ops.armature.bone_layers(layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False))
'''


class UE4TypeBone(bpy.types.Operator):#当骨骼物体名称为Rig时，导出将自动添加物体名称根骨骼，否则绑定好后可以勾选Root骨骼的形变
    bl_idname = "am.ue4typebone"
    bl_label = "UE4 Type Bone"
    bl_description = "在Rig层级添加要导出使用的UE4骨骼。" 
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.object.name='Armature'#骨骼名称为Armature时才会删掉
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='EDIT')

        if "ORG-face" in bpy.context.object.data.bones:
            MakeSureSelectOneLayer(31)#头最全
            #！！！这里加个判断是否存在ORG-face"

            SelectBone("ORG-face")

            bpy.ops.armature.select_similar(type='CHILDREN')#选择该骨骼层级的所有子级
            DuplicateMove()#直接到23层

            MakeSureSelectOneLayer(23)
            bpy.context.object.data.layers[31] = False#以上脸操作完成

        MakeSureSelectOneLayer(29)#身体最全
        bpy.context.object.data.layers[23] = False
        bpy.ops.armature.select_all(action='SELECT')
        bpy.ops.wm.context_collection_boolean_set(data_path_iter="selected_bones", data_path_item="use_deform", type='DISABLE')
        bpy.ops.armature.select_all(action='DESELECT')

        #！！！这里也加个判断是否存在ORG-face" 否则在29层执行
        if "ORG-face" in bpy.context.object.data.bones:
            SelectBone("ORG-face")
            bpy.ops.armature.select_similar(type='CHILDREN')
            bpy.ops.armature.select_all(action='INVERT')
        else:
            bpy.ops.armature.select_all(action='SELECT')

        DuplicateMove()
        MakeSureSelectOneLayer(23)
        bpy.context.object.data.layers[29] = False#以上身体操作完成

        bpy.ops.armature.select_all(action='SELECT')

        bpy.ops.wm.context_collection_boolean_set(data_path_iter="selected_bones", data_path_item="use_deform", type='ENABLE')#Shift+W启用形变 无法赋值

        bpy.ops.armature.select_all(action='DESELECT')

        for bone in bpy.context.object.data.bones:
            if ('belly' in bone.name) or ('Wing' in bone.name) or ('tail' in bone.name) or ('side_fin' in bone.name) or ('front_toe' in bone.name):
                bpy.ops.object.mode_set(mode='OBJECT')
                return {'FINISHED'}

        #面 子父 头
        if "ORG-face" in bpy.context.object.data.bones:
            Select2Bone("ORG-face.001","DEF-head.001")

            bpy.ops.armature.parent_set(type='OFFSET')#指向活跃骨骼为父级

            bpy.ops.armature.select_all(action='DESELECT')

            #面 子父 头
            MakeSureSelectOneLayer(31)
            bpy.context.object.data.layers[23] = False

            bpy.ops.armature.select_all(action='DESELECT')
            Select2Bone("ORG-face","ORG-head")
            bpy.ops.armature.parent_set(type='OFFSET')#指向活跃骨骼为父级
            bpy.ops.armature.select_all(action='DESELECT')


        #fk fix

        MakeSureSelectOneLayer(8)
        bpy.context.object.data.layers[31] = False
        bpy.context.object.data.layers[23] = False

        bpy.ops.armature.select_all(action='DESELECT')
        Select2Bone("lowerarm_fk.l","upperarm_fk.l")
        bpy.ops.armature.parent_set(type='OFFSET')#指向活跃骨骼为父级
        bpy.ops.armature.select_all(action='DESELECT')


        MakeSureSelectOneLayer(11)
        bpy.context.object.data.layers[8] = False

        bpy.ops.armature.select_all(action='DESELECT')
        Select2Bone("lowerarm_fk.r","upperarm_fk.r")
        bpy.ops.armature.parent_set(type='OFFSET')#指向活跃骨骼为父级
        bpy.ops.armature.select_all(action='DESELECT')

        MakeSureSelectOneLayer(14)
        bpy.context.object.data.layers[11] = False

        bpy.ops.armature.select_all(action='DESELECT')
        Select2Bone("calf_fk.l","thigh_fk.l")
        bpy.ops.armature.parent_set(type='OFFSET')#指向活跃骨骼为父级
        bpy.ops.armature.select_all(action='DESELECT')

        MakeSureSelectOneLayer(17)
        bpy.context.object.data.layers[14] = False

        bpy.ops.armature.select_all(action='DESELECT')
        Select2Bone("calf_fk.r","thigh_fk.r")
        bpy.ops.armature.parent_set(type='OFFSET')#指向活跃骨骼为父级
        bpy.ops.armature.select_all(action='DESELECT')


        #bpy.ops.armature.duplicate_move(ARMATURE_OT_duplicate={"do_flip_names":False}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
        #bpy.ops.armature.bone_layers(layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False))
        #bpy.ops.armature.select_all(action='DESELECT')

        #复制根骨骼
        MakeSureSelectOneLayer(28)
        bpy.context.object.data.layers[17] = False

        SelectBone("root")# 001你就是IK手根骨骼

        DuplicateMove()


        MakeSureSelectOneLayer(28)
        bpy.context.object.data.layers[29] = False

        SelectBone("root") # 002 脚
        DuplicateMove()

        MakeSureSelectOneLayer(23)
        bpy.context.object.data.layers[28] = False
        bpy.ops.armature.select_all(action='DESELECT')



        """
        MakeSureSelectOneLayer(29)
        bpy.context.object.data.layers[23] = False
        SelectBone("DEF-hand.r")#ik_hand_r(handr的位置)——>ik_hand_gun
        bpy.ops.armature.duplicate_move(ARMATURE_OT_duplicate={"do_flip_names":False}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
        bpy.ops.armature.bone_layers(layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False))
        #bpy.ops.armature.select_all(action='DESELECT')

        MakeSureSelectOneLayer(29)
        bpy.context.object.data.layers[23] = False
        SelectBone("DEF-hand.l")#ik_hand_l(handl的位置)——>ik_hand_gun
        bpy.ops.armature.duplicate_move(ARMATURE_OT_duplicate={"do_flip_names":False}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
        bpy.ops.armature.bone_layers(layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False))
        #bpy.ops.armature.select_all(action='DESELECT')

        MakeSureSelectOneLayer(29)
        bpy.context.object.data.layers[23] = False
        SelectBone("DEF-foot.r")#ik_foot_r(footr的位置)——> ik_foot_root
        bpy.ops.armature.duplicate_move(ARMATURE_OT_duplicate={"do_flip_names":False}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
        bpy.ops.armature.bone_layers(layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False))
        #bpy.ops.armature.select_all(action='DESELECT')

        MakeSureSelectOneLayer(29)
        bpy.context.object.data.layers[23] = False
        SelectBone("DEF-foot.l")#ik_foot_l(footl的位置)——>ik_foot_root
        bpy.ops.armature.duplicate_move(ARMATURE_OT_duplicate={"do_flip_names":False}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
        bpy.ops.armature.bone_layers(layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False))
        #bpy.ops.armature.select_all(action='DESELECT')
        """

        MakeSureSelectOneLayer(23)
        bpy.context.object.data.layers[28] = False
        bpy.ops.object.mode_set(mode='OBJECT')
        #复制手骨骼

        #MakeSureSelectOneLayer(29)
        #bpy.context.object.data.layers[17] = False
        #bpy.ops.armature.select_all(action='DESELECT')

        #SelectBone("DEF-hand.r.001")#ik_hand_gun(handr的位置)——>ik_hand_root

        #SelectBone("DEF-hand.r.001")#ik_hand_r(handr的位置)——>ik_hand_gun

        #SelectBone("DEF-hand.l.001")#ik_hand_l(handl的位置)——>ik_hand_gun

        #SelectBone("DEF-foot.r.001")#ik_foot_r(footr的位置)——> ik_foot_root

        #SelectBone("DEF-foot.l.001")#ik_foot_l(footl的位置)——>ik_foot_root
        #bpy.ops.armature.duplicate_move(ARMATURE_OT_duplicate={"do_flip_names":False}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":0.0220949, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})


        #bpy.ops.armature.select_all(action='SELECT')
        #bpy.context.object.data.bones["root.001"].name = "ik_foot_root"#ik_foot_root ik_hand_root
        #bpy.context.object.data.bones["root.002"].name = "ik_hand_root"

        self.report({'INFO'}, "Add UE4 Type Bone")
        return {'FINISHED'}





