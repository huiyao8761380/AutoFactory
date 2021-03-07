import bpy
from AutoFactory import BL_Properties#AMProperties
from .RIG_Tool import *


class AutoLatticeShape(bpy.types.Operator):
    bl_idname = "am.autolatticeshape"
    bl_label = "AutoLatticeShape"
    bl_description = "选择多个物体，其中活动物体为晶格体，其他的为网格" 
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        amProperty = context.scene.amProperties
        sel = bpy.context.selected_objects

        Latticename=bpy.context.object.name
        ObjL_vertex_group=amProperty.LeftBodyGroupSTR#'LeftBody'#给予各个中心边缘点50%权重，且不要漏选
        ObjR_vertex_group=amProperty.RightBodyGroupSTR#'RightBody'#给予各个中心边缘点50%权重，且不要漏选
        vertex_group=amProperty.VertexGroupSTR
        
        ObjsName=[]

        sel.remove(bpy.context.active_object)
        for ob in sel:
            #if (ob.name!=ObjName) and (ob.type=='LATTICE'):
            ObjsName.append(ob.name)

                #ObjName=ob.name#'Human'



        Lattice=bpy.data.objects[Latticename]

        Lattice.data.name=Latticename
        LatticeData=bpy.data.lattices[Latticename]

        for ObjName in ObjsName:

            ObjShapeKeyList=[]


            
            RealObj=bpy.data.objects[ObjName]
            RealObjData=bpy.data.objects[ObjName].data



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
                            
                            bpy.context.object.name=bpy.context.object.name.split('.')[0]+'_'+key.name#若包含下划线会去掉。。
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
                RealObj.active_shape_key_index=0

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
                        RealObj.active_shape_key_index=0
                        
                        #for key in shapekey.key_blocks:
                        for i in range(len(ObjShapeKeyList)):
                            #int(next(ShapeCount))
                            
                            RealObj.active_shape_key_index+=1
                            
                            shapename=RealObj.active_shape_key.name.split('_')[1]
                            RealObj.active_shape_key.value=0
                            RealObj.active_shape_key.slider_min = -1
                            RealObj.active_shape_key.name=shapename
                            RealObj.active_shape_key.vertex_group = vertex_group


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



class ShapekeyDriver(bpy.types.Operator):
    bl_idname = "am.shapekeydriver"
    bl_label = "ShapekeyDriver"
    bl_description = "选择至少两个物体，同步所选物体至活动物体的重名形状键" 
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        #Driver
        #obj=bpy.context.object
        #啊这 直接拿来用了https://blender.stackexchange.com/questions/86757/python-how-to-connect-shapekeys-via-drivers

        selected_obj = bpy.context.selected_objects
        active_obj = bpy.context.active_object
        shapekey_list_string = str(active_obj.data.shape_keys.key_blocks.keys())


        for obj in selected_obj:
            if not obj == active_obj:
                for key in obj.data.shape_keys.key_blocks:
                    if key.name.lstrip(obj.name) in shapekey_list_string:
                        if not key.name == "Basis":
                            skey_driver = key.driver_add('value')
                            skey_driver.driver.type = 'AVERAGE'
                        # skey_driver.driver.show_debug_info = True
                            newVar = skey_driver.driver.variables.new()
                            newVar.name = "var"
                            newVar.type = 'SINGLE_PROP'
                            newVar.targets[0].id_type = 'KEY'
                            newVar.targets[0].id = active_obj.data.shape_keys
                            newVar.targets[0].data_path = 'key_blocks["' + key.name.lstrip(obj.name)+ '"].value' 
                            # litlle change was made here by deleting the active object name for the path


        #add_driver(SourceType,Source,SourceDataPath,SourceIndex,expType,exp,TargetNum,FuncName,FuncType,TargetType,targetName,TargetDataPath,transform_type,transform_space,rotation_mode)
        #add_driver('OBJECT',RealObj.name,0,SourceIndex,expType,exp,TargetNum,FuncName,FuncType,TargetType,targetName,TargetDataPath,transform_type,transform_space,rotation_mode)


        self.report({'INFO'}, "Done")

        return {'FINISHED'}



class TransferAllKey(bpy.types.Operator):
    bl_idname = "am.transferallkey"
    bl_label = "TransferAllKey"
    bl_description = "选择两个物体，传递所有形态键到活动物体(适用于双晶格体或不识别的镜像物体)" 
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        sel = bpy.context.selected_objects
        amProperty = context.scene.amProperties
        ActObj=bpy.context.active_object
        vertex_group=amProperty.VertexGroupSTR
        bpy.context.active_object

        sel.remove(bpy.context.active_object)


        for ob in sel:
            if (ob.name!=bpy.context.active_object) and (ob.type=='MESH'):
                selObj=ob
        selObj.active_shape_key_index = 0

        #bpy.context.active_object.data.shape_keys

        #selObj.active_shape_key
        for i in range(len(selObj.data.shape_keys.key_blocks)):
            selObj.active_shape_key_index=i

            bpy.ops.object.shape_key_transfer()
            ActObj.active_shape_key.vertex_group = selObj.active_shape_key.vertex_group
            #bpy.data.shape_keys["Key.015"].key_blocks["TriangleUP"].slider_min = -1
            ActObj.active_shape_key.slider_min = -1
            #bpy.context.object.active_shape_key_index = 0
        bpy.context.object.show_only_shape_key = False
        


        self.report({'INFO'}, "Done")

        return {'FINISHED'}

class BlendKey(bpy.types.Operator):
    bl_idname = "am.blendkey"
    bl_label = "BlendKey"
    bl_description = "将活动物体相似名称且相同排序形态键合并(适用于双晶格体或不识别的镜像物体)" 
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):

        ActObj=bpy.context.active_object

        ActObj.active_shape_key_index = 0

        #ActObj.active_shape_key.name
        maxmirror=len(ActObj.data.shape_keys.key_blocks)
        for i in range(int(maxmirror/2)):
            #if '_blend' not in ActObj.active_shape_key.name:
            ActObj.active_shape_key_index = i
            onekey=ActObj.active_shape_key
            onekey.value=100
            onekey.slider_min = -1
            oneName=ActObj.active_shape_key.name


            ActObj.active_shape_key_index = i+int(maxmirror/2)
            twokey=ActObj.active_shape_key
            twokey.value=100
            twokey.slider_min = -1
            bpy.ops.object.shape_key_add(from_mix=True)
            ActObj.active_shape_key.name=oneName+'_blend'
            ActObj.active_shape_key.slider_min = -1
            onekey.value=0
            twokey.value=0
            '''
            for key in ActObj.data.shape_keys.key_blocks:#这些地方有问题
                if (oneName in key.name) and(oneName != key.name):
                    twokey=key
                    twokey.value=100

            bpy.ops.object.shape_key_add(from_mix=True)
            ActObj.active_shape_key.name=oneName+'_blend'
            onekey.value=0
            if twokey.name in ActObj.data.shape_keys.key_blocks:
                twokey.value=0
            '''

        bpy.context.object.active_shape_key_index = maxmirror-1

        #ActObj.active_shape_key_index=maxmirror
        for i in range(maxmirror):
            bpy.ops.object.shape_key_remove(all=False)

        for key in ActObj.data.shape_keys.key_blocks:
            key.name=key.name.split('_')[0]



        self.report({'INFO'}, "Done")

        return {'FINISHED'}



class Bonelayered(bpy.types.Operator):
    bl_idname = "am.bonelayered"
    bl_label = "Bonelayered"
    bl_description = "开关形变，将名称或所选骨骼及子集通过开关形变的方式进行骨骼分层切换，有助于更换身体部位，例如头与身体的分离，随时替换修改导出" 
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        amProperty = context.scene.amProperties


        #bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.object.mode_set(mode='EDIT')
        if amProperty.BoneSTR!='':
            SelectBone(amProperty.BoneSTR)
        parentbone=bpy.context.active_bone
        parentbonename=bpy.context.active_bone.name


        #选择face
        #alt 点击 形变
        bpy.ops.armature.select_similar(type='CHILDREN')
        if parentbone.use_deform == True:#bpy.context.object.data.edit_bones[parentbonename]

            for bone in bpy.context.selected_bones:
                #if bone.use_deform == True:
                bone.use_deform = False
                #else:
        else:
            for bone in bpy.context.selected_bones:
                bone.use_deform = True

        bpy.ops.armature.select_all(action='DESELECT')
        SelectBone(parentbonename)
        bpy.context.object.data.edit_bones[parentbonename]
        bpy.ops.object.mode_set(mode='OBJECT')

        






        self.report({'INFO'}, "Done")

        return {'FINISHED'}