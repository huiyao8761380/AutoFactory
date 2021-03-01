import bpy
from . BL_Tool import *


class BindRig(bpy.types.Operator):
    bl_idname = "aw.bindrig"
    bl_label = "Bind Rig"
    bl_description = "(Old)Bind Rig,select obj, then bind it to the rig"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        if "6AddRig" in bpy.data.objects:
            for obj in bpy.data.objects:
                #把该物体放到该合集
                if obj.name =='6AddRig':
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.select_all(action='SELECT')
                    obj.select_set(True)
                    bpy.ops.object.parent_set(type='ARMATURE_NAME')
                    col_name="7BindRig"
                    addrig = bpy.data.objects[obj.name]
                    cube_collection = find_collection(bpy.context, addrig)#2通过函数find_collection制作合集
                    new_collection = make_collection(col_name,bpy.data.collections["0AutoMech"])
                    col = bpy.data.collections.get(col_name)#4
                    col.objects.link(addrig)
                    cube_collection.objects.unlink(addrig)
                    addrig.name = col_name
                else:
                    col_name="7BindRig"
                    addrig = bpy.data.objects[obj.name]
                    cube_collection = find_collection(bpy.context, addrig)#2通过函数find_collection制作合集
                    new_collection = make_collection(col_name,bpy.data.collections["0AutoMech"])
                    col = bpy.data.collections.get(col_name)#4
                    col.objects.link(addrig)
                    cube_collection.objects.unlink(addrig)

        elif "7BindRig" in bpy.data.objects:
            
            for obj in bpy.data.objects:
                if obj.name == "7BindRig":
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.select_all(action='SELECT')
                    obj.select_set(True)
                    bpy.ops.object.parent_set(type='ARMATURE_NAME')#绑定附带空顶点组

#bpy.ops.object.parent_set(type='ARMATURE')骨骼形变
#bpy.ops.object.parent_set(type='ARMATURE_NAME')空顶点组V
#bpy.ops.object.parent_set(type='ARMATURE_ENVELOPE')封套权重
#bpy.ops.object.parent_set(type='ARMATURE_AUTO')自动权重


                else:
                    col_name="7BindRig"
                    addrig = bpy.data.objects[obj.name]
                    cube_collection = find_collection(bpy.context, addrig)#2通过函数find_collection制作合集
                    new_collection = make_collection(col_name,bpy.data.collections["0AutoMech"])
                    col = bpy.data.collections.get(col_name)#4

                    #genLine_result = bpy.data.collections[col_name]
                    #if obj.name not in genLine_result.objects[obj.name]:

                    #col for col in bpy.data.collections if col not in y]
                    #for childObject in genLine_result.objects:

                #if obj.modifiers.get("Armature"):# in obj.modifiers:
                    #return
                #else:
                    #other=bpy.data.objects[obj.name]
                    #col.objects.link(addrig)
                    #cube_collection.objects.unlink(addrig)

                    '''                 
                    col_name="7BindRig"
                    addrig = bpy.data.objects[obj.name]
                    cube_collection = find_collection(bpy.context, addrig)#2通过函数find_collection制作合集
                    new_collection = make_collection(col_name,cube_collection)
                    col = bpy.data.collections.get(col_name)#4

                    #rigcol=bpy.data.collections[col_name]
                    #bpy.ops.object.move_to_collection(rigcol)
                    if obj != col.objects:
                        col.objects.link(addrig)
                        bpy.context.objects.unlink(addrig)
                    '''
            
        #对于骨骼里的物体，如果他的名字等于它的顶点组
            #那么切换到物体的编辑模式，顶点模式 我们将它的顶点全选 之后全部指定给它的顶点组

        '''
        RigMaster = bpy.data.objects["7BindRig"]
        for Rigobj in bpy.data.collections["7BindRig"].objects:
        #for Rigobj in RigMaster.objects:

            RigMaster.select_set(False)
            Rigobj.select_set(True)
            bpy.context.view_layer.objects.active = Rigobj
            
            GROUP_NAME=Rigobj.name
            #if Rigobj.vertex_groups[GROUP_NAME]:
            if Rigobj.name == Rigobj.vertex_groups[GROUP_NAME].name:
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT', action='TOGGLE')
                    bpy.ops.mesh.select_all(action='SELECT')
                    RigobjVg = Rigobj.vertex_groups[GROUP_NAME].get
                    bpy.ops.object.vertex_group_assign()
        '''
            
            #gi = Rigobj.vertex_groups[GROUP_NAME].index
            #for v in Rigobj.data.vertices:
                #for g in v.groups:
            #for RigobjVg in Rigobj.vertex_groups:
            #if Rigobj.name == Rigobj.vertex_groups:
                
        self.report({'INFO'}, "7BindRig")
        return {"FINISHED"}

