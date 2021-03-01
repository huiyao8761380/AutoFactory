import bpy
import os
import random
from itertools import count
#import sys
#sys.path.append(r'C:/Users/Administrator/AppData/Roaming/Blender Foundation/Blender/2.82/scripts/addons/Bmesh clean 2_8x v1_1')
#import __init__

def find_collection(context, item):
    collections = item.users_collection
    if len(collections) > 0:
        return collections[0]
    return context.scene.collection

def make_collection(collection_name, parent_collection):
    if collection_name in bpy.data.collections:
        return bpy.data.collections[collection_name]
    else:
        new_collection = bpy.data.collections.new(collection_name)
        parent_collection.children.link(new_collection)
        return new_collection

def find_object(find_name,new_col):#通过名字找到该物体并放入或新建的合集名字，所有输入都为''""
    for FindCol in bpy.data.collections:#遍历所有合集
        FindCol_result = FindCol
        if len(FindCol_result.objects) > 0:#如果在当前Collection中有物体
            for FindObj in FindCol_result.objects:
                #此处添加的代码判断它的名字来获取
                if find_name in FindObj.name:#如果该物体的名字中出现Cube
                    FindObj.select_set(True)#选择所有找到有cube字符的物体
                    cube = bpy.data.objects[FindObj.name]#选择这些物体并赋值给cube
            #cube = bpy.data.objects["Cube.001"]
                    cube_collection = find_collection(bpy.context, cube)#通过函数find_collection制作合集
                    new_collection = make_collection(new_col, cube_collection)
                    # Step 2
                    #if aready in coll
                    if FindObj.name not in new_collection.objects:
                        new_collection.objects.link(cube)  
                        cube_collection.objects.unlink(cube)  
                    #cube.name = new_col

def move_to_collection(old_col, new_col):#是调用上面两个函数的函数，所有输入都为’‘ 或“” 这个是在知道合集固定名称的情况下使用
    genLine_result = bpy.data.collections[old_col]#在这个合集中找到所有物体，修改这里的合集0AutoMech
    if len(genLine_result.objects) > 0:#如果在当前Collection中有物体
        for childObject in genLine_result.objects:
        
            if childObject in bpy.context.selected_objects:
                #此处添加的代码判断它的名字来获取
                #if len(childObject.data.vertices) <=2500:
                #if find_name in childObject.name:#如果该物体的名字中出现Cube
                childObject.select_set(True)#选择所有找到有cube字符的物体
                cube = bpy.data.objects[childObject.name]#选择这些物体并赋值给cube
                cube_collection = find_collection(bpy.context, cube)#通过函数find_collection制作合集
                if cube_collection.name == "0AutoMech":
                    new_collection = make_collection(new_col,cube_collection)#, cube_collection)#NEW col 将合集交给1GenLine
                else:
                    new_collection = make_collection(new_col,bpy.data.collections['0AutoMech'])
                new_collection.objects.link(cube)  # put the cube in the new collection 从新合集中添加物体
                cube_collection.objects.unlink(cube)  # remove it from the old collection 从旧合集中删除物体
            else:
                childObject.select_set(False)

def move_object(Source_obj_name,Target_obj_name):#OBJ们的名称
    Source_obj=bpy.data.objects[Source_obj_name]#"原OBJ的名字"
    Target_obj=bpy.data.objects[Target_obj_name]#"目标OBJ的名字"

    Target_obj_collection = find_collection(bpy.context, Target_obj)

    Source_obj.parent = Target_obj
    Source_obj_collection = find_collection(bpy.context, Source_obj)
    if Target_obj_name in Source_obj_name:#
        Target_obj_collection.objects.link(Source_obj)
        Source_obj_collection.objects.unlink(Source_obj)

class HideChildObj(bpy.types.Operator):
    bl_idname = "am.hidechildobj"
    bl_label = "HideChildObj"
    bl_description = "开/关显示子物体,仅限非相机或灯光的物体" 
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        amProperty = context.scene.amProperties
        sel = bpy.context.selected_objects
        if amProperty.HideChildObj_Bool ==True:
            for ob in sel:
                #OBJ = bpy.data.objects[ob.name].parent#bpy.data.objects["Cube"].children len(bpy.data.objects["Cube"].modifiers) >=100
                if len(ob.modifiers) >= 50:#'MESH' in ob.parent.type:#如果没有父级那就直接执行
                    for ChildObj in ob.children:
                        ChildObj.hide_viewport = True#隐藏
                else:#如果有且是网格物体则执行
                    if not( 'CAMERA'  in ob.type or 'LIGHT' in ob.type):#if 'CAMERA' not in ob.type or 'LIGHT' not in ob.type:
                        for ParentChildObj in ob.parent.children:
                            ParentChildObj.hide_viewport = True
            amProperty.HideChildObj_Bool = False
            self.report({'INFO'}, "隐藏子物体")
        else:
            for ob in sel:
                
                if len(ob.modifiers) >= 50:#if ob.parent== []:
                    for ChildObj in ob.children:
                        ChildObj.hide_viewport = False
                else:
                    if not( 'CAMERA'  in ob.type or 'LIGHT' in ob.type):
                        for ParentChildObj in ob.parent.children:
                            ParentChildObj.hide_viewport = False#显示
            amProperty.HideChildObj_Bool = True
            self.report({'INFO'}, "显示子物体")

        return {'FINISHED'}
'''
class UnrealSize(bpy.types.Operator):
    bl_idname = "am.unrealsize"
    bl_label = "UnrealSize"
    bl_description = "设置UE4引擎缩放单位" 
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        amProperty = context.scene.amProperties
        if amProperty.UnrealSize_Bool ==False:
            bpy.context.scene.unit_settings.system = 'METRIC'
            bpy.context.scene.unit_settings.scale_length = 0.01
            bpy.context.space_data.clip_end = 1000000
            amProperty.UnrealSize_Bool =True
            self.report({'INFO'}, "Unreal Size")

        else:
            bpy.context.scene.unit_settings.system = 'METRIC'
            bpy.context.scene.unit_settings.scale_length = 1
            amProperty.UnrealSize_Bool =False
            self.report({'INFO'}, "Default Size")

        return {'FINISHED'}
'''


def HideChildObj_update(self, context):
    amProperty = context.scene.amProperties
    sel = bpy.context.selected_objects
    #ActiveObj = bpy.context.active_object
    #if ActiveObj.children[0].hide_viewport == True:
        #amProperty.HideChildObj_Bool == True
    #else:
        #amProperty.HideChildObj_Bool == False

    if amProperty.HideChildObj_Bool ==True:#False
        if sel == []:
            sel = bpy.ops.object.select_all(action='SELECT')
            for ob in sel:
                #OBJ = bpy.data.objects[ob.name].parent#bpy.data.objects["Cube"].children len(bpy.data.objects["Cube"].modifiers) >=100
                if len(ob.modifiers) >= 50:#'MESH' in ob.parent.type:#如果没有父级那就直接执行
                    for ChildObj in ob.children:
                        ChildObj.hide_viewport = True#隐藏
                else:#如果有且是网格物体则执行
                    if not( 'CAMERA'  in ob.type or 'LIGHT' in ob.type):#if 'CAMERA' not in ob.type or 'LIGHT' not in ob.type:
                        for ParentChildObj in ob.parent.children:
                            ParentChildObj.hide_viewport = True
        else:
            for ob in sel:
                
                if len(ob.modifiers) >= 50:#'MESH' in ob.parent.type:#如果没有父级那就直接执行
                    for ChildObj in ob.children:
                        ChildObj.hide_viewport = True#隐藏
                else:#如果有且是网格物体则执行
                    if not( 'CAMERA'  in ob.type or 'LIGHT' in ob.type):#if 'CAMERA' not in ob.type or 'LIGHT' not in ob.type:
                        for ParentChildObj in ob.parent.children:
                            ParentChildObj.hide_viewport = True

    else:
        if sel == []:
            sel = bpy.ops.object.select_all(action='SELECT')
            for ob in sel:
                if len(ob.modifiers) >= 50:#if ob.parent== []:
                    for ChildObj in ob.children:
                        ChildObj.hide_viewport = False
                else:
                    if not( 'CAMERA'  in ob.type or 'LIGHT' in ob.type):
                        for ParentChildObj in ob.parent.children:
                            ParentChildObj.hide_viewport = False#显示
        else:
            for ob in sel:
                if len(ob.modifiers) >= 50:#if ob.parent== []:
                    for ChildObj in ob.children:
                        ChildObj.hide_viewport = False
                else:
                    if not( 'CAMERA'  in ob.type or 'LIGHT' in ob.type):
                        for ParentChildObj in ob.parent.children:
                            ParentChildObj.hide_viewport = False#显示



def UnrealSize_update(self, context):
    amProperty = context.scene.amProperties
    if amProperty.UnrealSize_Bool ==True:
        bpy.context.scene.unit_settings.system = 'METRIC'
        bpy.context.scene.unit_settings.scale_length = 0.01
        bpy.context.space_data.clip_end = 1000000

    else:
        bpy.context.scene.unit_settings.system = 'METRIC'
        bpy.context.scene.unit_settings.scale_length = 1

def FaceOrient_update(self, context):
    amProperty = context.scene.amProperties
    if amProperty.FaceOrient_Bool ==True:
        areas = [area for screen in context.workspace.screens for area in screen.areas if area.type == "VIEW_3D"]
        for area in areas:
            space = area.spaces[0]
            space.overlay.show_overlays = True
            space.overlay.show_face_orientation = True
    else:
        areas = [area for screen in context.workspace.screens for area in screen.areas if area.type == "VIEW_3D"]
        for area in areas:
            space = area.spaces[0]
            space.overlay.show_overlays = True
            space.overlay.show_face_orientation = False

def FreezeTime_update(self, context):
    amProperty = context.scene.amProperties##.keyframe_delete(
    sel = bpy.context.selected_objects
    RightNowTime=bpy.context.scene.frame_current
    if amProperty.FreezeTime_Bool ==True:
        for ob in sel:
            Wave040 = ob.modifiers['040_Wave']
            Laplaciansmooth041 = ob.modifiers['041_Laplaciansmooth']

            bpy.context.scene.frame_current = 1
            Wave040.keyframe_delete('height')
            Laplaciansmooth041.keyframe_delete('lambda_border')#.keyframe_delete(
            Laplaciansmooth041.keyframe_delete('lambda_factor')

            bpy.context.scene.frame_current = 250
            Wave040.keyframe_delete('height')
            Laplaciansmooth041.keyframe_delete('lambda_border')
            Laplaciansmooth041.keyframe_delete('lambda_factor')
            
            bpy.context.scene.frame_current = RightNowTime
    else:
        for ob in sel:
            Wave040 = ob.modifiers['040_Wave']
            Laplaciansmooth041 = ob.modifiers['041_Laplaciansmooth']

            Wave040.height = 1
            Laplaciansmooth041.iterations = 3
            Laplaciansmooth041.lambda_factor = 0.1
            Laplaciansmooth041.lambda_border = 0.1
            bpy.context.scene.frame_current = 1
            Wave040.keyframe_insert('height')
            Laplaciansmooth041.keyframe_insert('lambda_border')#.keyframe_delete(
            Laplaciansmooth041.keyframe_insert('lambda_factor')

            Wave040.height = 25
            Laplaciansmooth041.lambda_factor = 1
            Laplaciansmooth041.lambda_border = 5
            bpy.context.scene.frame_current = 250
            Wave040.keyframe_insert('height')
            Laplaciansmooth041.keyframe_insert('lambda_border')
            Laplaciansmooth041.keyframe_insert('lambda_factor')
            
            bpy.context.scene.frame_current = RightNowTime


class FaceOrient(bpy.types.Operator):
    bl_idname = "am.faceorient"
    bl_label = "FaceOrient"
    bl_description = "简易设置显示模式" 
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        amProperty = context.scene.amProperties
        areas = [area for screen in context.workspace.screens for area in screen.areas if area.type == "VIEW_3D"]
        if amProperty.FaceOrient_Int ==0:
            for area in areas:
                space = area.spaces[0]
                space.overlay.show_overlays = True
                space.overlay.show_face_orientation = False
                space.shading.type = 'SOLID'
                space.shading.color_type = 'MATERIAL'
                amProperty.FaceOrient_Int =1
        elif amProperty.FaceOrient_Int ==1:
            for area in areas:
                space = area.spaces[0]
                space.overlay.show_overlays = True
                space.overlay.show_face_orientation = True
                amProperty.FaceOrient_Int =2
        elif amProperty.FaceOrient_Int ==2:
            for area in areas:
                space = area.spaces[0]
                space.overlay.show_overlays = True
                space.overlay.show_face_orientation = False
                space.shading.type = 'SOLID'
                space.shading.color_type = 'RANDOM'
                amProperty.FaceOrient_Int =0
        self.report({'INFO'}, "切换模式")

        return {'FINISHED'}

class AddBoolModifier(bpy.types.Operator):
    bl_idname = "am.addboolmodifier"
    bl_label = "AddBoolModifier"
    bl_description = "选择物体，然后添加布尔到活动物体设定的修改器位置" 
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        amProperty = context.scene.amProperties
        #bpy.ops.object.modifier_copy(modifier="050_Bool_sub++++++++++")#50 85 90 95 107布尔key
        #for 
        #bpy.data.objects[ob.name].modifiers['050_Bool_sub++++++++++'].name#for一下bpy.data.objects['Cube'].modifiers.items()#for key,value in bpy.data.objects['Cube'].modifiers.items():
        sel=bpy.context.selected_objects
        act=bpy.context.active_object
        if amProperty.LinkMaterialBool == True:
            bpy.ops.object.make_links_data(type='MATERIAL')
        for ob in sel:
            if ob !=  act:
                ob.display_type = 'WIRE'
                ob.hide_render = True
                ob.show_bounds = True

                find_object(ob.name,'AutoBool')
                if amProperty.BoolParentBool==True:
                    if ob.parent != act:
                        #move_object(ob.name,act.name)
                        bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
                '''
                i=0
                for key,value in act.modifiers.items():#bpy.data.objects['Cube']VVV
                    i=i+1
                    if amProperty.AddBoolModifier[4:] in key:
                        bpy.ops.object.modifier_copy(modifier=key)
                        act.modifiers[i].show_viewport = False
                        act.modifiers[i].show_render = False

                        #bpy.data.objects['Cube'].modifiers[i].name = key.replace(bpy.data.objects['Cube'].modifiers[i-1].name[:-3], str(len(bpy.data.objects['Cube'].modifiers))+"_Bool_"+bpy.data.objects['Cube'].modifiers[i].operation)#len(bpy.data.objects['Cube'].modifiers) time.strftime("Bool %Y-%m-%d %H:%M:%S", time.localtime())  
                        #bpy.data.objects['Cube'].modifiers[i].name = key.replace("085", str(len(bpy.data.objects['Cube'].modifiers)))#获取选择到的物体除活跃的
                        act.modifiers[i].name = key.replace(act.modifiers[i-1].name[:-3], str(len(act.modifiers))+'_Bool_'+ob.name+'_'+amProperty.BoolModifierType)
                        act.modifiers[i].operation=amProperty.BoolModifierType
                        #bpy.data.objects['Cube'].hide_render = True
                        #ob.display_type = 'WIRE'
                        act.modifiers[i].object = bpy.data.objects[ob.name]
                        act.modifiers[i].show_viewport = True
                        act.modifiers[i].show_render = True

                        print(key)
                '''
                #移动布尔至修改器index /编号位置
                
                boolName=str(len(bpy.context.object.modifiers))+'_Bool_'+ob.name+'_'+amProperty.BoolModifierType
                act.modifiers.new(boolName, "BOOLEAN")
                act.modifiers[boolName].operation=amProperty.BoolModifierType
                act.modifiers[boolName].object = bpy.data.objects[ob.name]
                act.modifiers[boolName].show_viewport = True
                act.modifiers[boolName].show_render = True
                if amProperty.BoolNum >0:
                    BoolIndex=amProperty.BoolNum-1
                    bpy.ops.object.modifier_move_to_index(modifier=boolName, index=BoolIndex)





        self.report({'INFO'}, "添加布尔")

        return {'FINISHED'}


def ModifierApplyTo_update(sel):#self, context
    amProperty = bpy.context.scene.amProperties
    
    if amProperty.ModifiersApplyTo_Int <= 9:
        ApplyTo ='00' + str(amProperty.ModifiersApplyTo_Int)
    elif amProperty.ModifiersApplyTo_Int <= 99 and amProperty.ModifiersApplyTo_Int >= 10:
        ApplyTo ='0' + str(amProperty.ModifiersApplyTo_Int)
    elif amProperty.ModifiersApplyTo_Int <= 999 and amProperty.ModifiersApplyTo_Int >= 100:
        ApplyTo = str(amProperty.ModifiersApplyTo_Int)
    
    for ob in sel:
        if ('_WIP'  in ob.name or '_ObjBool'  in ob.name or '_ObjCurve' in ob.name or '_ObjLattice' in ob.name or '_SourceARROW' in ob.name or '_TargetARROW' in ob.name  or 'CAMERA'  in ob.type or 'LIGHT' in ob.type):
            ob.select_set(False)
    #sel = bpy.context.selected_objects
    for ob in sel:
        #ob = bpy.context.active_object
        
        i=0
        '''
        if len(ob.modifiers) < 114:
            #a = int(ob.modifiers[i].name[:3])#i=00 a=im=51 amProperty.ModifiersApplyTo_Int=51开始
            #b = ob.modifiers[i].name.split('_')
            applyInt=amProperty.ModifiersApplyTo_Int
            name = ob.modifiers[applyInt].name.split('_')

            a = int(name[0])
            
        else:
            a = i+1
        '''
        #a = i+1
        #ApplyInt=amProperty.ModifiersApplyTo_Int
        #ApplyModname = ob.modifiers[ApplyInt].name.split('_')
        #ModItem=ob.modifiers.items()
        #ModList=[]
        #for key,value in ModItem:#bpy.data.objects['Cube']VVV
            #Modname = ob.modifiers[i].name.split('_')
            #if i < amProperty.ModifiersApplyTo_Int:#if int(Modname[0]) <= amProperty.ModifiersApplyTo_Int: #int(ApplyTo): and int(ob.modifiers[i].name[:3]) <= amProperty.ModifiersApplyTo_Int:

            #001 = 001
                #ModList.append(i)
            #i=i+1
            
        if len(ob.modifiers) < amProperty.ModifiersApplyTo_Int:
            ModNum=len(ob.modifiers)
        else:
            ModNum=amProperty.ModifiersApplyTo_Int
        for Mod in range(ModNum):
            if ob.modifiers[0].show_viewport == True :
                bpy.ops.object.modifier_apply(modifier=ob.modifiers[0].name)#应用 这里只是一个物体的
            else:
                bpy.ops.object.modifier_remove(modifier=ob.modifiers[0].name)#移除
        
        


class ApplyModify(bpy.types.Operator):
    bl_idname = "am.applymodify"
    bl_label = "应用修改器"
    bl_description = "应用修改器至当前排序位置" 
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        amProperty = context.scene.amProperties
        C = bpy.context
        #bpy.ops.object.mode_set(mode='OBJECT')
        sel = bpy.context.selected_objects
        
        for ob in sel:
            if ('_ObjBool'  in ob.name or '_ObjCurve' in ob.name or '_ObjLattice' in ob.name or '_SourceARROW' in ob.name or '_TargetARROW' in ob.name  or 'CAMERA'  in ob.type or 'LIGHT' in ob.type):
                ob.select_set(False)

        sel = bpy.context.selected_objects
        if amProperty.ModifiersApplyTo_Int >= 1:
            sel = [bpy.context.active_object]#如果应用值是1以上就选一个物体 只能先这样

        if len(ob.modifiers) < amProperty.ModifiersApplyTo_Int:
            ModNum=len(ob.modifiers)-1
        else:
            ModNum=amProperty.ModifiersApplyTo_Int

        if amProperty.AutoSave_Bool ==True:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            for ob in sel:
                
                new_obj = ob.copy()
                new_obj.data = ob.data.copy()
                #new_obj.animation_data_clear()时间轴不删
                new_collection = make_collection('3ApplyMech', C.collection)#v'AutoSave' 大挪移
                new_collection.objects.link(new_obj)#new to 3ApplyMech，old+child to AutoSave
                if '_WIP' not in ob.name:
                    ob.name=new_obj.name[:-4]+'_WIP'
                new_obj.name=ob.name[:4]
                bpy.context.view_layer.objects.active = new_obj
                ob.select_set(False)
                new_obj.select_set(True)
                
                for ChildObj in ob.children:
                    find_object(ChildObj.name,'AutoSave')
                    ChildObj.hide_viewport = True
                
                find_object(ob.name,'AutoSave')
                
            for ob in sel:
                if '_WIP' in ob.name and len(ob.modifiers) >= 1:
                    ob.select_set(False)
                    ob.hide_viewport = True
                    ob.hide_render = True
                    
            if amProperty.ModifiersApplyTo_Int >= 1:
                ModName=bpy.context.object.modifiers[ModNum].name
                ModifierApplyTo_update(sel)
                
            else:
                ModName='All'
                bpy.ops.object.convert(target='MESH')
        #
        else:
            if amProperty.ModifiersApplyTo_Int >= 1:
                ModName=bpy.context.object.modifiers[ModNum].name
                ModifierApplyTo_update(sel)
            else:
                ModName='All'
                bpy.ops.object.mode_set(mode='OBJECT')
                for ob in sel:
                    bpy.ops.object.convert(target='MESH')#ob.convert(target='MESH') bpy.ops.object.convert(target='MESH')
                    for ChildObj in ob.children:
                        bpy.data.objects.remove(ChildObj)
                    find_object(ob.name,"3ApplyMech")
        #bpy.ops.object.mode_set(mode='EDIT')#todo ！出错是因为没有返回值
        #bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE', action='TOGGLE')#
        self.report({'INFO'}, "Apply Modifiers "+ModName)
        return {'FINISHED'}


class ApplyClean(bpy.types.Operator):#bpy.ops.mesh.fill_holes() 使用网格下的清理填充洞面
    bl_idname = "object.applyclean"
    bl_label = "Apply Clean"
    bl_description = "Only One direction now,apply Clean Operator UV，mirror" 
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        #find_object('4MechClean', '4MechClean',"5ApplyClean")
        #rename_object('GenMech')
        #sel = bpy.context.selected_objects
        #amProperty = context.scene.amProperties
        
        #for ob in sel:
            #ob.select_set(True)
            #bpy.context.view_layer.objects.active = ob
            #ob.convert(target='MESH')


        bpy.ops.mesh.hide(unselected=False)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.delete(type='ONLY_FACE')
        bpy.ops.mesh.reveal()
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT', action='TOGGLE')
        bpy.ops.mesh.select_all(action='INVERT')
        bpy.ops.mesh.delete(type='EDGE_FACE')
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE', action='TOGGLE')
        amProperty = context.scene.amProperties



        bpy.ops.object.mode_set(mode='OBJECT')

        sel = bpy.context.selected_objects
        for ob in sel:
            bpy.context.view_layer.objects.active = ob

            add_weld(ob,'WELD')#bpy.ops.object.modifier_add(type='WELD')  add_weld(bpy.context.object,'WELD')
            ob.modifiers["WELD"].merge_threshold = 0.0035   
            ob.modifiers["WELD"].max_interactions = 4
            bpy.ops.object.modifier_apply(modifier="WELD")#bpy.ops.object.modifier_apply(modifier="WELD")


        '''绝对路径问题
        if amProperty.GenMechBemeshClean ==True:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.context.scene.scene_check_set.preset_list = '2 - Blender Default'
            #bpy.context.scene.scene_check_set.in_out_menu = 'OUT'
            __init__.bmesh_clean()
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.context.scene.scene_check_set.preset_list = '1 - Import clean'
            #bpy.context.scene.scene_check_set.in_out_menu = 'OUT'
            __init__.bmesh_clean()
            bpy.ops.object.mode_set(mode='OBJECT')
            #bpy.ops.object.mode_set(mode='EDIT')
        '''

        bpy.ops.object.mode_set(mode='EDIT')
        
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.delete_loose()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.remove_doubles(threshold=0.0005)

        bpy.ops.object.mode_set(mode='EDIT')


        bpy.ops.mesh.select_all(action='SELECT')

        if amProperty.MOD_MIRROR_Bool ==True:
            if "_l" in bpy.context.object.data.name or "_r" in bpy.context.object.data.name :
                if "clavicle" in bpy.context.object.data.name:
                    bpy.ops.mesh.bisect(plane_co=(-1, 0.2, -10), plane_no=(0, 1, 0), use_fill=False, clear_inner=False, clear_outer=True, xstart=204, xend=713, ystart=198, yend=196)
                elif "upperarm" in bpy.context.object.data.name:
                    bpy.ops.mesh.bisect(plane_co=(-1, 0.15, -10), plane_no=(0, 1, 0), use_fill=False, clear_inner=False, clear_outer=True, xstart=204, xend=713, ystart=198, yend=196)
                elif "lowerarm" in bpy.context.object.data.name:
                    bpy.ops.mesh.bisect(plane_co=(-1, 0.2, -10), plane_no=(0, 1, 0), use_fill=False, clear_inner=False, clear_outer=True, xstart=204, xend=713, ystart=198, yend=196)
                elif "hand" in bpy.context.object.data.name:
                    bpy.ops.mesh.bisect(plane_co=(-1, 0.2, -10), plane_no=(0, 1, 0), use_fill=False, clear_inner=False, clear_outer=True, xstart=204, xend=713, ystart=198, yend=196)
                else:
                    bpy.ops.mesh.bisect(plane_co=(0.5, 0, 50), plane_no=(1, 0, 0), use_fill=False, clear_inner=True, clear_outer=False, xstart=243, xend=243, ystart=349, yend=20)
            else:
                bpy.ops.mesh.bisect(plane_co=(0, 0, 50), plane_no=(1, 0, 0), use_fill=False, clear_inner=True, clear_outer=False, xstart=243, xend=243, ystart=349, yend=20)



        bpy.ops.mesh.select_all(action='SELECT')

        bpy.ops.uv.smart_project()
        
        if amProperty.GenMechUVPackmaster ==True:
            try:
                bpy.context.scene.tool_settings.use_uv_select_sync = True
                bpy.context.space_data.uv_editor.show_stretch = True
                bpy.ops.uv.pack_islands(margin=0)
                
                bpy.ops.uvpackmaster2.uv_overlap_check() 
                bpy.ops.uvpackmaster2.uv_measure_area()
                bpy.ops.uvpackmaster2.uv_validate()
                
                bpy.context.scene.uvp2_props.margin = 0.002
                bpy.context.scene.uvp2_props.precision = 1000
                bpy.context.scene.uvp2_props.prerot_disable = False
                bpy.context.scene.uvp2_props.rot_step = 90
                bpy.context.scene.uvp2_props.island_rot_step_enable = True
                
                bpy.context.scene.uvp2_props.pre_validate = False
                bpy.context.scene.uvp2_props.pack_to_others = False
                bpy.context.scene.uvp2_props.lock_overlapping = True#重叠

            except:
                print("problem")
            finally:
                #bpy.ops.mesh.mark_seam(clear=False) #
                bpy.ops.uvpackmaster2.uv_pack()
                
                #bpy.app.timers.register(UVpack)
                
                #bpy.ops.object.mode_set(mode='OBJECT')
        #bpy.ops.object.mode_set(mode='OBJECT')

        if amProperty.MOD_MIRROR_Bool ==True:
            #bpy.ops.mesh.bisect(plane_co=(0, 0, 50), plane_no=(1, 0, 0), use_fill=False, clear_inner=True, clear_outer=False, xstart=243, xend=243, ystart=349, yend=20)
            #bpy.ops.mesh.select_all(action='SELECT')
            #bpy.ops.uv.smart_project()
            #bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.modifier_add(type='MIRROR')
            if "clavicle" in bpy.context.object.data.name:
                bpy.context.object.modifiers["Mirror"].use_axis[0] = False
                bpy.context.object.modifiers["Mirror"].use_axis[1] = True
            elif "upperarm" in bpy.context.object.data.name:
                bpy.context.object.modifiers["Mirror"].use_axis[0] = False
                bpy.context.object.modifiers["Mirror"].use_axis[1] = True
            elif "lowerarm" in bpy.context.object.data.name:
                bpy.context.object.modifiers["Mirror"].use_axis[0] = False
                bpy.context.object.modifiers["Mirror"].use_axis[1] = True
            elif "hand" in bpy.context.object.data.name:
                bpy.context.object.modifiers["Mirror"].use_axis[0] = False
                bpy.context.object.modifiers["Mirror"].use_axis[1] = True       
            #bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Mirror")
        #else:
            #bpy.ops.mesh.select_all(action='SELECT')
            #bpy.ops.uv.smart_project()
            #bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.space_data.overlay.show_face_orientation = False# 法线
        #bpy.ops.object.make_links_data(type='MODIFIERS')




        
        #edit
        self.report({'INFO'}, "5.Apply Clean")
        return {'FINISHED'}

class ReName(bpy.types.Operator):
    bl_idname = "am.rename"
    bl_label = "ReName"
    bl_description = "如果名称中含有“.”则重命名" 
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for reobj in bpy.context.selected_objects:
            if '.' in reobj.name:#
                reobj.name = reobj.name[:-4]
                reobj.data.name = reobj.name

        self.report({'INFO'}, "重命名成功")
        return {'FINISHED'}



class MirrorSelect(bpy.types.Operator):
    bl_idname = "am.mirrorselect"
    bl_label = "Mirror Select"
    bl_description = "MirrorX Select,rename '_l  _r  ' OBJ" #_L _R .l .L .r .R r_ R_ l_ L_
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        #if bpy.context.mode !='OBJECT':
        #bpy.ops.object.mode_set(mode='OBJECT')
        
        #bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
        #amProperty = context.scene.amProperties
        #bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        #bpy.ops.object.mode_set(mode='OBJECT')
        #bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
        bpy.ops.object.duplicate_move()
        sel = bpy.context.selected_objects
        for ob in sel:
                
                #bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'
                #bpy.ops.transform.mirror(orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
            ob.scale[0]=0-ob.scale[0]
            ob.rotation_euler[1] = 0-ob.rotation_euler[1]
            ob.rotation_euler[2] = 0-ob.rotation_euler[2]
            ob.location[0] = 0-ob.location[0]
            name=ob.name.split('.')
            if '_l' in ob.name:
                ob.name=name[0].replace('_l','_r')
            elif '_r' in ob.name:
                ob.name=name[0].replace('_r','_l')
            '''
            if ('_l' in ob.name) or ('_L' in ob.name):
                ob.name=name[0].replace('_l','_r')
                ob.name=name[0].replace('_L','_R')
            elif ('_r' in ob.name) or ('_R' in ob.name):
                ob.name=name[0].replace('_r','_l')
                ob.name=name[0].replace('_R','_L')

            if ('.l' in ob.name) or ('.L' in ob.name):
                ob.name=name[0].replace('.l','.r')
                ob.name=name[0].replace('.L','.R')
            if ('.r' in ob.name) or ('.R' in ob.name):
                ob.name=name[0].replace('.r','.l')
                ob.name=name[0].replace('.R','.L')
            
            elif ('l_' in ob.name) or ('L_' in ob.name):
                ob.name=name[0].replace('l_','r_')
                ob.name=name[0].replace('L_','R_')
            elif ('r_' in ob.name) or ('R_' in ob.name):
                ob.name=name[0].replace('r_','l_')
                ob.name=name[0].replace('R_','L_')
            '''

        #for rob in bpy.data.objects:
            #if '_l' in rob.name:
                #if '.' in rob.name:#
                    #rob.name = rob.name[:-6] + "_r"
                    #rob.data.name = rob.name
            #if rob.name.endswith("_l"):
                #rob.name = rob.name[:-2] + "_r"
                #rob.data.name = rob.name

                #bpy.context.object.data.name = "upperarm_r"
        '''
        for ob in sel:
            if '_l' in ob.name:
                ob.select_set(True)
                #bpy.context.view_layer.objects.active = ob
                bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

                #bpy.context.view_layer.objects.active = ob
                if '.' in bpy.context.object.name:
                    bpy.context.object.name = bpy.context.object.name[:-4]
                if bpy.context.object.name.endswith("_l"):
                    bpy.context.object.name = bpy.context.object.name[:-2] + "_r"
                    bpy.context.object.data.name = bpy.context.object.name
                #bpy.context.object.data.name = "upperarm_r"

                #bpy.context.object.select_set(False)


        for rob in bpy.data.objects:
            if '_r' in rob.name:
                ob.select_set(True)
                bpy.context.view_layer.objects.active = rob
                bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'
                bpy.ops.transform.mirror(orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
            '''


                #bpy.context.object.location[0] = 0 - bpy.context.object.location[0]
                #bpy.ops.transform.mirror(orient_type='GLOBAL', constraint_axis=(True, False, False), use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

        
        self.report({'INFO'}, "6.Mirror Select form _l to _r")
        return {'FINISHED'}



def edgeLoc_update(self, context):
    ob = context.object
    sampleProperty = context.scene.AMOldPropertyGroup
    edgeLoc = sampleProperty.edgeLoc
    if sampleProperty.LocEdgeBool == True:
        ob.location = edgeLoc
    else:
        edgeLoc= (0, 0, 0)#sampleProperty.LocEdgeBool = (0, 0, 0)
        #ob.location = edgeLoc

def LocEdit_update(self, context):
    ob = context.object
    sampleProperty = context.scene.AMOldPropertyGroup
    LocEdit = sampleProperty.LocEdit
    if sampleProperty.LocEditBool == True:
        bpy.ops.object.mode_set(mode='OBJECT')
        #bpy.ops.object.select_all(action='DESELECT')
        bpy.context.active_object
        #bpy.ops.object.mode_set(mode='EDIT')
        #bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT', action='TOGGLE')
        
        #bpy.ops.mesh.select_all(action='SELECT')
        bpy.context.scene.cursor.location = sampleProperty.LocEdit
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        #bpy.ops.transform.translate(value=sampleProperty.LocEdit)
        #bpy.ops.object.mode_set(mode='OBJECT')

        #
        #
    else:
        edgeLoc= (0, 0, 0)
    '''
    if sampleProperty.LocEditBool == True:
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.active_object
        bpy.ops.object.mode_set(mode='EDIT')
        #bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT', action='TOGGLE')
        #bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.transform.translate(value=sampleProperty.LocEdit)
        bpy.ops.object.mode_set(mode='OBJECT')

        #bpy.context.scene.cursor.location = (0,0,0)
        #bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    else:
        edgeLoc= (0, 0, 0)
    '''
def RemeshEnum_update(self, context):#要设置回调函数才行callback
    '''
    items=[
        ('BLOCKS', 'BLOCKS', ""),
        ('SMOOTH', 'SMOOTH', ""),
        ('SHARP', 'SHARP', "")
    ]
    '''
    amProperty = context.scene.amProperties
    GenMechRemeshEnum=amProperty.GenMechRemeshEnum
    sel = bpy.context.selected_objects
    for ob in sel:
        bpy.context.view_layer.objects.active = ob
        #GenMechRemeshEnum = ob.modifiers["Remesh"].mode
    #if GenMechRemeshEnum == '':
        #ob.mode = 'SHARP'
        if ob.modifiers["Remesh"].mode != GenMechRemeshEnum:
            ob.modifiers["Remesh"].mode = GenMechRemeshEnum
    #return items
        #GenMechRemeshEnum = ob.modifiers["Remesh"].mode
    #return GenMechRemeshEnum.items
    #return ob.modifiers["Remesh"].mode
        #amProperty.GenMechRemeshEnum = ob.mode
    #GenMechRemeshEnum = ob.modifiers["Remesh"].mode
    #bpy.context.object.modifiers["Remesh"].mode = 'SHARP'

def GenMechBevel0Enum_callback(self, context):
    #amProperty = context.scene.amProperties
    items = [
            ('OFFSET', 'OFFSET', "", 0),
            ('WIDTH', 'WIDTH', "", 1),
            ('DEPTH', 'DEPTH', "", 2),
            ('PERCENT', 'PERCENT', "", 3)
            #('None', 'None', "", 5)
        ]
    #ob = context.object
    #if ob is not None:
        #items.valus = int(ob.modifiers["Bevel"].offset_type)
    return items

def GenMechBevel0Enum_update(self, context):
    amProperty = context.scene.amProperties
    sel = bpy.context.selected_objects
    if sel is not None:
        for ob in sel:
            if ob.modifiers.get("Bevel"):
                bpy.context.view_layer.objects.active = ob
                ob.modifiers["Bevel"].offset_type = amProperty.GenMechBevel0Enum
            #b = ob.modifiers["Bevel"].offset_type
            #amProperty.GenMechBevel0Enum = b
            #get_Bevel0Enum()
    '''
    for ob in sel:
        if ob.modifiers.get("Bevel"):
            bpy.context.view_layer.objects.active = ob
            ob.modifiers["Bevel"].offset_type = amProperty.GenMechBevel0Enum
    '''

def GenMechBevel0float_update(self, context):
    #amProperty = context.scene.amProperties
    sampleProperty = context.scene.AMOldPropertyGroup
    sel = bpy.context.selected_objects
    for ob in sel:
        if ob.modifiers.get("Bevel"):
            bpy.context.view_layer.objects.active = ob
            ob.modifiers["Bevel"].width_pct = sampleProperty.Bevel0float

def GenMechResize_update(self, context):
    amProperty = context.scene.amProperties
    sel = bpy.context.selected_objects
    if amProperty.GenMechResizeBool == True:
        bpy.ops.object.mode_set(mode='OBJECT')
            #   bpy.ops.object.select_all(action='DESELECT')
            #bpy.context.active_object
            #bpy.ops.mesh.select_all(action='TOGGLE')
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT', action='TOGGLE')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.transform.resize(value=(1,1,1))
        bpy.ops.transform.resize(value=amProperty.GenMechResize)
        #bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE', action='TOGGLE')
        bpy.ops.object.mode_set(mode='OBJECT')
    else:
        bpy.ops.transform.resize(value=(1,1,1))

def GenMechSkinResize_update(self, context):
    amProperty = context.scene.amProperties
    sel = bpy.context.selected_objects
    if sel is not None:
        if amProperty.GenMechSkinSizeBool == True:
            bpy.ops.object.mode_set(mode='OBJECT')
                #   bpy.ops.object.select_all(action='DESELECT')
                #bpy.context.active_object
                #bpy.ops.mesh.select_all(action='TOGGLE')
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')    
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT', action='TOGGLE')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.transform.skin_resize(value=(amProperty.GenMechSkinResize), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
            #bpy.ops.transform.skin_resize(value=amProperty.GenMechSkinResize)
            #bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE', action='TOGGLE')
            bpy.ops.object.mode_set(mode='OBJECT')
    else:
            #amProperty.GenMechSkinResize = (1,1,1)
            #bpy.ops.transform.skin_resize(value=amProperty.GenMechSkinResize)
        bpy.ops.transform.skin_resize(value=(1,1,1))


def GenMechRemeshScale_update(self, context):
    amProperty = context.scene.amProperties
    #sampleProperty = context.scene.AMOldPropertyGroup
    sel = bpy.context.selected_objects
    for ob in sel:
        if ob.modifiers.get("115_Remesh"):
            bpy.context.view_layer.objects.active = ob
            ob.modifiers["115_Remesh"].mode = 'VOXEL'
            ob.modifiers["115_Remesh"].voxel_size = amProperty.GenMechRemeshScale


def set_GenMechResize(self, value):
    #x=0.1
    self["Bevel0Enum"] = (1,1,1)

def get_Bevel0Enum(self):
    ob = bpy.context.selected_objects
    #bpy.context.view_layer.objects.active = ob
    amProperty = bpy.context.scene.amProperties
    
    if bpy.context.object.modifiers.get("Bevel"):
        if ob is not None:
            amProperty.GenMechBevel0Enum = bpy.context.object.modifiers["Bevel"].offset_type
        #self["Bevel0Enum"] = amProperty.GenMechBevel0Enum
    #bpy.context.object.modifiers["Bevel"].offset_type =
            return self.get("Bevel0Enum")
    else:
        self["Bevel0Enum"] = 5
    
    return self["Bevel0Enum"]
    

    
    '''
    if bpy.context.object.modifiers["Bevel"].offset_type == 'OFFSET':
        return 1
    elif bpy.context.object.modifiers["Bevel"].offset_type == 'WIDTH':
        return 2
    elif bpy.context.object.modifiers["Bevel"].offset_type == 'DEPTH':
        return 3
    elif bpy.context.object.modifiers["Bevel"].offset_type == 'PERCENT':
        return 4
    #return ob.modifiers["Bevel"].offset_type
    '''

def set_Bevel0Enum(self, value):
    #print("setting value", value)
    amProperty = bpy.context.scene.amProperties
    #bpy.context.object.modifiers["Bevel"].offset_type = amProperty.GenMechBevel0Enum
    #value = amProperty.GenMechBevel0Enum
    #amProperty.GenMechBevel0Enum = bpy.context.object.modifiers["Bevel"].offset_type
    '''
    amProperty = bpy.context.scene.amProperties
    sel = bpy.context.selected_objects
    for ob in sel:
        bpy.context.view_layer.objects.active = ob
        ob.modifiers["Bevel"].offset_type = amProperty.GenMechBevel0Enum
        value = amProperty.GenMechBevel0Enum
        #return amProperty.GenMechBevel0Enum
    '''
    '''
    ob = bpy.context.selected_objects
    value = amProperty.GenMechBevel0Enum
    if ob is not None:
        if self["Bevel0Enum"] == 1:
            bpy.context.object.modifiers["Bevel"].offset_type = 'OFFSET'
        elif self["Bevel0Enum"] == 2:
            bpy.context.object.modifiers["Bevel"].offset_type = 'WIDTH'
        elif self["Bevel0Enum"] == 3:
            bpy.context.object.modifiers["Bevel"].offset_type = 'DEPTH'
        elif self["Bevel0Enum"] == 4:
            bpy.context.object.modifiers["Bevel"].offset_type = 'PERCENT'
        else:
            self["Bevel0Enum"] = value
        '''
    self["Bevel0Enum"] = value

def RemoveAllModifier():
    ob = bpy.context.object
    bpy.context.object.modifiers.clear()


class RenderScene(bpy.types.Operator):
    bl_idname = "am.renderscene"
    bl_label = "添加渲染预设场景"
    bl_description = "添加一个渲染环境预设,之前设置的某些参数会覆盖，使用前保存。" 
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        world = bpy.context.scene.world
        world_node_tree = world.node_tree
        world_nodes = world_node_tree.nodes


        bpy.context.scene.world.use_nodes = True
        RenderScenefilepath = os.path.join(os.path.dirname(__file__),"photo_studio_01_2k.hdr")#hdrihaven.com/hdri/?c=studio&h=photo_studio_01
        bpy.ops.image.open(filepath=RenderScenefilepath, directory=os.path.dirname(__file__), files=[{"name":"photo_studio_01_2k.hdr", "name":"photo_studio_01_2k.hdr"}], relative_path=True, show_multiview=False)
        bpy.data.images["photo_studio_01_2k.hdr"].name = "photo_studio_01_2k.hdr"
        #World_Output = bpy.context.scene.world.node_tree.nodes.get('World Output')
        World_Output = world_nodes.get('World Output')
        Background = world_nodes.get('Background')
        #bpy.ops.node.add_node(type="ShaderNodeTexEnvironment", use_transform=True)

        HDR = world_nodes.new('ShaderNodeTexEnvironment')
        #HDR.name = "photo_studio_01_2k.hdr"
        HDR.image=bpy.data.images["photo_studio_01_2k.hdr"]
        HDR.location = (-475,350)

        world_node_tree.links.new(HDR.outputs[0], Background.inputs[0])
        world_node_tree.links.new(Background.outputs[0], World_Output.inputs[0])

        #影子平面
        bpy.ops.mesh.primitive_plane_add(size=40, enter_editmode=False, align='WORLD', location=(0, 0, -1), scale=(1, 1, 1))
        bpy.context.object.name = "ShadowPlane"
        bpy.context.object.cycles.is_shadow_catcher = True
        bpy.context.object.display_type = 'WIRE'
        bpy.context.object.hide_select = True
        #bpy.context.object.select_set(False)


        #渲染参数
        bpy.context.scene.render.engine = 'CYCLES'#设置一下保证以下的代码能用
        bpy.context.scene.cycles.feature_set = 'EXPERIMENTAL'#打开试验特性

        bpy.context.scene.view_settings.look = 'Very High Contrast'#色彩管理

        bpy.context.scene.cycles.use_denoising = True#降噪 以下7项SID插件自定义
        OpenScripts = bpy.context.preferences.addons.keys()
        if 'SuperImageDenoiser' in OpenScripts:#uvpackmaster2
            bpy.context.scene.cycles.use_preview_denoising = True
            bpy.context.scene.cycles.preview_denoiser = 'OPENIMAGEDENOISE'
            bpy.context.scene.cycles.denoiser = 'OPENIMAGEDENOISE'
            bpy.context.scene.sid_settings.use_environment = True
            bpy.context.scene.sid_settings.use_volumetric = True
            bpy.context.scene.sid_settings.compositor_reset = True
            bpy.ops.object.superimagedenoise()

        bpy.context.scene.cycles.sample_clamp_direct = 4#光程
        bpy.context.scene.cycles.sample_clamp_indirect = 3
        bpy.context.scene.cycles.blur_glossy = 0

        bpy.context.scene.render.film_transparent = True#透明

        bpy.context.scene.render.tile_y = 32#性能
        bpy.context.scene.render.tile_x = 32
        bpy.context.scene.render.use_persistent_data = True


        #输出参数
        bpy.context.scene.render.resolution_percentage = 200
        bpy.context.scene.render.use_stamp_memory = True
        bpy.context.scene.render.use_stamp_lens = True

        bpy.context.scene.render.use_overwrite = False#不覆盖

        bpy.context.scene.render.dither_intensity = 0#后期处理


        #视图层
        bpy.context.scene.view_layers["View Layer"].use_pass_mist = True
        bpy.context.scene.view_layers["View Layer"].use_pass_normal = True
        bpy.context.scene.view_layers["View Layer"].use_pass_shadow = True
        bpy.context.scene.view_layers["View Layer"].use_pass_ambient_occlusion = True

        #无单位 bpy.context.scene.unit_settings.system = 'NONE'
        bpy.context.scene.world.cycles.sampling_method = 'MANUAL'#设置

        #bpy.ops.node.add_node(type="ShaderNodeBackground", use_transform=True)
        #bpy.ops.node.add_node(type="ShaderNodeOutputWorld", use_transform=True)

        self.report({'INFO'}, "添加渲染预设场景")
        return {'FINISHED'}


class HightoLowRemesh(bpy.types.Operator):
    bl_idname = "am.hightolowremesh"
    bl_label = "精简重构网格"
    bl_description = "重构该物体至低模并自动光滑,谨慎使用，会很卡。" 
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        amProperty=amProperty = bpy.context.scene.amProperties
        bpy.ops.am.applymodify()
        sel = bpy.context.selected_objects
        for ob in sel:
            bpy.context.view_layer.objects.active = ob
            Remesh115 = ob.modifiers.new("115_Remesh","REMESH")#建议布尔对象只使用单个重构修改器，否则两个非流形模型之间不好布尔 不要精简太过的
            Displace116 = ob.modifiers.new("116_Displace", "DISPLACE")
            Displace117 = ob.modifiers.new("117_Displace", "DISPLACE")
            Triangulate118 = ob.modifiers.new("118_Triangulate", "TRIANGULATE")
            Laplaciansmooth119 = ob.modifiers.new('119_Laplaciansmooth', 'LAPLACIANSMOOTH')
            Decimate120 = ob.modifiers.new("120_Decimate", "DECIMATE")
            Decimate128 = ob.modifiers.new("121_Decimate", "DECIMATE")
            Laplaciansmooth122 = ob.modifiers.new('122_Laplaciansmooth', 'LAPLACIANSMOOTH')
            Laplaciansmooth123 = ob.modifiers.new('123_Laplaciansmooth', 'LAPLACIANSMOOTH')
            Decimate131 = ob.modifiers.new("124_Decimate", "DECIMATE")
            Weld125 = ob.modifiers.new("125_Weld", "WELD")
            Weld126 = ob.modifiers.new("126_Weld", "WELD")
            Weld127 = ob.modifiers.new("127_Weld", "WELD")
            Decimate128 = ob.modifiers.new("128_Decimate", "DECIMATE")
            Decimate129 = ob.modifiers.new("129_Decimate", "DECIMATE")
            Decimate130 = ob.modifiers.new("130_Decimate", "DECIMATE")
            Decimate131 = ob.modifiers.new("131_Decimate", "DECIMATE")
            Decimate132 = ob.modifiers.new("132_Decimate", "DECIMATE")
            Decimate133 = ob.modifiers.new("133_Decimate", "DECIMATE")
            Decimate134 = ob.modifiers.new("134_Decimate", "DECIMATE")
            Mirror135 = ob.modifiers.new('135_Mirror', 'MIRROR')
            #Remesh115.show_viewport = False
            #Remesh115.show_render = False
            Remesh115.mode = 'VOXEL'
            Remesh115.voxel_size = amProperty.GenMechRemeshScale#0.012
            Remesh115.use_smooth_shade = True
            Displace116.show_viewport = False
            Displace116.show_render = False
            Displace117.show_viewport = False
            Displace117.show_render = False
            Laplaciansmooth119.iterations = 1
            Laplaciansmooth119.lambda_factor = 0.25
            Decimate120.decimate_type = 'DISSOLVE'
            Decimate120.angle_limit = 0.0174533
            Decimate120.use_dissolve_boundaries = True
            Decimate128.decimate_type = 'COLLAPSE'
            Decimate128.ratio = 0.3
            Laplaciansmooth122.iterations = 1
            Laplaciansmooth122.lambda_factor = 0.5
            Laplaciansmooth123.iterations = 3
            Laplaciansmooth123.lambda_factor = 1
            Decimate131.decimate_type = 'DISSOLVE'
            Decimate131.angle_limit = 0.0872665
            Decimate131.use_dissolve_boundaries = True
            Weld125.merge_threshold = 0.02
            Weld126.merge_threshold = 0.025
            Weld127.merge_threshold = 0.03
            Decimate128.decimate_type = 'DISSOLVE'
            Decimate128.angle_limit = 0.0349066
            Decimate128.delimit = {'NORMAL', 'MATERIAL', 'SEAM', 'SHARP', 'UV'}
            Decimate128.use_dissolve_boundaries = False
            Decimate129.decimate_type = 'DISSOLVE'
            Decimate129.angle_limit = 0.0872665
            Decimate129.delimit = {'NORMAL', 'MATERIAL', 'SEAM', 'SHARP', 'UV'}
            Decimate129.use_dissolve_boundaries = True
            Decimate130.decimate_type = 'DISSOLVE'
            Decimate130.angle_limit = 0.174533
            Decimate130.use_dissolve_boundaries = True
            Decimate131.decimate_type = 'DISSOLVE'
            Decimate131.angle_limit = 0.261799
            Decimate131.use_dissolve_boundaries = False
            Decimate132.decimate_type = 'DISSOLVE'
            Decimate132.angle_limit = 0.349066
            Decimate132.use_dissolve_boundaries = False
            Decimate133.decimate_type = 'DISSOLVE'
            Decimate133.angle_limit = 0.436332
            Decimate133.use_dissolve_boundaries = False
            Decimate134.decimate_type = 'DISSOLVE'
            Decimate134.angle_limit = 0.514872
            Decimate134.use_dissolve_boundaries = True
            Mirror135.use_axis[0] = True
            Mirror135.use_bisect_axis[0] = True

            for mod in ob.modifiers:
                mod.show_expanded = False
                mod.show_in_editmode = False

            ob.data.use_auto_smooth = True
            ob.data.auto_smooth_angle = 0.523599


        self.report({'INFO'}, "重构成功")
        return {'FINISHED'}


def UVPackmaster():#这里可以写点参数：margin==0.002
        OpenScripts = bpy.context.preferences.addons.keys()
        if 'uvpackmaster2' in OpenScripts:#rigify
            try:
                bpy.context.scene.tool_settings.use_uv_select_sync = True
                bpy.context.space_data.uv_editor.show_stretch = True
                bpy.ops.uv.pack_islands(margin=0)
                
                bpy.ops.uvpackmaster2.uv_overlap_check() 
                bpy.ops.uvpackmaster2.uv_measure_area()
                bpy.ops.uvpackmaster2.uv_validate()
                
                bpy.context.scene.uvp2_props.margin = 0.002
                bpy.context.scene.uvp2_props.precision = 1000
                bpy.context.scene.uvp2_props.prerot_disable = False
                bpy.context.scene.uvp2_props.rot_step = 90
                bpy.context.scene.uvp2_props.island_rot_step_enable = True
                
                bpy.context.scene.uvp2_props.pre_validate = False
                bpy.context.scene.uvp2_props.pack_to_others = False
                bpy.context.scene.uvp2_props.lock_overlapping = True#重叠
            except:
                print("problem")
            finally:
                bpy.ops.uvpackmaster2.uv_pack()

def HideObjs(Hide=True):# 物体模式下
        sel = bpy.context.selected_objects
        bpy.ops.object.select_all(action='INVERT')
        unsel = bpy.context.selected_objects
        bpy.ops.object.select_all(action='INVERT')
        for ob in unsel:
            ob.hide_set(Hide)


class DeleteUnusedModifier(bpy.types.Operator):#添加一个删除所选物体所有修改器
    bl_idname = "am.deleteunusedmodifier"
    bl_label = "Delete Unused Modifier"
    bl_description = "删除当前物体未在视图层、渲染层使用的修改器。" 
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        sel = bpy.context.selected_objects
        ModList=[]
        for ob in sel:
            for Mod in range(len(ob.modifiers)):
                if (ob.modifiers[Mod].show_viewport == False) and (ob.modifiers[Mod].show_render == False):
                    ModList.append(ob.modifiers[Mod].name)
                    #bpy.ops.object.modifier_apply(modifier=ob.modifiers[0].name)#应用 这里只是一个物体的
                    #bpy.ops.object.modifier_remove(modifier=ob.modifiers[Mod].name)#移除
            for ModName in range(len(ModList)):
                bpy.ops.object.modifier_remove(modifier=ModList[ModName])

        self.report({'INFO'}, "Delete Unused Modifier")
        return {'FINISHED'}


class RandomIndexModifier(bpy.types.Operator):
    bl_idname = "am.randomindexmodifier"
    bl_label = "随机排序至当前编号的修改器"
    bl_description = "随机排序选择物体的修改器,0为随机所有(使用前务必保存文件，预计无法回撤)" 
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        sel = bpy.context.selected_objects
        amProperty = bpy.context.scene.amProperties
        
        for ob in sel:
            bpy.context.view_layer.objects.active = ob
            if amProperty.ModifiersApplyTo_Int <=0:
                ModNum=len(ob.modifiers)-1
                ModRandom=random.uniform(0, ModNum)
            else:
                ModNum=amProperty.ModifiersApplyTo_Int-1
                ModRandom=random.uniform(0, ModNum)
            
            for Mod in range(ModNum):
                bpy.ops.object.modifier_move_to_index(modifier=ob.modifiers[Mod].name, index=ModRandom)
                #if (ob.modifiers[Mod].show_viewport == False) and (ob.modifiers[Mod].show_render == False):
                    #ModList.append(ob.modifiers[Mod].name)
                    #bpy.ops.object.modifier_apply(modifier=ob.modifiers[0].name)#应用 这里只是一个物体的
                    #bpy.ops.object.modifier_remove(modifier=ob.modifiers[Mod].name)#移除

        self.report({'INFO'}, "随机排序修改器成功")
        return {'FINISHED'}


class OpenPresetFolder(bpy.types.Operator):
    bl_idname = "am.openpresetfolder"
    bl_label = "打开预设文件夹"
    bl_description = "打开预设资源文件夹,编辑或删除预设。" 
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        amProperty = bpy.context.scene.amProperties
        if (amProperty.GenMechFolder=='Preset') or (amProperty.GenMechFolder==''):
            FolderPath=os.path.dirname(__file__)+'//Preset//'
        else:
            FolderPath=os.path.dirname(__file__)+'//Preset//'+amProperty.GenMechFolder+'//'

        #FolderPath=os.path.dirname(__file__)+'\Preset'#//
        path = os.path.realpath(FolderPath)
        os.startfile(path)
        self.report({'INFO'}, "打开预设文件夹")
        return {'FINISHED'}

'''
def PresetFile(self, context):
    FileList=['MechPro', 'Helmet', 'Mechfy']#, 'MechfyHigh'
    FolderPath=os.path.dirname(__file__)+'\Preset'
    path = os.path.realpath(FolderPath)
    for file in os.listdir(path):
        filename=file.split('.', 1)
        FileList.append(filename)
    return FileList

def FileName(self, context):
    amProperty = bpy.context.scene.amProperties
    dir_name = amProperty.GenMechEnum
    FileList=PresetFile(self, context)#

    if amProperty.GenMechName not in FileList :
        #amProperty.GenMechName = dir_name
        FinalFileName = amProperty.GenMechName#之后我们需要更新GenMechEnum不然文件会被覆盖
    else:
        if len(FileList) <= 9:
            count='00' + str(len(FileList))
        elif len(FileList) <= 99:
            count='0' + str(len(FileList))
        else:
            count = str(len(FileList))
        if '_' in dir_name:
            dir_name.split('_',1)
            FinalFileName = dir_name[0]+'_'+count
        else:
            FinalFileName = dir_name+'_'+count
    return FinalFileName
'''


def GenMechEnum_update(self, context):#保存的时候也要更新 items要扩展
    amProperty = context.scene.amProperties
    #sampleProperty = context.scene.AMOldPropertyGroup
    amProperty.GenMechName=amProperty.GenMechEnum



#text_create('mytxtfile', 'Hello world!')

class SavePreset(bpy.types.Operator):
    #保存预设 将文件存取到之后刷新Enum GenMechEnum_Item()。append
    bl_idname = "am.savepreset"
    bl_label = "保存预设"
    bl_description = "保存该物体修改器,文本内容不能含有中文，会乱码。" 
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        amProperty = context.scene.amProperties

        FileList=['MechPro', 'Helmet', 'Mechfy']

        #if (amProperty.GenMechFolder=='Preset') or (amProperty.GenMechFolder==''):
            #FolderPath=os.path.dirname(__file__)+'//Preset//'
        #else:
            #FolderPath=os.path.dirname(__file__)+'//Preset//'+amProperty.GenMechFolder+'//'

        FolderPath=os.path.dirname(__file__)+'//Preset//'#'\Preset'
        #path = os.path.realpath(FolderPath)
        for file in os.listdir(FolderPath):
            filename=file.split('.', 1)
            FileList.append(filename)

        dir_name = amProperty.GenMechEnum
        #FileList=PresetFile(self, context)#

        if len(FileList) <= 9:
            Filecount='00' + str(len(FileList)+1)
        elif len(FileList) <= 99:
            Filecount='0' + str(len(FileList)+1)
        else:
            Filecount = str(len(FileList)+1)

        if amProperty.GenMechName not in FileList :
            #amProperty.GenMechName = dir_name
            if '_' in dir_name:
                FinalFileName = amProperty.GenMechName[:-4]+'_'+ Filecount
            else:
                FinalFileName = amProperty.GenMechName+'_'+ Filecount
        else:
            if '_' in dir_name:
                #dir_name[:-4]
                FinalFileName = dir_name[:-4]+'_'+ Filecount
            else:
                FinalFileName = dir_name+'_'+ Filecount

        #FolderPath=os.path.dirname(__file__)+'//Preset//'
        #path = os.path.realpath(FolderPath)
        sel = bpy.context.selected_objects

        full_path = FolderPath + FinalFileName + '.txt'  # 也可以创建一个.doc的word文档
        file = open(full_path, 'w')
        file.write("#PresetName:"+FinalFileName+"\n")
        file.write("#Author:\n")
        file.write("#Description:"+"Add multiple modifier to object.\n")
        file.write("#Version:"+str(bpy.app.version)+"\n")
        file.write("#\n")
        file.write("#\n")#file.write("#add OBJ,OBJName,OBJInitialType,Xlocation,Ylocation,Zlocation,Xrotation,Yrotation,Zrotation,Xscale,Yscale,Zscale,AutoSmooth,EditXloc,EditYloc,EditZloc,EditXrot,EditYrot,EditZrot,EditXscale,EditYscale,EditZscale.\n")
        file.write("#\n")#file.write("#ModifierName,ModifierType,show_viewport,show_render,parameterCount,parameter[0],parameter[1],parameter[2]...\n")
        file.write("#\n")
        file.write("*Next|1|9|\n")#file.write("#We start form 11 line to generate.In theory,if We don't have select any OBJ,we will generate 11 line OBJ's initial type mesh.If OBJ's initial type not a simple mesh,Yeah!We generate a Cube again.\n")
        n=1
        LineCount=count(10, 1)
        
        for ob in sel:
            #FinalFileName=FileName(self, context)
            if ob.name == bpy.context.view_layer.objects.active.name:
                OBJType = "ParentOBJ"
            else:
                OBJType = "AddOBJ"
            next(LineCount)
            if ob.type == 'MESH':
                OBJAutoSmooth=ob.data.use_auto_smooth
            else:
                OBJAutoSmooth=''
            
            file.write(OBJType+"|"+ob.name+"|"+str(ob.name.split('.', 1)[0])+"|"+str(ob.location[0])+"|"+str(ob.location[1])+"|"+str(ob.location[2])+"|"+str(ob.rotation_euler[0])+"|"+str(ob.rotation_euler[1])+"|"+str(ob.rotation_euler[2])+"|"+str(ob.scale[0])+"|"+str(ob.scale[1])+"|"+str(ob.scale[2])+"|"+\
                    str(OBJAutoSmooth)+"|"+"0|0|0|0|0|0|1|1|1|"+"\n")
            
            i=0#ob.name if '.' not in ob.name else 
            for mod in ob.modifiers:
                i=i+1
                if amProperty.ReDataNameBool==True:
                    mod.name=str(i)+"_"+str.capitalize(mod.type)
                
                next(LineCount)
                file.write(str(mod.name)+"|"+str(mod.type) + "|" + str(mod.show_viewport) + "|" + str(mod.show_render) + "|" + ModInput(mod)+"|"+"\n")
            l=0
            for cons in ob.constraints:
                l=l+1
                if amProperty.ReDataNameBool==True:
                    cons.name=str(l)+"_"+str(cons.type.title().replace('_',''))
                next(LineCount)
                file.write(str(cons.name)+"|"+"Con_"+str(cons.type)+"|"+str(cons.mute)+"|"+ObjCon(cons)+"|"+"\n")#读取的时候[4:]
                #file.write(ObjCon(cons))

            n=n+1
            NextLineCount=next(LineCount)
            file.write("*Next|"+str(n)+'|'+str(NextLineCount)+"|\n")

        for Tex in bpy.data.textures:
            file.write('Texture'+"|"+TexInput(Tex)+"|\n")

        for Geo in bpy.data.node_groups:
            if Geo.type=='GEOMETRY':
                for Node in Geo.nodes:
                    file.write('GeometryNode'+"|"+Geo.name+"|"+GeoNodeInput(Node)+"|\n")

        
        for ob in sel:
            if ob.animation_data !=None:
                for d in ob.animation_data.drivers:#第2个参数如果是mesh则转换为OBJECT type
                    OBJDriver=''
                    dType='OBJECT'#ob.type
                    OBJDriver+='Drivers'+"|"+str(dType)+"|"+ob.name+"|"+str(d.data_path)+"|"+str(d.array_index)+'|'+str(d.driver.type)+"|"+str(d.driver.expression)+"|"+str(len(d.driver.variables))+"|"
                    for var in d.driver.variables:
                        for target in var.targets:
                            if target.id:
                                targetname=str(target.id).split('"')
                                targetname=targetname[1]
                            else:
                                targetname=''
                            OBJDriver+=str(var.type)+"|"+str(var.name)+"|"+str(target.id_type)+"|"+targetname+"|"+str(target.data_path)+"|"+str(target.transform_type)+"|"+str(target.transform_space)+"|"+str(target.rotation_mode)+"|"#|表达式1类型|脚本表达式||...
                    file.write(OBJDriver+'\n')
                            ##Drviers|源对象|源对象类型|源对象驱动器路径|index|表达式1类型|脚本表达式|对象数量|        对象函数名1|对象函数类型1|对象类型1|对象指针名1|对象1路径|...变换类型 变换空间 旋转模式('ROT' in transform_type时设置)
                            #Drivers|Cube|MESH|constraints["Floor"].offset|d.array_index|SCRIPTED|var -0.4|d.driver.variables|       var|SINGLE_PROP|NODETREE|Node1|nodes["Vector"].vector[2]|LOC_X|WORLD_SPACE|AUTO|
                                                                                            #var_001|TRANSFORMS|OBJECT|Cube||ROT_Z|TRANSFORM_SPACE|AUTO|
                            ##Drviers|source|sourceType(id_type)|prop|driver.type|expression           |Func1Name|Func1Type           target1Type(id_type)|target1(id)|dataPath1||

        for Tex in bpy.data.textures:
            if Tex.animation_data !=None:
                for d in Tex.animation_data.drivers:
                    OBJDriver=''
                    dType='TEXTURE'#Tex.type
                    OBJDriver+='Drivers'+"|"+str(dType)+"|"+Tex.name+"|"+str(d.data_path)+"|"+str(d.array_index)+'|'+str(d.driver.type)+"|"+str(d.driver.expression)+"|"+str(len(d.driver.variables))+"|"
                    for var in d.driver.variables:
                        for target in var.targets:
                            if target.id:
                                targetname=str(target.id).split('"')
                                targetname=targetname[1]
                            else:
                                targetname=''
                            OBJDriver+=str(var.type)+"|"+str(var.name)+"|"+str(target.id_type)+"|"+targetname+"|"+str(target.data_path)+"|"+str(target.transform_type)+"|"+str(target.transform_space)+"|"+str(target.rotation_mode)+"|"#|表达式1类型|脚本表达式||...
                    file.write(OBJDriver+'\n')

        for Geo in bpy.data.node_groups:
            if (Geo.animation_data !=None) and (Geo.type=='GEOMETRY'):
                for d in Geo.animation_data.drivers:
                    OBJDriver=''
                    dType='NODETREE'#Geo.type
                    OBJDriver+='Drivers'+"|"+dType+"|"+Geo.name+"|"+str(d.data_path)+"|"+str(d.array_index)+'|'+str(d.driver.type)+"|"+str(d.driver.expression)+"|"+str(len(d.driver.variables))+"|"
                    for var in d.driver.variables:
                        for target in var.targets:
                            if target.id:
                                targetname=str(target.id).split('"')
                                targetname=targetname[1]
                            else:
                                targetname=''
                            OBJDriver+=str(var.type)+"|"+str(var.name)+"|"+str(target.id_type)+"|"+targetname+"|"+str(target.data_path)+"|"+str(target.transform_type)+"|"+str(target.transform_space)+"|"+str(target.rotation_mode)+"|"#|表达式1类型|脚本表达式||...
                    file.write(OBJDriver+'\n')


        file.close()




        

        #amProperty.GenMechEnum=FinalFileName
        #GenMechEnum_Item()

        amProperty.GenMechFolder='Preset'
        amProperty.GenMechEnum=FinalFileName



        self.report({'INFO'}, "保存预设")
        return {'FINISHED'}


def ModInput(mod):
    Mod = mod
    ModInputList=''
    if Mod.type == 'SKIN':
        parameter = 5
        ModInputList=str(parameter)+'|'+str(Mod.branch_smoothing)+'|'+str(Mod.use_x_symmetry)+'|'+str(Mod.use_y_symmetry)+'|'+str(Mod.use_z_symmetry)+'|'+str(Mod.use_smooth_shade)

    elif Mod.type == 'CAST':
        parameter = 12#
        ModInputList=str(parameter)+'|'+\
                    str("'"+Mod.cast_type+"'")+'|'+\
                    str(Mod.use_x)+'|'+\
                    str(Mod.use_y)+'|'+\
                    str(Mod.use_z)+'|'+\
                    str(Mod.factor)+'|'+\
                    str(Mod.radius)+'|'+\
                    str(Mod.size)+'|'+\
                    str(Mod.use_radius_as_size)+'|'+\
                    str("'"+Mod.vertex_group+"'")+'|'+\
                    str(Mod.invert_vertex_group)+'|'+\
                    str("bpy.data.objects['"+Mod.object.name+"']" if Mod.object != None else Mod.object)+'|'+\
                    str(Mod.use_transform)

    elif Mod.type == 'BOOLEAN':
        parameter = 5#
        ModInputList=str(parameter)+'|'+\
                    str(Mod.operation)+'|'+\
                    str("bpy.data.objects['"+Mod.object.name+"']" if Mod.object != None else Mod.object)+'|'+\
                    str(Mod.double_threshold)

        if bpy.app.version >= (2, 92, 0):
            ModInputList+='|'+str(Mod.solver)+'|'+str(Mod.use_self)


    elif Mod.type == 'REMESH':
        parameter = 6
        ModInputList=str(parameter)+'|'+\
                    str("'"+Mod.mode+"'")+'|'+\
                    str(Mod.octree_depth)+'|'+\
                    str(Mod.scale)+'|'+\
                    str(Mod.use_remove_disconnected)+'|'+\
                    str(Mod.threshold)+'|'+\
                    str(Mod.use_smooth_shade)

    elif Mod.type == 'SIMPLE_DEFORM':
        parameter = 11
        ModInputList=str(parameter)+'|'+\
                    str("'"+Mod.deform_method+"'")+'|'+\
                    str(Mod.angle)+'|'+\
                    str("bpy.data.objects['"+Mod.origin.name+"']" if Mod.origin != None else Mod.origin)+'|'+\
                    str("'"+Mod.deform_axis+"'")+'|'+\
                    str(Mod.limits[0])+'|'+\
                    str(Mod.limits[1])+'|'+\
                    str(Mod.lock_x)+'|'+\
                    str(Mod.lock_y)+'|'+\
                    str(Mod.lock_z)+'|'+\
                    str("'"+Mod.vertex_group+"'")+'|'+\
                    str(Mod.invert_vertex_group)
                
        """                
        .deform_method = 'TWIST'
        .angle = 0.4
        .origin = None
        .deform_axis = 'X'
        .limits[0] = 0
        .limits[1] = 1
        .lock_X = True
        .lock_y = True
        .lock_z = True
        .vertex_group = ""
        """



    elif Mod.type == 'DISPLACE':
        parameter = 7#可以扩展一下这个纹理的参数，还有上面的布尔位置 旋转 大小参数 
        ModInputList=str(parameter)+'|'+\
                    str("bpy.data.textures['"+Mod.texture.name+"']" if Mod.texture != None else Mod.texture)+'|'+\
                    str("'"+Mod.direction+"'")+'|'+\
                    str("'"+Mod.space+"'")+'|'+\
                    str(Mod.strength)+'|'+\
                    str(Mod.mid_level)+'|'+\
                    str("'"+Mod.vertex_group+"'")+'|'+\
                    str(Mod.invert_vertex_group)

    elif Mod.type == 'ARRAY':
        parameter = 19
        ModInputList=str(parameter)+'|'+\
                    str("'"+Mod.fit_type+"'")+'|'+\
                    str(Mod.count)+'|'+\
                    str(Mod.use_relative_offset)+'|'+\
                    str(Mod.relative_offset_displace[0])+'|'+\
                    str(Mod.relative_offset_displace[1])+'|'+\
                    str(Mod.relative_offset_displace[2])+'|'+\
                    str(Mod.use_constant_offset)+'|'+\
                    str(Mod.constant_offset_displace[0])+'|'+\
                    str(Mod.constant_offset_displace[1])+'|'+\
                    str(Mod.constant_offset_displace[2])+'|'+\
                    str(Mod.use_object_offset)+'|'+\
                    str("bpy.data.objects['"+Mod.offset_object.name+"']" if Mod.offset_object != None else Mod.offset_object)+'|'+\
                    str(Mod.use_merge_vertices)+'|'+\
                    str(Mod.merge_threshold)+'|'+\
                    str(Mod.use_merge_vertices_cap)+'|'+\
                    str(Mod.offset_u)+'|'+\
                    str(Mod.offset_v)+'|'+\
                    str("bpy.data.objects['"+Mod.start_cap.name+"']" if Mod.start_cap != None else Mod.start_cap)+'|'+\
                    str("bpy.data.objects['"+Mod.end_cap.name+"']" if Mod.end_cap != None else Mod.end_cap)
                    #bpy.context.object.modifiers["Array"].end_cap = None



    elif Mod.type == 'WARP':
        parameter = 10#
        ModInputList=str(parameter)+'|'+\
                    str("bpy.data.objects['"+Mod.object_from.name+"']" if Mod.object_from != None else Mod.object_from)+'|'+\
                    str("bpy.data.objects['"+Mod.object_to.name+"']" if Mod.object_to != None else Mod.object_to)+'|'+\
                    str(Mod.use_volume_preserve)+'|'+\
                    str(Mod.strength)+'|'+\
                    str("'"+Mod.vertex_group+"'")+'|'+\
                    str(Mod.invert_vertex_group)+'|'+\
                    str("'"+Mod.falloff_type+"'")+'|'+\
                    str(Mod.falloff_radius)+'|'+\
                    str("bpy.data.textures['"+Mod.texture.name+"']" if Mod.texture != None else Mod.texture)+'|'+\
                    str("'"+Mod.texture_coords+"'")#
                

    elif Mod.type == 'WIREFRAME':
        parameter = 12#
        ModInputList=str(parameter)+'|'+\
                    str(Mod.thickness)+'|'+\
                    str(Mod.offset)+'|'+\
                    str(Mod.use_boundary)+'|'+\
                    str(Mod.use_replace)+'|'+\
                    str(Mod.use_even_offset)+'|'+\
                    str(Mod.use_relative_offset)+'|'+\
                    str(Mod.use_crease)+'|'+\
                    str(Mod.crease_weight)+'|'+\
                    str(Mod.material_offset)+'|'+\
                    str("'"+Mod.vertex_group+"'")+'|'+\
                    str(Mod.invert_vertex_group)+'|'+\
                    str(Mod.thickness_vertex_group)
        '''
        .thickness = 0.02
        .offset = 0
        .use_boundary = False
        .use_replace = True
        .use_even_offset = False
        .use_relative_offset = False
        .use_crease = True
        .crease_weight = 1
        .material_offset = 0
        .vertex_group = ""
        .thickness_vertex_group = 0
        '''

    elif Mod.type == 'SCREW':
        parameter = 15#
        ModInputList=str(parameter)+'|'+\
                    str(Mod.angle)+'|'+\
                    str(Mod.screw_offset)+'|'+\
                    str(Mod.iterations)+'|'+\
                    str("'"+Mod.axis+"'")+'|'+\
                    str("bpy.data.objects['"+Mod.object.name+"']" if Mod.object != None else Mod.object)+'|'+\
                    str(Mod.use_object_screw_offset)+'|'+\
                    str(Mod.steps)+'|'+\
                    str(Mod.render_steps)+'|'+\
                    str(Mod.use_merge_vertices)+'|'+\
                    str(Mod.merge_threshold)+'|'+\
                    str(Mod.use_stretch_u)+'|'+\
                    str(Mod.use_stretch_v)+'|'+\
                    str(Mod.use_smooth_shade)+'|'+\
                    str(Mod.use_normal_calculate)+'|'+\
                    str(Mod.use_normal_flip)

        """ 
        .angle = 18.8496
        .screw_offset = 100
        .iterations = 2
        .axis = 'X'
        .object = None
        .use_object_screw_offset = True
        .steps = 8
        .render_steps = 8
        .use_merge_vertices = True
        .merge_threshold = 0.01
        .use_stretch_u = True
        .use_stretch_v = True
        .use_smooth_shade = False
        .use_normal_calculate = True
        .use_normal_flip = True
        """

    elif Mod.type == 'SHRINKWRAP':
        parameter = 6#
        ModInputList=str(parameter)+'|'+\
                    str("'"+Mod.wrap_method+"'")+'|'+\
                    str("'"+Mod.wrap_mode+"'")+'|'+\
                    str("bpy.data.objects['"+Mod.target.name+"']" if Mod.target != None else Mod.target)+'|'+\
                    str(Mod.offset)+'|'+\
                    str("'"+Mod.vertex_group+"'")+'|'+\
                    str(Mod.invert_vertex_group)

        '''
        .wrap_method = 'NEAREST_SURFACEPOINT'
        .wrap_mode = 'ON_SURFACE'
        .target = bpy.data.objects["Cube_ObjBoolPlane"]
        .offset = 0.5
        .vertex_group = ""
        '''




    elif Mod.type == 'WAVE':
        parameter = 22
        ModInputList=str(parameter)+'|'+\
                    str(Mod.use_x)+'|'+\
                    str(Mod.use_y)+'|'+\
                    str(Mod.use_cyclic)+'|'+\
                    str(Mod.use_normal)+'|'+\
                    str(Mod.use_normal_x)+'|'+\
                    str(Mod.use_normal_y)+'|'+\
                    str(Mod.use_normal_z)+'|'+\
                    str(Mod.falloff_radius)+'|'+\
                    str(Mod.height)+'|'+\
                    str(Mod.width)+'|'+\
                    str(Mod.narrowness)+'|'+\
                    str("'"+Mod.vertex_group+"'")+'|'+\
                    str(Mod.invert_vertex_group)+'|'+\
                    str(Mod.start_position_object)+'|'+\
                    str(Mod.start_position_x)+'|'+\
                    str(Mod.start_position_y)+'|'+\
                    str(Mod.time_offset)+'|'+\
                    str(Mod.lifetime)+'|'+\
                    str(Mod.damping_time)+'|'+\
                    str(Mod.speed)+'|'+\
                    str("bpy.data.textures['"+Mod.texture.name+"']" if Mod.texture != None else Mod.texture)+'|'+\
                    str("'"+Mod.texture_coords+"'")

        '''
        .use_x = False
        .use_y = False
        .use_cyclic = False
        .use_normal = True
        .use_normal_x = False
        .use_normal_y = False
        .use_normal_z = False
        .falloff_radius = 0
        .height = 1
        .width = 1.5
        .narrowness = 1.5
        .vertex_group = ""
        .start_position_object = None
        .start_position_x = 0
        .start_position_y = 0
        .time_offset = 0
        .lifetime = 0
        .damping_time = 10
        .speed = 0.25
        Tex.name = "DisplaceTexture"
        .texture_coords = 'LOCAL'
        '''


    elif Mod.type == 'LAPLACIANSMOOTH':
        parameter = 10
        ModInputList=str(parameter)+'|'+\
                    str(Mod.iterations)+'|'+\
                    str(Mod.use_x)+'|'+\
                    str(Mod.use_y)+'|'+\
                    str(Mod.use_z)+'|'+\
                    str(Mod.lambda_factor)+'|'+\
                    str(Mod.lambda_border)+'|'+\
                    str(Mod.use_volume_preserve)+'|'+\
                    str(Mod.use_normalized)+'|'+\
                    str("'"+Mod.vertex_group+"'")+'|'+\
                    str(Mod.invert_vertex_group)

        '''
        .iterations = 3
        .use_x = False
        .use_y = False
        .use_z = False
        .lambda_factor = 0.1
        .lambda_border = 0.1
        .use_volume_preserve = False
        .use_normalized = False
        .vertex_group = ""
        '''

    elif Mod.type == 'LATTICE':
        parameter = 4
        ModInputList=str(parameter)+'|'+\
                    str("bpy.data.objects['"+Mod.object.name+"']" if Mod.object != None else Mod.object)+'|'+\
                    str("'"+Mod.vertex_group+"'")+'|'+\
                    str(Mod.invert_vertex_group)+'|'+\
                    str(Mod.strength)


        '''
        .object = bpy.data.objects["Cube_ObjLattice"]
        .vertex_group = ""
        .strength = 1
        '''

    elif Mod.type == 'BEVEL':
        parameter = 21
        ModInputList=str(parameter)+'|'+\
                    str("'"+Mod.affect+"'")+'|'+\
                    str("'"+Mod.offset_type+"'")+'|'+\
                    str(Mod.width_pct)+'|'+\
                    str(Mod.segments)+'|'+\
                    str(Mod.angle_limit)+'|'+\
                    str("'"+Mod.limit_method+"'")+'|'+\
                    str("'"+Mod.vertex_group+"'")+'|'+\
                    str(Mod.invert_vertex_group)+'|'+\
                    str("'"+Mod.profile_type+"'")+'|'+\
                    str(Mod.profile)+'|'+\
                    str("'"+Mod.miter_outer+"'")+'|'+\
                    str("'"+Mod.miter_inner+"'")+'|'+\
                    str(Mod.spread)+'|'+\
                    str("'"+Mod.vmesh_method+"'")+'|'+\
                    str(Mod.use_clamp_overlap)+'|'+\
                    str(Mod.loop_slide)+'|'+\
                    str(Mod.harden_normals)+'|'+\
                    str(Mod.mark_seam)+'|'+\
                    str(Mod.mark_sharp)+'|'+\
                    str(Mod.material)+'|'+\
                    str("'"+Mod.face_strength_mode+"'")

        '''
        .affect = 'EDGES'
        .offset_type = 'PERCENT'
        .width_pct = 8
        .segments = 1
        .angle_limit = 0.523599
        .limit_method = 'VGROUP'
        .vertex_group = ""
        .profile_type = 'SUPERELLIPSE'
        .profile = 0.5
        .miter_outer = 'MITER_PATCH'
        .miter_inner = 'MITER_ARC'
        .spread = 0.1
        .vmesh_method = 'CUTOFF'
        .use_clamp_overlap = False
        .loop_slide = False
        .harden_normals = True
        .mark_seam = True
        .mark_sharp = True
        .material = 1
        .face_strength_mode = 'FSTR_NONE'
        '''

    elif Mod.type == 'DECIMATE':
        parameter = 12#delimit
        ModInputList=str(parameter)+'|'+\
                    str("'"+Mod.decimate_type+"'")+'|'+\
                    str(Mod.ratio)+'|'+\
                    str(Mod.use_symmetry)+'|'+\
                    str("'"+Mod.symmetry_axis+"'")+'|'+\
                    str(Mod.use_collapse_triangulate)+'|'+\
                    str("'"+Mod.vertex_group+"'")+'|'+\
                    str(Mod.invert_vertex_group)+'|'+\
                    str(Mod.vertex_group_factor)+'|'+\
                    str(Mod.iterations)+'|'+\
                    str(Mod.angle_limit)+'|'+\
                    str(Mod.delimit)+'|'+\
                    str(Mod.use_dissolve_boundaries)

        '''
        .decimate_type = 'COLLAPSE'
        .ratio = 1
        .use_symmetry = False
        .symmetry_axis = 'X'
        .use_collapse_triangulate = False
        .vertex_group = ""
        .vertex_group_factor = 1

        .iterations = 0

        .angle_limit = 0.0872665
        .delimit = {'NORMAL'}|||
        .use_dissolve_boundaries = False
        '''

    elif Mod.type == 'CURVE':
        parameter = 4
        ModInputList=str(parameter)+'|'+\
                    str("bpy.data.objects['"+Mod.object.name+"']" if Mod.object != None else Mod.object)+'|'+\
                    str("'"+Mod.deform_axis+"'")+'|'+\
                    str("'"+Mod.vertex_group+"'")+'|'+\
                    str(Mod.invert_vertex_group)

        '''
        .object = bpy.data.objects["Cube_ObjCurve"]
        .deform_axis = 'POS_X'
        .vertex_group = ""
        '''

    elif Mod.type == 'EDGE_SPLIT':
        parameter = 3
        ModInputList=str(parameter)+'|'+\
                    str(Mod.use_edge_angle)+'|'+\
                    str(Mod.split_angle)+'|'+\
                    str(Mod.use_edge_sharp)
        '''
        .use_edge_angle = False
        .split_angle = 0.0523599
        .use_edge_sharp = False
        '''


    elif Mod.type == 'SOLIDIFY':
        parameter = 25
        ModInputList=str(parameter)+'|'+\
                    str("'"+Mod.solidify_mode+"'")+'|'+\
                    str("'"+Mod.nonmanifold_thickness_mode+"'")+'|'+\
                    str("'"+Mod.nonmanifold_boundary_mode+"'")+'|'+\
                    str(Mod.thickness)+'|'+\
                    str(Mod.offset)+'|'+\
                    str(Mod.nonmanifold_merge_threshold)+'|'+\
                    str(Mod.use_rim)+'|'+\
                    str(Mod.use_rim_only)+'|'+\
                    str("'"+Mod.vertex_group+"'")+'|'+\
                    str(Mod.invert_vertex_group)+'|'+\
                    str(Mod.thickness_vertex_group)+'|'+\
                    str(Mod.use_flat_faces)+'|'+\
                    str(Mod.use_flip_normals)+'|'+\
                    str(Mod.material_offset)+'|'+\
                    str(Mod.material_offset_rim)+'|'+\
                    str(Mod.bevel_convex)+'|'+\
                    str(Mod.thickness_clamp)+'|'+\
                    str(Mod.use_thickness_angle_clamp)+'|'+\
                    str("'"+Mod.shell_vertex_group+"'")+'|'+\
                    str("'"+Mod.rim_vertex_group+"'")+'|'+\
                    str(Mod.use_even_offset)+'|'+\
                    str(Mod.use_quality_normals)+'|'+\
                    str(Mod.edge_crease_inner)+'|'+\
                    str(Mod.edge_crease_outer)+'|'+\
                    str(Mod.edge_crease_rim)
        '''
        .solidify_mode = 'NON_MANIFOLD'
        .nonmanifold_thickness_mode = 'CONSTRAINTS'
        .nonmanifold_boundary_mode = 'FLAT'
        .thickness = 1.4
        .offset = 1
        .nonmanifold_merge_threshold = 0.02
        .use_rim = False
        .use_rim_only = False
        .vertex_group = ""
        .thickness_vertex_group = 0
        .use_flat_faces = True
        .use_flip_normals = True
        .material_offset = 0
        .material_offset_rim = 0
        .bevel_convex = 0
        .thickness_clamp = 0
        .use_thickness_angle_clamp = True
        .shell_vertex_group = ""
        .rim_vertex_group = ""


        .use_even_offset = True

        .use_quality_normals = True
        .edge_crease_inner = 0
        .edge_crease_outer = 0
        .edge_crease_rim = 0

        '''

    elif Mod.type == 'SMOOTH':
        parameter = 7
        ModInputList=str(parameter)+'|'+\
                    str(Mod.use_x)+'|'+\
                    str(Mod.use_y)+'|'+\
                    str(Mod.use_z)+'|'+\
                    str(Mod.factor)+'|'+\
                    str(Mod.iterations)+'|'+\
                    str("'"+Mod.vertex_group+"'")+'|'+\
                    str(Mod.invert_vertex_group)

        '''
        .use_x = False
        .use_y = False
        .use_z = False
        .factor = 0.97
        .iterations = 1
        .vertex_group = ""
        '''

    elif Mod.type == 'SUBSURF':
        parameter = 9
        ModInputList=str(parameter)+'|'+\
                    str("'"+Mod.subdivision_type+"'")+'|'+\
                    str(Mod.levels)+'|'+\
                    str(Mod.render_levels)+'|'+\
                    str(Mod.show_only_control_edges)+'|'+\
                    str(Mod.show_only_control_edges)+'|'+\
                    str(Mod.quality)+'|'+\
                    str(Mod.uv_smooth)+'|'+\
                    str(Mod.use_creases)+'|'+\
                    str(Mod.use_custom_normals)



        '''
        .subdivision_type = 'CATMULL_CLARK'
        .levels = 1
        .render_levels = 1
        .show_only_control_edges = False
        .show_only_control_edges = True
        .quality = 3
        .uv_smooth = 'NONE'
        .use_creases = False
        .use_custom_normals = True
        '''

    elif Mod.type == 'TRIANGULATE':
        parameter = 4
        ModInputList=str(parameter)+'|'+\
                    str("'"+Mod.quad_method+"'")+'|'+\
                    str("'"+Mod.ngon_method+"'")+'|'+\
                    str(Mod.min_vertices)+'|'+\
                    str(Mod.keep_custom_normals)

        '''
        .quad_method = 'BEAUTY'
        .ngon_method = 'BEAUTY'
        .min_vertices = 4
        .keep_custom_normals = True
        '''

    elif Mod.type == 'WELD':
        parameter = 4
        ModInputList=str(parameter)+'|'+\
                    str(Mod.merge_threshold)+'|'+\
                    str(Mod.mode)+'|'+\
                    str("'"+Mod.vertex_group+"'")+'|'+\
                    str(Mod.invert_vertex_group)

        '''
        .merge_threshold = 0.005
        .max_interactions = 1
        .vertex_group = ""
        '''


    elif Mod.type == 'MIRROR':
        parameter = 21
        ModInputList=str(parameter)+'|'+\
                    str(Mod.use_axis[0])+'|'+\
                    str(Mod.use_axis[1])+'|'+\
                    str(Mod.use_axis[2])+'|'+\
                    str(Mod.use_bisect_axis[0])+'|'+\
                    str(Mod.use_bisect_axis[1])+'|'+\
                    str(Mod.use_bisect_axis[2])+'|'+\
                    str(Mod.use_bisect_flip_axis[0])+'|'+\
                    str(Mod.use_bisect_flip_axis[1])+'|'+\
                    str(Mod.use_bisect_flip_axis[2])+'|'+\
                    str("bpy.data.objects['"+Mod.mirror_object.name+"']" if Mod.mirror_object != None else Mod.mirror_object)+'|'+\
                    str(Mod.use_clip)+'|'+\
                    str(Mod.use_mirror_merge)+'|'+\
                    str(Mod.merge_threshold)+'|'+\
                    str(Mod.use_mirror_u)+'|'+\
                    str(Mod.use_mirror_v)+'|'+\
                    str(Mod.mirror_offset_u)+'|'+\
                    str(Mod.mirror_offset_v)+'|'+\
                    str(Mod.offset_u)+'|'+\
                    str(Mod.offset_v)+'|'+\
                    str(Mod.use_mirror_vertex_groups)+'|'+\
                    str(Mod.use_mirror_udim)

        '''
        .use_axis[0] = True
        .use_axis[1] = True
        .use_axis[2] = True
        .use_bisect_axis[0] = True
        .use_bisect_axis[1] = True
        .use_bisect_axis[2] = True
        .use_bisect_flip_axis[0] = True
        .use_bisect_flip_axis[1] = True
        .use_bisect_flip_axis[2] = True
        .mirror_object = None
        .use_clip = True
        .use_mirror_merge = False
        .merge_threshold = 0.001
        .use_mirror_u = True
        .use_mirror_v = True
        .mirror_offset_u = 0
        .mirror_offset_v = 0
        .offset_u = 0
        .offset_v = 0
        .use_mirror_vertex_groups = False
        .use_mirror_udim = True
        '''

    elif Mod.type == 'BUILD':
        parameter = 5
        ModInputList=str(parameter)+'|'+\
                    str(Mod.frame_start)+'|'+\
                    str(Mod.frame_duration)+'|'+\
                    str(Mod.use_reverse)+'|'+\
                    str(Mod.use_random_order)+'|'+\
                    str(Mod.seed)

        '''
        .frame_start = -1
        .frame_duration = 1
        .use_reverse = False
        .use_random_order = True
        .seed = 12
        '''

    elif Mod.type == 'OCEAN':
        parameter = 26#后面烘培选项内容就不添加进来了
        ModInputList=str(parameter)+'|'+\
                    str("'"+Mod.geometry_mode+"'")+'|'+\
                    str(Mod.repeat_x)+'|'+\
                    str(Mod.repeat_y)+'|'+\
                    str(Mod.resolution)+'|'+\
                    str(Mod.time)+'|'+\
                    str(Mod.depth)+'|'+\
                    str(Mod.size)+'|'+\
                    str(Mod.spatial_size)+'|'+\
                    str(Mod.random_seed)+'|'+\
                    str(Mod.use_normals)+'|'+\
                    str(Mod.wave_scale)+'|'+\
                    str(Mod.wave_scale_min)+'|'+\
                    str(Mod.choppiness)+'|'+\
                    str(Mod.wind_velocity)+'|'+\
                    str(Mod.wave_alignment)+'|'+\
                    str(Mod.wave_direction)+'|'+\
                    str(Mod.damping)+'|'+\
                    str(Mod.use_foam)+'|'+\
                    str("'"+Mod.foam_layer_name+"'")+'|'+\
                    str(Mod.foam_coverage)+'|'+\
                    str(Mod.use_spray)+'|'+\
                    str("'"+Mod.spray_layer_name+"'")+'|'+\
                    str(Mod.invert_spray)+'|'+\
                    str("'"+Mod.spectrum+"'")+'|'+\
                    str(Mod.sharpen_peak_jonswap)+'|'+\
                    str(Mod.fetch_jonswap)

        '''
        .geometry_mode = 'GENERATE'
        .repeat_x = 1
        .repeat_y = 1
        .resolution = 5
        .time = 2.49
        .depth = 200
        .size = 1.07
        .spatial_size = 54
        .random_seed = 0
        .use_normals = True
        .wave_scale = 1
        .wave_scale_min = 0.01
        .choppiness = 1
        .wind_velocity = 30
        .wave_alignment = 0
        .wave_direction = 0
        .damping = 0.5
        .use_foam = False
        .foam_layer_name = ""
        .foam_coverage = 0
        .use_spray = False
        .spray_layer_name = ""
        .invert_spray = True
        .spectrum = 'PHILLIPS'
        .sharpen_peak_jonswap = 0.039823
        .fetch_jonswap = 115.6
        '''

    elif Mod.type == 'HOOK':
        parameter = 6
        ModInputList=str(parameter)+'|'+\
                    str("bpy.data.objects['"+Mod.object.name+"']" if Mod.object != None else Mod.object)+'|'+\
                    str("'"+Mod.vertex_group+"'")+'|'+\
                    str(Mod.invert_vertex_group)+'|'+\
                    str(Mod.strength)+'|'+\
                    str(Mod.falloff_radius)+'|'+\
                    str(Mod.use_falloff_uniform)

        '''
        .object = bpy.data.objects["立方体"]
        .vertex_group = "群组.001"
        .strength = 0.553097
        .falloff_radius = 60
        .use_falloff_uniform = False
        '''

    elif Mod.type == 'CORRECTIVE_SMOOTH':
        parameter = 9
        ModInputList=str(parameter)+'|'+\
                    str(Mod.factor)+'|'+\
                    str(Mod.iterations)+'|'+\
                    str(Mod.scale)+'|'+\
                    str("'"+Mod.smooth_type+"'")+'|'+\
                    str("'"+Mod.vertex_group+"'")+'|'+\
                    str(Mod.invert_vertex_group)+'|'+\
                    str(Mod.use_only_smooth)+'|'+\
                    str(Mod.use_pin_boundary)+'|'+\
                    str("'"+Mod.rest_source+"'")

        '''bpy.context.object.modifiers["CorrectiveSmooth"].
        .factor = 0.070796
        .iterations = 15
        .scale = 0.20354
        .smooth_type = 'SIMPLE'
        .vertex_group = "群组"
        invert_vertex_group = True
        .use_only_smooth = True
        .use_pin_boundary = True
        .rest_source = 'ORCO'
        '''


    elif Mod.type == 'EXPLODE':
        parameter = 9
        ModInputList=str(parameter)+'|'+\
                    str("'"+Mod.particle_uv+"'")+'|'+\
                    str(Mod.show_alive)+'|'+\
                    str(Mod.show_dead)+'|'+\
                    str(Mod.show_unborn)+'|'+\
                    str(Mod.use_edge_cut)+'|'+\
                    str(Mod.use_size)+'|'+\
                    str("'"+Mod.vertex_group+"'")+'|'+\
                    str(Mod.invert_vertex_group)+'|'+\
                    str(Mod.protect)

        '''
        Mod.particle_uv = "UVMap"
        Mod.show_alive = False
        Mod.show_dead = False
        Mod.show_unborn = False
        Mod.use_edge_cut = True
        Mod.use_size = True
        Mod.invert_vertex_group = True
        Mod.vertex_group = ""
        Mod.protect = 1 float

        str("'"+Mod.particle_uv+"'")
        str("'"+Mod.vertex_group+"'")
        '''

    elif Mod.type == 'PARTICLE_INSTANCE':
        parameter = 20
        ModInputList=str(parameter)+'|'+\
                    str("bpy.data.objects['"+Mod.object.name+"']" if Mod.object != None else Mod.object)+'|'+\
                    str(Mod.particle_system_index)+'|'+\
                    str(Mod.use_normal)+'|'+\
                    str(Mod.use_children)+'|'+\
                    str(Mod.use_size)+'|'+\
                    str(Mod.show_alive)+'|'+\
                    str(Mod.show_dead)+'|'+\
                    str(Mod.show_unborn)+'|'+\
                    str(Mod.particle_amount)+'|'+\
                    str(Mod.particle_offset)+'|'+\
                    str(Mod.space)+'|'+\
                    str(Mod.axis)+'|'+\
                    str(Mod.use_path)+'|'+\
                    str(Mod.position)+'|'+\
                    str(Mod.random_position)+'|'+\
                    str(Mod.rotation)+'|'+\
                    str(Mod.random_rotation)+'|'+\
                    str(Mod.use_preserve_shape)+'|'+\
                    str(Mod.index_layer_name)+'|'+\
                    str(Mod.value_layer_name)

        '''
        Mod.object = None
        Mod.particle_system_index = 2
        Mod.use_normal = False
        Mod.use_children = False
        Mod.use_size = True
        Mod.show_alive = True
        Mod.show_dead = True
        Mod.show_unborn = True
        Mod.particle_amount = 0.982301
        Mod.particle_offset = 0.048673
        Mod.space = 'LOCAL'
        Mod.axis = 'X'
        Mod.use_path = False
        Mod.position = 0.929204
        Mod.random_position = 0.106195
        Mod.rotation = 0.150442
        Mod.random_rotation = 0.044248
        Mod.use_preserve_shape = False
        Mod.index_layer_name = ""
        Mod.value_layer_name = ""
        '''

    elif Mod.type == 'MULTIRES':
        parameter = 6
        ModInputList=str(parameter)+'|'+\
                    str(Mod.show_only_control_edges)+'|'+\
                    str(Mod.subdivision_type)+'|'+\
                    str(Mod.quality)+'|'+\
                    str(Mod.uv_smooth)+'|'+\
                    str(Mod.use_creases)+'|'+\
                    str(Mod.use_custom_normals)

        '''
        Mod.show_only_control_edges = True
        Mod.subdivision_type = 'CATMULL_CLARK'
        Mod.quality = 4
        Mod.uv_smooth = 'PRESERVE_CORNERS'
        Mod.use_creases = True
        Mod.use_custom_normals = False
        '''

    elif Mod.type == 'MASK':
        parameter = 5
        ModInputList=str(parameter)+'|'+\
                    str(Mod.mode)+'|'+\
                    str(Mod.vertex_group)+'|'+\
                    str("bpy.data.objects['"+Mod.armature.name+"']" if Mod.armature != None else Mod.armature)+'|'+\
                    str(Mod.invert_vertex_group)+'|'+\
                    str(Mod.threshold)

        '''
        Mod.mode = 'VERTEX_GROUP'
        Mod.vertex_group = ""
        Mod.armature = None
        Mod.invert_vertex_group = True
        Mod.threshold = 0.0752212
        '''


    elif Mod.type == 'ARMATURE':
        parameter = 7
        ModInputList=str(parameter)+'|'+\
                    str("bpy.data.objects['"+Mod.object.name+"']" if Mod.object != None else Mod.object)+'|'+\
                    str(Mod.vertex_group)+'|'+\
                    str(Mod.invert_vertex_group)+'|'+\
                    str(Mod.use_deform_preserve_volume)+'|'+\
                    str(Mod.use_multi_modifier)+'|'+\
                    str(Mod.use_vertex_groups)+'|'+\
                    str(Mod.use_bone_envelopes)

        '''
        Mod.object = None
        Mod.vertex_group = ""
        Mod.invert_vertex_group = True
        Mod.use_deform_preserve_volume = True
        Mod.use_multi_modifier = True
        Mod.use_vertex_groups = False
        Mod.use_bone_envelopes = True
        '''

    elif Mod.type == 'LAPLACIANDEFORM':
        parameter = 3
        ModInputList=str(parameter)+'|'+\
                    str(Mod.iterations)+'|'+\
                    str(Mod.vertex_group)+'|'+\
                    str(Mod.invert_vertex_group)

        '''
        Mod.iterations = 1 int
        Mod.vertex_group = ""
        Mod.invert_vertex_group = True
        '''

    elif Mod.type == 'MESH_DEFORM':
        parameter = 5
        ModInputList=str(parameter)+'|'+\
                    str("bpy.data.objects['"+Mod.object.name+"']" if Mod.object != None else Mod.object)+'|'+\
                    str(Mod.vertex_group)+'|'+\
                    str(Mod.invert_vertex_group)+'|'+\
                    str(Mod.precision)+'|'+\
                    str(Mod.use_dynamic_bind)

        '''
        Mod.object = None
        Mod.vertex_group = ""
        Mod.invert_vertex_group = True
        Mod.precision = 5
        Mod.use_dynamic_bind = True
        '''

    elif Mod.type == 'SURFACE_DEFORM':
        parameter = 5
        ModInputList=str(parameter)+'|'+\
                    str("bpy.data.objects['"+Mod.target.name+"']" if Mod.target != None else Mod.target)+'|'+\
                    str(Mod.falloff)+'|'+\
                    str(Mod.strength)+'|'+\
                    str(Mod.vertex_group)+'|'+\
                    str(Mod.invert_vertex_group)

        '''
        Mod.target = bpy.data.objects["Cube.001"]
        Mod.falloff = 5.1
        Mod.strength = 2.5
        Mod.vertex_group = ""
        Mod.invert_vertex_group = True
        '''

    elif Mod.type == 'DATA_TRANSFER':
        parameter = 28
        ModInputList=str(parameter)+'|'+\
                    str("bpy.data.objects['"+Mod.object.name+"']" if Mod.object != None else Mod.object)+'|'+\
                    str(Mod.use_object_transform)+'|'+\
                    str(Mod.mix_mode)+'|'+\
                    str(Mod.mix_factor)+'|'+\
                    str(Mod.vertex_group)+'|'+\
                    str(Mod.invert_vertex_group)+'|'+\
                    str(Mod.use_vert_data)+'|'+\
                    str(Mod.data_types_verts)+'|'+\
                    str(Mod.vert_mapping)+'|'+\
                    str(Mod.layers_vgroup_select_src)+'|'+\
                    str(Mod.layers_vgroup_select_dst)+'|'+\
                    str(Mod.use_edge_data)+'|'+\
                    str(Mod.data_types_edges)+'|'+\
                    str(Mod.edge_mapping)+'|'+\
                    str(Mod.use_loop_data)+'|'+\
                    str(Mod.data_types_loops)+'|'+\
                    str(Mod.loop_mapping)+'|'+\
                    str(Mod.layers_vcol_select_src)+'|'+\
                    str(Mod.layers_vcol_select_dst)+'|'+\
                    str(Mod.layers_uv_select_src)+'|'+\
                    str(Mod.layers_uv_select_dst)+'|'+\
                    str(Mod.islands_precision)+'|'+\
                    str(Mod.use_poly_data)+'|'+\
                    str(Mod.data_types_polys)+'|'+\
                    str(Mod.poly_mapping)+'|'+\
                    str(Mod.use_max_distance)+'|'+\
                    str(Mod.max_distance)+'|'+\
                    str(Mod.ray_radius)
        '''
        Mod.object = bpy.data.objects["Cone"]
        Mod.use_object_transform = False
        Mod.mix_mode = 'REPLACE'
        Mod.mix_factor = 0.845133
        Mod.vertex_group = "Group"
        Mod.invert_vertex_group = True

        Mod.use_vert_data = True
        Mod.data_types_verts = {'VGROUP_WEIGHTS'}#
        Mod.vert_mapping = 'NEAREST'
        Mod.layers_vgroup_select_src = 'ALL'
        Mod.layers_vgroup_select_dst = 'NAME'

        Mod.use_edge_data = True
        Mod.data_types_edges = {'SEAM'}#
        Mod.edge_mapping = 'VERT_NEAREST'
        Mod.use_loop_data = True
        Mod.data_types_loops = {'VCOL'}#
        Mod.loop_mapping = 'NEAREST_NORMAL'
        Mod.layers_vcol_select_src = 'ALL'
        Mod.layers_vcol_select_dst = 'NAME'
        Mod.layers_uv_select_src = 'ALL'
        Mod.layers_uv_select_dst = 'NAME'
        Mod.islands_precision = 0.51

        Mod.use_poly_data = True
        Mod.data_types_polys = {'SMOOTH'}#
        Mod.poly_mapping = 'NEAREST'
        Mod.use_max_distance = False
        Mod.max_distance = 1.41
        Mod.ray_radius = 0.24
        '''

    elif Mod.type == 'MESH_CACHE':
        parameter = 13
        ModInputList=str(parameter)+'|'+\
                    str(Mod.cache_format)+'|'+\
                    str(Mod.filepath)+'|'+\
                    str(Mod.factor)+'|'+\
                    str(Mod.deform_mode)+'|'+\
                    str(Mod.interpolation)+'|'+\
                    str(Mod.time_mode)+'|'+\
                    str(Mod.play_mode)+'|'+\
                    str(Mod.frame_start)+'|'+\
                    str(Mod.frame_scale)+'|'+\
                    str(Mod.eval_frame)+'|'+\
                    str(Mod.forward_axis)+'|'+\
                    str(Mod.up_axis)+'|'+\
                    str(Mod.flip_axis)


        '''
        Mod.cache_format = 'MDD'
        Mod.filepath = "//..\\..\\..\\"
        Mod.factor = 0.880531
        Mod.deform_mode = 'OVERWRITE'
        Mod.interpolation = 'LINEAR'
        Mod.time_mode = 'FRAME'
        Mod.play_mode = 'SCENE'
        Mod.frame_start = 2.3
        Mod.frame_scale = 3.2
        Mod.eval_frame = 3.1
        Mod.forward_axis = 'POS_Y'
        Mod.up_axis = 'POS_X'
        Mod.flip_axis = {'X', 'Y', 'Z'}##
        '''


    elif Mod.type == 'MESH_SEQUENCE_CACHE':
        parameter = 1
        ModInputList=str(parameter)+'|'+\
                    str(Mod.read_data)

        #bpy.data.cache_files["ttest.abc"].name = "ttest.abc"
        #bpy.data.cache_files["ttest.abc"].is_sequence = True
        #bpy.data.cache_files["ttest.abc"].override_frame = True
        #bpy.data.cache_files["ttest.abc"].frame = 0
        #bpy.data.cache_files["ttest.abc"].frame_offset = 1.2
        #        Mod.object_path = ""
        #Mod.read_data = {'VERT', 'POLY', 'UV', 'COLOR'}####

    elif Mod.type == 'NORMAL_EDIT':
        parameter = 11
        ModInputList=str(parameter)+'|'+\
                    str(Mod.mode)+'|'+\
                    str("bpy.data.objects['"+Mod.target.name+"']" if Mod.target != None else Mod.target)+'|'+\
                    str(Mod.use_direction_parallel)+'|'+\
                    str(Mod.mix_mode)+'|'+\
                    str(Mod.mix_factor)+'|'+\
                    str(Mod.vertex_group)+'|'+\
                    str(Mod.invert_vertex_group)+'|'+\
                    str(Mod.mix_limit)+'|'+\
                    str(Mod.offset[0])+'|'+\
                    str(Mod.offset[1])+'|'+\
                    str(Mod.offset[2])
        '''
        Mod.mode = 'RADIAL'
        Mod.target = bpy.data.objects["Cone"]
        Mod.use_direction_parallel = True
        Mod.mix_mode = 'ADD'
        Mod.mix_factor = 0.92
        Mod.vertex_group = "Group"
        Mod.invert_vertex_group = False
        Mod.mix_limit = 3.1395
        Mod.offset[0] = 0.42
        Mod.offset[1] = 0.51
        Mod.offset[2] = 0.37
        '''

    elif Mod.type == 'WEIGHTED_NORMAL':
        parameter = 7
        ModInputList=str(parameter)+'|'+\
                    str(Mod.mode)+'|'+\
                    str(Mod.weight)+'|'+\
                    str(Mod.thresh)+'|'+\
                    str(Mod.keep_sharp)+'|'+\
                    str(Mod.face_influence)+'|'+\
                    str(Mod.vertex_group)+'|'+\
                    str(Mod.invert_vertex_group)

        '''
        Mod.mode = 'CORNER_ANGLE'
        Mod.weight = 48
        Mod.thresh = 0.01
        Mod.keep_sharp = True
        Mod.face_influence = True
        Mod.vertex_group = "Group"
        Mod.invert_vertex_group = True
        '''

    elif Mod.type == 'UV_PROJECT':
        parameter = 6
        ModInputList=str(parameter)+'|'+\
                    str(Mod.uv_layer)+'|'+\
                    str(Mod.aspect_x)+'|'+\
                    str(Mod.aspect_y)+'|'+\
                    str(Mod.scale_x)+'|'+\
                    str(Mod.scale_y)+'|'+\
                    str(Mod.projector_count)

        '''
        Mod.uv_layer = "UVMap"
        Mod.aspect_x = 1.21
        Mod.aspect_y = 1.12
        Mod.scale_x = 1.04
        Mod.scale_y = 1.22
        Mod.projector_count = 2#
        '''

    elif Mod.type == 'UV_WARP':
        parameter = 14
        ModInputList=str(parameter)+'|'+\
                    str(Mod.uv_layer)+'|'+\
                    str(Mod.center[0])+'|'+\
                    str(Mod.center[1])+'|'+\
                    str(Mod.axis_u)+'|'+\
                    str(Mod.axis_v)+'|'+\
                    str("bpy.data.objects['"+Mod.object_from.name+"']" if Mod.object_from != None else Mod.object_from)+'|'+\
                    str("bpy.data.objects['"+Mod.object_to.name+"']" if Mod.object_to != None else Mod.object_to)+'|'+\
                    str(Mod.vertex_group)+'|'+\
                    str(Mod.invert_vertex_group)+'|'+\
                    str(Mod.offset[0])+'|'+\
                    str(Mod.offset[1])+'|'+\
                    str(Mod.scale[0])+'|'+\
                    str(Mod.scale[1])+'|'+\
                    str(Mod.rotation)

        '''
        Mod.uv_layer = "UVMap"
        Mod.center[0] = 0.5
        Mod.center[1] = 0.5
        Mod.axis_u = 'X'
        Mod.axis_v = 'X'
        Mod.object_from = bpy.data.objects["Cone"]
        Mod.object_to = bpy.data.objects["Cube"]
        Mod.vertex_group = "Group"
        Mod.invert_vertex_group = True
        Mod.offset[0] = 1.4
        Mod.offset[1] = 1.6
        Mod.scale[0] = 1.5
        Mod.scale[1] = 1.4
        Mod.rotation = 0
        '''

    elif Mod.type == 'VERTEX_WEIGHT_EDIT':
        parameter = 16
        ModInputList=str(parameter)+'|'+\
                    str(Mod.vertex_group)+'|'+\
                    str(Mod.default_weight)+'|'+\
                    str(Mod.use_add)+'|'+\
                    str(Mod.add_threshold)+'|'+\
                    str(Mod.use_remove)+'|'+\
                    str(Mod.remove_threshold)+'|'+\
                    str(Mod.normalize)+'|'+\
                    str(Mod.falloff_type)+'|'+\
                    str(Mod.invert_falloff)+'|'+\
                    str(Mod.mask_constant)+'|'+\
                    str(Mod.mask_vertex_group)+'|'+\
                    str(Mod.invert_mask_vertex_group)+'|'+\
                    str(Mod.mask_tex_use_channel)+'|'+\
                    str(Mod.mask_tex_mapping)+'|'+\
                    str("bpy.data.objects['"+Mod.mask_tex_map_object.name+"']" if Mod.mask_tex_map_object != None else Mod.mask_tex_map_object)+'|'+\
                    str(Mod.mask_tex_uv_layer)

        '''
        Mod.vertex_group = "Group"
        Mod.default_weight = 0.0705882
        Mod.use_add = False
        Mod.add_threshold = 0.0575
        Mod.use_remove = False
        Mod.remove_threshold = 0.0475
        Mod.normalize = False
        Mod.falloff_type = 'LINEAR'
        Mod.invert_falloff = True
        Mod.mask_constant = 0.898823
        Mod.mask_vertex_group = "Group"
        Mod.invert_mask_vertex_group = True
                            str("bpy.data.textures['"+Mod.texture.name+"']" if Mod.texture != None else Mod.texture)+'|'+\#Tex.name = "Texture"
        Mod.mask_tex_use_channel = 'RED'
        Mod.mask_tex_mapping = 'OBJECT'
        Mod.mask_tex_map_object = bpy.data.objects["Cone"]
        Mod.mask_tex_uv_layer = "UVMap"
        '''

    elif Mod.type == 'VERTEX_WEIGHT_MIX':
        parameter = 15
        ModInputList=str(parameter)+'|'+\
                    str(Mod.vertex_group_a)+'|'+\
                    str(Mod.vertex_group_b)+'|'+\
                    str(Mod.default_weight_a)+'|'+\
                    str(Mod.default_weight_b)+'|'+\
                    str(Mod.mix_set)+'|'+\
                    str(Mod.mix_mode)+'|'+\
                    str(Mod.normalize)+'|'+\
                    str(Mod.mask_constant)+'|'+\
                    str(Mod.mask_vertex_group)+'|'+\
                    str(Mod.invert_mask_vertex_group)+'|'+\
                    str(Mod.mask_tex_use_channel)+'|'+\
                    str(Mod.mask_tex_mapping)+'|'+\
                    str("bpy.data.objects['"+Mod.mask_tex_map_object.name+"']" if Mod.mask_tex_map_object != None else Mod.mask_tex_map_object)+'|'+\
                    str(Mod.mask_tex_uv_layer)

        '''
        Mod.vertex_group_a = "Group"
        Mod.vertex_group_b = "Group"
        Mod.default_weight_a = 0.0211765
        Mod.default_weight_b = 0.0517647
        Mod.mix_set = 'ALL'
        Mod.mix_mode = 'ADD'
        Mod.normalize = True
        Mod.mask_constant = 0.889412
        Mod.mask_vertex_group = "Group"
        Mod.invert_mask_vertex_group = True
        Mod.mask_tex_use_channel = 'ALPHA'
        Mod.mask_tex_mapping = 'OBJECT'
        Mod.mask_tex_map_object = bpy.data.objects["Cone"] str("bpy.data.objects['"+Mod.mask_tex_map_object.name+"']" if Mod.mask_tex_map_object != None else Mod.mask_tex_map_object)+'|'+\
        Mod.mask_tex_uv_layer = "UVMap"
        '''

    elif Mod.type == 'VERTEX_WEIGHT_PROXIMITY':
        parameter = 16
        ModInputList=str(parameter)+'|'+\
                    str(Mod.vertex_group)+'|'+\
                    str("bpy.data.objects['"+Mod.target.name+"']" if Mod.target != None else Mod.target)+'|'+\
                    str(Mod.proximity_mode)+'|'+\
                    str(Mod.proximity_geometry)+'|'+\
                    str(Mod.min_dist)+'|'+\
                    str(Mod.max_dist)+'|'+\
                    str(Mod.normalize)+'|'+\
                    str(Mod.falloff_type)+'|'+\
                    str(Mod.invert_falloff)+'|'+\
                    str(Mod.mask_constant)+'|'+\
                    str(Mod.mask_vertex_group)+'|'+\
                    str(Mod.invert_mask_vertex_group)+'|'+\
                    str(Mod.mask_tex_use_channel)+'|'+\
                    str(Mod.mask_tex_mapping)+'|'+\
                    str("bpy.data.objects['"+Mod.mask_tex_map_object.name+"']" if Mod.mask_tex_map_object != None else Mod.mask_tex_map_object)+'|'+\
                    str(Mod.mask_tex_uv_layer)


        '''
        Mod.vertex_group = "Group"
        Mod.target = bpy.data.objects["Cone"]
        Mod.proximity_mode = 'GEOMETRY'
        Mod.proximity_geometry = {'VERTEX', 'EDGE', 'FACE'}
        Mod.min_dist = 2.4
        Mod.max_dist = 4.2
        Mod.normalize = True
        Mod.falloff_type = 'SHARP'
        Mod.invert_falloff = True
        Mod.mask_constant = 0.835294
        Mod.mask_vertex_group = "Group"
        Mod.invert_mask_vertex_group = False
        Mod.mask_tex_use_channel = 'ALPHA'
        Mod.mask_tex_mapping = 'OBJECT'
        Mod.mask_tex_map_object = bpy.data.objects["Cone"]# str("bpy.data.objects['"+Mod.mask_tex_map_object.name+"']" if Mod.mask_tex_map_object != None else Mod.mask_tex_map_object)+'|'+\
        Mod.mask_tex_uv_layer = "UVMap"#
        '''

    elif Mod.type == 'VOLUME_TO_MESH':
        parameter = 8
        ModInputList=str(parameter)+'|'+\
                    str("bpy.data.objects['"+Mod.object.name+"']" if Mod.object != None else Mod.object)+'|'+\
                    str(Mod.grid_name)+'|'+\
                    str(Mod.resolution_mode)+'|'+\
                    str(Mod.threshold)+'|'+\
                    str(Mod.adaptivity)+'|'+\
                    str(Mod.use_smooth_shade)+'|'+\
                    str(Mod.voxel_amount)+'|'+\
                    str(Mod.voxel_size)

        '''
        Mod.object = bpy.data.objects["Camera"]
        Mod.grid_name = "density"
        Mod.resolution_mode = 'GRID'
        Mod.threshold = 0.1
        Mod.adaptivity = 0.7
        Mod.use_smooth_shade = True
        Mod.voxel_amount = 32
        Mod.voxel_size = 0.1006
        '''


    elif Mod.type == 'NODES':
        parameter = 2
        ModInputList=str(parameter)+'|'+\
                    str(Mod.node_group.name)+'|'+\
                    str(Mod.node_group.use_fake_user)



        #str(Mod.node_group=bpy.data.node_groups['GeometryNodes']

        '''
        Mod.node_group.use_fake_user = True
        Mod.node_group.name='GeometryNodes'
        Mod.node_group=bpy.data.node_groups['GeometryNodes'] [Mod.node_group.name] 
        '''


    return ModInputList




#'DATA_TRANSFER', 'MESH_CACHE', 'MESH_SEQUENCE_CACHE', 'NORMAL_EDIT', 'WEIGHTED_NORMAL', 'UV_PROJECT', 'UV_WARP', 'VERTEX_WEIGHT_EDIT', 
# 'VERTEX_WEIGHT_MIX', 'VERTEX_WEIGHT_PROXIMITY', 'ARRAY', 'BEVEL', 'BOOLEAN', 'BUILD', 'DECIMATE', 'EDGE_SPLIT', 'MASK', 'MIRROR', 
# 'MULTIRES', 'REMESH', 'SCREW', 'SKIN', 'SOLIDIFY', 'SUBSURF', 'TRIANGULATE', 'WELD', 'WIREFRAME', 'ARMATURE', 'CAST', 'CURVE', 
# 'DISPLACE', 'HOOK', 'LAPLACIANDEFORM', 'LATTICE', 'MESH_DEFORM', 'SHRINKWRAP', 'SIMPLE_DEFORM', 'SMOOTH', 'CORRECTIVE_SMOOTH', 
# 'LAPLACIANSMOOTH', 'SURFACE_DEFORM', 'WARP', 'WAVE', 'CLOTH', 'COLLISION', 'DYNAMIC_PAINT', 'EXPLODE', 'FLUID', 'OCEAN', 
# 'PARTICLE_INSTANCE', 'PARTICLE_SYSTEM', 'SOFT_BODY', 'SURFACE', 'SIMULATION'


def TexInput(tex):
    Tex = tex
    TexInputList=''
    if Tex.type == 'BLEND':
        TexInputList=str(Tex.name)+'|'+str(Tex.type)+'|'+\
                    str(Tex.progression)+'|'+\
                    str(Tex.use_flip_axis)+'|'+\
                    str(Tex.use_clamp)+'|'+\
                    str(Tex.factor_red)+'|'+\
                    str(Tex.factor_green)+'|'+\
                    str(Tex.factor_blue)+'|'+\
                    str(Tex.intensity)+'|'+\
                    str(Tex.contrast)+'|'+\
                    str(Tex.saturation)+'|'+\
                    str(Tex.use_color_ramp)+'|'
        if Tex.use_color_ramp ==True:
            TexInputList+=str(Tex.color_ramp.elements[0].position)+'|'+\
                    str(Tex.color_ramp.elements[1].position)+'|'+\
                    str(Tex.color_ramp.elements[0].color[0])+'|'+\
                    str(Tex.color_ramp.elements[0].color[1])+'|'+\
                    str(Tex.color_ramp.elements[0].color[2])+'|'+\
                    str(Tex.color_ramp.elements[0].color[3])+'|'+\
                    str(Tex.color_ramp.elements[1].color[0])+'|'+\
                    str(Tex.color_ramp.elements[1].color[1])+'|'+\
                    str(Tex.color_ramp.elements[1].color[2])+'|'+\
                    str(Tex.color_ramp.elements[1].color[3])

        '''
        #Tex.progression = 'LINEAR'
        #Tex.use_flip_axis = 'HORIZONTAL'

        Tex.use_clamp = True
        Tex.factor_red = 1.13
        Tex.factor_green = 1.68
        Tex.factor_blue = 1.48
        Tex.intensity = 1.43
        Tex.contrast = 1.29
        Tex.saturation = 1.17
        Tex.use_color_ramp = True
        Tex.color_ramp.elements[1].position = 0.610312
        Tex.color_ramp.elements[0].position = 0.104746
        Tex.color_ramp.elements[0].color = (0.574733, 0.761052, 0.827123, 0.316092)
        Tex.color_ramp.elements[1].color = (0.948978, 0.276352, 1, 1)
        '''


    elif Tex.type == 'CLOUDS':
        TexInputList=str(Tex.name)+'|'+str(Tex.type)+'|'+\
                    str(Tex.noise_basis)+'|'+\
                    str(Tex.noise_type)+'|'+\
                    str(Tex.noise_scale)+'|'+\
                    str(Tex.noise_depth)+'|'+\
                    str(Tex.nabla)+'|'+\
                    str(Tex.cloud_type)+'|'+\
                    str(Tex.use_clamp)+'|'+\
                    str(Tex.factor_red)+'|'+\
                    str(Tex.factor_green)+'|'+\
                    str(Tex.factor_blue)+'|'+\
                    str(Tex.intensity)+'|'+\
                    str(Tex.contrast)+'|'+\
                    str(Tex.saturation)+'|'+\
                    str(Tex.use_color_ramp)+'|'
        if Tex.use_color_ramp ==True:
            TexInputList+=str(Tex.color_ramp.elements[0].position)+'|'+\
                    str(Tex.color_ramp.elements[1].position)+'|'+\
                    str(Tex.color_ramp.elements[0].color[0])+'|'+\
                    str(Tex.color_ramp.elements[0].color[1])+'|'+\
                    str(Tex.color_ramp.elements[0].color[2])+'|'+\
                    str(Tex.color_ramp.elements[0].color[3])+'|'+\
                    str(Tex.color_ramp.elements[1].color[0])+'|'+\
                    str(Tex.color_ramp.elements[1].color[1])+'|'+\
                    str(Tex.color_ramp.elements[1].color[2])+'|'+\
                    str(Tex.color_ramp.elements[1].color[3])

        '''
        Tex.noise_basis = 'BLENDER_ORIGINAL'
        Tex.noise_type = 'SOFT_NOISE'
        Tex.noise_scale = 1.72
        Tex.noise_depth = 2
        Tex.nabla = 0.05
        Tex.cloud_type = 'GRAYSCALE'
        '''

    elif Tex.type == 'DISTORTED_NOISE':
        TexInputList=str(Tex.name)+'|'+str(Tex.type)+'|'+\
                    str(Tex.noise_basis)+'|'+\
                    str(Tex.noise_distortion)+'|'+\
                    str(Tex.distortion)+'|'+\
                    str(Tex.noise_scale)+'|'+\
                    str(Tex.nabla)+'|'+\
                    str(Tex.use_clamp)+'|'+\
                    str(Tex.factor_red)+'|'+\
                    str(Tex.factor_green)+'|'+\
                    str(Tex.factor_blue)+'|'+\
                    str(Tex.intensity)+'|'+\
                    str(Tex.contrast)+'|'+\
                    str(Tex.saturation)+'|'+\
                    str(Tex.use_color_ramp)+'|'
        if Tex.use_color_ramp ==True:
            TexInputList+=str(Tex.color_ramp.elements[0].position)+'|'+\
                    str(Tex.color_ramp.elements[1].position)+'|'+\
                    str(Tex.color_ramp.elements[0].color[0])+'|'+\
                    str(Tex.color_ramp.elements[0].color[1])+'|'+\
                    str(Tex.color_ramp.elements[0].color[2])+'|'+\
                    str(Tex.color_ramp.elements[0].color[3])+'|'+\
                    str(Tex.color_ramp.elements[1].color[0])+'|'+\
                    str(Tex.color_ramp.elements[1].color[1])+'|'+\
                    str(Tex.color_ramp.elements[1].color[2])+'|'+\
                    str(Tex.color_ramp.elements[1].color[3])



        '''
        Tex.noise_basis = 'IMPROVED_PERLIN'
        Tex.noise_distortion = 'ORIGINAL_PERLIN'
        Tex.distortion = 5.9
        Tex.noise_scale = 1.89
        Tex.nabla = 0.05
        '''

    elif Tex.type == 'IMAGE':
        TexInputList=str(Tex.name)+'|'+str(Tex.type)+'|'+\
                    str(Tex.use_alpha)+'|'+\
                    str(Tex.use_calculate_alpha)+'|'+\
                    str(Tex.invert_alpha)+'|'+\
                    str(Tex.use_flip_axis)+'|'+\
                    str(Tex.extension)+'|'+\
                    str(Tex.crop_min_x)+'|'+\
                    str(Tex.crop_min_y)+'|'+\
                    str(Tex.crop_max_x)+'|'+\
                    str(Tex.crop_max_y)+'|'+\
                    str(Tex.repeat_x)+'|'+\
                    str(Tex.repeat_y)+'|'+\
                    str(Tex.use_mirror_x)+'|'+\
                    str(Tex.use_mirror_y)+'|'+\
                    str(Tex.extension)+'|'+\
                    str(Tex.checker_distance)+'|'+\
                    str(Tex.use_checker_even)+'|'+\
                    str(Tex.use_checker_odd)+'|'+\
                    str(Tex.use_clamp)+'|'+\
                    str(Tex.factor_red)+'|'+\
                    str(Tex.factor_green)+'|'+\
                    str(Tex.factor_blue)+'|'+\
                    str(Tex.intensity)+'|'+\
                    str(Tex.contrast)+'|'+\
                    str(Tex.saturation)+'|'+\
                    str(Tex.use_color_ramp)+'|'
        if Tex.use_color_ramp ==True:
            TexInputList+=str(Tex.color_ramp.elements[0].position)+'|'+\
                    str(Tex.color_ramp.elements[1].position)+'|'+\
                    str(Tex.color_ramp.elements[0].color[0])+'|'+\
                    str(Tex.color_ramp.elements[0].color[1])+'|'+\
                    str(Tex.color_ramp.elements[0].color[2])+'|'+\
                    str(Tex.color_ramp.elements[0].color[3])+'|'+\
                    str(Tex.color_ramp.elements[1].color[0])+'|'+\
                    str(Tex.color_ramp.elements[1].color[1])+'|'+\
                    str(Tex.color_ramp.elements[1].color[2])+'|'+\
                    str(Tex.color_ramp.elements[1].color[3])

        '''
        Tex.type = 'IMAGE'
        Tex.use_alpha = False
        Tex.use_calculate_alpha = True
        Tex.invert_alpha = True
        Tex.use_flip_axis = True
        Tex.extension = 'EXTEND'
        Tex.crop_min_x = 0.29
        Tex.crop_min_y = 0.25
        Tex.crop_max_x = 0.87
        Tex.crop_max_y = 0.87
        Tex.repeat_x = 3
        Tex.repeat_y = 3
        Tex.use_mirror_x = False
        Tex.use_mirror_y = False
        Tex.extension = 'CHECKER'
        Tex.checker_distance = 0.032
        Tex.use_checker_even = True
        Tex.use_checker_odd = False
        '''

    elif Tex.type == 'MAGIC':
        TexInputList=str(Tex.name)+'|'+str(Tex.type)+'|'+\
                    str(Tex.noise_depth)+'|'+\
                    str(Tex.turbulence)+'|'+\
                    str(Tex.use_clamp)+'|'+\
                    str(Tex.factor_red)+'|'+\
                    str(Tex.factor_green)+'|'+\
                    str(Tex.factor_blue)+'|'+\
                    str(Tex.intensity)+'|'+\
                    str(Tex.contrast)+'|'+\
                    str(Tex.saturation)+'|'+\
                    str(Tex.use_color_ramp)+'|'
        if Tex.use_color_ramp ==True:
            TexInputList+=str(Tex.color_ramp.elements[0].position)+'|'+\
                    str(Tex.color_ramp.elements[1].position)+'|'+\
                    str(Tex.color_ramp.elements[0].color[0])+'|'+\
                    str(Tex.color_ramp.elements[0].color[1])+'|'+\
                    str(Tex.color_ramp.elements[0].color[2])+'|'+\
                    str(Tex.color_ramp.elements[0].color[3])+'|'+\
                    str(Tex.color_ramp.elements[1].color[0])+'|'+\
                    str(Tex.color_ramp.elements[1].color[1])+'|'+\
                    str(Tex.color_ramp.elements[1].color[2])+'|'+\
                    str(Tex.color_ramp.elements[1].color[3])

        '''
        Tex.type = 'MAGIC'
        Tex.noise_depth = 3
        Tex.turbulence = 5.1
        '''

    elif Tex.type == 'MARBLE':
        TexInputList=str(Tex.name)+'|'+str(Tex.type)+'|'+\
                    str(Tex.noise_basis)+'|'+\
                    str(Tex.marble_type)+'|'+\
                    str(Tex.noise_basis_2)+'|'+\
                    str(Tex.noise_type)+'|'+\
                    str(Tex.noise_scale)+'|'+\
                    str(Tex.noise_depth)+'|'+\
                    str(Tex.turbulence)+'|'+\
                    str(Tex.nabla)+'|'+\
                    str(Tex.use_clamp)+'|'+\
                    str(Tex.factor_red)+'|'+\
                    str(Tex.factor_green)+'|'+\
                    str(Tex.factor_blue)+'|'+\
                    str(Tex.intensity)+'|'+\
                    str(Tex.contrast)+'|'+\
                    str(Tex.saturation)+'|'+\
                    str(Tex.use_color_ramp)+'|'
        if Tex.use_color_ramp ==True:
            TexInputList+=str(Tex.color_ramp.elements[0].position)+'|'+\
                    str(Tex.color_ramp.elements[1].position)+'|'+\
                    str(Tex.color_ramp.elements[0].color[0])+'|'+\
                    str(Tex.color_ramp.elements[0].color[1])+'|'+\
                    str(Tex.color_ramp.elements[0].color[2])+'|'+\
                    str(Tex.color_ramp.elements[0].color[3])+'|'+\
                    str(Tex.color_ramp.elements[1].color[0])+'|'+\
                    str(Tex.color_ramp.elements[1].color[1])+'|'+\
                    str(Tex.color_ramp.elements[1].color[2])+'|'+\
                    str(Tex.color_ramp.elements[1].color[3])


        '''
        Tex.type = 'MARBLE'
        Tex.noise_basis = 'IMPROVED_PERLIN'
        Tex.marble_type = 'SHARP'
        Tex.noise_basis_2 = 'SAW'
        Tex.noise_type = 'SOFT_NOISE'
        Tex.noise_scale = 1.89
        Tex.noise_depth = 3
        Tex.turbulence = 5.1
        Tex.nabla = 0.05
        '''

    elif Tex.type == 'MUSGRAVE':
        TexInputList=str(Tex.name)+'|'+str(Tex.type)+'|'+\
                    str(Tex.noise_basis)+'|'+\
                    str(Tex.musgrave_type)+'|'+\
                    str(Tex.noise_scale)+'|'+\
                    str(Tex.nabla)+'|'+\
                    str(Tex.dimension_max)+'|'+\
                    str(Tex.lacunarity)+'|'+\
                    str(Tex.octaves)+'|'+\
                    str(Tex.offset)+'|'+\
                    str(Tex.noise_intensity)+'|'+\
                    str(Tex.gain)+'|'+\
                    str(Tex.use_clamp)+'|'+\
                    str(Tex.factor_red)+'|'+\
                    str(Tex.factor_green)+'|'+\
                    str(Tex.factor_blue)+'|'+\
                    str(Tex.intensity)+'|'+\
                    str(Tex.contrast)+'|'+\
                    str(Tex.saturation)+'|'+\
                    str(Tex.use_color_ramp)+'|'
        if Tex.use_color_ramp ==True:
            TexInputList+=str(Tex.color_ramp.elements[0].position)+'|'+\
                    str(Tex.color_ramp.elements[1].position)+'|'+\
                    str(Tex.color_ramp.elements[0].color[0])+'|'+\
                    str(Tex.color_ramp.elements[0].color[1])+'|'+\
                    str(Tex.color_ramp.elements[0].color[2])+'|'+\
                    str(Tex.color_ramp.elements[0].color[3])+'|'+\
                    str(Tex.color_ramp.elements[1].color[0])+'|'+\
                    str(Tex.color_ramp.elements[1].color[1])+'|'+\
                    str(Tex.color_ramp.elements[1].color[2])+'|'+\
                    str(Tex.color_ramp.elements[1].color[3])

        '''
        Tex.type = 'MUSGRAVE'
        Tex.noise_basis = 'CELL_NOISE'
        Tex.musgrave_type = 'MULTIFRACTAL'
        Tex.noise_scale = 0.36
        Tex.nabla = 0.01
        Tex.dimension_max = 1.11
        Tex.lacunarity = 2.13
        Tex.octaves = 2.22
        Tex.offset = 1.29#
        Tex.noise_intensity = 1.38
        Tex.gain = 1.15#
        '''


    elif Tex.type == 'NOISE':
        TexInputList=str(Tex.name)+'|'+str(Tex.type)+'|'+\
                    str(Tex.use_clamp)+'|'+\
                    str(Tex.factor_red)+'|'+\
                    str(Tex.factor_green)+'|'+\
                    str(Tex.factor_blue)+'|'+\
                    str(Tex.intensity)+'|'+\
                    str(Tex.contrast)+'|'+\
                    str(Tex.saturation)+'|'+\
                    str(Tex.use_color_ramp)+'|'
        if Tex.use_color_ramp ==True:
            TexInputList+=str(Tex.color_ramp.elements[0].position)+'|'+\
                    str(Tex.color_ramp.elements[1].position)+'|'+\
                    str(Tex.color_ramp.elements[0].color[0])+'|'+\
                    str(Tex.color_ramp.elements[0].color[1])+'|'+\
                    str(Tex.color_ramp.elements[0].color[2])+'|'+\
                    str(Tex.color_ramp.elements[0].color[3])+'|'+\
                    str(Tex.color_ramp.elements[1].color[0])+'|'+\
                    str(Tex.color_ramp.elements[1].color[1])+'|'+\
                    str(Tex.color_ramp.elements[1].color[2])+'|'+\
                    str(Tex.color_ramp.elements[1].color[3])

        '''
        Tex.type = 'NOISE' #
        '''

    elif Tex.type == 'STUCCI':
        TexInputList=str(Tex.name)+'|'+str(Tex.type)+'|'+\
                    str(Tex.noise_basis)+'|'+\
                    str(Tex.stucci_type)+'|'+\
                    str(Tex.noise_type)+'|'+\
                    str(Tex.noise_scale)+'|'+\
                    str(Tex.turbulence)+'|'+\
                    str(Tex.use_clamp)+'|'+\
                    str(Tex.factor_red)+'|'+\
                    str(Tex.factor_green)+'|'+\
                    str(Tex.factor_blue)+'|'+\
                    str(Tex.intensity)+'|'+\
                    str(Tex.contrast)+'|'+\
                    str(Tex.saturation)+'|'+\
                    str(Tex.use_color_ramp)+'|'
        if Tex.use_color_ramp ==True:
            TexInputList+=str(Tex.color_ramp.elements[0].position)+'|'+\
                    str(Tex.color_ramp.elements[1].position)+'|'+\
                    str(Tex.color_ramp.elements[0].color[0])+'|'+\
                    str(Tex.color_ramp.elements[0].color[1])+'|'+\
                    str(Tex.color_ramp.elements[0].color[2])+'|'+\
                    str(Tex.color_ramp.elements[0].color[3])+'|'+\
                    str(Tex.color_ramp.elements[1].color[0])+'|'+\
                    str(Tex.color_ramp.elements[1].color[1])+'|'+\
                    str(Tex.color_ramp.elements[1].color[2])+'|'+\
                    str(Tex.color_ramp.elements[1].color[3])

        '''
        Tex.type = 'STUCCI'
        Tex.noise_basis = 'ORIGINAL_PERLIN'
        Tex.stucci_type = 'WALL_IN'
        Tex.noise_type = 'SOFT_NOISE'
        Tex.noise_scale = 0.36
        Tex.turbulence = 5.1
        '''

    elif Tex.type == 'VORONOI':
        TexInputList=str(Tex.name)+'|'+str(Tex.type)+'|'+\
                    str(Tex.distance_metric)+'|'+\
                    str(Tex.minkovsky_exponent)+'|'+\
                    str(Tex.color_mode)+'|'+\
                    str(Tex.noise_intensity)+'|'+\
                    str(Tex.noise_scale)+'|'+\
                    str(Tex.nabla)+'|'+\
                    str(Tex.weight_1)+'|'+\
                    str(Tex.weight_2)+'|'+\
                    str(Tex.weight_3)+'|'+\
                    str(Tex.weight_4)+'|'+\
                    str(Tex.use_clamp)+'|'+\
                    str(Tex.factor_red)+'|'+\
                    str(Tex.factor_green)+'|'+\
                    str(Tex.factor_blue)+'|'+\
                    str(Tex.intensity)+'|'+\
                    str(Tex.contrast)+'|'+\
                    str(Tex.saturation)+'|'+\
                    str(Tex.use_color_ramp)+'|'
        if Tex.use_color_ramp ==True:
            TexInputList+=str(Tex.color_ramp.elements[0].position)+'|'+\
                    str(Tex.color_ramp.elements[1].position)+'|'+\
                    str(Tex.color_ramp.elements[0].color[0])+'|'+\
                    str(Tex.color_ramp.elements[0].color[1])+'|'+\
                    str(Tex.color_ramp.elements[0].color[2])+'|'+\
                    str(Tex.color_ramp.elements[0].color[3])+'|'+\
                    str(Tex.color_ramp.elements[1].color[0])+'|'+\
                    str(Tex.color_ramp.elements[1].color[1])+'|'+\
                    str(Tex.color_ramp.elements[1].color[2])+'|'+\
                    str(Tex.color_ramp.elements[1].color[3])

        '''
        Tex.type = 'VORONOI'
        Tex.distance_metric = 'DISTANCE_SQUARED'
        Tex.minkovsky_exponent = 7.1
        Tex.color_mode = 'POSITION'
        Tex.noise_intensity = 2.21
        Tex.noise_scale = 0.84
        Tex.nabla = 0.1
        Tex.weight_1 = -0.475728
        Tex.weight_2 = -0.297734
        Tex.weight_3 = 0.478964
        Tex.weight_4 = 1.02265
        '''

    elif Tex.type == 'WOOD':
        TexInputList=str(Tex.name)+'|'+str(Tex.type)+'|'+\
                    str(Tex.noise_basis)+'|'+\
                    str(Tex.wood_type)+'|'+\
                    str(Tex.noise_basis_2)+'|'+\
                    str(Tex.noise_type)+'|'+\
                    str(Tex.noise_scale)+'|'+\
                    str(Tex.turbulence)+'|'+\
                    str(Tex.nabla)+'|'+\
                    str(Tex.use_clamp)+'|'+\
                    str(Tex.factor_red)+'|'+\
                    str(Tex.factor_green)+'|'+\
                    str(Tex.factor_blue)+'|'+\
                    str(Tex.intensity)+'|'+\
                    str(Tex.contrast)+'|'+\
                    str(Tex.saturation)+'|'+\
                    str(Tex.use_color_ramp)+'|'
        if Tex.use_color_ramp ==True:
            TexInputList+=str(Tex.color_ramp.elements[0].position)+'|'+\
                    str(Tex.color_ramp.elements[1].position)+'|'+\
                    str(Tex.color_ramp.elements[0].color[0])+'|'+\
                    str(Tex.color_ramp.elements[0].color[1])+'|'+\
                    str(Tex.color_ramp.elements[0].color[2])+'|'+\
                    str(Tex.color_ramp.elements[0].color[3])+'|'+\
                    str(Tex.color_ramp.elements[1].color[0])+'|'+\
                    str(Tex.color_ramp.elements[1].color[1])+'|'+\
                    str(Tex.color_ramp.elements[1].color[2])+'|'+\
                    str(Tex.color_ramp.elements[1].color[3])

        '''
        Tex.type = 'WOOD'
        Tex.noise_basis = 'BLENDER_ORIGINAL'
        Tex.wood_type = 'BANDNOISE'
        Tex.noise_basis_2 = 'SAW'
        Tex.noise_type = 'HARD_NOISE'
        Tex.noise_scale = 0.5
        Tex.turbulence = 6.4
        Tex.nabla = 0.1
        '''

    else:
        TexInputList=str(Tex.name)+'|'+str(Tex.type)

    return TexInputList

#bpy.data.textures.new("NewTexture", type='IMAGE')

#if Tex.type(Parm1)=='MUSGRAVE':
    #Tex.type = 'MUSGRAVE'
    #etc。。
    #Tex.color_ramp.elements[1].color[0]  1 2 3 

def ReNodeType(type):
    Type=type
    if 'COMBXYZ' in Type:
        #NewType=#Type.title()
        #NewType=NewType.replace('_xyz','XYZ')
        NewType='CombineXYZ'
    elif 'COMBRGB' in Type:
        NewType='CombineRGB'
    elif 'SEPXYZ' in Type:
        NewType='SeparateXYZ'
    elif 'SEPRGB' in Type:
        NewType='SeparateRGB'
    elif 'VALTORGB' in Type:
        NewType='ValToRGB'
    elif 'EULER' in Type:
        NewType='RotatePoints'
    elif 'VECT_MATH' in Type:
        NewType='VectorMath'
    #elif Type=='FRAME':
        #NewType='NodeFrame'
    else:
        NewType=Type.title().replace('_','')
        if 'Xyz' in NewType:
            NewType=NewType.replace('Xyz','XYZ')


    if (Type == 'VECT_MATH') or (Type == 'SEPXYZ') or (Type == 'COMBXYZ') or (Type == 'CLAMP') or (Type == 'MATH') or (Type == 'MAP_RANGE') or (Type == 'VALUE') or (Type == 'COMBRGB') or (Type == 'SEPRGB') or (Type == 'VALTORGB'):
        FinalType='ShaderNode'+NewType#ValToRGB
    elif (Type == 'BOOLEAN_MATH') or (Type == 'FLOAT_COMPARE') or (Type == 'RANDOM_FLOAT') or (Type == 'INPUT_VECTOR') or (Type == 'INPUT_STRING'):
        FinalType='FunctionNode'+NewType
    elif (Type == 'FRAME') or (Type == 'REROUTE') or (Type == 'GROUP_OUTPUT') or (Type == 'GROUP_INPUT'):
        FinalType='Node'+NewType
    else:
        FinalType='GeometryNode'+NewType

    return FinalType



def GeoNodeInput(node):
    Node = node
    InputsNum=len(Node.inputs)
    OutPutsNum=len(Node.outputs)

    GeoNodeList=str(Node.name)+'|'+str(ReNodeType(Node.type))+'|'+str(Node.location[0])+'|'+str(Node.location[1])+'|'+str(InputsNum)+'|'+str(OutPutsNum)+'|'
    


    if (Node.type=='ATTRIBUTE_COLOR_RAMP') or (Node.type=='VALTORGB'):
        GeoNodeList+=str(3+len(Node.color_ramp.elements))+'|'+str(Node.color_ramp.color_mode)+'|'+str(Node.color_ramp.interpolation)+'|'+str(Node.color_ramp.hue_interpolation)+'|'

        for elements in Node.color_ramp.elements:
            #elements.color[0]
            #elements.position
            GeoNodeList+=str(elements.position)+'|'+str(elements.color[0])+'|'+str(elements.color[1])+'|'+str(elements.color[2])+'|'+str(elements.color[3])+'|'

        '''
        bpy.data.node_groups['GeometryNodes'].nodes.active.color_ramp.color_mode
        bpy.data.node_groups['GeometryNodes'].nodes.active.color_ramp.interpolation

        bpy.data.node_groups['GeometryNodes'].nodes.active.color_ramp.elements[0].color[0]
        bpy.data.node_groups['GeometryNodes'].nodes.active.color_ramp.elements[0].position
        '''


    elif (Node.type=='ATTRIBUTE_COMPARE') or (Node.type=='ATTRIBUTE_MATH'):
        GeoNodeList+='3|'+str(Node.operation)+'|'+str(Node.input_type_a)+'|'+str(Node.input_type_b)+'|'
        '''
        bpy.data.node_groups["GeometryNodes"].nodes["Attribute Compare"].operation = 'NOT_EQUAL'
        bpy.data.node_groups["GeometryNodes"].nodes["Attribute Compare"].input_type_a = 'FLOAT'
        bpy.data.node_groups["GeometryNodes"].nodes["Attribute Compare"].input_type_b = 'COLOR'
        '''


    elif (Node.type=='ATTRIBUTE_FILL') or (Node.type=='ATTRIBUTE_RANDOMIZE'):
        GeoNodeList+='1|'+str(Node.data_type)+'|'
        #bpy.data.node_groups["GeometryNodes"].nodes["Attribute Fill"].data_type = 'FLOAT_VECTOR'

    elif Node.type=='ATTRIBUTE_MIX':
        GeoNodeList+='4|'+str(Node.blend_type)+'|'+str(Node.input_type_factor)+'|'+str(Node.input_type_a)+'|'+str(Node.input_type_b)+'|'

        '''
        bpy.data.node_groups["GeometryNodes"].nodes["Attribute Mix"].blend_type = 'MIX'
        bpy.data.node_groups["GeometryNodes"].nodes["Attribute Mix"].input_type_factor = 'FLOAT'
        bpy.data.node_groups["GeometryNodes"].nodes["Attribute Mix"].input_type_a = 'FLOAT'
        bpy.data.node_groups["GeometryNodes"].nodes["Attribute Mix"].input_type_b = 'VECTOR'
        '''

    elif Node.type=='ATTRIBUTE_SAMPLE_TEXTURE':# and (bpy.app.version >= (2, 93, 0))
        GeoNodeList+='1|'+str(Node.texture.name)+'|'



    elif Node.type=='ATTRIBUTE_VECTOR_MATH':
        GeoNodeList+='4|'+str(Node.operation)+'|'+str(Node.input_type_a)+'|'+str(Node.input_type_b)+'|'+str(Node.input_type_c)+'|'
        '''
        bpy.data.node_groups["GeometryNodes"].nodes["Attribute Vector Math"].operation = 'SUBTRACT'
        bpy.data.node_groups["GeometryNodes"].nodes["Attribute Vector Math"].input_type_a = 'ATTRIBUTE'
        bpy.data.node_groups["GeometryNodes"].nodes["Attribute Vector Math"].input_type_b = 'VECTOR'
        bpy.data.node_groups["GeometryNodes"].nodes["Attribute Vector Math"].input_type_c = 'VECTOR'
        '''


    elif (Node.type=='COLLECTION_INFO') or (Node.type=='OBJECT_INFO'):
        GeoNodeList+='1|'+str(Node.transform_space)+'|'
        #bpy.data.node_groups["GeometryNodes"].nodes["Collection Info"].transform_space = 'ORIGINAL'


    elif Node.type=='VALUE':
        GeoNodeList+='1|'+str(Node.outputs[0].default_value)+'|'
        #bpy.data.node_groups["GeometryNodes"].nodes["Value"].outputs[0].default_value = 0.5

    elif Node.type=='INPUT_VECTOR':
        GeoNodeList+='3|'+str(Node.vector[0])+'|'+str(Node.vector[1])+'|'+str(Node.vector[2])+'|'

        '''
        bpy.data.node_groups["GeometryNodes"].nodes["Vector"].vector[0] = 0
        bpy.data.node_groups["GeometryNodes"].nodes["Vector"].vector[1] = 0
        bpy.data.node_groups["GeometryNodes"].nodes["Vector"].vector[2] = 0
        '''


    elif (Node.type=='BOOLEAN') or (Node.type=='BOOLEAN_MATH') or (Node.type=='FLOAT_COMPARE') or (Node.type=='VECT_MATH'):
        GeoNodeList+='1|'+str(Node.operation)+'|'
        #bpy.data.node_groups["GeometryNodes"].nodes["Boolean"].operation = 'INTERSECT'

    elif Node.type=='TRIANGULATE':
        GeoNodeList+='2|'+str(Node.quad_method)+'|'+str(Node.ngon_method)+'|'

        #bpy.data.node_groups["GeometryNodes"].nodes["Triangulate"].quad_method = 'FIXED_ALTERNATE'
        #bpy.data.node_groups["GeometryNodes"].nodes["Triangulate"].ngon_method = 'CLIP'

    elif Node.type=='ALIGN_ROTATION_TO_VECTOR':
        GeoNodeList+='3|'+str(Node.axis)+'|'+str(Node.input_type_factor)+'|'+str(Node.input_type_vector)+'|'
        '''
        bpy.data.node_groups["GeometryNodes"].nodes["Align Rotation to Vector"].axis = 'Y'
        bpy.data.node_groups["GeometryNodes"].nodes["Align Rotation to Vector"].input_type_factor = 'ATTRIBUTE'
        bpy.data.node_groups["GeometryNodes"].nodes["Align Rotation to Vector"].input_type_vector = 'VECTOR'
        '''



    elif Node.type=='POINT_DISTRIBUTE':
        GeoNodeList+='1|'+str(Node.distribute_method)+'|'
        #bpy.data.node_groups["GeometryNodes"].nodes["Point Distribute"].distribute_method = 'POISSON'

    elif Node.type=='POINT_INSTANCE':
        GeoNodeList+='1|'+str(Node.instance_type)+'|'
        #bpy.data.node_groups["GeometryNodes"].nodes["Point Instance"].instance_type = 'OBJECT'


    elif Node.type=='EULER':
        GeoNodeList+='3|'+str(Node.type)+'|'+str(Node.space)+'|'+str(Node.input_type_rotation)+'|'
        #bpy.data.node_groups["GeometryNodes"].nodes["Point Rotate"].type = 'EULER'
        #bpy.data.node_groups["GeometryNodes"].nodes["Point Rotate"].space = 'POINT'
        #bpy.data.node_groups["GeometryNodes"].nodes["Point Rotate"].input_type_rotation = 'ATTRIBUTE'


    elif (Node.type=='POINT_SCALE') or (Node.type=='POINT_TRANSLATE'):
        GeoNodeList+='1|'+str(Node.input_type)+'|'
        #bpy.data.node_groups["GeometryNodes"].nodes["Point Scale"].input_type = 'ATTRIBUTE'


    elif Node.type=='POINTS_TO_VOLUME':
        GeoNodeList+='2|'+str(Node.resolution_mode)+'|'+str(Node.input_type_radius)+'|'
        #bpy.data.node_groups["GeometryNodes"].nodes["Points to Volume"].resolution_mode = 'VOXEL_AMOUNT'
        #bpy.data.node_groups["GeometryNodes"].nodes["Points to Volume"].input_type_radius = 'FLOAT'


    elif Node.type=='CLAMP':
        GeoNodeList+='1|'+str(Node.clamp_type)+'|'
        #bpy.data.node_groups["GeometryNodes"].nodes["Clamp"].clamp_type = 'RANGE'


    elif Node.type=='MAP_RANGE':
        GeoNodeList+='1|'+str(Node.interpolation_type)+'|'
        #bpy.data.node_groups["GeometryNodes"].nodes["Map Range"].interpolation_type = 'SMOOTHERSTEP'

    elif Node.type=='MATH':
        GeoNodeList+='2|'+str(Node.operation)+'|'+str(Node.use_clamp)+'|'
        '''
        bpy.data.node_groups["GeometryNodes"].nodes["Math"].operation = 'CEIL'
        bpy.data.node_groups["GeometryNodes"].nodes["Math"].use_clamp = True
        '''

    elif Node.type=='ATTRIBUTE_COMBINE_XYZ':
        GeoNodeList+='3|'+str(Node.input_type_x)+'|'+str(Node.input_type_y)+'|'+str(Node.input_type_z)+'|'

        #bpy.data.node_groups["Nodes"].nodes["Attribute Combine XYZ"].input_type_x = 'ATTRIBUTE'
        #bpy.data.node_groups["Nodes"].nodes["Attribute Combine XYZ"].input_type_y = 'ATTRIBUTE'
        #bpy.data.node_groups["Nodes"].nodes["Attribute Combine XYZ"].input_type_z = 'ATTRIBUTE'


    elif Node.type=='ATTRIBUTE_PROXIMITY':
        GeoNodeList+='1|'+str(Node.target_geometry_element)+'|'

        #bpy.data.node_groups["Nodes"].nodes["Attribute Proximity"].target_geometry_element = 'POINTS'

    elif Node.type=='ATTRIBUTE_SEPARATE_XYZ':
        GeoNodeList+='1|'+str(Node.input_type)+'|'

        #bpy.data.node_groups["Nodes"].nodes["Attribute Separate XYZ"].input_type = 'VECTOR'

    elif Node.type=='INPUT_STRING':
        GeoNodeList+='1|'+str(Node.string)+'|'

        #bpy.data.node_groups["Nodes"].nodes["String"].string = ""

    elif Node.type=='VOLUME_TO_MESH':
        GeoNodeList+='1|'+str(Node.resolution_mode)+'|'

        #bpy.data.node_groups["Nodes"].nodes["Volume to Mesh"].resolution_mode = 'GRID'

    #elif Node.type=='FRAME':
        #GeoNodeList+='9|'+str(Node.label)+'|'+str(Node.use_custom_color)+'|'+str(Node.color[0])+'|'+str(Node.color[1])+'|'+str(Node.color[2])+'|'+str(Node.label_size)+'|'+str(Node.shrink)+'|'+str(Node.height)+'|'+str(Node.width)+'|'
        '''
        bpy.data.node_groups["Nodes"].nodes["Frame"].label = "属性"
        >>> bpy.data.node_groups["Nodes"].nodes["Frame"].use_custom_color = True
        >>> bpy.data.node_groups["Nodes"].nodes["Frame"].color[0] = (0.311498, 0.371446, 0.589418)
        >>> bpy.data.node_groups["Nodes"].nodes["Frame"].label_size = 55
        >>> bpy.data.node_groups["Nodes"].nodes["Frame"].shrink = False
        bpy.data.node_groups['GeometryNodes'].nodes.active.height
        bpy.data.node_groups['GeometryNodes'].nodes.active.width
        '''





    else:
        GeoNodeList+='0|'


    if InputsNum>=1:
        for Input in range(InputsNum):
        #if Node.type == 'GROUP_INPUT':
            if (Node.inputs[Input].type != 'GEOMETRY') and (Node.inputs[Input].type != 'CUSTOM') and (Node.inputs[Input].type != 'VECTOR') and (Node.inputs[Input].type != 'RGBA') and (Node.inputs[Input].type != 'OBJECT') and (Node.inputs[Input].type != 'COLLECTION'):
                GeoNodeList+=str(Node.inputs[Input].default_value)+'|'#str(Node.inputs[Input].type)+'|'+

            elif Node.inputs[Input].type == 'GEOMETRY':
                GeoNodeList+=str(len(Node.inputs[Input].links))+'|'#str(Node.inputs[Input].type)+'|'+

            elif Node.inputs[Input].type == 'VECTOR':
                GeoNodeList+=str(Node.inputs[Input].default_value[0])+'|'+str(Node.inputs[Input].default_value[1])+'|'+str(Node.inputs[Input].default_value[2])+'|'
            
            elif Node.inputs[Input].type == 'RGBA':
                GeoNodeList+=str(Node.inputs[Input].default_value[0])+'|'+str(Node.inputs[Input].default_value[1])+'|'+str(Node.inputs[Input].default_value[2])+'|'+str(Node.inputs[Input].default_value[3])+'|'

            elif (Node.inputs[Input].type == 'OBJECT') or (Node.inputs[Input].type == 'COLLECTION'):
                if Node.inputs[Input].default_value == None:
                    GeoNodeList+='None'+'|'
                else:
                    GeoNodeList+=str(Node.inputs[Input].default_value.name)+'|'#str(Node.inputs[Input].type)+'|'+



    
    if OutPutsNum>=1:
        for OutPut in range(OutPutsNum):
            #总数 以遍历
            #第一个输出节点。。。第n个输出节点
            #各节点的连接数
            
            #GeoNodeList+=str(Node.outputs[OutPut].name)+'|'
            #if Node.outputs[OutPut].type != 'CUSTOM':
            if len(Node.outputs[OutPut].links)>=1:
                GeoNodeList+=str(len(Node.outputs[OutPut].links))+'|'
            else:
                GeoNodeList+='NoLinks|'

        for OutPut in range(OutPutsNum):
            if len(Node.outputs[OutPut].links)>=1:
                for Link in Node.outputs[OutPut].links:
                    if ((Link.to_socket.name == 'Vector') and (Link.to_socket.type == 'VECTOR')) or (Link.to_socket.name == 'Value') or (Link.to_socket.name == 'Boolean'):#针对重名的连接
                        if Link.to_socket.name == Link.to_socket.identifier:
                            GeoNodeList+=str(Link.to_node.name)+'|'+str(Link.to_socket.identifier)+'|'
                        else:
                            GeoNodeList+=str(Link.to_node.name)+'|'+str(Link.to_socket.identifier.split('_00')[1])+'|'
                    else:
                        GeoNodeList+=str(Link.to_node.name)+'|'+str(Link.to_socket.name)+'|'
                    #GeoNodeList+=str(Link.to_socket.name)+'|'

    #if (Node.type!='GROUP_INPUT') and (Node.type!='GROUP_OUTPUT') and (Node.type!='REROUTE') and ('ATTRIBUTE' not in Node.type):
    GeoNodeList+='Node_Label'+'|'+str(Node.label)+'|'+str(Node.use_custom_color)+'|'+str(Node.color[0])+'|'+str(Node.color[1])+'|'+str(Node.color[2])+'|'+str(Node.height)+'|'+str(Node.width)+'|'
    if Node.type=='FRAME':
        GeoNodeList+=str(Node.label_size)+'|'+str(Node.shrink)+'|'

    if (Node.type=='GROUP_INPUT') and (len(Node.outputs)>=3):
        #max=len(Node.outputs>=3)
        for GInum in Node.outputs:
            GeoNodeList+=GInum.name+'|'

    return GeoNodeList



def ObjCon(Con):
    con = Con
    conlist=''


    if con.type=='CAMERA_SOLVER':
        conlist+=str(con.use_active_clip)+'|'+str(con.influence)+'|'#+str(con.clip)+'|'
        '''
        bpy.context.object.constraints["Camera Solver"].use_active_clip = False
        bpy.context.object.constraints["Camera Solver"].influence = 0.955801
        bpy.context.object.constraints["Camera Solver"].clip = None
        '''

    elif con.type=='FOLLOW_TRACK':
        conlist+=str(con.use_active_clip)+'|'+str(con.use_3d_position)+'|'+str(con.use_undistorted_position)+'|'+str(con.frame_method)+'|'+str(con.camera.name)+'|'+str(con.depth_object.name)+'|'+str(con.influence)+'|'#+str(con.clip)+'|'

        '''
        bpy.context.object.constraints["Follow Track"].use_active_clip = False
        bpy.context.object.constraints["Follow Track"].use_3d_position = False
        bpy.context.object.constraints["Follow Track"].use_undistorted_position = False
        bpy.context.object.constraints["Follow Track"].frame_method = 'FIT'
        bpy.context.object.constraints["Follow Track"].camera = bpy.data.objects["Camera"]
        bpy.context.object.constraints["Follow Track"].depth_object = bpy.data.objects["Circle"]
        bpy.context.object.constraints["Follow Track"].influence = 0.906077

        bpy.context.object.constraints["Camera Solver"].clip = None
        '''

    elif con.type=='OBJECT_SOLVER':
        conlist+=str(con.use_active_clip)+'|'+str(con.camera.name)+'|'+str(con.influence)+'|'#+str(con.clip)+'|'
        '''
        bpy.context.object.constraints["Object Solver"].use_active_clip = True
        bpy.context.object.constraints["Object Solver"].camera = bpy.data.objects["Camera"]
        bpy.context.object.constraints["Object Solver"].influence = 0.955801

        bpy.context.object.constraints["Camera Solver"].clip = None
        '''


    elif con.type=='COPY_LOCATION':
        if con.space_object ==None:
            spaceName='None'
        else:
            spaceName=con.space_object.name
        conlist+=str(con.target.name)+'|'+\
                str(con.subtarget)+'|'+\
                str(con.use_x)+'|'+\
                str(con.use_y)+'|'+\
                str(con.use_z)+'|'+\
                str(con.invert_x)+'|'+\
                str(con.invert_y)+'|'+\
                str(con.invert_z)+'|'+\
                str(con.use_offset)+'|'+\
                str(con.target_space)+'|'+\
                str(con.owner_space)+'|'+\
                str(spaceName)+'|'+\
                str(con.space_subtarget)+'|'+\
                str(con.influence)+'|'


        '''
        bpy.context.object.constraints["Copy Location"].target = bpy.data.objects["Circle"]
        bpy.context.object.constraints["Copy Location"].subtarget = "Group"
        bpy.context.object.constraints["Copy Location"].use_x = True
        bpy.context.object.constraints["Copy Location"].use_y = True
        bpy.context.object.constraints["Copy Location"].use_z = True
        bpy.context.object.constraints["Copy Location"].invert_x = True
        bpy.context.object.constraints["Copy Location"].invert_y = True
        bpy.context.object.constraints["Copy Location"].invert_z = True
        bpy.context.object.constraints["Copy Location"].use_offset = True
        bpy.context.object.constraints["Copy Location"].target_space = 'CUSTOM'
        bpy.context.object.constraints["Copy Location"].owner_space = 'LOCAL'
        bpy.context.object.constraints["Copy Location"].space_object = bpy.data.objects["Circle"]
        bpy.context.object.constraints["Copy Location"].space_subtarget = "Group"
        bpy.context.object.constraints["Copy Location"].influence = 0.944751
        '''


    elif con.type=='COPY_ROTATION':
        if con.space_object ==None:
            spaceName='None'
        else:
            spaceName=con.space_object.name
        conlist+=str(con.target.name)+'|'+\
                str(con.subtarget)+'|'+\
                str(con.euler_order)+'|'+\
                str(con.use_x)+'|'+\
                str(con.use_y)+'|'+\
                str(con.use_z)+'|'+\
                str(con.invert_x)+'|'+\
                str(con.invert_y)+'|'+\
                str(con.invert_z)+'|'+\
                str(con.mix_mode)+'|'+\
                str(con.target_space)+'|'+\
                str(con.owner_space)+'|'+\
                str(spaceName)+'|'+\
                str(con.space_subtarget)+'|'+\
                str(con.influence)+'|'
        '''
        bpy.context.object.constraints["Copy Rotation"].target = bpy.data.objects["Circle"]
        bpy.context.object.constraints["Copy Rotation"].subtarget = "Group"
        bpy.context.object.constraints["Copy Rotation"].euler_order = 'XYZ'
        bpy.context.object.constraints["Copy Rotation"].use_x = False
        bpy.context.object.constraints["Copy Rotation"].use_y = False
        bpy.context.object.constraints["Copy Rotation"].use_z = False
        bpy.context.object.constraints["Copy Rotation"].invert_x = True
        bpy.context.object.constraints["Copy Rotation"].invert_y = True
        bpy.context.object.constraints["Copy Rotation"].invert_z = True
        bpy.context.object.constraints["Copy Rotation"].mix_mode = 'BEFORE'
        bpy.context.object.constraints["Copy Rotation"].target_space = 'CUSTOM'
        bpy.context.object.constraints["Copy Rotation"].owner_space = 'CUSTOM'
        bpy.context.object.constraints["Copy Rotation"].space_object = bpy.data.objects["Circle"]
        bpy.context.object.constraints["Copy Rotation"].space_subtarget = "Group"
        bpy.context.object.constraints["Copy Rotation"].influence = 0.883978
        '''


    elif con.type=='COPY_SCALE':
        if con.space_object ==None:
            spaceName='None'
        else:
            spaceName=con.space_object.name
        conlist+=str(con.target.name)+'|'+\
                str(con.subtarget)+'|'+\
                str(con.use_x)+'|'+\
                str(con.use_y)+'|'+\
                str(con.use_z)+'|'+\
                str(con.power)+'|'+\
                str(con.use_make_uneliform)+'|'+\
                str(con.use_offset)+'|'+\
                str(con.use_add)+'|'+\
                str(con.target_space)+'|'+\
                str(con.owner_space)+'|'+\
                str(spaceName)+'|'+\
                str(con.space_subtarget)+'|'+\
                str(con.influence)+'|'


        '''
        bpy.context.object.constraints["Copy Scale"].target = bpy.data.objects["Circle"]
        bpy.context.object.constraints["Copy Scale"].subtarget = "Group"
        bpy.context.object.constraints["Copy Scale"].use_x = False
        bpy.context.object.constraints["Copy Scale"].use_y = False
        bpy.context.object.constraints["Copy Scale"].use_z = False
        bpy.context.object.constraints["Copy Scale"].power = 0.71
        bpy.context.object.constraints["Copy Scale"].use_make_uneliform = True
        bpy.context.object.constraints["Copy Scale"].use_offset = True
        bpy.context.object.constraints["Copy Scale"].use_add = True
        bpy.context.object.constraints["Copy Scale"].target_space = 'CUSTOM'
        bpy.context.object.constraints["Copy Scale"].owner_space = 'CUSTOM'
        bpy.context.object.constraints["Copy Scale"].space_object = bpy.data.objects["Circle"]
        bpy.context.object.constraints["Copy Scale"].space_subtarget = "Group"
        bpy.context.object.constraints["Copy Scale"].influence = 0.823204
        '''


    elif con.type=='COPY_TRANSFORMS':
        if con.space_object ==None:
            spaceName='None'
        else:
            spaceName=con.space_object.name
        conlist+=str(con.target.name)+'|'+\
                str(con.subtarget)+'|'+\
                str(con.mix_mode)+'|'+\
                str(con.target_space)+'|'+\
                str(con.owner_space)+'|'+\
                str(spaceName)+'|'+\
                str(con.space_subtarget)+'|'+\
                str(con.influence)+'|'

        '''
        bpy.context.object.constraints["Copy Transforms"].target = bpy.data.objects["Circle"]
        bpy.context.object.constraints["Copy Transforms"].subtarget = "Group"
        bpy.context.object.constraints["Copy Transforms"].mix_mode = 'BEFORE'
        bpy.context.object.constraints["Copy Transforms"].target_space = 'CUSTOM'
        bpy.context.object.constraints["Copy Transforms"].owner_space = 'CUSTOM'
        bpy.context.object.constraints["Copy Transforms"].space_object = bpy.data.objects["Circle"]
        bpy.context.object.constraints["Copy Transforms"].space_subtarget = "Group"
        bpy.context.object.constraints["Copy Transforms"].influence = 0.812155
        '''


    elif con.type=='LIMIT_DISTANCE':
        if con.space_object ==None:
            spaceName='None'
        else:
            spaceName=con.space_object.name
        conlist+=str(con.target.name)+'|'+\
                str(con.subtarget)+'|'+\
                str(con.distance)+'|'+\
                str(con.limit_mode)+'|'+\
                str(con.use_transform_limit)+'|'+\
                str(con.target_space)+'|'+\
                str(con.owner_space)+'|'+\
                str(spaceName)+'|'+\
                str(con.space_subtarget)+'|'+\
                str(con.influence)+'|'

        '''
        bpy.context.object.constraints["Limit Distance"].target = bpy.data.objects["Circle"]
        bpy.context.object.constraints["Limit Distance"].subtarget = "Group"
        bpy.context.object.constraints["Limit Distance"].distance = 3.00739
        bpy.context.object.constraints["Limit Distance"].limit_mode = 'LIMITDIST_OUTSIDE'
        bpy.context.object.constraints["Limit Distance"].use_transform_limit = True
        bpy.context.object.constraints["Limit Distance"].target_space = 'CUSTOM'
        bpy.context.object.constraints["Limit Distance"].owner_space = 'CUSTOM'
        bpy.context.object.constraints["Limit Distance"].space_object = bpy.data.objects["Circle"]
        bpy.context.object.constraints["Limit Distance"].space_subtarget = "Group"
        bpy.context.object.constraints["Limit Distance"].influence = 0.922652
        '''


    elif (con.type=='LIMIT_LOCATION') or (con.type=='LIMIT_SCALE'):
        if con.space_object ==None:
            spaceName='None'
        else:
            spaceName=con.space_object.name
        conlist+=str(con.use_min_x)+'|'+\
                str(con.use_min_y)+'|'+\
                str(con.use_min_z)+'|'+\
                str(con.use_max_x)+'|'+\
                str(con.use_max_y)+'|'+\
                str(con.use_max_z)+'|'+\
                str(con.use_transform_limit)+'|'+\
                str(con.min_x)+'|'+\
                str(con.min_y)+'|'+\
                str(con.min_z)+'|'+\
                str(con.max_x)+'|'+\
                str(con.max_y)+'|'+\
                str(con.max_z)+'|'+\
                str(con.owner_space)+'|'+\
                str(spaceName)+'|'+\
                str(con.space_subtarget)+'|'+\
                str(con.influence)+'|'

        '''
        bpy.context.object.constraints["Limit Location"].use_min_x = True
        bpy.context.object.constraints["Limit Location"].use_min_y = True
        bpy.context.object.constraints["Limit Location"].use_min_z = True
        bpy.context.object.constraints["Limit Location"].use_max_x = True
        bpy.context.object.constraints["Limit Location"].use_max_y = True
        bpy.context.object.constraints["Limit Location"].use_max_z = True
        bpy.context.object.constraints["Limit Location"].use_transform_limit = True
        bpy.context.object.constraints["Limit Location"].min_x = 0.1
        bpy.context.object.constraints["Limit Location"].min_y = 0.1
        bpy.context.object.constraints["Limit Location"].min_z = 0.1
        bpy.context.object.constraints["Limit Location"].max_x = 0.1
        bpy.context.object.constraints["Limit Location"].max_y = 0.1
        bpy.context.object.constraints["Limit Location"].max_z = 0.1
        bpy.context.object.constraints["Limit Location"].owner_space = 'CUSTOM'
        bpy.context.object.constraints["Limit Location"].space_object = bpy.data.objects["Circle"]
        bpy.context.object.constraints["Limit Location"].space_subtarget = "Group"
        bpy.context.object.constraints["Limit Location"].influence = 0.933702
        '''


    elif con.type=='LIMIT_ROTATION':
        if con.space_object ==None:
            spaceName='None'
        else:
            spaceName=con.space_object.name
        conlist+=str(con.use_limit_x)+'|'+\
                str(con.use_limit_y)+'|'+\
                str(con.use_limit_z)+'|'+\
                str(con.min_x)+'|'+\
                str(con.max_x)+'|'+\
                str(con.min_y)+'|'+\
                str(con.max_y)+'|'+\
                str(con.min_z)+'|'+\
                str(con.max_z)+'|'+\
                str(con.use_transform_limit)+'|'+\
                str(con.owner_space)+'|'+\
                str(spaceName)+'|'+\
                str(con.space_subtarget)+'|'+\
                str(con.influence)+'|'
        '''
        con.use_limit_x = True
        con.use_limit_y = True
        con.use_limit_z = True
        con.min_x = 0.00174533
        con.max_x = 0.00174533
        con.min_y = 0.00174533
        con.max_y = 0.00174533
        con.min_z = 0.00174533
        con.max_z = 0.00174533
        con.use_transform_limit = True
        con.owner_space = 'CUSTOM'
        con.space_object = bpy.data.objects["Circle"]
        con.space_subtarget = "Group"
        con.influence = 0.872928
        '''

    elif con.type=='MAINTAIN_VOLUME':
        if con.space_object ==None:
            spaceName='None'
        else:
            spaceName=con.space_object.name
        conlist+=str(con.mode)+'|'+\
                str(con.free_axis)+'|'+\
                str(con.volume)+'|'+\
                str(con.owner_space)+'|'+\
                str(spaceName)+'|'+\
                str(con.space_subtarget)+'|'+\
                str(con.influence)+'|'

        '''
        bpy.context.object.constraints["Maintain Volume"].mode = 'STRICT'
        bpy.context.object.constraints["Maintain Volume"].free_axis = 'SAMEVOL_Y'
        bpy.context.object.constraints["Maintain Volume"].volume = 1.1
        bpy.context.object.constraints["Maintain Volume"].owner_space = 'CUSTOM'
        bpy.context.object.constraints["Maintain Volume"].space_object = bpy.data.objects["Circle"]
        bpy.context.object.constraints["Maintain Volume"].space_subtarget = "Group"
        bpy.context.object.constraints["Maintain Volume"].influence = 0.734807
        '''

    elif con.type=='TRANSFORM':
        if con.space_object ==None:
            spaceName='None'
        else:
            spaceName=con.space_object.name
        conlist+=str(con.target.name)+'|'+\
                str(con.subtarget)+'|'+\
                str(con.use_motion_extrapolate)+'|'+\
                str(con.target_space)+'|'+\
                str(con.owner_space)+'|'+\
                str(spaceName)+'|'+\
                str(con.space_subtarget)+'|'+\
                str(con.influence)+'|'+\
                str(con.map_from)+'|'+\
                str(con.from_min_x)+'|'+\
                str(con.from_max_x)+'|'+\
                str(con.from_min_y)+'|'+\
                str(con.from_max_y)+'|'+\
                str(con.from_min_z)+'|'+\
                str(con.from_max_z)+'|'+\
                str(con.from_rotation_mode)+'|'+\
                str(con.from_min_x_rot)+'|'+\
                str(con.from_max_x_rot)+'|'+\
                str(con.from_min_y_rot)+'|'+\
                str(con.from_max_y_rot)+'|'+\
                str(con.from_min_z_rot)+'|'+\
                str(con.from_max_z_rot)+'|'+\
                str(con.from_min_x_scale)+'|'+\
                str(con.from_max_x_scale)+'|'+\
                str(con.from_min_y_scale)+'|'+\
                str(con.from_max_y_scale)+'|'+\
                str(con.from_min_z_scale)+'|'+\
                str(con.from_max_z_scale)+'|'+\
                str(con.map_to)+'|'+\
                str(con.map_to_x_from)+'|'+\
                str(con.map_to_y_from)+'|'+\
                str(con.map_to_z_from)+'|'+\
                str(con.to_min_x)+'|'+\
                str(con.to_max_x)+'|'+\
                str(con.to_min_y)+'|'+\
                str(con.to_max_y)+'|'+\
                str(con.to_min_z)+'|'+\
                str(con.to_max_z)+'|'+\
                str(con.mix_mode)+'|'+\
                str(con.to_euler_order)+'|'+\
                str(con.map_to_x_from)+'|'+\
                str(con.map_to_y_from)+'|'+\
                str(con.map_to_z_from)+'|'+\
                str(con.to_min_x_rot)+'|'+\
                str(con.to_max_x_rot)+'|'+\
                str(con.to_min_y_rot)+'|'+\
                str(con.to_max_y_rot)+'|'+\
                str(con.to_min_z_rot)+'|'+\
                str(con.to_max_z_rot)+'|'+\
                str(con.mix_mode_rot)+'|'+\
                str(con.map_to_x_from)+'|'+\
                str(con.map_to_y_from)+'|'+\
                str(con.map_to_z_from)+'|'+\
                str(con.to_min_x_scale)+'|'+\
                str(con.to_max_x_scale)+'|'+\
                str(con.to_min_y_scale)+'|'+\
                str(con.to_max_y_scale)+'|'+\
                str(con.to_min_z_scale)+'|'+\
                str(con.to_max_z_scale)+'|'+\
                str(con.mix_mode_scale)+'|'

        '''
        bpy.context.object.constraints["Transformation"].target = bpy.data.objects["Circle"]
        bpy.context.object.constraints["Transformation"].subtarget = "Group"
        bpy.context.object.constraints["Transformation"].use_motion_extrapolate = True
        bpy.context.object.constraints["Transformation"].target_space = 'CUSTOM'
        bpy.context.object.constraints["Transformation"].owner_space = 'CUSTOM'
        bpy.context.object.constraints["Transformation"].space_object = bpy.data.objects["Circle"]
        bpy.context.object.constraints["Transformation"].space_subtarget = "Group"
        bpy.context.object.constraints["Transformation"].influence = 0.751381

        bpy.context.object.constraints["Transformation"].map_from = 'LOCATION'
        bpy.context.object.constraints["Transformation"].from_min_x = 0.1
        bpy.context.object.constraints["Transformation"].from_max_x = 0.1
        bpy.context.object.constraints["Transformation"].from_min_y = 0.1
        bpy.context.object.constraints["Transformation"].from_max_y = 0.1
        bpy.context.object.constraints["Transformation"].from_min_z = 0.1
        bpy.context.object.constraints["Transformation"].from_max_z = 0.1
        bpy.context.object.constraints["Transformation"].from_rotation_mode = 'XZY'#
        bpy.context.object.constraints["Transformation"].from_min_x_rot = 0.00174533
        bpy.context.object.constraints["Transformation"].from_max_x_rot = 0.00174533
        bpy.context.object.constraints["Transformation"].from_min_y_rot = 0.00174533
        bpy.context.object.constraints["Transformation"].from_max_y_rot = 0.00174533
        bpy.context.object.constraints["Transformation"].from_min_z_rot = 0.00174533
        bpy.context.object.constraints["Transformation"].from_max_z_rot = 0.00174533
        bpy.context.object.constraints["Transformation"].from_min_x_scale = 1.1#
        bpy.context.object.constraints["Transformation"].from_max_x_scale = 1.1
        bpy.context.object.constraints["Transformation"].from_min_y_scale = 1.1
        bpy.context.object.constraints["Transformation"].from_max_y_scale = 1.1
        bpy.context.object.constraints["Transformation"].from_min_z_scale = 1.1
        bpy.context.object.constraints["Transformation"].from_max_z_scale = 1.1

        bpy.context.object.constraints["Transformation"].map_to = 'LOCATION'
        bpy.context.object.constraints["Transformation"].map_to_x_from = 'Y'
        bpy.context.object.constraints["Transformation"].map_to_y_from = 'X'
        bpy.context.object.constraints["Transformation"].map_to_z_from = 'Z'
        bpy.context.object.constraints["Transformation"].to_min_x = 0.1
        bpy.context.object.constraints["Transformation"].to_max_x = 0.1
        bpy.context.object.constraints["Transformation"].to_min_y = 0.1
        bpy.context.object.constraints["Transformation"].to_max_y = 0.1
        bpy.context.object.constraints["Transformation"].to_min_z = 0.1
        bpy.context.object.constraints["Transformation"].to_max_z = 0.1
        bpy.context.object.constraints["Transformation"].mix_mode = 'REPLACE'
        bpy.context.object.constraints["Transformation"].to_euler_order = 'XZY'#
        bpy.context.object.constraints["Transformation"].map_to_x_from = 'X'
        bpy.context.object.constraints["Transformation"].map_to_y_from = 'Y'
        bpy.context.object.constraints["Transformation"].map_to_z_from = 'Z'
        bpy.context.object.constraints["Transformation"].to_min_x_rot = 0.00174533
        bpy.context.object.constraints["Transformation"].to_max_x_rot = 0.00174533
        bpy.context.object.constraints["Transformation"].to_min_y_rot = 0.00174533
        bpy.context.object.constraints["Transformation"].to_max_y_rot = 0.00174533
        bpy.context.object.constraints["Transformation"].to_min_z_rot = 0.00174533
        bpy.context.object.constraints["Transformation"].to_max_z_rot = 0.00174533
        bpy.context.object.constraints["Transformation"].mix_mode_rot = 'ADD'#
        bpy.context.object.constraints["Transformation"].map_to_x_from = 'X'
        bpy.context.object.constraints["Transformation"].map_to_y_from = 'Y'
        bpy.context.object.constraints["Transformation"].map_to_z_from = 'Z'
        bpy.context.object.constraints["Transformation"].to_min_x_scale = 1.1
        bpy.context.object.constraints["Transformation"].to_max_x_scale = 1.1
        bpy.context.object.constraints["Transformation"].to_min_y_scale = 1.1
        bpy.context.object.constraints["Transformation"].to_max_y_scale = 1.1
        bpy.context.object.constraints["Transformation"].to_min_z_scale = 1.1
        bpy.context.object.constraints["Transformation"].to_max_z_scale = 1.1
        bpy.context.object.constraints["Transformation"].mix_mode_scale = 'MULTIPLY'
        '''

    elif con.type=='TRANSFORM_CACHE':
        conlist+=str(con.influence)+'|'
        #bpy.context.object.constraints["Transform Cache"].influence = 0.834254

    elif con.type=='CLAMP_TO':
        conlist+=str(con.target.name)+'|'+\
                str(con.main_axis)+'|'+\
                str(con.use_cyclic)+'|'+\
                str(con.influence)+'|'

        '''
        bpy.context.object.constraints["Clamp To"].target = bpy.data.objects["BezierCircle"]
        bpy.context.object.constraints["Clamp To"].main_axis = 'CLAMPTO_AUTO'
        bpy.context.object.constraints["Clamp To"].use_cyclic = True
        bpy.context.object.constraints["Clamp To"].influence = 0.933702
        '''

    elif con.type=='DAMPED_TRACK':
        conlist+=str(con.target.name)+'|'+\
                str(con.subtarget)+'|'+\
                str(con.track_axis)+'|'+\
                str(con.influence)+'|'
        '''
        bpy.context.object.constraints["Damped Track"].target = bpy.data.objects["Circle"]
        bpy.context.object.constraints["Damped Track"].subtarget = "Group"
        bpy.context.object.constraints["Damped Track"].track_axis = 'TRACK_X'
        bpy.context.object.constraints["Damped Track"].influence = 0.718232
        '''

    elif con.type=='LOCKED_TRACK':
        conlist+=str(con.target.name)+'|'+\
                str(con.subtarget)+'|'+\
                str(con.track_axis)+'|'+\
                str(con.lock_axis)+'|'+\
                str(con.influence)+'|'
        '''
        bpy.context.object.constraints["Locked Track"].target = bpy.data.objects["Circle"]
        bpy.context.object.constraints["Locked Track"].subtarget = "Group"
        bpy.context.object.constraints["Locked Track"].track_axis = 'TRACK_X'
        bpy.context.object.constraints["Locked Track"].lock_axis = 'LOCK_Y'
        bpy.context.object.constraints["Locked Track"].influence = 0.729282
        '''

    elif con.type=='STRETCH_TO':
        conlist+=str(con.target.name)+'|'+\
                str(con.subtarget)+'|'+\
                str(con.rest_length)+'|'+\
                str(con.bulge)+'|'+\
                str(con.use_bulge_min)+'|'+\
                str(con.use_bulge_max)+'|'+\
                str(con.bulge_min)+'|'+\
                str(con.bulge_max)+'|'+\
                str(con.bulge_smooth)+'|'+\
                str(con.volume)+'|'+\
                str(con.keep_axis)+'|'+\
                str(con.influence)+'|'


        '''
        bpy.context.object.constraints["Stretch To"].target = bpy.data.objects["Circle"]
        bpy.context.object.constraints["Stretch To"].subtarget = "Group"
        bpy.context.object.constraints["Stretch To"].rest_length = 8.07397
        bpy.context.object.constraints["Stretch To"].bulge = 1.1
        bpy.context.object.constraints["Stretch To"].use_bulge_min = True
        bpy.context.object.constraints["Stretch To"].use_bulge_max = True
        bpy.context.object.constraints["Stretch To"].bulge_min = 0.9
        bpy.context.object.constraints["Stretch To"].bulge_max = 1.1
        bpy.context.object.constraints["Stretch To"].bulge_smooth = 0.0873786
        bpy.context.object.constraints["Stretch To"].volume = 'VOLUME_X'
        bpy.context.object.constraints["Stretch To"].keep_axis = 'PLANE_Z'
        bpy.context.object.constraints["Stretch To"].influence = 0.895028
        '''

    elif con.type=='TRACK_TO':
        if con.space_object ==None:
            spaceName='None'
        else:
            spaceName=con.space_object.name
        conlist+=str(con.target.name)+'|'+\
                str(con.subtarget)+'|'+\
                str(con.track_axis)+'|'+\
                str(con.up_axis)+'|'+\
                str(con.use_target_z)+'|'+\
                str(con.target_space)+'|'+\
                str(con.owner_space)+'|'+\
                str(spaceName)+'|'+\
                str(con.space_subtarget)+'|'+\
                str(con.influence)+'|'

        '''
        bpy.context.object.constraints["Track To"].target = bpy.data.objects["Circle"]
        bpy.context.object.constraints["Track To"].subtarget = "Group"
        bpy.context.object.constraints["Track To"].track_axis = 'TRACK_Z'
        bpy.context.object.constraints["Track To"].up_axis = 'UP_X'
        bpy.context.object.constraints["Track To"].use_target_z = True
        bpy.context.object.constraints["Track To"].target_space = 'CUSTOM'
        bpy.context.object.constraints["Track To"].owner_space = 'CUSTOM'
        bpy.context.object.constraints["Track To"].space_object = bpy.data.objects["Circle"]
        bpy.context.object.constraints["Track To"].space_subtarget = "Group"
        bpy.context.object.constraints["Track To"].influence = 0.978177
        '''


    elif con.type=='ACTION':
        if con.space_object ==None:
            spaceName='None'
        else:
            spaceName=con.space_object.name
        conlist+=str(con.target.name)+'|'+\
                str(con.subtarget)+'|'+\
                str(con.use_eval_time)+'|'+\
                str(con.eval_time)+'|'+\
                str(con.mix_mode)+'|'+\
                str(con.influence)+'|'+\
                str(con.transform_channel)+'|'+\
                str(con.target_space)+'|'+\
                str(spaceName)+'|'+\
                str(con.space_subtarget)+'|'+\
                str(con.min)+'|'+\
                str(con.max)+'|'+\
                str(con.use_bone_object_action)+'|'+\
                str(con.frame_start)+'|'+\
                str(con.frame_end)+'|'

        '''
        bpy.context.object.constraints["Action"].target = bpy.data.objects["Circle"]
        bpy.context.object.constraints["Action"].subtarget = "Group"
        bpy.context.object.constraints["Action"].use_eval_time = True
        bpy.context.object.constraints["Action"].eval_time = 0.0607735
        bpy.context.object.constraints["Action"].mix_mode = 'AFTER'
        bpy.context.object.constraints["Action"].influence = 0.773481
        bpy.context.object.constraints["Action"].transform_channel = 'LOCATION_Y'
        bpy.context.object.constraints["Action"].target_space = 'CUSTOM'
        bpy.context.object.constraints["Action"].space_object = bpy.data.objects["Circle"]
        bpy.context.object.constraints["Action"].space_subtarget = "Group"
        bpy.context.object.constraints["Action"].min = 7.7
        bpy.context.object.constraints["Action"].max = 8.4
            #bpy.context.object.constraints["Action"].action = bpy.data.actions["CubeAction"]
        bpy.context.object.constraints["Action"].use_bone_object_action = True
        bpy.context.object.constraints["Action"].frame_start = 1
        bpy.context.object.constraints["Action"].frame_end = 1
        '''

    elif con.type=='ARMATURE':
        conlist+=str(con.use_deform_preserve_volume)+'|'+\
                str(con.use_bone_envelopes)+'|'+\
                str(con.influence)+'|'
        '''
        bpy.context.object.constraints["Armature"].use_deform_preserve_volume = True
        bpy.context.object.constraints["Armature"].use_bone_envelopes = True
        bpy.context.object.constraints["Armature"].influence = 0.696133
        '''

    elif con.type=='CHILD_OF':
        conlist+=str(con.target.name)+'|'+\
                str(con.subtarget)+'|'+\
                str(con.use_location_x)+'|'+\
                str(con.use_location_y)+'|'+\
                str(con.use_location_z)+'|'+\
                str(con.use_rotation_x)+'|'+\
                str(con.use_rotation_y)+'|'+\
                str(con.use_rotation_z)+'|'+\
                str(con.use_scale_x)+'|'+\
                str(con.use_scale_y)+'|'+\
                str(con.use_scale_z)+'|'+\
                str(con.influence)+'|'

        '''
        bpy.context.object.constraints["Child Of"].target = bpy.data.objects["Circle"]
        bpy.context.object.constraints["Child Of"].subtarget = "Group"
        bpy.context.object.constraints["Child Of"].use_location_x = False
        bpy.context.object.constraints["Child Of"].use_location_y = False
        bpy.context.object.constraints["Child Of"].use_location_z = False
        bpy.context.object.constraints["Child Of"].use_rotation_x = False
        bpy.context.object.constraints["Child Of"].use_rotation_y = False
        bpy.context.object.constraints["Child Of"].use_rotation_z = False
        bpy.context.object.constraints["Child Of"].use_scale_x = False
        bpy.context.object.constraints["Child Of"].use_scale_y = False
        bpy.context.object.constraints["Child Of"].use_scale_z = False
        bpy.context.object.constraints["Child Of"].influence = 0.767956
        '''

    elif con.type=='FLOOR':
        if con.space_object ==None:
            spaceName='None'
        else:
            spaceName=con.space_object.name
        conlist+=str(con.target.name)+'|'+\
                str(con.subtarget)+'|'+\
                str(con.offset)+'|'+\
                str(con.floor_location)+'|'+\
                str(con.use_rotation)+'|'+\
                str(con.target_space)+'|'+\
                str(con.owner_space)+'|'+\
                str(spaceName)+'|'+\
                str(con.space_subtarget)+'|'+\
                str(con.influence)+'|'

        '''
        bpy.context.object.constraints["Floor"].target = bpy.data.objects["Circle"]
        bpy.context.object.constraints["Floor"].subtarget = "Group"
        bpy.context.object.constraints["Floor"].offset = 0.01
        bpy.context.object.constraints["Floor"].floor_location = 'FLOOR_NEGATIVE_X'
        bpy.context.object.constraints["Floor"].use_rotation = True
        bpy.context.object.constraints["Floor"].target_space = 'CUSTOM'
        bpy.context.object.constraints["Floor"].owner_space = 'CUSTOM'
        bpy.context.object.constraints["Floor"].space_object = bpy.data.objects["Circle"]
        bpy.context.object.constraints["Floor"].space_subtarget = "Group"
        bpy.context.object.constraints["Floor"].influence = 0.861878
        '''

    elif con.type=='FOLLOW_PATH':
        conlist+=str(con.target.name)+'|'+\
                str(con.offset)+'|'+\
                str(con.forward_axis)+'|'+\
                str(con.up_axis)+'|'+\
                str(con.use_fixed_location)+'|'+\
                str(con.use_curve_radius)+'|'+\
                str(con.use_curve_follow)+'|'+\
                str(con.influence)+'|'

        '''
        bpy.context.object.constraints["Follow Path"].target = bpy.data.objects["BezierCircle"]
        bpy.context.object.constraints["Follow Path"].offset = 9.1
        bpy.context.object.constraints["Follow Path"].forward_axis = 'FORWARD_Z'
        bpy.context.object.constraints["Follow Path"].up_axis = 'UP_Y'
        bpy.context.object.constraints["Follow Path"].use_fixed_location = True
        bpy.context.object.constraints["Follow Path"].use_curve_radius = True
        bpy.context.object.constraints["Follow Path"].use_curve_follow = True
        bpy.context.object.constraints["Follow Path"].influence = 0.712707
        '''


    elif con.type=='PIVOT':
        conlist+=str(con.target.name)+'|'+\
                str(con.subtarget)+'|'+\
                str(con.offset[0])+'|'+\
                str(con.offset[1])+'|'+\
                str(con.offset[2])+'|'+\
                str(con.rotation_range)+'|'+\
                str(con.influence)+'|'


        '''
        bpy.context.object.constraints["Pivot"].target = bpy.data.objects["Circle"]
        bpy.context.object.constraints["Pivot"].subtarget = "Group"
        bpy.context.object.constraints["Pivot"].offset[0] = 1.9
        bpy.context.object.constraints["Pivot"].offset[1] = 2.2
        bpy.context.object.constraints["Pivot"].offset[2] = 7.1
        bpy.context.object.constraints["Pivot"].rotation_range = 'ALWAYS_ACTIVE'
        bpy.context.object.constraints["Pivot"].influence = 0.723757
        '''


    elif con.type=='SHRINKWRAP':
        conlist+=str(con.target.name)+'|'+\
                str(con.distance)+'|'+\
                str(con.shrinkwrap_type)+'|'+\
                str(con.project_axis_space)+'|'+\
                str(con.project_limit)+'|'+\
                str(con.use_project_opposite)+'|'+\
                str(con.cull_face)+'|'+\
                str(con.use_invert_cull)+'|'+\
                str(con.wrap_mode)+'|'+\
                str(con.use_track_normal)+'|'+\
                str(con.track_axis)+'|'+\
                str(con.influence)+'|'
        '''
        bpy.context.object.constraints["Shrinkwrap"].target = bpy.data.objects["Sphere"]
        bpy.context.object.constraints["Shrinkwrap"].distance = 2.9
        bpy.context.object.constraints["Shrinkwrap"].shrinkwrap_type = 'NEAREST_SURFACE'
        bpy.context.object.constraints["Shrinkwrap"].project_axis_space = 'CUSTOM'
        bpy.context.object.constraints["Shrinkwrap"].project_limit = 0.1
        bpy.context.object.constraints["Shrinkwrap"].use_project_opposite = True
        bpy.context.object.constraints["Shrinkwrap"].cull_face = 'FRONT'
        bpy.context.object.constraints["Shrinkwrap"].use_invert_cull = True#
        bpy.context.object.constraints["Shrinkwrap"].wrap_mode = 'OUTSIDE'
        bpy.context.object.constraints["Shrinkwrap"].use_track_normal = True
        bpy.context.object.constraints["Shrinkwrap"].track_axis = 'TRACK_Z'#
        bpy.context.object.constraints["Shrinkwrap"].influence = 0.79558
        '''


    return conlist


#'CAMERA_SOLVER', 'FOLLOW_TRACK', 'OBJECT_SOLVER',
#'COPY_LOCATION', 'COPY_ROTATION', 'COPY_SCALE', 'COPY_TRANSFORMS', 'LIMIT_DISTANCE', 'LIMIT_LOCATION', 'LIMIT_ROTATION', 'LIMIT_SCALE', 'MAINTAIN_VOLUME', 'TRANSFORM', 'TRANSFORM_CACHE', 
#'CLAMP_TO', 'DAMPED_TRACK', 'IK'!, 'LOCKED_TRACK', 'SPLINE_IK'!, 'STRETCH_TO', 'TRACK_TO', 
#'ACTION', 'ARMATURE', 'CHILD_OF', 'FLOOR', 'FOLLOW_PATH', 'PIVOT', 'SHRINKWRAP'


##Drviers|源对象类型|源对象|源对象驱动器路径|index|表达式1类型|脚本表达式|对象数量|        对象函数名1|对象函数类型1|对象类型1|对象指针名1|对象1路径|...变换类型 变换空间 旋转模式('ROT' in transform_type时设置)
#Drivers|MESH|Cube|constraints["Floor"].offset|d.array_index|SCRIPTED|var -0.4|d.driver.variables|       var|SINGLE_PROP|NODETREE|Node1|nodes["Vector"].vector[2]|LOC_X|WORLD_SPACE|AUTO|
                                                                #var_001|TRANSFORMS|OBJECT|Cube||ROT_Z|TRANSFORM_SPACE|AUTO|
##Drviers|sourceType(id_type)|source|prop|driver.type|expression           |Func1Name|Func1Type           target1Type(id_type)|target1(id)|dataPath1||
'''
def add_driver(SourceType,Source,SourceDataPath,SourceIndex,expType,exp,TargetNum,FuncName,FuncType,TargetType,targetName,TargetDataPath,transform_type,transform_space,rotation_mode):
    if SourceType=='OBJECT':
        if Source in bpy.data.objects:
            source=bpy.data.objects[Source]
    elif SourceType=='TEXTURE':
        if Source in bpy.data.textures:
            source=bpy.data.textures[Source]
    elif SourceType=='GEOMETRY':
        if Source in bpy.data.node_groups:
            source=bpy.data.node_groups[Source]
    
    if TargetType=='OBJECT':
        if targetName in bpy.data.objects:
            target=bpy.data.objects[Source]
    elif TargetType=='TEXTURE':
        if targetName in bpy.data.textures:
            target=bpy.data.textures[Source]
    elif TargetType=='NODETREE':
        if targetName in bpy.data.node_groups:
            target=bpy.data.node_groups[Source]

    if int(SourceIndex) != 0:
        d = source.driver_add( SourceDataPath, int(SourceIndex) ).driver
    else:
        d = source.driver_add( SourceDataPath ).driver

    d.type=expType
    if d.type=='SCRIPTED':
        d.expression = exp

    varnum=int(TargetNum)
    for var in range(varnum):
        v = d.variables.new()
        v.name                 = FuncName
        v.targets[0].id_type=FuncType
        v.targets[0].id        = target
        v.targets[0].data_path = TargetDataPath
        v.targets[0].transform_type=transform_type
        v.targets[0].transform_space=transform_space
        v.targets[0].rotation_mode=rotation_mode
'''

#add_driver( cube, Node, 'constraints["Floor"].offset', 'nodes["Vector"].vector[2]',-1,False,'constraints["Floor"].offset-0.4' )