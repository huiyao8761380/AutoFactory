import bpy
from . BL_Tool import *


class AddRig(bpy.types.Operator):
    bl_idname = "aw.addrig"
    bl_label = "Add Rig"
    bl_description = "(Old)AddRig,please append the rigify add-on at first"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        
        if "6AddRig" not in bpy.data.objects:
            if "metarig" not in bpy.data.objects:
                if bpy.context.mode !='OBJECT':
                    bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.armature_basic_human_metarig_add()
                

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

                #bpy.ops.object.mode_set(mode='EDIT')
                #bpy.ops.armature.bone_primitive_add(name='root')
                #bpy.ops.transform.rotate(value=-1.5708, orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.mode_set(mode='EDIT')

                bpy.ops.armature.select_all(action='SELECT')

                #骨骼扭动 清零
                for bone in bpy.context.selected_bones:
                    bpy.context.object.data.edit_bones[bone.name].roll = 0

                #bpy.context.object.data.bones["pelvis"].select = True
                #bpy.context.object.data.bones["root"].select = True
                bpy.ops.armature.select_all(action='DESELECT')
                #bpy.context.object.data.edit_bones['pelvis'].parent = bpy.context.object.data.edit_bones['root']

                bpy.context.scene.tool_settings.transform_pivot_point = 'ACTIVE_ELEMENT'
                bpy.context.object.data.edit_bones["upperarm.l"].select_head = True
                bpy.context.object.data.edit_bones["upperarm.l"].select_tail = True
                bpy.context.object.data.edit_bones["upperarm.l"].select = True

                bpy.context.object.data.edit_bones["lowerarm.l"].select = True
                bpy.context.object.data.edit_bones["lowerarm.l"].select_head = True
                bpy.context.object.data.edit_bones["lowerarm.l"].select_tail = True

                bpy.context.object.data.edit_bones["hand.l"].select = True
                bpy.context.object.data.edit_bones["hand.l"].select_head = True
                bpy.context.object.data.edit_bones["hand.l"].select_tail = True

                bpy.context.scene.tool_settings.transform_pivot_point = 'ACTIVE_ELEMENT'


                bpy.ops.transform.rotate(value=-0.5, orient_axis='Y', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                #bpy.ops.transform.translate(value=(0, 0, 0.597073), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                bpy.ops.transform.translate(value=(0.22, 0, -0.355), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                bpy.ops.armature.select_all(action='DESELECT')

                bpy.context.object.data.edit_bones["upperarm.r"].select_head = True
                bpy.context.object.data.edit_bones["upperarm.r"].select_tail = True
                bpy.context.object.data.edit_bones["upperarm.r"].select = True

                bpy.context.object.data.edit_bones["lowerarm.r"].select = True
                bpy.context.object.data.edit_bones["lowerarm.r"].select_head = True
                bpy.context.object.data.edit_bones["lowerarm.r"].select_tail = True

                bpy.context.object.data.edit_bones["hand.r"].select = True
                bpy.context.object.data.edit_bones["hand.r"].select_head = True
                bpy.context.object.data.edit_bones["hand.r"].select_tail = True

                bpy.ops.transform.rotate(value=0.5, orient_axis='Y', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                #bpy.ops.transform.translate(value=(0, 0, 0.597073), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                bpy.ops.transform.translate(value=(-0.059, 0, 0.275), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                bpy.ops.armature.select_all(action='DESELECT')
                
                bpy.ops.object.mode_set(mode='OBJECT')
                


                bpy.ops.transform.resize(value=(4.8, 3.5, 3.5), orient_type='CURSOR', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
                
                for rig in bpy.data.objects:
                    #if "metarig" in bpy.data.objects:
                    if rig.name =='metarig':
                        rig.select_set(True)
                        col_name="6AddRig"
                        addrig = bpy.data.objects[rig.name]
                        cube_collection = find_collection(bpy.context, addrig)#2通过函数find_collection制作合集
                        new_collection = make_collection(col_name,bpy.data.collections["0AutoMech"])

                        col = bpy.data.collections.get(col_name)#4
                        col.objects.link(addrig)
                        cube_collection.objects.unlink(addrig)
                        move_to_collection(cube_collection.name,col_name)
                        addrig.name = col_name


        #for rig in bpy.data.objects:
            #if "metarig" in bpy.data.objects:
                #make_collection("6AddRig","0AutoMech")
                #bpy.data.collections["6AddRig"].objects.link(rig)

        #bpy.data.collections["0AutoMech"].objects.unlink(rig) 
        #make_collection("6AddRig","0AutoMech")
        #bpy.data.collections["4MechClean"].objects.link(rig)
        #only_find_object("metarig","6AddRig")
        self.report({'INFO'}, "6AddRig")
        return {"FINISHED"}


