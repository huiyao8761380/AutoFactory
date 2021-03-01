import bpy
import bmesh
from .BL_Tool import *


class WeightRig(bpy.types.Operator):
    bl_idname = "aw.weightrig"
    bl_label = "Weight Rig"
    bl_description = "(Old)Paint Weight for Rig,在此之前需要应用修改器"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        RigMaster = bpy.data.objects["7BindRig"]
        for Rigobj in bpy.data.collections["7BindRig"].objects:
            if Rigobj.name != '7BindRig':
                # for Rigobj in RigMaster.objects:

                RigMaster.select_set(False)
                Rigobj.select_set(True)
                bpy.context.view_layer.objects.active = Rigobj

                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT', action='TOGGLE')

                me = Rigobj.data

                # bm = bmesh.from_edit_mesh(me)
                # 设置你的顶点索引值
                # v_index = 0

                # 遍历顶点组
                for group in Rigobj.vertex_groups:

                    # 将当前顶点组设置为活动的_.
                    if Rigobj.name == group.name:
                        bpy.ops.object.vertex_group_set_active(group=str(group.name))

                        # 选择活动顶点组
                        bpy.ops.object.vertex_group_select()

                        # 获取当前选择的所有顶点(可能不用)
                        # vertices = [v for v in bm.verts if (v.select and not v.hide)]

                        bpy.ops.mesh.select_all(action='SELECT')  # 选择所有该顶点组的网格

                        bpy.ops.object.vertex_group_assign()  # 赋予
                        # 顶点的迭代 vertex iteration(可能不用)
                        '''
                        for vertex in vertices:
                            if vertex.index ==  v_index:
                                print("Vertex ", v_index, " is in ", group.name)        
                        '''
                        # 取消选择当前顶点组
                        bpy.ops.object.vertex_group_deselect()

                bmesh.update_edit_mesh(me, True)
                bpy.ops.object.mode_set(mode='OBJECT')

            # 在viewport中显示更新 show the updates in the viewport

        '''
            #if Rigobj.vertex_groups[GROUP_NAME]:
            if Rigobj.name == Rigobj.vertex_groups[GROUP_NAME].name:
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT', action='TOGGLE')
                    bpy.ops.mesh.select_all(action='SELECT')
                    RigobjVg = Rigobj.vertex_groups[GROUP_NAME].get
                    bpy.ops.object.vertex_group_assign()


            #遍历顶点组
            for group in Rigobj.vertex_groups:
                
                #将当前顶点组设置为活动的
                bpy.ops.object.vertex_group_set_active(group=str(group.name))

                # 选择活动顶点组
                bpy.ops.object.vertex_group_select()

                #获取当前选择的所有顶点
                vertices = [v for v in bm.verts if (v.select and not v.hide)]

                #顶点的迭代 vertex iteration
                for vertex in vertices:
                    if vertex.index ==  v_index:
                        print("Vertex ", v_index, " is in ", group.name)        

                #取消选择当前顶点组        
                bpy.ops.object.vertex_group_deselect()

        '''

        # gi = Rigobj.vertex_groups[GROUP_NAME].index
        # for v in Rigobj.data.vertices:
        # for g in v.groups:
        # for RigobjVg in Rigobj.vertex_groups:
        # if Rigobj.name == Rigobj.vertex_groups:

        self.report({'INFO'}, "7BindRig")
        return {"FINISHED"}


def register():
    bpy.utils.register_class(WeightRig)


def unregister():
    bpy.utils.unregister_class(WeightRig)
