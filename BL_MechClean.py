import bpy
import functools
from bpy.types import Operator,PropertyGroup
from bpy.props import FloatProperty, PointerProperty,StringProperty
from . BL_Tool import *
from . BL_Panel import * #

from queue import Queue
from threading import Thread

#bpy.ops.view3d.view_orbit(context,angle=5.0, type='ORBITLEFT')
#bpy.ops.mesh.bisect(plane_co=(0, 0, 10), plane_no=(1, 0, 0), use_fill=False, clear_inner=True, clear_outer=False, xstart=243, xend=243, ystart=349, yend=20)

class MechClean(bpy.types.Operator):
    bl_idname = "object.mechclean"
    bl_label = "清理并展UV"
    bl_description = "清理非流形、展光照UV(使用前建议设为正交视图、保存文件，容易崩溃：在2.90中打开UV编辑器窗口执行自动展UV时会崩溃)" 
    bl_options = {'REGISTER', 'UNDO'}

    
    def __init__(self):
        self.select_box_up_counter = 0
        self.select_box_left_counter = 0
        self.select_box_down_counter = 0
        self.select_box_right_counter = 0

        self.context = bpy.context.copy()


    def select_box_up(self):
        self.select_box_up_counter +=1
        #print("select_box_up")
        bpy.ops.view3d.view_orbit(self.context,angle=0.2, type='ORBITUP')
        bpy.ops.view3d.select_box(self.context,xmin=-2160, xmax=2160, ymin=-2160, ymax=2160, wait_for_input=True, mode='ADD')
        if self.select_box_up_counter >= bpy.context.scene.amProperties.CleanScanTimes_Int:
            bpy.app.timers.register(self.select_box_left)
            return None
        return 0.02

    def select_box_left(self):
        self.select_box_left_counter +=1
        #print("select_box_left")
        bpy.ops.view3d.view_orbit(self.context,angle=0.2, type='ORBITLEFT')
        bpy.ops.view3d.select_box(self.context,xmin=-2160, xmax=2160, ymin=-2160, ymax=2160, wait_for_input=True, mode='ADD')
        if self.select_box_left_counter >= bpy.context.scene.amProperties.CleanScanTimes_Int:
            bpy.app.timers.register(self.select_box_down)
            return None
        return 0.02

    def select_box_down(self):
        self.select_box_down_counter +=1
        #print("select_box_down")
        bpy.ops.view3d.view_orbit(self.context,angle=0.2, type='ORBITDOWN')
        bpy.ops.view3d.select_box(self.context,xmin=-2160, xmax=2160, ymin=-2160, ymax=2160, wait_for_input=True, mode='ADD')
        if self.select_box_down_counter >= bpy.context.scene.amProperties.CleanScanTimes_Int:
            bpy.app.timers.register(self.select_box_right)
            return None
        return 0.02

    def select_box_right(self):
        self.select_box_right_counter +=1
        #print("select_box_right")
        bpy.ops.view3d.view_orbit(self.context,angle=0.2, type='ORBITRIGHT')
        bpy.ops.view3d.select_box(self.context,xmin=-2160, xmax=2160, ymin=-2160, ymax=2160, wait_for_input=True, mode='ADD')
        if self.select_box_right_counter >= bpy.context.scene.amProperties.CleanScanTimes_Int:
            self.clean()#
            
            return None
        return 0.02

    def EditMode(self):
        for area in bpy.context.screen.areas:
            if area.type == "VIEW_3D":
                break

        for region in area.regions:
            if region.type == "WINDOW":
                break

        space = area.spaces[0]
        self.context = bpy.context.copy()
        context = self.context
        context['area'] = area
        context['region'] = region
        context['space_data'] = space
        space.overlay.show_face_orientation = True
        bpy.ops.view3d.view_selected(context,use_all_regions=False)

        #bpy.ops.object.mode_set(mode='EDIT')
        #bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE', action='TOGGLE')
        bpy.ops.view3d.select_box(context,xmin=0, xmax=1080, ymin=0, ymax=1080, wait_for_input=True, mode='ADD')

    def ThreadOne(self):
        bpy.app.timers.register(self.EditMode)

    def ThreadTwo(self):
        bpy.app.timers.register(self.select_box_up, first_interval=0.1)

    def clean(self):
        bpy.ops.mesh.hide(unselected=False)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.delete(type='ONLY_FACE')
        bpy.ops.mesh.reveal()
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT', action='TOGGLE')
        bpy.ops.mesh.select_all(action='INVERT')
        bpy.ops.mesh.delete(type='EDGE_FACE')
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE', action='TOGGLE')
        amProperty = bpy.context.scene.amProperties

        #bpy.ops.object.mode_set(mode='OBJECT')

        sel = bpy.context.selected_objects
        
        #for ob not in sel:
            #ob.hide_set(False)

        #bpy.ops.view3d.localview()
        for ob in sel:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = ob

            bpy.ops.object.mode_set(mode='EDIT')
            
            bpy.ops.mesh.select_all(action='SELECT')


            
            if amProperty.UVMirror_Bool ==True:
                if "_l" in ob.data.name or "_r" in ob.data.name :
                    Mirror = ob.modifiers.new("Mirror", "MIRROR")
                    if "clavicle" in ob.name:
                        bpy.ops.mesh.bisect(plane_co=(-1, 0.2, -10), plane_no=(0, 1, 0), use_fill=False, clear_inner=False, clear_outer=True, xstart=204, xend=713, ystart=198, yend=196)
                        Mirror.use_axis[0] = False
                        Mirror.use_axis[1] = True
                    elif "upperarm" in ob.name:
                        bpy.ops.mesh.bisect(plane_co=(-1, 0.15, -10), plane_no=(0, 1, 0), use_fill=False, clear_inner=False, clear_outer=True, xstart=204, xend=713, ystart=198, yend=196)
                        Mirror.use_axis[0] = False
                        Mirror.use_axis[1] = True
                    elif "lowerarm" in ob.data.name:
                        bpy.ops.mesh.bisect(plane_co=(-1, 0.2, -10), plane_no=(0, 1, 0), use_fill=False, clear_inner=False, clear_outer=True, xstart=204, xend=713, ystart=198, yend=196)
                        Mirror.use_axis[0] = False
                        Mirror.use_axis[1] = True
                    elif "hand" in ob.data.name:
                        bpy.ops.mesh.bisect(plane_co=(-1, 0.2, -10), plane_no=(0, 1, 0), use_fill=False, clear_inner=False, clear_outer=True, xstart=204, xend=713, ystart=198, yend=196)
                        Mirror.use_axis[0] = False
                        Mirror.use_axis[1] = True
                    else:
                        bpy.ops.mesh.bisect(plane_co=(0.5, 0, 50), plane_no=(1, 0, 0), use_fill=False, clear_inner=True, clear_outer=False, xstart=243, xend=243, ystart=349, yend=20)
                else:
                    bpy.ops.mesh.bisect(plane_co=(ob.location[0], 0, 50), plane_no=(1, 0, 0), use_fill=False, clear_inner=True, clear_outer=False)
                    Mirror = ob.modifiers.new("Mirror", "MIRROR")

        #bpy.ops.object.mode_set(mode='OBJECT')

        
        for ob in sel:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            ob.select_set(True)
            bpy.context.view_layer.objects.active = ob
            
            bpy.ops.object.mode_set(mode='EDIT')
            if amProperty.UVMaterial_Bool == True:
                bpy.ops.mesh.select_all(action='DESELECT')
                NumMaterial=len(ob.material_slots)
                for i in range(0,NumMaterial):
                    ob.active_material_index = i
                    bpy.ops.object.material_slot_select()
                    bpy.ops.uv.lightmap_pack(PREF_IMG_PX_SIZE=2048, PREF_BOX_DIV=12, PREF_MARGIN_DIV=0.1)
                    if amProperty.GenMechUVPackmaster ==True:
                        UVPackmaster()
                    bpy.ops.mesh.select_all(action='DESELECT')

            else:
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.uv.lightmap_pack(PREF_IMG_PX_SIZE=2048, PREF_BOX_DIV=12, PREF_MARGIN_DIV=0.05)
                if amProperty.GenMechUVPackmaster ==True:
                    UVPackmaster()


        for area in bpy.context.screen.areas:
            if area.type == "VIEW_3D":
                break

        for region in area.regions:
            if region.type == "WINDOW":
                break

        space = area.spaces[0]
        self.context = bpy.context.copy()
        context = self.context
        context['area'] = area
        context['region'] = region
        context['space_data'] = space
        #bpy.ops.view3d.localview()
        space.overlay.show_face_orientation = False
        bpy.ops.object.mode_set(mode='OBJECT')
        #HideObjs(False)
        
        
        if amProperty.UVModifierApply_Bool ==True:
            bpy.ops.object.convert(target='MESH')

    
    def execute(self, context):

        #find_object('1GenLine','3ApplyMech',"4MechClean")
        bpy.ops.am.applymodify()#强行应用修改器
        #areas = [area for screen in context.workspace.screens for area in screen.areas if area.type == "VIEW_3D"]
        #bpy.ops.view3d.view_selected(use_all_regions=False)V
        #bpy.ops.view3d.view_persportho()#实现这俩PERSPECTIVE x
        move_to_collection('3ApplyMech',"4MechClean")
        #bpy.context.space_data.overlay.show_face_orientation = True#法线 这里直接可以。。
        #HideObjs(True)
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE', action='TOGGLE')


        '''
        for area in bpy.context.screen.areas:
            if area.type == "VIEW_3D":
                break

        for region in area.regions:
            if region.type == "WINDOW":
                break

        space = area.spaces[0]

        context = bpy.context.copy()
        context['area'] = area
        context['region'] = region
        context['space_data'] = space
        '''

        T1 = Thread(target=self.ThreadOne)
        T2 = Thread(target=self.ThreadTwo)

        T1.start()
        T2.start()

        self.report({'INFO'}, "清理成功")
        return {'FINISHED'}


