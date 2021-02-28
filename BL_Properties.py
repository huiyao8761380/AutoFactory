import bpy
import os
from bpy.types import Panel,Operator,PropertyGroup
from bpy.props import FloatProperty, PointerProperty, EnumProperty, BoolProperty, FloatVectorProperty, IntProperty, StringProperty
from . BL_Tool import *

def GenMechFolder_Item(self, context):#self, context
    enum_items = [('Preset', "Preset", "Preset Folder",1)]
    FolderList=[]
    FolderPath=os.path.dirname(__file__)+'//Preset//'
    for Folder in os.listdir(FolderPath):
        if '.' not in Folder:#
            FolderList.append(Folder)
    i=1
    for name in FolderList:
        i=i+1
        enum_items.append((name, name, "",i))

    return enum_items

def GenMechEnum_Item(self, context):#self, context
    amProperty = context.scene.amProperties
    enum_items = [
            ('MechPro', "MechPro", "多重修改器",1),
            ('Helmet', "Helmet", "低聚程序化头盔样式修改器",2),
            ('Mechfy', "Mechfy", "首次由Emiliano Colantoni制作的修改器",3)
        ]

    FileList=[]
    #FolderPath=os.path.dirname(__file__)+'//Preset//'
    if (amProperty.GenMechFolder=='Preset') or (amProperty.GenMechFolder==''):
        FolderPath=os.path.dirname(__file__)+'//Preset//'
    else:
        FolderPath=os.path.dirname(__file__)+'//Preset//'+amProperty.GenMechFolder+'//'
    for file in os.listdir(FolderPath):
        if '.txt' in file:#
            filename=file.split('.txt', 1)
            #if len(filename[0]) < 1:
                #FileList.append(filename[1])
            #else:
            
            FileList.append(filename[0])
    i=3
    for name in FileList:
        i=i+1
        enum_items.append((name, name, "",i))

    return enum_items

class AMProperties(PropertyGroup):

    GenLineEnum: EnumProperty(
        name="",
        description="GenLineEnum,生成线的预设形状枚举",
        items=[
            ('GenLineOnly', "GenLineOnly", ""),
            ('GenLineMechBody', "Custom GenLineMechBody", ""),
            ('GenLineStruct', "GenLineStruct", ""),
            ('GenLineKit', "GenLineKit", ""),
            ('GenLineWeapon', "GenLineWeapon", "")
            #('MODE_GD_MARBLE', "大理石 Marble", ""),
            #('MODE_GD_MUSGRAVE', "马斯格雷夫分形 Musgrave", "")
        ],
        default="GenLineOnly"
    )

    MOD_BOOLEAN_Bool: BoolProperty(
        name="Boolean",
        description="开关显示布尔修改器(开关修改器目前只适用于MechPro)",
        default = True
        )

    MOD_WARP_Bool: BoolProperty(#根据当前物体的情况
        name="Warp",
        description="开关显示所有弯绕修改器(开关修改器目前只适用于MechPro)",
        default = True
        )

    MOD_LATTICE_Bool: BoolProperty(
        name="Lattice",
        description="开关显示晶格修改器(开关修改器目前只适用于MechPro)",
        default = True
        )

    MOD_CURVE_Bool: BoolProperty(
        name="Curve",
        description="开关显示所有曲线修改器(开关修改器目前只适用于MechPro)",
        default = False
        )

    MOD_ARRAY_Bool: BoolProperty(
        name="Array",
        description="开关显示所有阵列修改器(开关修改器目前只适用于MechPro)",
        default = False
        )

    MOD_SCREW_Bool: BoolProperty(
        name="Screw",
        description="开关显示所有螺旋修改器(打开前务必保存工程 与 减少重构深度)，需要牺牲很多性能",
        default = False
        )

    MOD_SIMPLEDEFORM_Bool: BoolProperty(
        name="Simpledeform",
        description="开关显示所有简易形变修改器(开关修改器目前只适用于MechPro)",
        default = False
        )

    MOD_TRIANGULATE_Bool: BoolProperty(#或开关显示所有cast
        name="Triangulate",
        description="开关显示所有三角化修改器(开关修改器目前只适用于MechPro)",
        default = False
        )

    MOD_MIRROR_Bool: BoolProperty(
        name="Mirror",
        description="开关显示镜像修改器(开关修改器目前只适用于MechPro)",
        default = True
        )

    UVMaterial_Bool: BoolProperty(
        name="UVMaterial",
        description="是否根据材质分离生成uv",
        default = True
        )

    UVMirror_Bool: BoolProperty(
        name="UVMirror",
        description="是否对称镜像UV",
        default = True
        )

    UVModifierApply_Bool: BoolProperty(
        name="UVModifierApply",
        description="是否立即应用修改器",
        default = True
        )

    HideChildObj_Bool: BoolProperty(
        name="HideChildObj",
        description="开关显示子物体",
        default = False,
        update=HideChildObj_update
        )

    UnrealSize_Bool: BoolProperty(
        name="UnrealSizeBool",
        description="开关UE4单位,建议在绑定前使用，不然会影响修改器等因素",
        default = False,
        update=UnrealSize_update
        )

    FaceOrient_Bool: BoolProperty(
        name="FaceOrientBool",
        description="开关面朝向",
        default = False,
        update=FaceOrient_update
        )

    FaceOrient_Int: IntProperty(
        name="FaceOrientBool",
        description="简易显示模式",
        default = 0#,
        #update=FaceOrient_update
        )

    FreezeTime_Bool: BoolProperty(#否不冻结 True冻结
        name="FreezeTimeBool",
        description="冻结默认的修改器的时间轴",
        default = False,
        update=FreezeTime_update
        )

    AutoSave_Bool: BoolProperty(#否不自动保存 True自动保存
        name="AutoSaveBool",
        description="应用修改器时自动保存WIP中间件",
        default = False
        )

    ModifiersApplyTo_Int: IntProperty(  #应用完当前编号的修改器，0将应用全部,40=040_Wave，如果含有自添加的布尔将需手动应用修改器
        name="ModifierApplyToInt",
        description="应用修改器至排序位置",
        default = 0
        )

    #'''
    AddBoolModifier: EnumProperty(#50 85 90 95 107布尔
        name="",
        description="在所选修改器后面添加布尔",
        items=[
            ('Bool050', "050_Bool", "随机性大,在050_BoolSub修改器后面再次添加布尔"),
            ('Bool085', "085_Bool", "随机性中,在085_BoolSub修改器后面再次添加布尔"),
            ('Bool090', "090_Bool", "随机性小，在090_BoolSub修改器后面再次添加布尔"),
            ('Bool095', "095_Bool", "随机性微，在095_BoolSub修改器后面再次添加布尔"),
            ('Bool107', "107_Bool", "随机性无，在107_BoolSub修改器后面再次添加布尔")
        ],
        default="Bool050"
    )
    BoolNum: IntProperty(#添加布尔对象到活动对象的指定修改器位置，0为末尾
        name="Boolean",
        description="添加布尔对象到指定修改器位置，0为末尾",
        default = 0
    )


    #'''
    BoolModifierType: EnumProperty(#50 85 90 95 107布尔
        name="",
        description="添加的布尔修改器类型",
        items=[
            ('INTERSECT', "Intersect", "Intersect"),
            ('UNION', "Union", "Union"),
            ('DIFFERENCE', "Difference", "Difference")
        ],
        default="UNION"
    )

    GenMechApplyBoll: BoolProperty(
        name="Apply modifiers",
        description="Aoto Apply modifiers",
        default = False
        )

    GenMechBemeshClean: BoolProperty(
        name="Bemesh Clean",
        description="Bemesh Clean1.1",
        default = False
        )

    GenMechUVPackmaster: BoolProperty(
        name="UVPackmaster",
        description="UVPackmaster2.3.2",
        default = False
        )

    GenMechRemeshEnum: EnumProperty(
        name="RemeshEnum",
        description="(Old)Gen Mech Remesh Enum Modify",
        items=[
            ('BLOCKS', 'BLOCKS', ""),
            ('SMOOTH', 'SMOOTH', ""),
            ('SHARP', 'SHARP', "")

        ],
        default='SMOOTH',
        update=RemeshEnum_update
    )


    GenMechBevel0Enum:EnumProperty(
        name="Bevel0Enum",
        description="(Old)Gen Mech Bevel0 Enum Modify",
        items=GenMechBevel0Enum_callback,
        options={'ANIMATABLE'},
        #default= bpy.context.object.modifiers["Bevel"].offset_type
        update=GenMechBevel0Enum_update

        #get=get_Bevel0Enum
        #set=set_Bevel0Enum
    )

    '''
    GenMechBevel0float:FloatProperty(
        name="width_pct",
        description="Gen Mech Bevel0 width_pct Modify",
        default=37,
        min=0,
        amx=100,
        #options={'ANIMATABLE'},
        #update=GenMechBevel0float_update
    )
    '''


    GenMechResizeBool: BoolProperty(
        name="Resize",
        description="开/关显示编辑模式下物体的变换参数",
        default = False
        )

    GenMechResize: FloatVectorProperty(
        name="Resize",
        description="修改编辑模式下物体的变换大小",
        default = (1,1,1),
        step=10,
        update=GenMechResize_update
        #set=set_GenMechResize
        )

    GenMechSkinSizeBool: BoolProperty(
        name="Skin",
        description="Skin Size,开/关显示蒙皮修改器大小参数",
        default = False
        )

    GenMechSkinResize: FloatVectorProperty(
        name="Skin",# modifier Size
        description="Skin Size,修改编辑模式下线拥有的蒙皮修改器大小",
        default = (1,1,1),
        update=GenMechSkinResize_update
        )

    GenMechRemeshScale: FloatProperty(
        name="Remesh",
        description="修改重构网格的体素大小(注意检查单位,可能有影响)",
        default = 0.03,
        min=0.001,
        max=10,
        step=0.1,
        update=GenMechRemeshScale_update
        )

    AutoToolBool: BoolProperty(
        name="Tool",
        description="开/关显示调用的工具或插件",
        default = False
        )

    RandomMaterialBool: BoolProperty(
        name="Material",
        description="开/关随机材质颜色",
        default = False
        )


    CleanScanTimes_Int: IntProperty(
        name="CleanScanTimes",
        description="单方向清理扫描的次数",
        default = 31#,
        #update=FaceOrient_update
        )

    LinkMaterialBool: BoolProperty(
        name="LinkMaterial",
        description="开/关链接活动物体材质",
        default = True
        )

    '''
    UIPositionBool: BoolProperty(
        name="UIPosition",
        description="设置插件UI的位置，开启则放于条目(Item)中,以便随时查看与操作。",
        default = False
        )

    UIPositionEnum: EnumProperty(
        name="UIPositionEnum",
        description="设置插件UI的位置，开启则放于条目(Item)中,以便随时查看与操作。",
        items=[
            ('AutoFactory', "Auto Factory", ""),
            ('Item', "Item", "")#
        ],
        default="AutoFactory"
    )
    '''
    GenMechName: StringProperty(
        name='',
        description='所选的预设修改器集名称',
        default='MechPro',
        subtype='FILE_NAME'
        #update=GenMechName_update
        )

    RenderImageBool: BoolProperty(
        name="RenderImageBool",
        description="开/关显示图片(，存在排序问题，未完成)",
        default = False
        )

    '''
    GenMechEnum: EnumProperty(
        name="GenMechEnum",
        description="Gen Mech Enum Modifier",
        items=GenMechEnum_Item,
        default='MechPro',#这里有问题
        update=GenMechEnum_update
        )#保存的时候也要更新items图片库 同时要扩展
    '''
    GenMechEnum: EnumProperty(items = GenMechEnum_Item, update = GenMechEnum_update )

    GenMechFolder: EnumProperty(items = GenMechFolder_Item)

    AutoMechBool: BoolProperty(name="Auto Mech",description="",default = True)

    AutoRigifyBool: BoolProperty(name="Auto Rigify",description="",default = False)

    StepRigBool: BoolProperty(name="分步绑定",description="",default = False)

    FakeRigBool: BoolProperty(name="虚假绑定",description="虚假绑定含有修改器的物体，（注意：需要用到很多性能，请在视图层关闭所有含有多重修改器的物体并绑定其他物体以进行预览）",default = True)

    ReDataNameBool: BoolProperty(name="重命名物体数据",description="导出时重命名修改器、约束,如果不重命名数据名称请不要包含'|,#'",default = True)

    BoolParentBool: BoolProperty(name="执行布尔操作时设置活动对象为父级",description="",default = True)

    PresetParentBool: BoolProperty(name="导入预设时设置父级",description="",default = False)

