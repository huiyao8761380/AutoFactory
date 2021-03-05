import bpy
from . BL_GenLine import GenLine 
from . BL_GenMech import GenMech
from . BL_EdgesGen import EdgesGen
from . BL_Properties import AMProperties
from . BL_Tool import *
from . BL_MechClean import MechClean
from . BL_AddRig import AddRig
from . BL_BindRig import BindRig
from . BL_WeightRig import WeightRig

from . AutoRigify.RIG_0Rename import RigRename
from . AutoRigify.RIG_1ReFace import RigReFace
from . AutoRigify.RIG_2UE4type import UE4TypeBone
from . AutoRigify.RIG_3ReBone import ReBone
from . AutoRigify.RIG_4RePose import RePose
from . AutoRigify.RIG_Tool import OneClickAddUE4Rig,RigMechByName,RemoveIKBoneGroup
from . AutoRigify.AutoCharacter import AutoLatticeShape,DefaultShapekey,ShapekeyDriver,TransferAllKey,BlendKey


from bpy.types import Panel, Operator, PropertyGroup, Menu, AddonPreferences
from bpy.props import FloatProperty, PointerProperty, StringProperty, IntProperty, BoolProperty



class AutoFactoryPanel(bpy.types.Panel):
    
    bl_label = "Auto Factory"
    bl_idname = "Auto_Mech_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Auto Factory'#bpy.context.scene.amProperties.UIPositionEnum#'Auto Factory'#'Item'
    '''
    if bpy.context.scene.amProperties.UIPositionBool ==True:
        bl_category = 'Item'
    else:
        bl_category = 'Auto Factory'
    '''

    def draw(self, context):
        sampleProperty = context.scene.AMOldPropertyGroup
        amProperty = context.scene.amProperties
        OpenScripts = bpy.context.preferences.addons.keys()

        layout = self.layout
        #pie = layout
        #pie.label(text='Auto Mech')
        col = layout.column(align=True)
        row4 = col.row(align=True)
        row = col.row(align=True)
        row5 = col.row(align=True)#layout.row(align=True)
        col2 = layout.column(align=True)
        row2a = col2.row(align=True)
        row2 = col2.row(align=True)
        row2b = col2.row(align=True)
        row2c = col2.row(align=True)
        row2d = col2.row(align=True)
        row2e = col2.row(align=True)
        row2f = col2.row(align=True)

        col3 = layout.column(align=True)
        row3g = col3.row(align=True)
        row3a = col3.row(align=True)
        row3e = col3.row(align=True)
        #split = row3e.split(factor=0.75)#小间隔
        #row3f = split.row()
        row3b = col3.row(align=True)
        row3c = col3.row(align=True)
        row3d = col3.row(align=True)

        #if amProperty.GenLineEnum =='GenLineOnly':
            
            #col.prop(sampleProperty, "edgeName")
        
        row4.prop(amProperty, 'AutoMechBool',  text="Auto Mech",icon = 'TRIA_DOWN' if amProperty.AutoMechBool else 'TRIA_RIGHT')

        if amProperty.AutoMechBool:

            row.operator("object.bl_genline" , text = "", icon='IPO_CONSTANT')
            row.prop(sampleProperty, "edgeMin")
            row.prop(sampleProperty, "edgeMax")
            row.prop(sampleProperty, "edgeVNumber")

                #col5 = layout.column(align=True)

            row5.prop(sampleProperty, "edgeXYZ", text = "", icon='PIVOT_BOUNDBOX')
            row5.prop(sampleProperty, "LocEdgeBool", text = "", icon='EMPTY_ARROWS')#EMPTY_AXIS
            row5.prop(sampleProperty, "LocEditBool", text = "", icon='PIVOT_MEDIAN')
            row5.prop(amProperty, "GenMechResizeBool", text = "", icon='CON_SIZELIMIT')
            row5.prop(amProperty, "GenMechSkinSizeBool", text = "", icon='MOD_SKIN')
            row5.prop(amProperty, "GenLineEnum")

            if sampleProperty.edgeXYZ == True:
                row2a.label(text="Bounds")
                row2.prop(sampleProperty, "xuMin")
                row2.prop(sampleProperty, "yuMin")
                row2.prop(sampleProperty, "zuMin")

                row2b.prop(sampleProperty, "xvMax")
                row2b.prop(sampleProperty, "yvMax")
                row2b.prop(sampleProperty, "zvMax")

            if sampleProperty.LocEdgeBool == True:
                row2c.prop(sampleProperty, "edgeLoc")

            if sampleProperty.LocEditBool == True:
                row2d.prop(sampleProperty, "LocEdit")

            if amProperty.GenMechResizeBool == True:
                row2e.prop(amProperty, "GenMechResize")

            if amProperty.GenMechSkinSizeBool == True:
                row2f.prop(amProperty, "GenMechSkinResize")

            if amProperty.RenderImageBool == True:
                row3g.prop(amProperty, "GenMechFolder", text = "")
                row3a.template_icon_view(amProperty, "GenMechEnum", show_labels=True, scale=5, scale_popup=4.0)#row3a.prop(amProperty, "GenMechEnum")
            else:
                row3g.prop(amProperty, "GenMechFolder", text = "")
                row3a.prop(amProperty, "GenMechEnum", text = "")

            row3e.operator("am.savepreset" , text = "",icon='FILE_TICK')#save OBJ All Modifiers Data
            row3e.operator("am.openpresetfolder" , text = "",icon='FOLDER_REDIRECT')#打开文件夹
            row3e.prop(amProperty, "GenMechName")
            row3e.prop(amProperty, "ReDataNameBool", text = "",icon='LINENUMBERS_ON')
            row3e.prop(amProperty, "PresetParentBool", text = "",icon='FILE_PARENT')
            #row3e.prop(amProperty, "RenderImageBool", text = "",icon='IMAGE')
            #添加立即生成图片
            #preference 是否是高质量渲染图片




            #GenMechRemeshEnum
            #row8.prop(amProperty, "GenMechRemeshEnum")

            #row6.prop(amProperty, "GenMechApplyBoll")
            
            col7 = layout.column(align=True)

            row7 = col7.row(align=True)#横里的竖
            row7.operator("object.bl_genmech" , text = "",icon='MODIFIER')#Modifier修改器bevel17蜂巢 三角形 切换风格 的进度条  Smooth50_ToFixHole
            row7.prop(amProperty, "MOD_BOOLEAN_Bool",text="",icon='MOD_BOOLEAN')#√多个物体不建议使用
            row7.prop(amProperty, "MOD_WARP_Bool",text="",icon='MOD_WARP')#√
            row7.prop(amProperty, "MOD_LATTICE_Bool",text="",icon='MOD_LATTICE')#√
            row7.prop(amProperty, "MOD_CURVE_Bool",text="",icon='MOD_CURVE')#√
            row7.prop(amProperty, "MOD_ARRAY_Bool",text="",icon='MOD_ARRAY')#√
            row7.prop(amProperty, "MOD_SCREW_Bool",text="",icon='MOD_SCREW')#√需要牺牲很多性能
            row7.prop(amProperty, "MOD_SIMPLEDEFORM_Bool",text="",icon='MOD_SIMPLEDEFORM')#√
            row7.prop(amProperty, "MOD_MIRROR_Bool",text="",icon='MOD_MIRROR')#√row横 col竖

            row7b = col7.row(align=True)#横里的竖
            #row7b.label(icon='SHADERFX',text="")#功能
            row7b.prop(amProperty, "AutoToolBool",text="",icon='TOOL_SETTINGS')#TOOL_SETTINGS
            row7b.prop(amProperty, "FreezeTime_Bool",text="",icon='FREEZE')#√固定当前时间轴所选修改器参数 按钮 默认False 没能弄wave的波或者应用到Wave及之前的修改器 不包含显示跟渲染 这些应当去掉
            #row7b.prop(amProperty, "MOD_MIRROR_Bool",text="",icon='MOD_SHRINKWRAP')#X设置为预设让别人选择吧 将所选两个物体中其中一个设为容器并生成低模 按钮 #建议跟布尔一行
            row7b.prop(amProperty,"HideChildObj_Bool",text="",icon='VIS_SEL_11' if amProperty.HideChildObj_Bool else 'VIS_SEL_01', toggle=True)#VIS_SEL_11 √设置当前对象的所有子空物体不可选/不可见 RESTRICT_SELECT_ON 布尔 operator("am.hidechildobj",text="",icon='VIS_SEL_01')#！！！
            row7b.operator("am.faceorient",text="",icon='OVERLAY')#√开关面朝向、物体随机单色显示
            row7b.prop(amProperty, "AutoSave_Bool",text="",icon='DUPLICATE')#√自动保存 复制且保留一份并应用 按钮 或布尔的好习惯
            row7b.prop(amProperty, "RandomMaterialBool",text="",icon='NODE_MATERIAL')#随机材质颜色 NODE_MATERIAL
            row7b.operator("am.rename" , text = "",icon='SMALL_CAPS')#ReName
            row7b.prop(amProperty,"UnrealSize_Bool",text="",icon='EVENT_U')#√设置为ue4的模型比例，并增加摄像机距离 按钮 operator("am.unrealsize",text="",icon='EVENT_U')
            row7b.operator("am.renderscene", text = "",icon='SCENE_DATA')#添加一个渲染环境预设 按钮

            row7a = col7.row(align=True)#align=True横里的竖
            row7a.operator("am.addboolmodifier",text="",icon='MOD_BOOLEAN')#√选择两个物体，添加一个bool修改器在主要物体的重构网格11前（Bool_sub） 按钮#布尔位置 多 另起义行
            #row7b.prop(amProperty, "AutoSave_Bool",text="",icon='MATERIAL_DATA')#MATERIAL_DATA
            row7a.prop(amProperty, "LinkMaterialBool",text="",icon='MATERIAL_DATA')
            row7a.prop(amProperty, "BoolParentBool",text="",icon='OUTLINER')
            row7a.prop(amProperty, "BoolNum")#AddBoolModifier#√选择两个物体，添加一个bool修改器在主要物体的重构网格11前（Bool_sub） 按钮#布尔位置 多 另起义行
            row7a.prop(amProperty, "BoolModifierType")


            row7c = col7.row(align=True)#横里的竖
            row7c.operator("am.applymodify" , text = "",icon='OUTLINER_OB_MESH')#Apply
            row7c.operator("am.deleteunusedmodifier" , text = "",icon='FILE_REFRESH')
            row7c.operator("am.randomindexmodifier" , text = "",icon='EVENT_R')
            row7c.prop(amProperty, "ModifiersApplyTo_Int",text="Apply Modifiers")#V仅应用重构网格（或字符标记的）11前的修改器 按钮#还有一个应用并删除子物体 #还有哟个应用到40的波


            row7d = col7.row(align=True)#横里的竖
            #row7d.label(icon='RENDER_ANIMATION',text="")
            row7d.operator("object.mechclean" , text = "",icon='BRUSH_DATA')#4.MechClean(Edit)清理后Clean 和Apply 生成UV，关联对称 按钮
            
            row7d.prop(amProperty, "UVMaterial_Bool",text="",icon='SHADING_TEXTURE')#！！！关联 操作是否根据材质分离生成uv 布尔 
            
            row7d.prop(amProperty, "UVMirror_Bool",text="",icon='MOD_MIRROR')#X！！！对称UV 默认为开 布尔 应用前变更物体名称区别bisect
            row7d.prop(amProperty, "UVModifierApply_Bool",text="",icon='MODIFIER_ON')#应用修改器X！！！显示修改器常用设置如bevel17 MODIFIER_OFF  。。。。#MATERIAL变换材质 布尔 SHADING_RENDERED
            #row7d.operator("am.rename" , text = "",icon='SMALL_CAPS')
            row7d.prop(amProperty, "CleanScanTimes_Int",text="Frame Rate")#CleanScanTimes_Int
            #其他功能:
            #col7.operator("object.bl_genmech" , text = "2.Gen Mech")#修改器bevel17蜂巢 三角形 切换风格 的进度条  Smooth50_ToFixHole
            row7e = col7.row(align=True)#横里的竖
            row7e.operator("am.hightolowremesh",text="",icon='MOD_REMESH')#。√ REMESH 简易重构该物体 重构当前网格体然后塌陷 按钮 可用作bool
            row7e.prop(amProperty, "GenMechRemeshScale")

            row7f = col7.row(align=True)
            row7f.operator("am.geonodereplacestr",text="",icon='BORDERMOVE')
            row7f.prop(amProperty, "GeoNodeBeforeSTR")
            row7f.prop(amProperty, "GeoNodeAfterSTR")




            col8 = layout.column(align=True)
            row8 = col8.row(align=True)
            
            col9 = layout.column(align=True)
            row9 = col8.row(align=True)

            #col8.operator("object.mechclean" , text = "4.MechClean(Edit)")

            if amProperty.AutoToolBool ==True:
                #row8.prop(amProperty, "GenMechBemeshClean")
                row8.prop(amProperty, "GenMechUVPackmaster")


            if (amProperty.GenMechEnum =='MechfyHigh') or (amProperty.GenMechEnum =='Mechfy'):
                row3b.prop(amProperty, "GenMechRemeshEnum")
                row3c.prop(amProperty, "GenMechBevel0Enum")

                if amProperty.GenMechBevel0Enum =='PERCENT':
                    row3d.prop(sampleProperty, "Bevel0float")


        col10 = layout.column(align=True)
        row4a = col10.row(align=True)
        row10m = col10.row(align=True)
        row10n = col10.row(align=True)
        row10a = col10.row(align=True)
        row10b = col10.row(align=True)
        row10c = col10.row(align=True)
        row10d = col10.row(align=True)
        row10j = col10.row(align=True)
        row10e = col10.row(align=True)
        row10f = col10.row(align=True)
        row10g = col10.row(align=True)
        row10h = col10.row(align=True)
        row10i = col10.row(align=True)
        row10l = col10.row(align=True)
        row10k = col10.row(align=True)
        

        row4a.prop(amProperty, 'AutoRigifyBool',  text="Auto Rigify",icon = 'TRIA_DOWN' if amProperty.AutoRigifyBool else 'TRIA_RIGHT')
        if amProperty.AutoRigifyBool:
            row10m.operator("am.autolatticeshape" , text = "",icon = 'MATCLOTH')
            row10m.prop(amProperty, 'LatticeMirrorBool',  text="",icon = 'LATTICE_DATA')
            row10m.prop(amProperty, 'DoubleLatticeBool',  text="",icon = 'MOD_MIRROR')
            row10m.prop(amProperty, 'DeleteShapeObjBool',  text="",icon = 'TRASH')
            row10m.operator("am.defaultshapekey" , text = "",icon = 'SHAPEKEY_DATA')
            row10m.operator("am.shapekeydriver" , text = "",icon = 'DRIVER')
            row10m.operator("am.transferallkey" , text = "",icon = 'EVENT_T')
            row10m.operator("am.blendkey" , text = "",icon = 'EVENT_B')



            if amProperty.LatticeMirrorBool ==True:
                row10n.prop(amProperty, 'LeftBodyGroupSTR')
                row10n.prop(amProperty, 'RightBodyGroupSTR')
            else:
                row10n.prop(amProperty, 'VertexGroupSTR')

            row10a.operator("am.mirrorselect" , text = "MirrorX Select")
            if 'rigify' in OpenScripts:
                if amProperty.GenMechEnum =='Mechfy':
                    row10b.operator("aw.addrig" , text = "AddRig(Rigify)")
                    row10c.operator("aw.bindrig" , text = "BindAllRig")
                    row10d.operator("aw.weightrig" , text = "WeightRig")
                row10j.prop(amProperty, 'StepRigBool',  text="",icon = 'TRIA_DOWN' if amProperty.AutoRigifyBool else 'TRIA_RIGHT')
                row10j.operator("am.oneclickaddue4rig" , text = "Add UE4 Rig")
                if amProperty.StepRigBool ==True:
                    row10e.operator("am.rigrename" , text = "0.Rename")
                    row10f.operator("am.rigreface" , text = "1.Reface")
                    row10g.operator("am.ue4typebone" , text = "2.UE4Bone")
                    row10h.operator("am.rebone" , text = "3.ReBone")
                    row10i.operator("am.repose" , text = "4.RePose")
                row10l.operator("am.rigmechbyname" , text = "RigMechByName")
                row10l.prop(amProperty, 'FakeRigBool',  text="",icon = 'MOD_ARMATURE')
                row10k.operator("am.removeikbonegroup" , text = "Reset IK Weight")


'''
class AutoRigifyPanel(bpy.types.Panel):
    
    bl_label = "Auto Rigify"
    bl_idname = "Auto_Rigify_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Auto Factory'


    def draw(self, context):
        sampleProperty = context.scene.AMOldPropertyGroup
        amProperty = context.scene.amProperties
        
        layout = self.layout
        pie = layout
        pie.label(text='Auto Factory')
        col10 = layout.column(align=True)
        row10a = col10.row(align=True)
        row10b = col10.row(align=True)
        row10c = col10.row(align=True)
        row10d = col10.row(align=True)
        row10a.operator("am.mirrorselect" , text = "MirrorSelect")
        if (amProperty.GenMechEnum =='MechfyHigh') or (amProperty.GenMechEnum =='Mechfy'):
            row10b.operator("aw.addrig" , text = "AddRig(Rigify)")
            row10c.operator("aw.bindrig" , text = "BindAllRig")
            row10d.operator("aw.weightrig" , text = "WeightRig")

        #box = layout.box()
        #box.label(text='--- Default value ---')
        
        #box.prop(amProperty, "AutoSave_Bool",text="",icon='DUPLICATE')
        
'''