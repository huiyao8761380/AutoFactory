import bpy



#执行顺序5 点击绑定好的人体模型清理含有ik昵称的顶点组ik权重
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')


ob = bpy.context.edit_object

avg = ob.vertex_groups.active
for vg in ob.vertex_groups:
    ob.vertex_groups.active = vg
    if vg.name.find("ik_") != -1:
        bpy.ops.object.vertex_group_remove_from()
ob.vertex_groups.active = avg

bpy.ops.object.mode_set(mode='OBJECT')

"""