import bpy
from AutoFactory import BL_Properties#AMProperties


class AutoLatticeShape(bpy.types.Operator):
    bl_idname = "am.autolatticeshape"
    bl_label = "AutoLatticeShape"
    bl_description = "选择两个物体，其中活动物体为网格，另一个为晶格体" 
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        amProperty = context.scene.amProperties
        sel = bpy.context.selected_objects

        ObjName=bpy.context.object.name#'Human'
        ObjL_vertex_group=amProperty.LeftBodyGroupSTR#'LeftBody'#给予各个中心边缘点50%权重，且不要漏选
        ObjR_vertex_group=amProperty.RightBodyGroupSTR#'RightBody'#给予各个中心边缘点50%权重，且不要漏选
        
        for ob in sel:
            if (ob.name!=ObjName) and (ob.type=='LATTICE'):
                Latticename=ob.name



        RealObj=bpy.data.objects[ObjName]
        RealObjData=bpy.data.objects[ObjName].data

        Lattice=bpy.data.objects[Latticename]

        Lattice.data.name=Latticename
        LatticeData=bpy.data.lattices[Latticename]

        ObjShapeKeyList=[]


        #delete all shape key for duplicate
        bpy.context.view_layer.objects.active = RealObj
        RealObj.select_set(True)
        bpy.ops.object.shape_key_add(from_mix=False)
        bpy.ops.object.shape_key_remove(all=True)


        for shapekey in bpy.data.shape_keys:
            if shapekey.user == LatticeData:
                print(ObjName)
                print(shapekey.name)
                print(LatticeData.name)
                for key in shapekey.key_blocks:#bpy.data.shape_keys["Key.002"].key_blocks["Hand"].name = "Hand"
                    key.value = 0
                    
                for key in shapekey.key_blocks:
                    key.value = 100#make it max! 
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.context.view_layer.objects.active = RealObj
                    RealObj.select_set(True)
                    
                        
                    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":14.7843, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
                    RealObj.select_set(False)
                    
                    if RealObj.name.split('.')[0] in bpy.context.object.name:
                        bpy.ops.object.apply_all_modifiers()
                        #if mirror：
                        bpy.context.object.name=bpy.context.object.name.split('.')[0]+'_'+key.name
                        key.value = 0
                        ObjShapeKeyList.append(bpy.context.object.name)
                        
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = RealObj
        RealObj.select_set(True)
        bpy.ops.object.shape_key_add(from_mix=False)#add a Basis shapekey
        #RealObj.active_shape_key_index=0


        print(ObjShapeKeyList)


        #如果是晶格体包围全身非镜像的：
        if amProperty.LatticeMirrorBool==False:
            for shapekey in bpy.data.shape_keys:
                if shapekey.user == RealObjData:
                    for ObjShapeName in ObjShapeKeyList:
                        
                        bpy.context.view_layer.objects.active = RealObj
                        RealObj.select_set(True)
                        
                        bpy.data.objects[ObjShapeName].select_set(True)
                        bpy.ops.object.join_shapes()
                        bpy.data.objects[ObjShapeName].select_set(False)
                        bpy.ops.object.select_all(action='DESELECT')
                        
                        
                    for key in shapekey.key_blocks:
                        key.value = 0


            #否则执行以下
        else:
            RealObj.active_shape_key_index=0

            for shapekey in bpy.data.shape_keys:
                if shapekey.user == RealObjData:
                    for ObjShapeName in ObjShapeKeyList:
                        
                        bpy.context.view_layer.objects.active = RealObj
                        RealObj.select_set(True)
                        
                        bpy.data.objects[ObjShapeName].select_set(True)
                        bpy.ops.object.join_shapes()
                        bpy.ops.object.join_shapes()
                        bpy.data.objects[ObjShapeName].select_set(False)
                        bpy.ops.object.select_all(action='DESELECT')
                        
                        
                        

                    for key in shapekey.key_blocks:
                        key.value = 0
                        
                    RealObj.active_shape_key_index=0
                    
                    #for key in shapekey.key_blocks:
                    for i in range(len(ObjShapeKeyList)):
                        #int(next(ShapeCount))
                        
                        RealObj.active_shape_key_index+=1
                        shapename=RealObj.active_shape_key.name.split('_')[1]
                        RealObj.active_shape_key.value=100
                        RealObj.active_shape_key.slider_min = -1
                        RealObj.active_shape_key.vertex_group = ObjL_vertex_group

                        RealObj.active_shape_key_index+=1#MirrorShapekey
                        RealObj.active_shape_key.value=100
                        RealObj.active_shape_key.slider_min = -1
                        RealObj.active_shape_key.vertex_group = ObjR_vertex_group
                        shapeindex=RealObj.active_shape_key_index
                        bpy.ops.object.shape_key_mirror(use_topology=False)
                        
                        bpy.ops.object.shape_key_add(from_mix=True)
                        RealObj.active_shape_key.name=shapename
                        RealObj.active_shape_key.slider_min = -1
                        RealObj.active_shape_key_index=shapeindex#len(shapekey.key_blocks)
                        bpy.ops.object.shape_key_remove(all=False)
                        bpy.ops.object.shape_key_remove(all=False)


        if amProperty.DeleteShapeObjBool==True:
            bpy.ops.object.select_all(action='DESELECT')
            #删除形状键网格体
            for ObjShapeName in ObjShapeKeyList:
                removeObj=bpy.data.objects[ObjShapeName]
                bpy.context.view_layer.objects.active = removeObj
                removeObj.select_set(True)
                bpy.ops.object.delete(use_global=False)



        self.report({'INFO'}, "Done")

        return {'FINISHED'}

class DefaultShapekey(bpy.types.Operator):
    bl_idname = "am.defaultshapekey"
    bl_label = "DefaultShapekey"
    bl_description = "将所选物体拥有的所有形状键设为0" 
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):

        #obj=bpy.context.object

        RealObj=bpy.context.object
        RealObjData=RealObj.data
        for shapekey in bpy.data.shape_keys:
            if shapekey.user == RealObjData:
                for key in shapekey.key_blocks:#bpy.data.shape_keys["Key.002"].key_blocks["Hand"].name = "Hand"
                    key.value = 0

        self.report({'INFO'}, "Done")

        return {'FINISHED'}