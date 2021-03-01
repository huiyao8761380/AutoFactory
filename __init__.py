bl_info = {
    "name": "AutoFactory", "AutoFactory-main"
                           "author": "透过现象看本质(Hui)",
    "description": "(N键显示菜单)尽可能的自动做硬表面建模，导入导出修改器预设参数来方便管理使用等。",
    "blender": (2, 90, 1),
    "version": (0, 9, 2),
    "location": "View3D > Tools > AutoFactory",
    "warning": "如果不能正确安装使用，请重命名插件文件夹名为'AutoFactory'.",
    "category": "Object",
    "wiki_url": "https://github.com/huiyao8761380/AutoFactory"
}
# ReadMe:如果出现切换着色方式卡顿或是想要变更预览材质，可以备份并修改AMpresets.blend下的PreMColor材质节点(已用黄色标记，不要删除)，或是查询PreMColor代码进行修改。

import bpy
from bpy.types import Panel, Operator, PropertyGroup, Menu, AddonPreferences
from bpy.props import *

# tools for auto reload addon
import importlib
import sys
import os
from itertools import groupby

# get folder name
__folder_name__ = __name__
__dict__ = {}
addon_dir = os.path.dirname(__file__)

# get all .py file path
py_paths = [os.path.join(root, f) for root, dirs, files in os.walk(addon_dir) for f in files if
            f.endswith('.py') and f != '__init__.py']

for path in py_paths:
    name = os.path.basename(path)[:-3]
    correct_path = path.replace('\\', '/')
    # split path with folder name
    dir_list = [list(g) for k, g in groupby(correct_path.split('/'), lambda x: x == __folder_name__) if
                not k]
    # combine path and make dict like this: 'name:folder.name'
    if 'preset' not in dir_list[-1]:
        r_name_raw = __folder_name__ + '.' + '.'.join(dir_list[-1])
        __dict__[name] = r_name_raw[:-3]

# auto reload
for name in __dict__.values():
    if name in sys.modules:
        importlib.reload(sys.modules[name])
    else:
        globals()[name] = importlib.import_module(name)
        setattr(globals()[name], 'modules', __dict__)


class ExampleAddonPreferences(AddonPreferences):
    bl_idname = __name__

    filepath: StringProperty(
        name="Example File Path",
        default=''
        # subtype='FILE_PATH',
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

        # layout.label(text="This is a preferences view for our add-on")
        # layout.prop(self, "filepath")
        # layout.prop(self, "number")
        # layout.prop(self, "boolean")#self为这个py文件里的 属性
        # layout.prop(bpy.context.scene.amProperties, "UIPositionBool",text="将插件UI放于条目中")#,icon='DUPLICATE'


class OBJECT_OT_addon_prefs_example(Operator):
    """Display example preferences"""
    bl_idname = "object.addon_prefs_example"
    bl_label = "Add-on Preferences Example"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        preferences = context.preferences
        addon_prefs = preferences.addons[__name__].preferences

        # info = ("Path: %s, Number: %d, Boolean %r" %
        # (addon_prefs.filepath, addon_prefs.number, addon_prefs.boolean))

        # self.report({'INFO'}, info)
        # print(info)

        return {'FINISHED'}


# register, unregister = bpy.utils.register_classes_factory(classes)
def register():
    for name in __dict__.values():
        if name in sys.modules and hasattr(sys.modules[name], 'register'):
            sys.modules[name].register()
        else:
            print(f'ERROR:{name} register failed!')

    bpy.utils.register_class(ExampleAddonPreferences)
    bpy.utils.register_class(OBJECT_OT_addon_prefs_example)
    # bpy.types.Scene.AutoFactoryPanel = PointerProperty(type=AutoFactoryPanel)


def unregister():
    for name in __dict__.values():
        if name in sys.modules and hasattr(sys.modules[name], 'unregister'):
            sys.modules[name].unregister()

    bpy.utils.unregister_class(ExampleAddonPreferences)
    bpy.utils.unregister_class(OBJECT_OT_addon_prefs_example)
    # del bpy.types.Scene.AutoFactoryPanel


if __name__ == "__main__":
    register()
    # bpy.ops.object.GenLine()
