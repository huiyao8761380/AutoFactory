bl_info = {
    "name" : "AutoFactory",  "AutoFactory-main"
    "author" : "透过现象看本质(Hui)",
    "description" : "(N键显示菜单)尽可能的自动做硬表面建模，导入导出修改器预设参数来方便管理使用等。",
    "blender" : (2, 90, 1),
    "version" : (0, 9, 2),
    "location" : "View3D > Tools > AutoFactory",
    "warning" : "如果不能正确安装使用，请重命名插件文件夹名为'AutoFactory'.",
    "category" : "Object",
    "wiki_url" : "https://github.com/huiyao8761380/AutoFactory"
}
#ReadMe:如果出现切换着色方式卡顿或是想要变更预览材质，可以备份并修改AMpresets.blend下的PreMColor材质节点(已用黄色标记，不要删除)，或是查询PreMColor代码进行修改。

import bpy
from bpy.utils import register_class, unregister_class
from bpy.props import *

import webbrowser

from . BL_Panel import *
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
from . AutoRigify.AutoCharacter import AutoLatticeShape,DefaultShapekey

from bpy.types import Panel, Operator, PropertyGroup, Menu, AddonPreferences
from bpy.props import FloatProperty, PointerProperty, StringProperty, IntProperty, BoolProperty

class AMOldPropertyGroup(PropertyGroup):

    edgeName: StringProperty(name="NameEdge", default='1GenLine')
    edgeMin: IntProperty(name="MinEdge", description="预生成连接线的xyz轴负向范围", default=-5)
    edgeMax: IntProperty(name="MaxEdge", description="预生成连接线的xyz轴正向范围", default=5)
    edgeVNumber: IntProperty(name="VNumberedge", description="预生成连接线的顶点数量", default=10)
    edgeXYZ: BoolProperty(name="Bounds", description="开/关显示生成线局部范围", default=False)
    xuMin: FloatProperty(name="-x", description="生成线-x局部范围", default=-1)
    yuMin: FloatProperty(name="-y", description="生成线-y局部范围", default=-1)
    zuMin: FloatProperty(name="-z", description="生成线-z局部范围", default=-1)
    xvMax: FloatProperty(name="x", description="生成线+x局部范围", default=1)
    yvMax: FloatProperty(name="y", description="生成线+y局部范围", default=1)
    zvMax: FloatProperty(name="z", description="生成线+z局部范围", default=1)
    edgeLoc: FloatVectorProperty(name="Location", description="生成线的XYZ位置", default=(0,0,0),step=10, update=edgeLoc_update)
    LocEdgeBool: BoolProperty(name="LocEdge", description="开/关显示生成线位置", default=False)
    LocEdit: FloatVectorProperty(name="Origin", description="生成线中心点的XYZ位置", default=(0,0,0),step=10, update=LocEdit_update)
    LocEditBool: BoolProperty(name="LocEdit", description="开/关显示生成线中心点位置", default=False)
    Bevel0float: FloatProperty(name="width_pct", default=37, min=0, max=100, update=GenMechBevel0float_update)


class ExampleAddonPreferences(AddonPreferences):
    
    bl_idname = __name__

    filepath: StringProperty(
        name="Example File Path",
        default=''
        #subtype='FILE_PATH',
    )
    number: IntProperty(
        name="Example Number",
        default=4,
    )
    boolean: BoolProperty(
        name="Example Boolean",
        default=False,
    )

    def draw(self, context):
        amProperty = context.scene.amProperties
        layout = self.layout

        #layout.label(text="This is a preferences view for our add-on") 
        #layout.prop(self, "filepath")
        #layout.prop(self, "number")
        #layout.prop(self, "boolean")#self为这个py文件里的 属性
        #layout.prop(bpy.context.scene.amProperties, "UIPositionBool",text="将插件UI放于条目中")#,icon='DUPLICATE'



class OBJECT_OT_addon_prefs_example(Operator):
    """Display example preferences"""
    bl_idname = "object.addon_prefs_example"
    bl_label = "Add-on Preferences Example"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        preferences = context.preferences
        addon_prefs = preferences.addons[__name__].preferences


        #info = ("Path: %s, Number: %d, Boolean %r" %
                #(addon_prefs.filepath, addon_prefs.number, addon_prefs.boolean))

        #self.report({'INFO'}, info)
        print(info)

        return {'FINISHED'}




classes = ( AMOldPropertyGroup, 
        AMProperties, 
        AutoFactoryPanel, 
        ExampleAddonPreferences,
        SavePreset, 
        OpenPresetFolder, 
        OBJECT_OT_addon_prefs_example, 
        GenLine, 
        GenMech, 
        ApplyModify,
        HideChildObj,
        FaceOrient,
        AddBoolModifier, 
        MechClean, 
        ApplyClean, 
        RenderScene, 
        HightoLowRemesh, 
        AddRig, 
        BindRig, 
        WeightRig, 
        MirrorSelect, 
        ReName, 
        RigRename,
        RigReFace,
        UE4TypeBone,
        ReBone,
        RePose,
        OneClickAddUE4Rig,
        RigMechByName,
        RemoveIKBoneGroup,
        DeleteUnusedModifier,
        RandomIndexModifier,
        GeoNodeReplaceSTR,
        AutoLatticeShape,
        DefaultShapekey
        )
#register, unregister = bpy.utils.register_classes_factory(classes)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.AMOldPropertyGroup = PointerProperty(type=AMOldPropertyGroup)
    bpy.types.Scene.amProperties = PointerProperty(type=AMProperties)
    #bpy.types.Scene.AutoFactoryPanel = PointerProperty(type=AutoFactoryPanel)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.AMOldPropertyGroup
    del bpy.types.Scene.amProperties
    #del bpy.types.Scene.AutoFactoryPanel

#bpy.types.Scene.AMOldPropertyGroup = PointerProperty(type=AMOldPropertyGroup)
#def register():
    #bpy.utils.register_class(AutoFactoryPanel)
    #bpy.utils.register_class(GenLine)

#def unregister():
    #bpy.utils.unregister_class(AutoFactoryPanel)
    #bpy.utils.unregister_class(GenLine)

if __name__ == "__main__":
    register()
    #bpy.ops.object.GenLine()