import bpy
from .RIG_Tool import *
#from . BL_UE4type import *

#执行顺序3 Armature编辑模式

'''
def SelectBone(bone):#选择该层级的骨骼及子级

    bpy.ops.armature.select_all(action='DESELECT')
    SelectBone=bpy.context.object.data.edit_bones[bone]

    SelectBone.select_head = True
    SelectBone.select_tail = True
    SelectBone.select = True

    bpy.context.object.data.edit_bones.active = SelectBone #GOOD!
'''

class ReBone(bpy.types.Operator):
    bl_idname = "am.rebone"
    bl_label = "ReBone"
    bl_description = "设置要导出的UE4骨骼父级指向" 
    bl_options = {'REGISTER'}

    def execute(self, context):

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.armature.select_all(action='SELECT')
        bpy.context.object.data.use_mirror_x = False

        for bone in bpy.context.selected_bones:#bpy.context.edit_bones:
            #if bone.name='root':
            #SetBoneParent(bone.name,bone.name[:-4])
            if "ORG-lip" in bone.name:
                bone.parent = bpy.context.object.data.edit_bones['ORG-face.001']
            if "ORG-cheek" in bone.name:
                bone.parent = bpy.context.object.data.edit_bones['ORG-face.001']
            if "ORG-nose" in bone.name:
                bone.parent = bpy.context.object.data.edit_bones['ORG-face.001']

        for bone in bpy.context.selected_bones:
            if ('belly' in bone.name) or ('Wing' in bone.name) or ('tail' in bone.name) or ('side_fin' in bone.name) or ('front_toe' in bone.name):
                bpy.ops.object.mode_set(mode='OBJECT')
                return {'FINISHED'}

        MakeSureSelectOneLayer(23)
        #！！！这里判断29层是否存在ORG-face.001
        if "ORG-face" in bpy.context.object.data.bones:
            #额头
            SetBoneParent("ORG-forehead.L.003","ORG-face.001")
            SetBoneParent("ORG-forehead.L.004","ORG-face.001")
            SetBoneParent("ORG-forehead.L.005","ORG-face.001")


            #眉毛
            SetBoneParent("ORG-brow.T.L.007","ORG-face.001")

            SetBoneParent("ORG-brow.T.L.006","ORG-face.001")

            SetBoneParent("ORG-brow.T.L.005","ORG-face.001")

            SetBoneParent("ORG-brow.T.L.004","ORG-face.001")


            #眼部
            SetBoneParent("ORG-brow.B.L.007","ORG-face.001")

            SetBoneParent("ORG-brow.B.L.006","ORG-face.001")

            SetBoneParent("ORG-brow.B.L.005","ORG-face.001")

            SetBoneParent("ORG-brow.B.L.004","ORG-face.001")


            SetBoneParent("ORG-lid.T.L.007","ORG-face.001")

            SetBoneParent("ORG-lid.T.L.006","ORG-face.001")

            SetBoneParent("ORG-lid.T.L.005","ORG-face.001")

            SetBoneParent("ORG-lid.T.L.004","ORG-face.001")


            SetBoneParent("ORG-lid.B.L.007","ORG-face.001")

            SetBoneParent("ORG-lid.B.L.006","ORG-face.001")

            SetBoneParent("ORG-lid.B.L.005","ORG-face.001")

            SetBoneParent("ORG-lid.B.L.004","ORG-face.001")


            SetBoneParent("ORG-eye.L.001","ORG-face.001")




            #脸颊
            SetBoneParent("ORG-cheek.T.L.003","ORG-face.001")

            SetBoneParent("ORG-cheek.T.L.002","ORG-face.001")

            SetBoneParent("ORG-cheek.B.L.003","ORG-face.001")

            SetBoneParent("ORG-cheek.B.L.002","ORG-face.001")

            SetBoneParent("ORG-chin.L.001","ORG-face.001")

            SetBoneParent("ORG-jaw.L.002","ORG-face.001")

            SetBoneParent("ORG-jaw.L.003","ORG-face.001")

            #耳朵
            SetBoneParent("ORG-ear.L.005","ORG-face.001")

            SetBoneParent("ORG-ear.L.009","ORG-face.001")

            SetBoneParent("ORG-ear.L.008","ORG-face.001")

            SetBoneParent("ORG-ear.L.007","ORG-face.001")

            #嘴巴
            SetBoneParent("ORG-lip.T.L.003","ORG-face.001")

            SetBoneParent("ORG-lip.B.L.003","ORG-face.001")


            #鼻翼

            SetBoneParent("ORG-nose.L.003","ORG-face.001")

            SetBoneParent("ORG-nose.L.002","ORG-face.001")

            #___________________________________________________






            #额头
            SetBoneParent("ORG-forehead.R.003","ORG-face.001")
            SetBoneParent("ORG-forehead.R.004","ORG-face.001")
            SetBoneParent("ORG-forehead.R.005","ORG-face.001")


            #眉毛
            SetBoneParent("ORG-brow.T.R.007","ORG-face.001")

            SetBoneParent("ORG-brow.T.R.006","ORG-face.001")

            SetBoneParent("ORG-brow.T.R.005","ORG-face.001")

            SetBoneParent("ORG-brow.T.R.004","ORG-face.001")


            #眼部
            SetBoneParent("ORG-brow.B.R.007","ORG-face.001")

            SetBoneParent("ORG-brow.B.R.006","ORG-face.001")

            SetBoneParent("ORG-brow.B.R.005","ORG-face.001")

            SetBoneParent("ORG-brow.B.R.004","ORG-face.001")


            SetBoneParent("ORG-lid.T.R.007","ORG-face.001")

            SetBoneParent("ORG-lid.T.R.006","ORG-face.001")

            SetBoneParent("ORG-lid.T.R.005","ORG-face.001")

            SetBoneParent("ORG-lid.T.R.004","ORG-face.001")


            SetBoneParent("ORG-lid.B.R.007","ORG-face.001")

            SetBoneParent("ORG-lid.B.R.006","ORG-face.001")

            SetBoneParent("ORG-lid.B.R.005","ORG-face.001")

            SetBoneParent("ORG-lid.B.R.004","ORG-face.001")


            SetBoneParent("ORG-eye.R.001","ORG-face.001")




            #脸颊
            SetBoneParent("ORG-cheek.T.R.003","ORG-face.001")

            SetBoneParent("ORG-cheek.T.R.002","ORG-face.001")

            SetBoneParent("ORG-cheek.B.R.003","ORG-face.001")

            SetBoneParent("ORG-cheek.B.R.002","ORG-face.001")

            SetBoneParent("ORG-chin.R.001","ORG-face.001")

            SetBoneParent("ORG-jaw.R.002","ORG-face.001")

            SetBoneParent("ORG-jaw.R.003","ORG-face.001")

            #耳朵
            SetBoneParent("ORG-ear.R.005","ORG-face.001")

            SetBoneParent("ORG-ear.R.009","ORG-face.001")

            SetBoneParent("ORG-ear.R.008","ORG-face.001")

            SetBoneParent("ORG-ear.R.007","ORG-face.001")

            #嘴巴
            SetBoneParent("ORG-lip.T.R.003","ORG-face.001")

            SetBoneParent("ORG-lip.B.R.003","ORG-face.001")


            #鼻翼

            SetBoneParent("ORG-nose.R.003","ORG-face.001")

            SetBoneParent("ORG-nose.R.002","ORG-face.001")



            #鼻子___________________________________
            SetBoneParent("ORG-nose.009","ORG-face.001")

            SetBoneParent("ORG-nose.008","ORG-face.001")

            SetBoneParent("ORG-nose.006","ORG-face.001")

            SetBoneParent("ORG-nose.007","ORG-face.001")

            SetBoneParent("ORG-nose.005","ORG-face.001")

            #舌头
            #5 4 ORG-tongue.003
            SetBoneParent("ORG-tongue.005","ORG-face.001")

            SetBoneParent("ORG-tongue.004","ORG-face.001")

            SetBoneParent("ORG-tongue.003","ORG-face.001")


            #下巴 ORG-chin.003 2 ORG-jaw.001 

            SetBoneParent("ORG-chin.003","ORG-face.001")

            SetBoneParent("ORG-chin.002","ORG-face.001")

            SetBoneParent("ORG-jaw.001","ORG-face.001")





        #身体!!!!!!!!!!
        #DE F-upperarm.l.002 DEF-clavicle.l.001
        SetBoneParent("DEF-upperarm.l.002","DEF-clavicle.l.001")
        SetBoneParent("DEF-lowerarm.l.002","DEF-upperarm.l.002")
        SetBoneParent("DEF-hand.l.001","DEF-lowerarm.l.002")

        SetBoneParent("DEF-calf.l.002","DEF-thigh.l.002")
        SetBoneParent("DEF-foot.l.001","DEF-calf.l.002")



        ##########

        SetBoneParent("DEF-breast.l.001","DEF-spine.004")

        SetBoneParent("DEF-clavicle.l.001","DEF-spine.004")

        SetBoneParent("DEF-pelvis.l.001","DEF-pelvis.001")
        SetBoneParent("DEF-thigh.l.002","DEF-pelvis.l.001")


        #脚 自定义的
        if 'DEF-feet_thumb.01' in bpy.context.object.data.bones:
            SetBoneParent("DEF-feet_thumb.01.L.001","DEF-ball.l.001")
            SetBoneParent("DEF-feet_pinky.01.L.001","DEF-ball.l.001")

        #手
        if 'DEF-f_index.01.L' in bpy.context.object.data.bones:
            SetBoneParent("DEF-f_index.01.L.001","DEF-palm.01.L.001")
            SetBoneParent("DEF-f_middle.01.L.001","DEF-palm.02.L.001")
            SetBoneParent("DEF-f_ring.01.L.001","DEF-palm.03.L.001")
            SetBoneParent("DEF-f_pinky.01.L.001","DEF-palm.04.L.001")

            SetBoneParent("DEF-palm.01.L.001","DEF-hand.l.001")
            SetBoneParent("DEF-palm.02.L.001","DEF-hand.l.001")
            SetBoneParent("DEF-palm.03.L.001","DEF-hand.l.001")
            SetBoneParent("DEF-palm.04.L.001","DEF-hand.l.001")

            SetBoneParent("DEF-thumb.01.L.001","DEF-hand.l.001")





        #身体rrrrrrrrrrrrrr
        SetBoneParent("DEF-upperarm.r.002","DEF-clavicle.r.001")
        SetBoneParent("DEF-lowerarm.r.002","DEF-upperarm.r.002")
        SetBoneParent("DEF-hand.r.001","DEF-lowerarm.r.002")

        SetBoneParent("DEF-calf.r.002","DEF-thigh.r.002")
        SetBoneParent("DEF-foot.r.001","DEF-calf.r.002")
        #######
        SetBoneParent("DEF-breast.r.001","DEF-spine.004")

        SetBoneParent("DEF-clavicle.r.001","DEF-spine.004")


        SetBoneParent("DEF-pelvis.r.001","DEF-pelvis.001")
        SetBoneParent("DEF-thigh.r.002","DEF-pelvis.r.001")


        #脚 自定义的
        if 'DEF-feet_thumb.01' in bpy.context.object.data.bones:
            SetBoneParent("DEF-feet_thumb.01.R.001","DEF-ball.r.001")
            SetBoneParent("DEF-feet_pinky.01.R.001","DEF-ball.r.001")

        #手
        if 'DEF-f_index.01.R' in bpy.context.object.data.bones:
            SetBoneParent("DEF-f_index.01.R.001","DEF-palm.01.R.001")
            SetBoneParent("DEF-f_middle.01.R.001","DEF-palm.02.R.001")
            SetBoneParent("DEF-f_ring.01.R.001","DEF-palm.03.R.001")
            SetBoneParent("DEF-f_pinky.01.R.001","DEF-palm.04.R.001")

            SetBoneParent("DEF-palm.01.R.001","DEF-hand.r.001")
            SetBoneParent("DEF-palm.02.R.001","DEF-hand.r.001")
            SetBoneParent("DEF-palm.03.R.001","DEF-hand.r.001")
            SetBoneParent("DEF-palm.04.R.001","DEF-hand.r.001")

            SetBoneParent("DEF-thumb.01.R.001","DEF-hand.r.001")

        bpy.ops.armature.select_all(action='DESELECT')
        SelectBone("DEF-hand.r.001")#ik_hand_gun(handr的位置)——>ik_hand_root
        bpy.ops.armature.duplicate_move(ARMATURE_OT_duplicate={"do_flip_names":False}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":0.0220949, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})

        SelectBone("DEF-hand.r.001")#ik_hand_r(handr的位置)——>ik_hand_gun
        bpy.ops.armature.duplicate_move(ARMATURE_OT_duplicate={"do_flip_names":False}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":0.0220949, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})

        SelectBone("DEF-hand.l.001")#ik_hand_l(handl的位置)——>ik_hand_gun
        bpy.ops.armature.duplicate_move(ARMATURE_OT_duplicate={"do_flip_names":False}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":0.0220949, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})

        SelectBone("DEF-foot.r.001")#ik_foot_r(footr的位置)——> ik_foot_root
        bpy.ops.armature.duplicate_move(ARMATURE_OT_duplicate={"do_flip_names":False}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":0.0220949, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})

        SelectBone("DEF-foot.l.001")#ik_foot_l(footl的位置)——>ik_foot_root
        bpy.ops.armature.duplicate_move(ARMATURE_OT_duplicate={"do_flip_names":False}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":0.0220949, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})



        SetBoneParent("DEF-hand.r.003","root.001")#ik_hand_gun 003
        SetBoneParent("DEF-hand.r.002","DEF-hand.r.003")#ik_hand_r 002
        SetBoneParent("DEF-hand.l.002","DEF-hand.r.003")#ik_hand_l 002

        SetBoneParent("DEF-foot.r.002","root.002")#ik_foot_r 002 
        SetBoneParent("DEF-foot.l.002","root.002")#ik_foot_l 002 



        #骨骼名称为Armature时才会删掉
        #CleanBoneParent("DEF-pelvis.001")
        #CleanBoneParent("root.001")
        #CleanBoneParent("root.002")

        



        SetBoneParent("root.001","root")#ik_hand_root 001不能有父级
        SetBoneParent("root.002","root")#ik_foot_root 002不能有父级
        bpy.ops.object.mode_set(mode='OBJECT')

        self.report({'INFO'}, "Add UE4 Type Bone")
        return {'FINISHED'}
