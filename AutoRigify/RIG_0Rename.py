import bpy






class RigRename(bpy.types.Operator):
    bl_idname = "am.rigrename"
    bl_label = "Rig Rename"
    bl_description = "将Rigify生成的materig重命名为UE4常用绑定格式" 
    bl_options = {'REGISTER'}

    def execute(self, context):
        sel = bpy.context.selected_objects
        if len(sel) == 0:
            bpy.ops.object.armature_human_metarig_add()
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.mode_set(mode='EDIT')
            
        else:
            for ob in sel:
                if ob.type == 'ARMATURE':#if bpy.context.object.type =='ARMATURE':
                    bpy.ops.object.select_all(action='DESELECT')
                    ob.select_set(True)
                    bpy.context.view_layer.objects.active = ob
                    bpy.ops.object.mode_set(mode='OBJECT')
                    bpy.ops.object.mode_set(mode='EDIT')



        bpy.context.object.data.use_mirror_x = True
        bpy.ops.armature.select_all(action='SELECT')
        #骨骼扭动 清零
        for bone in bpy.context.selected_bones:
            bpy.context.object.data.edit_bones[bone.name].roll = 0
        #执行顺序0 点击metarig 生成的骨骼名为Armature 判断是否是人型骨骼
        for bone in bpy.context.selected_bones:
            if ('belly' in bone.name) or ('Wing' in bone.name) or ('tail' in bone.name) or ('side_fin' in bone.name) or ('front_toe' in bone.name):
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
                return {'FINISHED'}
        bpy.context.object.data.bones["spine"].name = "pelvis"
        bpy.context.object.data.bones["spine.001"].name = "spine.01"
        bpy.context.object.data.bones["spine.002"].name = "spine.02"
        bpy.context.object.data.bones["spine.003"].name = "spine.03"
        bpy.context.object.data.bones["spine.004"].name = "neck.01"
        bpy.context.object.data.bones["spine.005"].name = "neck.02"#
        bpy.context.object.data.bones["spine.006"].name = "head"
        bpy.context.object.data.bones["shoulder.L"].name = "clavicle.l"
        bpy.context.object.data.bones["shoulder.R"].name = "clavicle.r"
        bpy.context.object.data.bones["upper_arm.L"].name = "upperarm.l"
        bpy.context.object.data.bones["upper_arm.R"].name = "upperarm.r"
        bpy.context.object.data.bones["forearm.L"].name = "lowerarm.l"
        bpy.context.object.data.bones["forearm.R"].name = "lowerarm.r"
        bpy.context.object.data.bones["hand.L"].name = "hand.l"
        bpy.context.object.data.bones["hand.R"].name = "hand.r"
        bpy.context.object.data.bones["pelvis.L"].name = "pelvis.l"
        bpy.context.object.data.bones["pelvis.R"].name = "pelvis.r"
        bpy.context.object.data.bones["thigh.L"].name = "thigh.l"
        bpy.context.object.data.bones["thigh.R"].name = "thigh.r"
        bpy.context.object.data.bones["shin.L"].name = "calf.l"
        bpy.context.object.data.bones["shin.R"].name = "calf.r"
        bpy.context.object.data.bones["foot.L"].name = "foot.l"
        bpy.context.object.data.bones["foot.R"].name = "foot.r"
        bpy.context.object.data.bones["toe.L"].name = "ball.l"
        bpy.context.object.data.bones["toe.R"].name = "ball.r"
        bpy.context.object.data.bones["breast.L"].name = "breast.l"
        bpy.context.object.data.bones["breast.R"].name = "breast.r"
        bpy.context.object.data.bones["heel.02.L"].name = "heel.l"
        bpy.context.object.data.bones["heel.02.R"].name = "heel.r"
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        self.report({'INFO'}, "Rig Rename")
        return {'FINISHED'}
