import bpy
import random
import os
from itertools import count,islice

from . BL_Tool import *
from . BL_EdgesGen import EdgesGen

from bpy.types import Operator,PropertyGroup
from bpy.props import FloatProperty, PointerProperty,StringProperty


def str_to_bool(str):
    return True if str.lower() == 'true' else False

def str_to_obj(str):
    if 'bpy.data.textures' in str:
        OBJname=str[:-2].replace("bpy.data.textures['","")
        if OBJname in bpy.data.textures:
            OBJ = bpy.data.textures[OBJname]
            return OBJ
        else:
            return None
    elif 'bpy.data.objects' in str:
        OBJname=str[:-2].replace("bpy.data.objects['","")
        if OBJname in bpy.data.objects:
            OBJ = bpy.data.objects[OBJname]
            return OBJ
        else:
            return None
    else:
        return None

def to_Tex(str):
    Texname=str
    if Texname in bpy.data.textures:
        Tex = bpy.data.textures[Texname]
        return Tex
    else:
        return None

def to_Col(str):
    Colname=str
    if Colname in bpy.data.collections:
        Col = bpy.data.collections[Colname]
        return Col
    else:
        return None

def to_Obj(str):
    Objname=str
    if Objname in bpy.data.objects:
        Obj = bpy.data.objects[Objname]
        return Obj
    else:
        return None

def Dict_str(str):
    #这里{}还没想好怎么转换
    #if 'set()' in str:
    return set()


def real_str(str):
    return str.replace("'","")

class GenMech(bpy.types.Operator):
    bl_idname = "object.bl_genmech"
    bl_label = "生成修改器预设"
    bl_description = "点击生成当前预设修改器的物体，该插件的核心之一。" 
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        col_name='0AutoMech'

        #3NEW col 将合集交给1GenLine
        #rename_object('GenMech')

        sel = bpy.context.selected_objects
        amProperty = context.scene.amProperties
        OBJType=None
        #FolderPath=os.path.dirname(__file__)+'\\Preset\\'

        if (amProperty.GenMechFolder=='Preset') or (amProperty.GenMechFolder==''):
            FolderPath=os.path.dirname(__file__)+'//Preset//'
        else:
            FolderPath=os.path.dirname(__file__)+'//Preset//'+amProperty.GenMechFolder+'//'

        File=FolderPath + amProperty.GenMechEnum + ".txt"

        OBJModEndList=[]
        OBJNameList = []
        OBJParmList = []
        OBJParentName =''
        DriversList=[]

        #如果不是文本修改器生成则自动创建Cube
        if not ((amProperty.GenMechEnum == 'MechPro') or (amProperty.GenMechEnum == 'Helmet') or (amProperty.GenMechEnum == 'Mechfy') or (amProperty.GenMechEnum == '')):
            f = open(File, encoding='utf-8')# "r")
            for line in f:
                parameter = line.split("|")
                if "*Next" in line:
                    OBJModEnd = parameter[2]
                    OBJModEndList.append(OBJModEnd)
                elif ("AddOBJ" in parameter[0]) or ("ParentOBJ" in parameter[0]):#elif "ParentOBJ" in line:#else:#ADD 如果是父级就选为活动元素
                    Param=parameter
                    OBJType=parameter[2]
                    OBJParmList.append(line)
                    OBJNameList.append(parameter[1])
                elif 'Texture' in parameter[0]:
                    TexCount=count(1, 1)
                    if parameter[2]!='None':
                        Tex=bpy.data.textures.new(parameter[1], type=parameter[2])
                        
                        if Tex.type == 'BLEND':
                            Tex.progression = parameter[2+int(next(TexCount))]
                            Tex.use_flip_axis = parameter[2+int(next(TexCount))]


                        elif Tex.type == 'CLOUDS':
                            Tex.noise_basis = parameter[2+int(next(TexCount))]
                            Tex.noise_type = parameter[2+int(next(TexCount))]
                            Tex.noise_scale = float(parameter[2+int(next(TexCount))])
                            Tex.noise_depth = int(parameter[2+int(next(TexCount))])
                            Tex.nabla = float(parameter[2+int(next(TexCount))])
                            Tex.cloud_type = parameter[2+int(next(TexCount))]

                        elif Tex.type == 'DISTORTED_NOISE':
                            Tex.noise_basis = parameter[2+int(next(TexCount))]
                            Tex.noise_distortion = parameter[2+int(next(TexCount))]
                            Tex.distortion = float(parameter[2+int(next(TexCount))])
                            Tex.noise_scale = float(parameter[2+int(next(TexCount))])
                            Tex.nabla = float(parameter[2+int(next(TexCount))])


                        elif Tex.type == 'IMAGE':
                            Tex.use_alpha = str_to_bool(parameter[2+int(next(TexCount))])
                            Tex.use_calculate_alpha = str_to_bool(parameter[2+int(next(TexCount))])
                            Tex.invert_alpha = str_to_bool(parameter[2+int(next(TexCount))])
                            Tex.use_flip_axis = str_to_bool(parameter[2+int(next(TexCount))])
                            Tex.extension = parameter[2+int(next(TexCount))]
                            Tex.crop_min_x = float(parameter[2+int(next(TexCount))])
                            Tex.crop_min_y = float(parameter[2+int(next(TexCount))])
                            Tex.crop_max_x = float(parameter[2+int(next(TexCount))])
                            Tex.crop_max_y = float(parameter[2+int(next(TexCount))])
                            Tex.repeat_x = int(parameter[2+int(next(TexCount))])
                            Tex.repeat_y = int(parameter[2+int(next(TexCount))])
                            Tex.use_mirror_x = str_to_bool(parameter[2+int(next(TexCount))])
                            Tex.use_mirror_y = str_to_bool(parameter[2+int(next(TexCount))])
                            Tex.extension = parameter[2+int(next(TexCount))]
                            Tex.checker_distance = float(parameter[2+int(next(TexCount))])
                            Tex.use_checker_even = str_to_bool(parameter[2+int(next(TexCount))])
                            Tex.use_checker_odd = str_to_bool(parameter[2+int(next(TexCount))])

                        elif Tex.type == 'MAGIC':
                            Tex.noise_depth = int(parameter[2+int(next(TexCount))])
                            Tex.turbulence = float(parameter[2+int(next(TexCount))])

                        elif Tex.type == 'MARBLE':
                            Tex.noise_basis = parameter[2+int(next(TexCount))]
                            Tex.marble_type = parameter[2+int(next(TexCount))]
                            Tex.noise_basis_2 = parameter[2+int(next(TexCount))]
                            Tex.noise_type = parameter[2+int(next(TexCount))]
                            Tex.noise_scale = float(parameter[2+int(next(TexCount))])
                            Tex.noise_depth = int(parameter[2+int(next(TexCount))])
                            Tex.turbulence = float(parameter[2+int(next(TexCount))])
                            Tex.nabla = float(parameter[2+int(next(TexCount))])

                        elif Tex.type == 'MUSGRAVE':
                            Tex.noise_basis = parameter[2+int(next(TexCount))]
                            Tex.musgrave_type = parameter[2+int(next(TexCount))]
                            Tex.noise_scale = float(parameter[2+int(next(TexCount))])
                            Tex.nabla = float(parameter[2+int(next(TexCount))])
                            Tex.dimension_max = float(parameter[2+int(next(TexCount))])
                            Tex.lacunarity = float(parameter[2+int(next(TexCount))])
                            Tex.octaves = float(parameter[2+int(next(TexCount))])
                            Tex.offset = float(parameter[2+int(next(TexCount))])#
                            Tex.noise_intensity = float(parameter[2+int(next(TexCount))])
                            Tex.gain = float(parameter[2+int(next(TexCount))])#

                        #elif Tex.type == 'NOISE':


                        elif Tex.type == 'STUCCI':
                            Tex.noise_basis = parameter[2+int(next(TexCount))]
                            Tex.stucci_type = parameter[2+int(next(TexCount))]
                            Tex.noise_type = parameter[2+int(next(TexCount))]
                            Tex.noise_scale = float(parameter[2+int(next(TexCount))])
                            Tex.turbulence = float(parameter[2+int(next(TexCount))])

                        elif Tex.type == 'VORONOI':
                            Tex.distance_metric = parameter[2+int(next(TexCount))]
                            Tex.minkovsky_exponent = float(parameter[2+int(next(TexCount))])
                            Tex.color_mode = parameter[2+int(next(TexCount))]
                            Tex.noise_intensity = float(parameter[2+int(next(TexCount))])
                            Tex.noise_scale = float(parameter[2+int(next(TexCount))])
                            Tex.nabla = float(parameter[2+int(next(TexCount))])
                            Tex.weight_1 = float(parameter[2+int(next(TexCount))])
                            Tex.weight_2 = float(parameter[2+int(next(TexCount))])
                            Tex.weight_3 = float(parameter[2+int(next(TexCount))])
                            Tex.weight_4 = float(parameter[2+int(next(TexCount))])

                        elif Tex.type == 'WOOD':
                            Tex.noise_basis = parameter[2+int(next(TexCount))]
                            Tex.wood_type = parameter[2+int(next(TexCount))]
                            Tex.noise_basis_2 = parameter[2+int(next(TexCount))]
                            Tex.noise_type = parameter[2+int(next(TexCount))]
                            Tex.noise_scale = float(parameter[2+int(next(TexCount))])
                            Tex.turbulence = float(parameter[2+int(next(TexCount))])
                            Tex.nabla = float(parameter[2+int(next(TexCount))])

                        
                        Tex.use_clamp = str_to_bool(parameter[2+int(next(TexCount))])
                        Tex.factor_red = float(parameter[2+int(next(TexCount))])
                        Tex.factor_green = float(parameter[2+int(next(TexCount))])
                        Tex.factor_blue = float(parameter[2+int(next(TexCount))])
                        Tex.intensity = float(parameter[2+int(next(TexCount))])
                        Tex.contrast = float(parameter[2+int(next(TexCount))])
                        Tex.saturation = float(parameter[2+int(next(TexCount))])
                        Tex.use_color_ramp = str_to_bool(parameter[2+int(next(TexCount))])
                        if Tex.use_color_ramp == True:
                            Tex.color_ramp.elements[1].position = float(parameter[2+int(next(TexCount))])
                            Tex.color_ramp.elements[0].position = float(parameter[2+int(next(TexCount))])
                            Tex.color_ramp.elements[0].color[0] = float(parameter[2+int(next(TexCount))])
                            Tex.color_ramp.elements[0].color[1] = float(parameter[2+int(next(TexCount))])
                            Tex.color_ramp.elements[0].color[2] = float(parameter[2+int(next(TexCount))])
                            Tex.color_ramp.elements[0].color[3] = float(parameter[2+int(next(TexCount))])
                            Tex.color_ramp.elements[1].color[0] = float(parameter[2+int(next(TexCount))])
                            Tex.color_ramp.elements[1].color[1] = float(parameter[2+int(next(TexCount))])
                            Tex.color_ramp.elements[1].color[2] = float(parameter[2+int(next(TexCount))])
                            Tex.color_ramp.elements[1].color[3] = float(parameter[2+int(next(TexCount))])
                    else:
                        Tex=bpy.data.textures.new(parameter[1], type='NONE')

                elif parameter[0]=='Drivers':
                    DriversList.append(parameter)

                '''
                elif 'GeometryNode' in parameter[0]:##########################################################################################################################
                    if parameter[1] not in bpy.data.node_groups:
                        NodeGroup=bpy.data.node_groups.new(parameter[1],'GeometryNodeTree')
                    NodeGroup=bpy.data.node_groups[parameter[1]]
                    if parameter[2] not in NodeGroup:#if (parameter[2] not in NodeGroup) and (not(parameter[2]=='Group Output') or (parameter[2]=='Group Input'))
                        if parameter[2] != 'Group Output':
                            if parameter[2] != 'Group Input':
                                ThisNode=NodeGroup.nodes.new(parameter[3])
                                ThisNode.name=parameter[2]
                    ThisNode=NodeGroup.nodes[parameter[2]]
                    ThisNode.location[0]=float(parameter[4])
                    ThisNode.location[1]=float(parameter[5])
                '''


        elif len(sel) == 0:
            bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))#这里添加物体


        #遍历每个文本中的物体
        for OBJParm in OBJParmList:
            OBJparameter=OBJParm.split("|")
            Param=OBJparameter
            OBJType=Param[2]
            if Param[0]=="ParentOBJ":
                OBJParentName=Param[1]


            if Param[1] not in bpy.data.objects:#

                
                if len(sel)==0:

                    if OBJType=='Cube':
                            bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(float(Param[3]), float(Param[4]), float(Param[5])), rotation=(float(Param[6]), float(Param[7]), float(Param[8])), scale=(float(Param[9]), float(Param[10]), float(Param[11])))
                            bpy.context.object.data.use_auto_smooth = str_to_bool(Param[12])
                            bpy.context.object.name=Param[1]

                    elif OBJType=='Plane':
                            bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(float(Param[3]), float(Param[4]), float(Param[5])), rotation=(float(Param[6]), float(Param[7]), float(Param[8])), scale=(float(Param[9]), float(Param[10]), float(Param[11])))
                            bpy.context.object.data.use_auto_smooth = str_to_bool(Param[12])
                            bpy.context.object.name=Param[1]

                    elif OBJType=='Sphere':
                            bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(float(Param[3]), float(Param[4]), float(Param[5])), rotation=(float(Param[6]), float(Param[7]), float(Param[8])), scale=(float(Param[9]), float(Param[10]), float(Param[11])))
                            bpy.context.object.data.use_auto_smooth = str_to_bool(Param[12])
                            bpy.context.object.name=Param[1]

                    elif OBJType=='Icosphere':
                            bpy.ops.mesh.primitive_ico_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(float(Param[3]), float(Param[4]), float(Param[5])), rotation=(float(Param[6]), float(Param[7]), float(Param[8])), scale=(float(Param[9]), float(Param[10]), float(Param[11])))
                            bpy.context.object.data.use_auto_smooth = str_to_bool(Param[12])
                            bpy.context.object.name=Param[1]

                    elif OBJType=='Cylinder':
                            bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, enter_editmode=False, align='WORLD', location=(float(Param[3]), float(Param[4]), float(Param[5])), rotation=(float(Param[6]), float(Param[7]), float(Param[8])), scale=(float(Param[9]), float(Param[10]), float(Param[11])))
                            bpy.context.object.data.use_auto_smooth = str_to_bool(Param[12])
                            bpy.context.object.name=Param[1]

                    elif OBJType=='Cone':
                            bpy.ops.mesh.primitive_cone_add(radius1=1, radius2=0, depth=2, enter_editmode=False, align='WORLD', location=(float(Param[3]), float(Param[4]), float(Param[5])), rotation=(float(Param[6]), float(Param[7]), float(Param[8])), scale=(float(Param[9]), float(Param[10]), float(Param[11])))
                            bpy.context.object.data.use_auto_smooth = str_to_bool(Param[12])
                            bpy.context.object.name=Param[1]

                    elif OBJType=='Torus':#
                            bpy.ops.mesh.primitive_torus_add(align='WORLD', location=(float(Param[3]), float(Param[4]), float(Param[5])), rotation=(float(Param[6]), float(Param[7]), float(Param[8])), major_radius=float(Param[9]), minor_radius=0.25, abso_major_rad=1.25, abso_minor_rad=0.75)
                            bpy.context.object.data.use_auto_smooth = str_to_bool(Param[12])
                            bpy.context.object.name=Param[1]

                    elif OBJType=='Circle':
                            bpy.ops.mesh.primitive_circle_add(enter_editmode=False, align='WORLD', location=(float(Param[3]), float(Param[4]), float(Param[5])), rotation=(float(Param[6]), float(Param[7]), float(Param[8])), scale=(float(Param[9]), float(Param[10]), float(Param[11])))
                            bpy.context.object.data.use_auto_smooth = str_to_bool(Param[12])
                            bpy.context.object.name=Param[1]

                    elif OBJType=='Grid':
                            bpy.ops.mesh.primitive_grid_add(size=2, enter_editmode=False, align='WORLD', location=(float(Param[3]), float(Param[4]), float(Param[5])), rotation=(float(Param[6]), float(Param[7]), float(Param[8])), scale=(float(Param[9]), float(Param[10]), float(Param[11])))
                            bpy.context.object.data.use_auto_smooth = str_to_bool(Param[12])
                            bpy.context.object.name=Param[1]

                    elif 'Suzanne' in OBJType:
                            bpy.ops.mesh.primitive_monkey_add(size=2, enter_editmode=False, align='WORLD', location=(float(Param[3]), float(Param[4]), float(Param[5])), rotation=(float(Param[6]), float(Param[7]), float(Param[8])), scale=(float(Param[9]), float(Param[10]), float(Param[11])))
                            bpy.context.object.data.use_auto_smooth = str_to_bool(Param[12])
                            bpy.context.object.name=Param[1]

                    elif 'BezierCurve' in OBJType:
                            bpy.ops.curve.primitive_bezier_curve_add(radius=float(Param[9]), enter_editmode=False, align='WORLD', location=(float(Param[3]), float(Param[4]), float(Param[5])), rotation=(float(Param[6]), float(Param[7]), float(Param[8])), scale=(1, 1, 1))
                            bpy.context.object.name=Param[1]

                    elif 'BezierCircle' in OBJType:
                            bpy.ops.curve.primitive_bezier_circle_add(radius=float(Param[9]), enter_editmode=False, align='WORLD', location=(float(Param[3]), float(Param[4]), float(Param[5])), rotation=(float(Param[6]), float(Param[7]), float(Param[8])), scale=(1, 1, 1))
                            bpy.context.object.name=Param[1]

                    elif'NurbsCurve' in OBJType:
                            bpy.ops.curve.primitive_nurbs_curve_add(radius=float(Param[9]), enter_editmode=False, align='WORLD', location=(float(Param[3]), float(Param[4]), float(Param[5])), rotation=(float(Param[6]), float(Param[7]), float(Param[8])), scale=(1, 1, 1))
                            bpy.context.object.name=Param[1]

                    elif 'NurbsCircle' in OBJType:
                            bpy.ops.curve.primitive_nurbs_circle_add(radius=float(Param[9]), enter_editmode=False, align='WORLD', location=(float(Param[3]), float(Param[4]), float(Param[5])), rotation=(float(Param[6]), float(Param[7]), float(Param[8])), scale=(1, 1, 1))
                            bpy.context.object.name=Param[1]

                    elif 'NurbsPath' in OBJType:
                            bpy.ops.curve.primitive_nurbs_path_add(radius=float(Param[9]), enter_editmode=False, align='WORLD', location=(float(Param[3]), float(Param[4]), float(Param[5])), rotation=(float(Param[6]), float(Param[7]), float(Param[8])), scale=(1, 1, 1))
                            bpy.context.object.name=Param[1]

                    elif 'Lattice' in OBJType:
                            bpy.ops.object.add(radius=float(Param[9]), type='LATTICE', enter_editmode=False, align='WORLD', location=(float(Param[3]), float(Param[4]), float(Param[5])), rotation=(float(Param[6]), float(Param[7]), float(Param[8])), scale=(1, 1, 1))
                            bpy.context.object.name=Param[1]

                    elif ('Empty' in OBJType) or ('Field' in OBJType):
                            bpy.ops.object.empty_add(type='SINGLE_ARROW', radius=float(Param[9]), align='WORLD', location=(float(Param[3]), float(Param[4]), float(Param[5])), rotation=(float(Param[6]), float(Param[7]), float(Param[8])), scale=(1, 1, 1))
                            bpy.context.object.name=Param[1]

                    elif 'Mball' in OBJType:
                            bpy.ops.object.metaball_add(type='CUBE', radius=float(Param[9]), enter_editmode=False, align='WORLD', location=(float(Param[3]), float(Param[4]), float(Param[5])), rotation=(float(Param[6]), float(Param[7]), float(Param[8])), scale=(1, 1, 1))
                            bpy.context.object.name=Param[1]

                    elif 'SurfCurve' in OBJType:
                            bpy.ops.curve.primitive_nurbs_surface_curve_add(radius=float(Param[9]), enter_editmode=False, align='WORLD', location=(float(Param[3]), float(Param[4]), float(Param[5])), rotation=(float(Param[6]), float(Param[7]), float(Param[8])), scale=(1, 1, 1))
                            bpy.context.object.name=Param[1]

                    elif 'Surface' in OBJType:
                            bpy.ops.curve.primitive_nurbs_surface_cylinder_add(radius=float(Param[9]), enter_editmode=False, align='WORLD', location=(float(Param[3]), float(Param[4]), float(Param[5])), rotation=(float(Param[6]), float(Param[7]), float(Param[8])), scale=(1, 1, 1))
                            bpy.context.object.name=Param[1]

                    elif 'SurfCircle' in OBJType:
                            bpy.ops.curve.primitive_nurbs_surface_circle_add(radius=float(Param[9]), enter_editmode=False, align='WORLD', location=(float(Param[3]), float(Param[4]), float(Param[5])), rotation=(float(Param[6]), float(Param[7]), float(Param[8])), scale=(1, 1, 1))
                            bpy.context.object.name=Param[1]

                    elif 'SurfPatch' in OBJType:
                            bpy.ops.curve.primitive_nurbs_surface_surface_add(radius=float(Param[9]), enter_editmode=False, align='WORLD', location=(float(Param[3]), float(Param[4]), float(Param[5])), rotation=(float(Param[6]), float(Param[7]), float(Param[8])), scale=(1, 1, 1))
                            bpy.context.object.name=Param[1]

                    elif 'SurfSphere' in OBJType:
                            bpy.ops.curve.primitive_nurbs_surface_sphere_add(radius=float(Param[9]), enter_editmode=False, align='WORLD', location=(float(Param[3]), float(Param[4]), float(Param[5])), rotation=(float(Param[6]), float(Param[7]), float(Param[8])), scale=(1, 1, 1))
                            bpy.context.object.name=Param[1]

                    elif 'SurfTorus' in OBJType:
                            bpy.ops.curve.primitive_nurbs_surface_torus_add(radius=float(Param[9]), enter_editmode=False, align='WORLD', location=(float(Param[3]), float(Param[4]), float(Param[5])), rotation=(float(Param[6]), float(Param[7]), float(Param[8])), scale=(1, 1, 1))
                            bpy.context.object.name=Param[1]

                    elif 'Stroke' in OBJType:
                            bpy.ops.object.gpencil_add(radius=float(Param[9]), align='WORLD', location=(float(Param[3]), float(Param[4]), float(Param[5])), rotation=(float(Param[6]), float(Param[7]), float(Param[8])), scale=(1, 1, 1), type='STROKE')
                            bpy.context.object.name=Param[1]

                    elif ('Armature' in OBJType) or ('metarig' in OBJType):
                            bpy.ops.object.armature_add(radius=float(Param[9]), enter_editmode=False, align='WORLD', location=(float(Param[3]), float(Param[4]), float(Param[5])), rotation=(float(Param[6]), float(Param[7]), float(Param[8])), scale=(1, 1, 1))
                            bpy.context.object.name=Param[1]

                    elif 'GenLine' in OBJType:
                        if 'GenLineKit' in OBJType:
                            bpy.context.scene.amProperties.GenLineEnum = 'GenLineKit'
                        elif 'GenLineStruct' in OBJType:
                            bpy.context.scene.amProperties.GenLineEnum = 'GenLineStruct'
                        elif 'GenLineWeapon' in OBJType:
                            bpy.context.scene.amProperties.GenLineEnum = 'GenLineWeapon'
                        else:
                            bpy.context.scene.amProperties.GenLineEnum = 'GenLineStruct'
                        bpy.ops.object.bl_genline()
                        bpy.context.object.name=Param[1]


                    elif len(OBJParmList)>1:#集成这里绕道算了
                        bpy.ops.object.select_all(action='DESELECT')
                        bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
                        bpy.context.object.name=Param[1]

                    else:#集成问题在这里
                        bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))#这里添加物体
                        bpy.context.object.name=Param[1]


                #elif len(sel) == 1:
                        #bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))#这里添加物体
                    #bpy.context.object.name=Param[1]

                elif (len(sel)==1) and (len(OBJParmList)==1):
                    bpy.context.object.name=Param[1]

                elif (len(sel)>=1) and (len(OBJParmList)>1):
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
                    bpy.context.object.name=Param[1]

                else:
                    for ob in sel:
                        ob.name=Param[1]

            else:
                #
                bpy.data.objects[Param[1]].hide_viewport = False

            if not ((amProperty.GenMechEnum == 'MechPro') or (amProperty.GenMechEnum == 'Helmet') or (amProperty.GenMechEnum == 'Mechfy') or (amProperty.GenMechEnum == '')):#选择的物体为parentOBJ
                #for ob in sel:
                bpy.data.objects[Param[1]].location[0] = float(Param[3])
                bpy.data.objects[Param[1]].location[1] = float(Param[4])
                bpy.data.objects[Param[1]].location[2] = float(Param[5])
                bpy.data.objects[Param[1]].rotation_euler[0] = float(Param[6])
                bpy.data.objects[Param[1]].rotation_euler[1] = float(Param[7])
                bpy.data.objects[Param[1]].rotation_euler[2] = float(Param[8])
                bpy.data.objects[Param[1]].scale[0] = float(Param[9])
                bpy.data.objects[Param[1]].scale[1] = float(Param[10])
                bpy.data.objects[Param[1]].scale[2] = float(Param[11])
                if bpy.data.objects[Param[1]].type=='MESH':
                    bpy.data.objects[Param[1]].data.use_auto_smooth = str_to_bool(Param[12])



            if (not ((amProperty.GenMechEnum == 'MechPro') or (amProperty.GenMechEnum == 'Helmet') or (amProperty.GenMechEnum == 'Mechfy') or (amProperty.GenMechEnum == ''))) and Param[13].isdigit() == True:
                
                
                if bpy.data.objects[Param[1]].type=='MESH':
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.select_all(action='SELECT')
                elif (bpy.data.objects[Param[1]].type=='SURFACE') or (bpy.data.objects[Param[1]].type=='CURVE'):
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.curve.select_all(action='SELECT')
                elif bpy.data.objects[Param[1]].type=='META':
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mball.select_all(action='SELECT')
                elif bpy.data.objects[Param[1]].type=='GPENCIL':
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.gpencil.select_all(action='SELECT')
                elif bpy.data.objects[Param[1]].type=='ARMATURE':
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.armature.select_all(action='SELECT')


                if bpy.data.objects[Param[1]].type !='EMPTY':
                    bpy.ops.transform.translate(value=(float(Param[13]), float(Param[14]), float(Param[15])))
                    bpy.ops.transform.rotate(value=float(Param[16]), orient_axis='X')
                    bpy.ops.transform.rotate(value=float(Param[17]), orient_axis='Y')
                    bpy.ops.transform.rotate(value=float(Param[18]), orient_axis='Z')
                    bpy.ops.transform.resize(value=(float(Param[19]),float(Param[20]), float(Param[21])))
                    bpy.ops.object.mode_set(mode='OBJECT')
                    bpy.ops.object.select_all(action='DESELECT')


        if not ((amProperty.GenMechEnum == 'MechPro') or (amProperty.GenMechEnum == 'Helmet') or (amProperty.GenMechEnum == 'Mechfy') or (amProperty.GenMechEnum == '')):
            Obj=bpy.data.objects[OBJParentName]#bpy.context.object
            NodeName=''
            nodegroupName=[]
            OutName=[]
            OutLink=[]
            IntName=[]
            IntLink=[]
            NodeInputsNum=0
            NodeInputsName=[]
            f = open(File, encoding='utf-8')#f = open(File, "r")
            for line in f:
                NodeParm = line.split("|")
                if 'GeometryNode' in NodeParm[0]:##########################################################################################################################
                    #NodesMod=Obj.modifiers[NodeParm[1]]
                    WeCanAddNode=False
                    NodeName=NodeParm[1]
                    if NodeName not in Obj.modifiers:
                        NodesMod = Obj.modifiers.new(NodeName,'NODES')
                        NodesMod.node_group.name = NodeName
                        NodeGroup=NodesMod.node_group#bpy.data.node_groups[NodeParm[1]]
                        node_group=bpy.data.node_groups[NodeParm[1]]
                    else:
                        NodeGroup=bpy.data.node_groups[NodeParm[1]]
                        node_group=NodeGroup

                    if (NodeParm[2] not in NodeGroup) and (NodeParm[2] != 'Group Output') and (NodeParm[2] != 'Group Input'):#if (NodeParm[2] not in NodeGroup) and (not(NodeParm[2]=='Group Output') or (NodeParm[2]=='Group Input'))
                        #if NodeParm[2] != 'Group Output':
                            #if NodeParm[2] != 'Group Input':
                        #if (NodeParm[3] != 'GeometryNodeAttributeCombineXYZ') and
                        if bpy.app.version >= (2, 93, 0):
                            Node=NodeGroup.nodes.new(NodeParm[3])
                            Node.name=NodeParm[2]
                            #WeCanAddNode=True
                        elif (bpy.app.version < (2, 93, 0)) and (NodeParm[3] != 'GeometryNodeAttributeCombineXYZ') and (NodeParm[3] != 'GeometryNodeAttributeProximity') and (NodeParm[3] != 'GeometryNodeAttributeSampleTexture') and (NodeParm[3] != 'GeometryNodeAttributeSeparateXYZ') and (NodeParm[3] != 'GeometryNodeCollectionInfo') and (NodeParm[3] != 'GeometryNodeIsViewport') and (NodeParm[3] != 'FunctionNodeInputString') and (NodeParm[3] != 'GeometryNodeSubdivisionSurfaceSimple') and (NodeParm[3] != 'GeometryNodePointsToVolume') and (NodeParm[3] != 'GeometryNodeVolumeToMesh'):
                            Node=NodeGroup.nodes.new(NodeParm[3])
                            Node.name=NodeParm[2]
                            #WeCanAddNode=True
                    #if WeCanAddNode==True:
                    if (bpy.app.version < (2, 93, 0)) and (NodeParm[3] != 'GeometryNodeAttributeCombineXYZ') and (NodeParm[3] != 'GeometryNodeAttributeProximity') and (NodeParm[3] != 'GeometryNodeAttributeSampleTexture') and (NodeParm[3] != 'GeometryNodeAttributeSeparateXYZ') and (NodeParm[3] != 'GeometryNodeCollectionInfo') and (NodeParm[3] != 'GeometryNodeIsViewport') and (NodeParm[3] != 'FunctionNodeInputString') and (NodeParm[3] != 'GeometryNodeSubdivisionSurfaceSimple') and (NodeParm[3] != 'GeometryNodePointsToVolume') and (NodeParm[3] != 'GeometryNodeVolumeToMesh'): 
                        WeCanAddNode=True
                    elif bpy.app.version >= (2, 93, 0):
                        WeCanAddNode=True

                    if WeCanAddNode==True:
                        Node=NodeGroup.nodes[NodeParm[2]]
                        Node.location[0]=float(NodeParm[4])
                        Node.location[1]=float(NodeParm[5])
                        NodeCount=count(1, 1)
                        if (Node.type=='ATTRIBUTE_COLOR_RAMP') or (Node.type=='VALTORGB'):
                            Node.color_ramp.color_mode=NodeParm[8+int(next(NodeCount))]
                            Node.color_ramp.interpolation=NodeParm[8+int(next(NodeCount))]
                            Node.color_ramp.hue_interpolation=NodeParm[8+int(next(NodeCount))]
                            for Num in range(int(NodeParm[8])-3):
                                Node.color_ramp.elements[Num].position=float(NodeParm[8+int(next(NodeCount))])
                                Node.color_ramp.elements[Num].color[0]=float(NodeParm[8+int(next(NodeCount))])
                                Node.color_ramp.elements[Num].color[1]=float(NodeParm[8+int(next(NodeCount))])
                                Node.color_ramp.elements[Num].color[2]=float(NodeParm[8+int(next(NodeCount))])
                                Node.color_ramp.elements[Num].color[3]=float(NodeParm[8+int(next(NodeCount))])
                            '''
                            bpy.data.node_groups['GeometryNodes'].nodes.active.color_ramp.color_mode
                            bpy.data.node_groups['GeometryNodes'].nodes.active.color_ramp.interpolation

                            bpy.data.node_groups['GeometryNodes'].nodes.active.color_ramp.elements[0].color[0]
                            bpy.data.node_groups['GeometryNodes'].nodes.active.color_ramp.elements[0].position
                            '''
                        elif (Node.type=='ATTRIBUTE_COMPARE') or (Node.type=='ATTRIBUTE_MATH'):
                            Node.operation=NodeParm[8+int(next(NodeCount))]
                            Node.input_type_a=NodeParm[8+int(next(NodeCount))]
                            Node.input_type_b=NodeParm[8+int(next(NodeCount))]
                            
                            '''
                            bpy.data.node_groups["GeometryNodes"].nodes["Attribute Compare"].operation = 'NOT_EQUAL'
                            bpy.data.node_groups["GeometryNodes"].nodes["Attribute Compare"].input_type_a = 'FLOAT'
                            bpy.data.node_groups["GeometryNodes"].nodes["Attribute Compare"].input_type_b = 'COLOR'
                            '''

                        elif (Node.type=='ATTRIBUTE_FILL') or (Node.type=='ATTRIBUTE_RANDOMIZE'):
                            Node.data_type=NodeParm[8+int(next(NodeCount))]
                            
                            #bpy.data.node_groups["GeometryNodes"].nodes["Attribute Fill"].data_type = 'FLOAT_VECTOR'

                        elif Node.type=='ATTRIBUTE_MIX':
                            Node.blend_type=NodeParm[8+int(next(NodeCount))]
                            Node.input_type_factor=NodeParm[8+int(next(NodeCount))]
                            Node.input_type_a=NodeParm[8+int(next(NodeCount))]
                            Node.input_type_b=NodeParm[8+int(next(NodeCount))]

                            '''
                            bpy.data.node_groups["GeometryNodes"].nodes["Attribute Mix"].blend_type = 'MIX'
                            bpy.data.node_groups["GeometryNodes"].nodes["Attribute Mix"].input_type_factor = 'FLOAT'
                            bpy.data.node_groups["GeometryNodes"].nodes["Attribute Mix"].input_type_a = 'FLOAT'
                            bpy.data.node_groups["GeometryNodes"].nodes["Attribute Mix"].input_type_b = 'VECTOR'
                            '''

                        elif Node.type=='ATTRIBUTE_SAMPLE_TEXTURE':# and (bpy.app.version >= (2, 93, 0))
                            Node.texture=to_Tex(NodeParm[8+int(next(NodeCount))])#



                        elif Node.type=='ATTRIBUTE_VECTOR_MATH':
                            Node.operation=NodeParm[8+int(next(NodeCount))]
                            Node.input_type_a=NodeParm[8+int(next(NodeCount))]
                            Node.input_type_b=NodeParm[8+int(next(NodeCount))]
                            Node.input_type_c=NodeParm[8+int(next(NodeCount))]
                            '''
                            bpy.data.node_groups["GeometryNodes"].nodes["Attribute Vector Math"].operation = 'SUBTRACT'
                            bpy.data.node_groups["GeometryNodes"].nodes["Attribute Vector Math"].input_type_a = 'ATTRIBUTE'
                            bpy.data.node_groups["GeometryNodes"].nodes["Attribute Vector Math"].input_type_b = 'VECTOR'
                            bpy.data.node_groups["GeometryNodes"].nodes["Attribute Vector Math"].input_type_c = 'VECTOR'
                            '''


                        elif (Node.type=='COLLECTION_INFO') or (Node.type=='OBJECT_INFO'):
                            Node.transform_space=NodeParm[8+int(next(NodeCount))]
                            #bpy.data.node_groups["GeometryNodes"].nodes["Collection Info"].transform_space = 'ORIGINAL'


                        elif Node.type=='VALUE':
                            Node.outputs[0].default_value=float(NodeParm[8+int(next(NodeCount))])
                            #bpy.data.node_groups["GeometryNodes"].nodes["Value"].outputs[0].default_value = 0.5

                        elif Node.type=='INPUT_VECTOR':
                            Node.vector[0]=float(NodeParm[8+int(next(NodeCount))])
                            Node.vector[1]=float(NodeParm[8+int(next(NodeCount))])
                            Node.vector[2]=float(NodeParm[8+int(next(NodeCount))])

                            '''
                            bpy.data.node_groups["GeometryNodes"].nodes["Vector"].vector[0] = 0
                            bpy.data.node_groups["GeometryNodes"].nodes["Vector"].vector[1] = 0
                            bpy.data.node_groups["GeometryNodes"].nodes["Vector"].vector[2] = 0
                            '''


                        elif (Node.type=='BOOLEAN') or (Node.type=='BOOLEAN_MATH') or (Node.type=='FLOAT_COMPARE') or (Node.type=='VECT_MATH'):
                            Node.operation=NodeParm[8+int(next(NodeCount))]
                            #bpy.data.node_groups["GeometryNodes"].nodes["Boolean"].operation = 'INTERSECT'

                        elif Node.type=='TRIANGULATE':
                            Node.quad_method=NodeParm[8+int(next(NodeCount))]
                            Node.ngon_method=NodeParm[8+int(next(NodeCount))]

                            #bpy.data.node_groups["GeometryNodes"].nodes["Triangulate"].quad_method = 'FIXED_ALTERNATE'
                            #bpy.data.node_groups["GeometryNodes"].nodes["Triangulate"].ngon_method = 'CLIP'

                        elif Node.type=='ALIGN_ROTATION_TO_VECTOR':
                            Node.axis=NodeParm[8+int(next(NodeCount))]
                            Node.input_type_factor=NodeParm[8+int(next(NodeCount))]
                            Node.input_type_vector=NodeParm[8+int(next(NodeCount))]
                            '''
                            bpy.data.node_groups["GeometryNodes"].nodes["Align Rotation to Vector"].axis = 'Y'
                            bpy.data.node_groups["GeometryNodes"].nodes["Align Rotation to Vector"].input_type_factor = 'ATTRIBUTE'
                            bpy.data.node_groups["GeometryNodes"].nodes["Align Rotation to Vector"].input_type_vector = 'VECTOR'
                            '''



                        elif Node.type=='POINT_DISTRIBUTE':
                            Node.distribute_method=NodeParm[8+int(next(NodeCount))]
                            #bpy.data.node_groups["GeometryNodes"].nodes["Point Distribute"].distribute_method = 'POISSON'

                        elif Node.type=='POINT_INSTANCE':
                            POINT_INSTANCE=8+int(next(NodeCount))
                            #POINT_INSTANCE=NodeParm[8+int(next(NodeCount))]
                            Node.instance_type=NodeParm[POINT_INSTANCE]
                            if len(NodeParm[POINT_INSTANCE+1])>=4:#漏写补偿
                                Node.use_whole_collection=str_to_bool(NodeParm[8+int(next(NodeCount))])
                            #bpy.data.node_groups["GeometryNodes"].nodes["Point Instance"].instance_type = 'OBJECT'


                        elif Node.type=='EULER':
                            Node.type=NodeParm[8+int(next(NodeCount))]
                            Node.space=NodeParm[8+int(next(NodeCount))]
                            Node.input_type_rotation=NodeParm[8+int(next(NodeCount))]
                            #bpy.data.node_groups["GeometryNodes"].nodes["Point Rotate"].type = 'EULER'
                            #bpy.data.node_groups["GeometryNodes"].nodes["Point Rotate"].space = 'POINT'
                            #bpy.data.node_groups["GeometryNodes"].nodes["Point Rotate"].input_type_rotation = 'ATTRIBUTE'


                        elif (Node.type=='POINT_SCALE') or (Node.type=='POINT_TRANSLATE'):
                            Node.input_type=NodeParm[8+int(next(NodeCount))]
                            #bpy.data.node_groups["GeometryNodes"].nodes["Point Scale"].input_type = 'ATTRIBUTE'


                        elif Node.type=='POINTS_TO_VOLUME':
                            Node.resolution_mode=NodeParm[8+int(next(NodeCount))]
                            Node.input_type_radius=NodeParm[8+int(next(NodeCount))]
                            #bpy.data.node_groups["GeometryNodes"].nodes["Points to Volume"].resolution_mode = 'VOXEL_AMOUNT'
                            #bpy.data.node_groups["GeometryNodes"].nodes["Points to Volume"].input_type_radius = 'FLOAT'


                        elif Node.type=='CLAMP':
                            Node.clamp_type=NodeParm[8+int(next(NodeCount))]
                            #bpy.data.node_groups["GeometryNodes"].nodes["Clamp"].clamp_type = 'RANGE'


                        elif Node.type=='MAP_RANGE':
                            Node.interpolation_type=NodeParm[8+int(next(NodeCount))]
                            #bpy.data.node_groups["GeometryNodes"].nodes["Map Range"].interpolation_type = 'SMOOTHERSTEP'

                        elif Node.type=='MATH':
                            Node.operation=NodeParm[8+int(next(NodeCount))]
                            Node.use_clamp=str_to_bool(NodeParm[8+int(next(NodeCount))])
                            '''
                            bpy.data.node_groups["GeometryNodes"].nodes["Math"].operation = 'CEIL'
                            bpy.data.node_groups["GeometryNodes"].nodes["Math"].use_clamp = True
                            '''

                        elif (Node.type=='ATTRIBUTE_COMBINE_XYZ') and (bpy.app.version >= (2, 93, 0)):
                            Node.input_type_x = NodeParm[8+int(next(NodeCount))]
                            Node.input_type_y = NodeParm[8+int(next(NodeCount))]
                            Node.input_type_z = NodeParm[8+int(next(NodeCount))]

                        elif (Node.type=='ATTRIBUTE_PROXIMITY') and (bpy.app.version >= (2, 93, 0)):
                            Node.target_geometry_element = NodeParm[8+int(next(NodeCount))]

                        elif (Node.type=='ATTRIBUTE_SEPARATE_XYZ') and (bpy.app.version >= (2, 93, 0)):
                            Node.input_type = NodeParm[8+int(next(NodeCount))]

                        elif (Node.type=='INPUT_STRING') and (bpy.app.version >= (2, 93, 0)):
                            Node.string = NodeParm[8+int(next(NodeCount))]

                        elif (Node.type=='VOLUME_TO_MESH') and (bpy.app.version >= (2, 93, 0)):
                            Node.resolution_mode = NodeParm[8+int(next(NodeCount))]



                        
                        #if (bpy.app.version < (2, 93, 0)) and (Node.type=='ATTRIBUTE_RANDOMIZE'):
                            #InputsNum=int(NodeParm[6])-2
                        #else:
                            #InputsNum=int(NodeParm[6])


                        InputsNum=int(NodeParm[6])
                        InputsRealNum=int(len(Node.inputs))

                        DiffValue=InputsNum-InputsRealNum#多出来或少的部分

                        OutputsNum=int(NodeParm[7])
                        #OutputRealNum=int(len(Node.outputs))

                        if InputsNum>=1:
                            for Input in range(InputsRealNum):
                                #next(NodeCount)
                                if Node.inputs[Input].type == 'GEOMETRY':
                                    next(NodeCount)
                                elif Node.inputs[Input].type == 'VECTOR':
                                    Node.inputs[Input].default_value[0]=float(NodeParm[8+int(next(NodeCount))])
                                    Node.inputs[Input].default_value[1]=float(NodeParm[8+int(next(NodeCount))])
                                    Node.inputs[Input].default_value[2]=float(NodeParm[8+int(next(NodeCount))])
                                elif Node.inputs[Input].type == 'RGBA':
                                    Node.inputs[Input].default_value[0]=float(NodeParm[8+int(next(NodeCount))])
                                    Node.inputs[Input].default_value[1]=float(NodeParm[8+int(next(NodeCount))])
                                    Node.inputs[Input].default_value[2]=float(NodeParm[8+int(next(NodeCount))])
                                    Node.inputs[Input].default_value[3]=float(NodeParm[8+int(next(NodeCount))])
                                elif Node.inputs[Input].type == 'INT':
                                    Node.inputs[Input].default_value=int(NodeParm[8+int(next(NodeCount))])
                                elif Node.inputs[Input].type == 'VALUE':
                                    Node.inputs[Input].default_value=float(NodeParm[8+int(next(NodeCount))])
                                elif Node.inputs[Input].type == 'STRING':
                                    Node.inputs[Input].default_value=NodeParm[8+int(next(NodeCount))]
                                elif Node.inputs[Input].type == 'OBJECT':
                                    Node.inputs[Input].default_value=to_Obj(NodeParm[8+int(next(NodeCount))])
                                elif Node.inputs[Input].type == 'COLLECTION':
                                    Node.inputs[Input].default_value=to_Col(NodeParm[8+int(next(NodeCount))])
                                elif Node.inputs[Input].type == 'BOOLEAN':
                                    Node.inputs[Input].default_value=str_to_bool(NodeParm[8+int(next(NodeCount))])


                        if OutputsNum>=1:
                            #ThisNodeName=[]
                            OutputLink=[]

                            #if (bpy.app.version < (2, 93, 0)) and (Node.type=='ATTRIBUTE_RANDOMIZE'):
                                #next(NodeCount)
                                #next(NodeCount)

                            #if DiffValue >0:
                                #for i in range(DiffValue):
                                    #next(NodeCount)
                            #elif DiffValue<0:
                                #for i in range(abs(DiffValue)):


                            for Output in range(OutputsNum):
                                NumOutput=NodeParm[8+int(next(NodeCount))+DiffValue]
                                OutputLink.append(NumOutput)


                            for Output in range(OutputsNum):
                                if OutputLink[Output] !='NoLinks':
                                    for NewLink in range(int(OutputLink[Output])):#对于每个连接数 （获取的单个输出口连接数）
                                        nodegroupName.append(node_group.name)
                                        OutName.append(Node.name)#节点1
                                        OutLink.append(Output)#节点1出口
                                        #OutLink.append(NewLink)#第几个连接
                                        
                                        IntName.append(NodeParm[8+int(next(NodeCount))+DiffValue])#节点2
                                        IntLink.append(NodeParm[8+int(next(NodeCount))+DiffValue])#节点2进口



                        if ('Node_Label' in NodeParm) and ((bpy.app.version >= (2, 93, 0)) or (Node.type=='FRAME')):#2.92这有问题，先不弄节点颜色等
                            #if bpy.app.version >= (2, 93, 0):#2.93以下的不识别中文
                            NodeParm[8+int(next(NodeCount))]
                            Node.label = NodeParm[8+int(next(NodeCount))]
                            Node.use_custom_color = str_to_bool(NodeParm[8+int(next(NodeCount))])
                            Node.color[0] = float(NodeParm[8+int(next(NodeCount))])
                            Node.color[1] = float(NodeParm[8+int(next(NodeCount))])
                            Node.color[2] = float(NodeParm[8+int(next(NodeCount))])
                            Node.height = float(NodeParm[8+int(next(NodeCount))])
                            Node.width = float(NodeParm[8+int(next(NodeCount))])
                            if Node.type=='FRAME':
                                Node.label_size = int(NodeParm[8+int(next(NodeCount))])
                                Node.shrink = str_to_bool(NodeParm[8+int(next(NodeCount))])

                        
                        if (Node.type=='GROUP_INPUT') and (OutputsNum>=3):
                            NodeInputsNum=OutputsNum
                            for i in range(OutputsNum):
                                
                                NodeInputsName.append(NodeParm[8+int(next(NodeCount))])
                                #bpy.ops.node.tree_socket_add(in_out='IN')
                            



            outputNode=[]
            #print('节点组: '+str(nodegroupName))#列出来 节点1连节点2尾
            print('节点1: '+str(OutName))
            print('节点1出口: '+str(OutLink))#0
            print('节点2: '+str(IntName))
            print('节点2进口: '+str(IntLink))
            print(NodeInputsName)
            #try:
            LinkNum=len(OutName)

            for NodeLink in range(LinkNum):
                Link_group=bpy.data.node_groups[nodegroupName[NodeLink]]

                
                OutNode=Link_group.nodes[OutName[NodeLink]]
                '''
                if (OutNode.type=='GROUP_INPUT') and (NodeInputsNum!=0) and (OutName[NodeLink] !='Geometry'):# and (LinkOut.type!='GEOMETRY'):
                    outputNode.append(OutNode)
                    LinkOutint=len(OutNode.outputs)-1
                    #LinkOutint=OutNode#int(next(InputNumCount))
                    #print(LinkOutint)
                    #if LinkOut.name
                    LinkOut=OutNode.outputs[LinkOutint]

                    #if 'Geometry' in LinkOut.name:#LinkOut.type=='GEOMETRY':
                        #LinkOut=OutNode.outputs[0]
                    #else:
                    #LinkOut=OutNode.outputs[LinkOutint]
                else:
                '''
                LinkOut=OutNode.outputs[OutLink[NodeLink]]#尾outputs

                IntNode=Link_group.nodes[IntName[NodeLink]]
                if IntLink[NodeLink].isdigit():
                    LinkInt=IntNode.inputs[int(IntLink[NodeLink])]#头inputs
                else:
                    LinkInt=IntNode.inputs[IntLink[NodeLink]]

                if OutName[NodeLink]=='Value':
                    print('尾')
                    print(OutNode)
                    print(LinkOut)

                    print('头')
                    print(IntNode)
                    print(LinkInt)


                Link_group.links.new(LinkOut,LinkInt)#尾连头
            '''
            InputNumCount=count(0, 1)
            if outputNode:
                for groupnode in outputNode:
                    thisintput=groupnode.outputs
                    for intputout in thisintput:
                        intputout.name=NodeInputsName[int(next(InputNumCount))]
            '''


            '''
            except:#抛出异常时读取的可能是前一批次节点的
                print(NodeLink)
                print(len(OutName))
                print('尾')
                print(OutNode)
                print(LinkOut)

                print('头')
                print(IntNode)#bpy.data.node_groups['Geometry Nodes'].nodes['Math'].select=True
                print(LinkInt)#凶手是Math 
            '''



            if len(NodeName)>0:
                bpy.ops.object.modifier_remove(modifier=NodeName)


        for OBJParm in OBJParmList:
            OBJparameter=OBJParm.split("|")
            Param=OBJparameter
            OBJName=Param[1]
            bpy.data.objects[OBJName].select_set(True)
        #if OBJName !=OBJParentName:
            #bpy.data.objects[OBJName].parent = bpy.data.objects[OBJParentName]
        if len(OBJParentName)!=0:
            bpy.context.view_layer.objects.active = bpy.data.objects[OBJParentName]#
            if amProperty.PresetParentBool ==True:
                bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)#
        sel = bpy.context.selected_objects



        if col_name not in bpy.data.collections:

            for obj in sel:
                    bpy.context.view_layer.objects.active = obj
                    #bpy.ops.object.select_all(action='SELECT')
                    obj.select_set(True)

                    GenMechObj = bpy.data.objects[obj.name]
                    cube_collection = find_collection(bpy.context, GenMechObj)#根据物体查找到它所在的合集
                    new_collection = make_collection(col_name,cube_collection)
                    col = bpy.data.collections.get(col_name)#4
                    col.objects.link(GenMechObj)
                    cube_collection.objects.unlink(GenMechObj)
                    move_to_collection(col_name,"2GenMech")
            

        else:
            for obj in sel:
                bpy.context.view_layer.objects.active = obj
                obj.select_set(True)
                GenMechObj = bpy.data.objects[obj.name]
                cube_collection = find_collection(bpy.context, GenMechObj)
                col = bpy.data.collections.get(col_name)#4
                #if '1GenLine' not in obj.name:
                if obj.name not in col.objects:
                    col.objects.link(GenMechObj)
                    cube_collection.objects.unlink(GenMechObj)
            move_to_collection(col_name,"2GenMech")

        

        #if 'metarig' in rig.name :请添加这个判断
        for ob in sel:
            
            bpy.context.view_layer.objects.active = ob
            #for mod in [m for m in ob.modifiers if m.type != 'SKIN']:
            #if len(ob.data.vertices) <=900000:# #防误触 顶点小于的时候才能运行
            if ob.type =='MESH':


                #暂时切勿更改以下修改器名字
                if len(ob.material_slots) <= 1:##如果没有槽，那么我们追加创建槽和分配
                    bpy.ops.object.material_slot_remove()
                    bpy.ops.object.material_slot_add()
                    bpy.ops.object.material_slot_add()
                    bpy.ops.object.material_slot_add()
                    bpy.ops.object.material_slot_add()
                    bpy.ops.object.material_slot_add()

                    MatList=''
                    for materials,value in  bpy.data.materials.items():
                        MatList+=" "+materials
                    
                    filepath = os.path.join(os.path.dirname(__file__),"AMpresets.blend")#以下将添加预览材质
                    
                    if "PreM0" not in MatList:
                        with bpy.data.libraries.load(filepath, link=False,relative=True) as (data_from, data_to):
                            #data_to.materials = ["3.001"]
                            data_to.materials = data_from.materials #  append all materials from blend
                            #print(data_to.materials)
                            #Datamaterials


                    for materials,value in  bpy.data.materials.items():
                        #print(materials)
                        #bpy.data.materials['3.001'].use_fake_user = True
                        if ("PreM"  in materials) and ("_" not in materials):
                            if "." not in materials:
                                bpy.data.materials[materials].use_fake_user = True

                    for i in range(0,5):
                        MatName = "PreM0"+str(i)
                        if bpy.data.materials.get(MatName) is not None:
                            Mat = bpy.data.materials[MatName]

                            if len(ob.data.materials):
                                ob.data.materials[i] = Mat
                            else:
                                ob.data.materials.append(i)


                    #bpy.context.object.active_material_index = 1
                    #bpy.ops.object.material_slot_move(direction='UP')




                if amProperty.GenMechEnum =='Mechfy':
                    ob.modifiers.clear()
                    mod_Skin = ob.modifiers.new("Skin", "SKIN")

                    Wave2 = ob.modifiers.new('Wave', 'WAVE')#0
                    Ocean3 = ob.modifiers.new('Ocean', 'OCEAN')
                    Ocean3.geometry_mode = 'DISPLACE'


                    #bpy.ops.object.modifier_add(type='REMESH')
                    mod_Remesh = ob.modifiers.new("Remesh", "REMESH")
                    mod_Remesh.mode = 'SMOOTH'
                    #bpy.context.object.modifiers["Remesh"].mode = 'SHARP'
                    mod_Remesh.octree_depth = 4 #
                    mod_Remesh.scale = 0.88 #0.75

                    mod_Bevel = ob.modifiers.new("Bevel", "BEVEL")
                    mod_Bevel.offset_type = 'PERCENT'
                    mod_Bevel.width_pct = 37 #动画
                    mod_Bevel.affect = 'VERTICES'
                    mod_Bevel.use_clamp_overlap = True
                    mod_Bevel.loop_slide = True
                    mod_Bevel.material = 1         #1 1323（4）

                    mod_Decimate = ob.modifiers.new("Decimate", "DECIMATE")
                    mod_Decimate.ratio = 0.02

                    mod_Decimate2 = ob.modifiers.new("Decimate.001", "DECIMATE")
                    mod_Decimate2.decimate_type = 'DISSOLVE'
                    mod_Decimate2.delimit = {'MATERIAL'}

                    mod_Bevel1 = ob.modifiers.new("Bevel.001", "BEVEL")
                    mod_Bevel1.offset_type = 'PERCENT'
                    mod_Bevel1.width_pct = 33
                    mod_Bevel1.affect = 'VERTICES'
                    mod_Bevel1.use_clamp_overlap = True
                    mod_Bevel1.loop_slide = True
                    mod_Bevel1.material = 3         #0

                    mod_EdgeSplit = ob.modifiers.new("EdgeSplit", "EDGE_SPLIT")

                    mod_Solidify = ob.modifiers.new("Solidify", "SOLIDIFY")
                    mod_Solidify.thickness = -0.02
                    mod_Solidify.use_rim_only = True
                    mod_Solidify.material_offset_rim = 2  #1

                    mod_Bevel2 = ob.modifiers.new("Bevel.002", "BEVEL")
                    mod_Bevel2.offset_type = 'OFFSET'
                    mod_Bevel2.width = 0.05
                    mod_Bevel2.material = 3             #-1

                    mod_Displace = ob.modifiers.new("Displace", "DISPLACE")
                    mod_Displace.direction = 'NORMAL'
                    mod_Displace.mid_level = 0.5
                    mod_Displace.strength = 0.01#

                    if amProperty.MOD_MIRROR_Bool == True:
                        mod_Mirror = ob.modifiers.new("Mirror", "MIRROR")
                        if '_l' in ob.name:
                            mod_Mirror.use_axis[0] = False
                            mod_Mirror.use_axis[1] = True
                            mod_Mirror.use_bisect_axis[0] = False
                            mod_Mirror.use_bisect_flip_axis[0] = False
                            if 'thigh_l' in ob.name:
                                mod_Mirror.use_axis[0] = True
                                mod_Mirror.use_axis[1] = False
                            elif 'calf_l' in ob.name:
                                mod_Mirror.use_axis[0] = True
                                mod_Mirror.use_axis[1] = False
                            elif 'foot_l' in ob.name:
                                mod_Mirror.use_axis[0] = True
                                mod_Mirror.use_axis[1] = False
                    #else:
                        #if Mirror:
                            #ob.modifiers.remove(Mirror)
                        
                elif (amProperty.GenMechEnum =='MechPro') or (amProperty.GenMechEnum ==''):#总共72个修改器节点
                    ob.modifiers.clear()
                    amProperty.GenMechEnum ='MechPro'
                    Skin001 = ob.modifiers.new("001_Skin", "SKIN")
                    Cast002 = ob.modifiers.new("002_//////////Cast//////////", "CAST")
                    Bool003_01Uniun = ob.modifiers.new("003_Bool_01U++++++++++", "BOOLEAN")
                    Remesh004 = ob.modifiers.new("004_------------Remesh------------","REMESH")
                    Bool005_02Uniun = ob.modifiers.new("005_Bool_02U++++++++++", "BOOLEAN")

                    Simpledeform006 = ob.modifiers.new("006_&&&&Simpledeform", "SIMPLE_DEFORM")

                    Displace007 = ob.modifiers.new("007_____________Displace", "DISPLACE")
                    Array008 = ob.modifiers.new("008_$$$Array$$$", "ARRAY")
                    Cast009 = ob.modifiers.new("009_//////////Cast//////////", "CAST")

                    Warp010_x0 = ob.modifiers.new('010_Warp_x0', 'WARP')
                    Warp011_x1 = ob.modifiers.new('011_Warp_x1', 'WARP')
                    Warp012_y0 = ob.modifiers.new('012_Warp_y0', 'WARP')
                    Warp013_y1 = ob.modifiers.new('013_Warp_y1', 'WARP')
                    Warp014_z0 = ob.modifiers.new('014_Warp_z0', 'WARP')
                    Warp015_z1 = ob.modifiers.new('015_Warp_z1', 'WARP')

                    Bool016_03Intersect = ob.modifiers.new("016_Bool_03I++++++++++", "BOOLEAN")
                    Remesh017 = ob.modifiers.new("017_------------Remesh------------", "REMESH")
                    Bool018_04Uniun = ob.modifiers.new("018_Bool_04U++++++++++", "BOOLEAN")
                    Wireframe019 = ob.modifiers.new("019_Wireframe", "WIREFRAME")

                    Cast020 = ob.modifiers.new("020_//////////Cast//////////", "CAST")

                    Warp021_x0 = ob.modifiers.new('021_Warp_x0', 'WARP')
                    Warp022_x1 = ob.modifiers.new('022_Warp_x1', 'WARP')
                    Warp023_y0 = ob.modifiers.new('023_Warp_y0', 'WARP')
                    Warp024_y1 = ob.modifiers.new('024_Warp_y1', 'WARP')
                    Warp025_z0 = ob.modifiers.new('025_Warp_z0', 'WARP')
                    Warp026_z1 = ob.modifiers.new('026_Warp_z1', 'WARP')

                    Cast027 = ob.modifiers.new("027_//////////Cast//////////", "CAST")

                    Array028 = ob.modifiers.new("028_$$$Array$$$", "ARRAY")

                    Simpledeform029 = ob.modifiers.new("029_&&&&Simpledeform", "SIMPLE_DEFORM")
                    Simpledeform030 = ob.modifiers.new("030_&&&&Simpledeform", "SIMPLE_DEFORM")
                    Simpledeform031 = ob.modifiers.new("031_&&&&Simpledeform", "SIMPLE_DEFORM")

                    Cast032 = ob.modifiers.new("032_//////////Cast//////////", "CAST")



                    Array033 = ob.modifiers.new("033_$$$Array$$$", "ARRAY")
                    Screw034 = ob.modifiers.new("034_Screw", "SCREW")

                    Simpledeform035 = ob.modifiers.new("035_&&&&Simpledeform", "SIMPLE_DEFORM")
                    Simpledeform036 = ob.modifiers.new("036_&&&&Simpledeform", "SIMPLE_DEFORM")
                    Simpledeform037 = ob.modifiers.new("037_&&&&Simpledeform", "SIMPLE_DEFORM")


                    Bool038_05Uniun = ob.modifiers.new("038_Bool_05U++++++++++", "BOOLEAN")

                    Shrinkwrap039 = ob.modifiers.new("039_Shrinkwrap", "SHRINKWRAP")

                    Wave040 = ob.modifiers.new('040_Wave', 'WAVE')

                    Laplaciansmooth041 = ob.modifiers.new('041_Laplaciansmooth', 'LAPLACIANSMOOTH')

                    Lattice042 = ob.modifiers.new('042_Lattice', 'LATTICE')

                    Bevel043 = ob.modifiers.new("043_<<<<<Bevel>>>>>", "BEVEL")
                    Decimate044 = ob.modifiers.new("044_Decimate", "DECIMATE")

                    Curve045 = ob.modifiers.new("045_(((((((Curve)))))))", "CURVE")

                    Bevel046 = ob.modifiers.new("046_<<<<<Bevel>>>>>", "BEVEL")
                    Shrinkwrap047 = ob.modifiers.new("047_Shrinkwrap", "SHRINKWRAP")
                    Edgesplit048 = ob.modifiers.new("048_Edgesplit", "EDGE_SPLIT")
                    Solidify049 = ob.modifiers.new("049_Solidify", "SOLIDIFY")

                    Bool050 = ob.modifiers.new("050_Bool_sub++++++++++", "BOOLEAN")

                    Remesh051 = ob.modifiers.new("051_------------Remesh------------", "REMESH")

                    Displace052 = ob.modifiers.new("052_____________Displace", "DISPLACE")


                    Warp053_x0 = ob.modifiers.new('053_Warp_x0', 'WARP')
                    Warp054_x1 = ob.modifiers.new('054_Warp_x1', 'WARP')
                    Warp055_y0 = ob.modifiers.new('055_Warp_y0', 'WARP')
                    Warp056_y1 = ob.modifiers.new('056_Warp_y1', 'WARP')
                    Warp057_z0 = ob.modifiers.new('057_Warp_z0', 'WARP')
                    Warp058_z1 = ob.modifiers.new('058_Warp_z1', 'WARP')

                    Decimate059 = ob.modifiers.new("059_Decimate", "DECIMATE")
                    Smooth060 = ob.modifiers.new("060_Smooth", "SMOOTH")

                    Curve061 = ob.modifiers.new("061_(((((((Curve)))))))", "CURVE")

                    Bool062_06Difference = ob.modifiers.new("062_Bool_06D++++++++++", "BOOLEAN")

                    Subsurf063 = ob.modifiers.new("063_Subsurf", "SUBSURF")
                    Cast064 = ob.modifiers.new("064_//////////Cast//////////", "CAST")

                    Bevel065 = ob.modifiers.new("065_<<<<<Bevel>>>>>", "BEVEL")

                    Triangulate066 = ob.modifiers.new("066_Triangulate", "TRIANGULATE")

                    Array067 = ob.modifiers.new("067_$$$Array$$$", "ARRAY")
                    Curve068 = ob.modifiers.new("068_(((((((Curve)))))))", "CURVE")
                    Simpledeform069 = ob.modifiers.new("069_&&&&Simpledeform", "SIMPLE_DEFORM")
                    Simpledeform070 = ob.modifiers.new("070_&&&&Simpledeform", "SIMPLE_DEFORM")
                    Simpledeform071 = ob.modifiers.new("071_&&&&Simpledeform", "SIMPLE_DEFORM")

                    Simpledeform072 = ob.modifiers.new("072_&&&&Simpledeform", "SIMPLE_DEFORM")
                    Simpledeform073 = ob.modifiers.new("073_&&&&Simpledeform", "SIMPLE_DEFORM")
                    Simpledeform074 = ob.modifiers.new("074_&&&&Simpledeform", "SIMPLE_DEFORM")

                    Cast075 = ob.modifiers.new("075_//////////Cast//////////", "CAST")
                    Array076 = ob.modifiers.new("076_$$$Array$$$", "ARRAY")
                    Curve077 = ob.modifiers.new("077_(((((((Curve)))))))", "CURVE")
                    Simpledeform078 = ob.modifiers.new("078_&&&&Simpledeform", "SIMPLE_DEFORM")
                    Simpledeform079 = ob.modifiers.new("079_&&&&Simpledeform", "SIMPLE_DEFORM")
                    Simpledeform080 = ob.modifiers.new("080_&&&&Simpledeform", "SIMPLE_DEFORM")

                    Simpledeform081 = ob.modifiers.new("081_&&&&Simpledeform", "SIMPLE_DEFORM")
                    Simpledeform082 = ob.modifiers.new("082_&&&&Simpledeform", "SIMPLE_DEFORM")
                    Simpledeform083 = ob.modifiers.new("083_&&&&Simpledeform", "SIMPLE_DEFORM")
                    Cast084 = ob.modifiers.new("084_//////////Cast//////////", "CAST")

                    Bool085 = ob.modifiers.new("085_Bool_sub++++++++++", "BOOLEAN")
                    Bevel086 = ob.modifiers.new("086_<<<<<Bevel>>>>>", "BEVEL")#顶点

                    Decimate087 = ob.modifiers.new("087_Decimate", "DECIMATE")
                    Lattice088 = ob.modifiers.new('088_Lattice', 'LATTICE')
                    Decimate089 = ob.modifiers.new("089_Decimate", "DECIMATE")

                    Bool090 = ob.modifiers.new("090_Bool_sub++++++++++", "BOOLEAN")

                    Cast091 = ob.modifiers.new("091_//////////Cast//////////", "CAST")
                    Cast092 = ob.modifiers.new("092_//////////Cast//////////", "CAST")
                    Cast093 = ob.modifiers.new("093_//////////Cast//////////", "CAST")

                    Bevel094 = ob.modifiers.new("094_<<<<<Bevel>>>>>", "BEVEL")#关联Bool090

                    Bool095 = ob.modifiers.new("095_Bool_sub++++++++++", "BOOLEAN")

                    Triangulate096 = ob.modifiers.new("096_Triangulate", "TRIANGULATE")

                    Edgesplit097 = ob.modifiers.new("097_Edgesplit", "EDGE_SPLIT")
                    Solidify098 = ob.modifiers.new("098_Solidify", "SOLIDIFY")#-0.02~-0.04
                    Bevel099 = ob.modifiers.new("099_<<<<<Bevel>>>>>", "BEVEL")
                    Displace100 = ob.modifiers.new("100_____________Displace", "DISPLACE")
                    Smooth101 = ob.modifiers.new("101_Smooth_ToFixHole", "SMOOTH")



                    Triangulate102 = ob.modifiers.new("102_Triangulate", "TRIANGULATE")

                    Weld103 = ob.modifiers.new("103_Weld", "WELD")

                    Subsurf104 = ob.modifiers.new("104_Subsurf", "SUBSURF")
                    Decimate105 = ob.modifiers.new("105_Decimate", "DECIMATE")

                    Mirror106 = ob.modifiers.new('106_Mirror_x', 'MIRROR')

                    Bool107 = ob.modifiers.new("107_Bool_sub++++++++++", "BOOLEAN")
                    Array108 = ob.modifiers.new("108_$$$Array$$$", "ARRAY")
                    Curve109 = ob.modifiers.new("109_(((((((Curve)))))))", "CURVE")

                    Simpledeform110 = ob.modifiers.new("110_&&&&Simpledeform", "SIMPLE_DEFORM")
                    Simpledeform111 = ob.modifiers.new("111_&&&&Simpledeform", "SIMPLE_DEFORM")
                    Simpledeform112 = ob.modifiers.new("112_&&&&Simpledeform", "SIMPLE_DEFORM")

                    Cast113 = ob.modifiers.new("113_//////////Cast//////////", "CAST")

                    Mirror114 = ob.modifiers.new('114_Mirror_Obj', 'MIRROR')



                    Skin001.show_viewport = False
                    Skin001.show_render = False



                    Cast002.show_in_editmode = True
                    Cast002.cast_type = 'SPHERE'
                    Cast002.use_radius_as_size = True
                    Cast002.factor = 0.2
                    Cast002.radius = 0
                    Cast002.use_z = False

                    Remesh004.show_in_editmode = True

                    Remesh004.show_in_editmode = True
                    Remesh004.mode = 'SMOOTH'
                    Remesh004.octree_depth = 4
                    Remesh004.use_remove_disconnected = True
                    Remesh004.scale = 0.9

                    Displace007.show_in_editmode = True

                    Array008.show_viewport = False
                    Array008.show_render = False
                    Array008.use_relative_offset = True
                    Array008.fit_type = 'FIXED_COUNT'
                    Array008.count = 2
                    Array008.relative_offset_displace[0] = 0
                    Array008.relative_offset_displace[1] = 1
                    Array008.relative_offset_displace[2] = 2.5

                    Simpledeform006.show_viewport = False
                    Simpledeform006.show_render = False
                    Simpledeform006.deform_method = 'BEND'
                    Simpledeform006.angle = 0.523599
                    Simpledeform006.deform_axis = 'Y'

                    Simpledeform035.show_viewport = False
                    Simpledeform035.show_render = False
                    Simpledeform035.deform_method = 'BEND'
                    Simpledeform035.angle = -0.981259
                    Simpledeform035.deform_axis = 'X'


                    Simpledeform036.show_viewport = False
                    Simpledeform036.show_render = False
                    Simpledeform036.deform_method = 'BEND'
                    Simpledeform036.angle = 0.7
                    Simpledeform036.deform_axis = 'X'

                    Simpledeform037.show_viewport = False
                    Simpledeform037.show_render = False
                    Simpledeform037.deform_method = 'TAPER'
                    Simpledeform037.factor = -0.342761
                    Simpledeform037.deform_axis = 'X'

                    Simpledeform070.show_viewport = False
                    Simpledeform070.show_render = False
                    Simpledeform070.deform_method = 'BEND'
                    Simpledeform070.angle = 4.71
                    Simpledeform070.deform_axis = 'Y'

                    Simpledeform071.show_viewport = False
                    Simpledeform071.show_render = False
                    Simpledeform071.deform_method = 'TAPER'
                    Simpledeform071.factor = -0.4
                    Simpledeform071.deform_axis = 'Z'

                    Simpledeform078.show_viewport = False
                    Simpledeform078.show_render = False
                    Simpledeform078.deform_method = 'BEND'
                    Simpledeform078.angle = 0.610865
                    Simpledeform078.deform_axis = 'X'


                    Simpledeform079.show_viewport = False
                    Simpledeform079.show_render = False
                    Simpledeform079.deform_method = 'BEND'
                    Simpledeform079.angle = -5.76
                    Simpledeform079.deform_axis = 'Y'

                    Simpledeform080.show_viewport = False
                    Simpledeform080.show_render = False
                    Simpledeform080.deform_method = 'BEND'
                    Simpledeform080.angle = -3.96
                    Simpledeform080.deform_axis = 'Y'

                    Simpledeform069.show_viewport = False
                    Simpledeform069.show_render = False
                    Simpledeform069.deform_method = 'BEND'
                    Simpledeform069.angle = 0.174533
                    Simpledeform069.deform_axis = 'X'

                    Simpledeform073.show_viewport = False
                    Simpledeform073.show_render = False
                    Simpledeform073.deform_method = 'BEND'
                    Simpledeform073.angle = 1.04
                    Simpledeform073.deform_axis = 'Y'

                    Simpledeform074.show_viewport = False
                    Simpledeform074.show_render = False
                    Simpledeform074.deform_method = 'BEND'
                    Simpledeform074.angle = -0.35
                    Simpledeform074.deform_axis = 'Z'

                    Simpledeform081.show_viewport = False
                    Simpledeform081.show_render = False
                    Simpledeform081.deform_method = 'BEND'
                    Simpledeform081.angle = 3.14159
                    Simpledeform081.deform_axis = 'X'

                    Simpledeform082.show_viewport = False
                    Simpledeform082.show_render = False
                    Simpledeform082.deform_method = 'BEND'
                    Simpledeform082.angle = 0.5235
                    Simpledeform082.deform_axis = 'Y'

                    Simpledeform083.show_viewport = False
                    Simpledeform083.show_render = False
                    Simpledeform083.deform_method = 'BEND'
                    Simpledeform083.angle = 2.0944
                    Simpledeform083.deform_axis = 'Z'

                    Cast009.show_in_editmode = True
                    Cast009.cast_type = 'SPHERE'
                    Cast009.use_radius_as_size = True
                    Cast009.factor = 0.2
                    Cast009.radius = 0
                    #Cast009.use_z = False

                    Remesh017.show_in_editmode = True
                    Remesh017.mode = 'SHARP'
                    Remesh017.octree_depth = 5
                    Remesh017.scale = 0.8
                    Remesh017.sharpness = 1
                    Remesh017.use_remove_disconnected = True

                    Cast020.show_in_editmode = True
                    Cast020.show_viewport = True
                    Cast020.cast_type = 'CYLINDER'
                    Cast020.factor = -0.1
                    Cast020.radius = 0

                    Cast027.show_in_editmode = True
                    Cast027.show_viewport = True
                    Cast027.cast_type = 'SPHERE'
                    Cast027.factor = 0.1
                    Cast027.radius = 0
                    Cast027.use_z = False

                    Array028.show_viewport = False
                    Array028.show_render = False
                    Array028.relative_offset_displace[0] = -33.9


                    Simpledeform029.deform_method = 'TAPER'
                    Simpledeform029.factor = 0.4
                    Simpledeform029.deform_axis = 'Y'

                    Simpledeform030.deform_method = 'BEND'#STRETCH
                    #Simpledeform030.factor = 0.5
                    Simpledeform030.angle = 0.523599
                    Simpledeform030.deform_axis = 'Z'

                    Simpledeform031.deform_method = 'TWIST'
                    Simpledeform031.angle = 0.698132
                    Simpledeform031.deform_axis = 'X'

                    Cast032.cast_type = 'CUBOID'
                    Cast032.factor = 0.6
                    Cast032.radius = 0
                    
                    Array033.show_viewport = False
                    Array033.show_render = False
                    Array033.use_relative_offset = True
                    Array033.fit_type = 'FIXED_COUNT'
                    Array033.count = 3
                    Array033.relative_offset_displace[0] = 0
                    Array033.relative_offset_displace[1] = 0
                    Array033.relative_offset_displace[2] = 1
                    Array033.use_constant_offset = True
                    Array033.constant_offset_displace[2] = 22

                    Screw034.show_viewport = False
                    Screw034.show_render = False
                    Screw034.angle = 18.8496
                    Screw034.screw_offset = 100
                    Screw034.iterations = 2
                    Screw034.axis = 'X'
                    Screw034.steps = 8
                    Screw034.render_steps = 8

                    Remesh051.mode = 'SMOOTH'
                    Remesh051.octree_depth = 5
                    Remesh051.scale = 0.9
                    Remesh051.use_remove_disconnected = True

                    Displace052.direction = 'NORMAL'
                    Displace052.strength = 0.1#中调
                    Displace052.mid_level = 0.5

                    Decimate059.decimate_type = 'COLLAPSE'
                    Decimate059.ratio = 0.2048
                    Decimate059.use_symmetry = False
                    Decimate059.use_collapse_triangulate = False

                    Smooth060.factor = 0.97
                    Smooth060.iterations = 1
                    Smooth060.use_x = True
                    Smooth060.use_y = True
                    Smooth060.use_z = True

                    Subsurf063.show_viewport = False
                    Subsurf063.show_render = False
                    Subsurf063.subdivision_type = 'CATMULL_CLARK'
                    Subsurf063.levels = 1
                    Subsurf063.render_levels = 1


                    Bevel043.show_viewport = False
                    Bevel043.show_render = False
                    Bevel043.affect = 'VERTICES'
                    Bevel043.offset_type = 'PERCENT'
                    Bevel043.width_pct = 44
                    Bevel043.segments = 1
                    Bevel043.material = 1

                    Array067.show_viewport = False
                    Array067.show_render = False
                    Array067.use_relative_offset = True
                    Array067.fit_type = 'FIXED_COUNT'
                    Array067.count = 2
                    Array067.relative_offset_displace[0] = 0
                    Array067.relative_offset_displace[1] = 0
                    Array067.relative_offset_displace[2] = 1
                    Array067.use_constant_offset = True
                    Array067.constant_offset_displace[2] = 10

                    Simpledeform072.show_viewport = False
                    Simpledeform072.show_render = False
                    Simpledeform072.deform_method = 'BEND'
                    Simpledeform072.angle = 0.785398
                    Simpledeform072.deform_axis = 'X'

                    Cast075.show_viewport = False
                    Cast075.show_render = False
                    Cast075.cast_type = 'SPHERE'
                    Cast075.use_z = False
                    Cast075.use_radius_as_size = True
                    Cast075.factor = 0.4
                    Cast075.radius = 0

                    Array076.show_viewport = False
                    Array076.show_render = False
                    Array076.fit_type = 'FIXED_COUNT'
                    Array076.count = 4
                    Array076.use_relative_offset = True
                    Array076.relative_offset_displace[2] = 1
                    Array076.use_constant_offset = True
                    Array076.constant_offset_displace[2] = 100
                    Array076.use_constant_offset = True
                    Array076.constant_offset_displace[2] = 10


                    Decimate087.decimate_type = 'COLLAPSE'
                    Decimate087.ratio = 0.02
                    Decimate087.use_symmetry = False
                    Decimate087.use_collapse_triangulate = False

                    Decimate089.decimate_type = 'DISSOLVE'
                    Decimate089.angle_limit = 0.0872665
                    Decimate089.delimit = {'MATERIAL'}#3

                    Bevel094.affect = 'VERTICES'#这次需要调切线倒角了
                    Bevel094.offset_type = 'PERCENT'
                    Bevel094.width_pct = 33#六角到三角
                    Bevel094.segments = 1
                    Bevel094.material = 3

                    Edgesplit097.use_edge_angle = True
                    Edgesplit097.use_edge_sharp = True
                    Edgesplit097.split_angle = 0.523599#2越小越以挤出的形式

                    Solidify098.solidify_mode = 'EXTRUDE'
                    Solidify098.thickness = 0.02#1负负为正
                    Solidify098.offset = 1 
                    Solidify098.use_even_offset = False
                    Solidify098.use_rim = True
                    Solidify098.use_rim_only = True
                    Solidify098.material_offset_rim = 2


                    Bevel099.affect = 'EDGES'
                    Bevel099.offset_type = 'OFFSET'
                    Bevel099.width = 0.05
                    Bevel099.segments = 1
                    Bevel099.material = 3

                    Displace100.direction = 'NORMAL'
                    Displace100.strength = 0.01
                    Displace100.mid_level = 0.5


                    #Smooth101.show_viewport = False
                    #Smooth101.show_render = False
                    Smooth101.factor = 0.1
                    Smooth101.iterations = 3
                    Smooth101.use_x = True
                    Smooth101.use_y = True
                    Smooth101.use_z = True

                    Cast091.show_viewport = False
                    Cast091.show_render = False
                    Cast091.cast_type = 'SPHERE'
                    Cast091.use_x = True
                    Cast091.use_y = False
                    Cast091.use_z = False
                    Cast091.use_radius_as_size = True
                    Cast091.factor = 0.4
                    Cast091.radius = 0


                    Cast092.show_viewport = False
                    Cast092.show_render = False
                    Cast092.cast_type = 'SPHERE'
                    Cast092.use_x = False
                    Cast092.use_y = True
                    Cast092.use_z = False
                    Cast092.use_radius_as_size = True
                    Cast092.factor = 0.4
                    Cast092.radius = 0

                    Cast093.show_viewport = False
                    Cast093.show_render = False
                    Cast093.cast_type = 'CUBOID'
                    Cast093.use_x = False
                    Cast093.use_y = False
                    Cast093.use_z = True
                    Cast093.use_radius_as_size = True
                    Cast093.factor = 0.4
                    Cast093.radius = 0

                    Cast064.show_viewport = False
                    Cast064.show_render = False
                    Cast064.cast_type = 'CUBOID'

                    Cast084.show_viewport = False
                    Cast084.show_render = False
                    Cast084.cast_type = 'CUBOID'



                    #Weld103.show_viewport = False
                    #Weld103.show_render = False
                    Weld103.merge_threshold = 0.005

                    #Weld103.max_interactions = 1

                    Warp010_x0.show_viewport = False
                    Warp010_x0.show_render = False
                    Warp010_x0.strength = 0.5
                    Warp010_x0.use_volume_preserve = True
                    Warp010_x0.falloff_type = 'SMOOTH'
                    Warp010_x0.falloff_radius = 1

                    Warp011_x1.show_viewport = False
                    Warp011_x1.show_render = False
                    Warp011_x1.strength = 0.5
                    Warp011_x1.use_volume_preserve = True
                    Warp011_x1.falloff_type = 'SMOOTH'
                    Warp011_x1.falloff_radius = 1

                    Warp012_y0.show_viewport = False
                    Warp012_y0.show_render = False
                    Warp012_y0.strength = 0.5
                    Warp012_y0.use_volume_preserve = True
                    Warp012_y0.falloff_type = 'SMOOTH'
                    Warp012_y0.falloff_radius = 1

                    Warp013_y1.show_viewport = False
                    Warp013_y1.show_render = False
                    Warp013_y1.strength = 0.5
                    Warp013_y1.use_volume_preserve = True
                    Warp013_y1.falloff_type = 'SMOOTH'
                    Warp013_y1.falloff_radius = 1

                    Warp014_z0.show_viewport = False
                    Warp014_z0.show_render = False
                    Warp014_z0.strength = 0.5
                    Warp014_z0.use_volume_preserve = True
                    Warp014_z0.falloff_type = 'SMOOTH'
                    Warp014_z0.falloff_radius = 1

                    Warp015_z1.show_viewport = False
                    Warp015_z1.show_render = False
                    Warp015_z1.strength = 0.5
                    Warp015_z1.use_volume_preserve = True
                    Warp015_z1.falloff_type = 'SMOOTH'
                    Warp015_z1.falloff_radius = 1

                    Warp021_x0.show_viewport = False
                    Warp021_x0.show_render = False
                    Warp021_x0.strength = 0.1
                    Warp021_x0.use_volume_preserve = True
                    Warp021_x0.falloff_type = 'SPHERE'
                    Warp021_x0.falloff_radius = 1

                    Warp022_x1.show_viewport = False
                    Warp022_x1.show_render = False
                    Warp022_x1.strength = 0.1
                    Warp022_x1.use_volume_preserve = True
                    Warp022_x1.falloff_type = 'SPHERE'
                    Warp022_x1.falloff_radius = 1

                    Warp023_y0.show_viewport = False
                    Warp023_y0.show_render = False
                    Warp023_y0.strength = 0.1
                    Warp023_y0.use_volume_preserve = True
                    Warp023_y0.falloff_type = 'SPHERE'
                    Warp023_y0.falloff_radius = 1

                    Warp024_y1.show_viewport = False
                    Warp024_y1.show_render = False
                    Warp024_y1.strength = 0.1
                    Warp024_y1.use_volume_preserve = True
                    Warp024_y1.falloff_type = 'SPHERE'
                    Warp024_y1.falloff_radius = 1

                    Warp025_z0.show_viewport = False
                    Warp025_z0.show_render = False
                    Warp025_z0.strength = 0.1
                    Warp025_z0.use_volume_preserve = True
                    Warp025_z0.falloff_type = 'SPHERE'
                    Warp025_z0.falloff_radius = 1

                    Warp026_z1.show_viewport = False
                    Warp026_z1.show_render = False
                    Warp026_z1.strength = 0.1
                    Warp026_z1.use_volume_preserve = True
                    Warp026_z1.falloff_type = 'SPHERE'
                    Warp026_z1.falloff_radius = 1


                    Wave040.show_viewport = True
                    Wave040.show_render = True
                    Laplaciansmooth041.show_viewport = True
                    Laplaciansmooth041.show_render = True
                    #Wave040.show_viewport = False
                    #Wave040.show_render = False
                    #Laplaciansmooth041.show_viewport = False
                    #Laplaciansmooth041.show_render = False

                    frametime = bpy.context.scene.frame_current
                    
                    Wave040.height = 1
                    Laplaciansmooth041.iterations = 3
                    Laplaciansmooth041.lambda_factor = 0.1
                    Laplaciansmooth041.lambda_border = 0.1
                    bpy.context.scene.frame_current = 1
                    if amProperty.FreezeTime_Bool ==False:
                        Wave040.keyframe_insert('height')
                        Laplaciansmooth041.keyframe_insert('lambda_border')#.keyframe_delete(
                        Laplaciansmooth041.keyframe_insert('lambda_factor')

                    Wave040.height = 25
                    Laplaciansmooth041.lambda_factor = 1
                    Laplaciansmooth041.lambda_border = 5
                    bpy.context.scene.frame_current = 250
                    if amProperty.FreezeTime_Bool ==False:
                        Wave040.keyframe_insert('height')
                        Laplaciansmooth041.keyframe_insert('lambda_border')
                        Laplaciansmooth041.keyframe_insert('lambda_factor')
                    
                    bpy.context.scene.frame_current = frametime

                    Warp053_x0.show_viewport = False
                    Warp053_x0.show_render = False
                    Warp053_x0.strength = 0.8
                    Warp053_x0.use_volume_preserve = True
                    Warp053_x0.falloff_type = 'SHARP'
                    Warp053_x0.falloff_radius = 1

                    Warp054_x1.show_viewport = False
                    Warp054_x1.show_render = False
                    Warp054_x1.strength = 0.8
                    Warp054_x1.use_volume_preserve = True
                    Warp054_x1.falloff_type = 'SHARP'
                    Warp054_x1.falloff_radius = 1

                    Warp055_y0.show_viewport = False
                    Warp055_y0.show_render = False
                    Warp055_y0.strength = 0.8
                    Warp055_y0.use_volume_preserve = True
                    Warp055_y0.falloff_type = 'SHARP'
                    Warp055_y0.falloff_radius = 1

                    Warp056_y1.show_viewport = False
                    Warp056_y1.show_render = False
                    Warp056_y1.strength = 0.8
                    Warp056_y1.use_volume_preserve = True
                    Warp056_y1.falloff_type = 'SHARP'
                    Warp056_y1.falloff_radius = 1

                    Warp057_z0.show_viewport = False
                    Warp057_z0.show_render = False
                    Warp057_z0.strength = 0.8
                    Warp057_z0.use_volume_preserve = True
                    Warp057_z0.falloff_type = 'SHARP'
                    Warp057_z0.falloff_radius = 1

                    Warp058_z1.show_viewport = False
                    Warp058_z1.show_render = False
                    Warp058_z1.strength = 0.8
                    Warp058_z1.use_volume_preserve = True
                    Warp058_z1.falloff_type = 'SHARP'
                    Warp058_z1.falloff_radius = 1


                    Triangulate066.show_viewport = False
                    Triangulate066.show_render = False
                    Triangulate066.min_vertices = 4


                    Triangulate096.show_viewport = False
                    Triangulate096.show_render = False
                    Triangulate096.min_vertices = 8

                    Triangulate102.show_viewport = False
                    Triangulate102.show_render = False
                    Triangulate102.min_vertices = 4

                    Subsurf104.show_viewport = False
                    Subsurf104.show_render = False
                    Subsurf104.subdivision_type = 'SIMPLE'
                    Subsurf104.levels = 1
                    Subsurf104.render_levels = 1
                    Subsurf104.quality = 6

                    Decimate105.show_viewport = False
                    Decimate105.show_render = False
                    Decimate105.decimate_type = 'DISSOLVE'
                    Decimate105.delimit = {'NORMAL', 'MATERIAL', 'SEAM', 'SHARP', 'UV'}
                    Decimate105.use_dissolve_boundaries = True

                    Wireframe019.show_viewport = False#线框主要切替换原物体 重构11取消移除分离元素 曲线
                    Wireframe019.show_render = False
                    Wireframe019.use_boundary = True
                    Wireframe019.use_replace = False
                    Wireframe019.use_even_offset = True
                    Wireframe019.use_relative_offset = True


                    Mirror106.show_viewport = False
                    Mirror106.show_render = False

                    Mirror114.show_viewport = False
                    Mirror114.show_render = False

                    Bool003_01Uniun.show_viewport = False
                    Bool003_01Uniun.show_render = False
                    Bool005_02Uniun.show_viewport = False
                    Bool005_02Uniun.show_render = False					
                    Bool016_03Intersect.show_viewport = False
                    Bool016_03Intersect.show_render = False					
                    Bool018_04Uniun.show_viewport = False
                    Bool018_04Uniun.show_render = False					
                    Bool038_05Uniun.show_viewport = False
                    Bool038_05Uniun.show_render = False					
                    Bool062_06Difference.show_viewport = False
                    Bool062_06Difference.show_render = False

                    Source_ARROW_x0 = ob.name+"_SourceARROW_x+"
                    Source_ARROW_x1 = ob.name+"_SourceARROW_x-"
                    Source_ARROW_y0 = ob.name+"_SourceARROW_y+"
                    Source_ARROW_y1 = ob.name+"_SourceARROW_y-"
                    Source_ARROW_z0 = ob.name+"_SourceARROW_z+"
                    Source_ARROW_z1 = ob.name+"_SourceARROW_z-"

                    Target_ARROW_x0 = ob.name+"_TargetARROW_x+"
                    Target_ARROW_x1 = ob.name+"_TargetARROW_x-"
                    Target_ARROW_y0 = ob.name+"_TargetARROW_y+"
                    Target_ARROW_y1 = ob.name+"_TargetARROW_y-"
                    Target_ARROW_z0 = ob.name+"_TargetARROW_z+"
                    Target_ARROW_z1 = ob.name+"_TargetARROW_z-"

                    ObjLattice = ob.name+"_ObjLattice"
                    ObjBoolTarget = ob.name+"_ObjBoolTarget"
                    ObjBoolPlane = ob.name+"_ObjBoolPlane"
                    ObjCurve = ob.name+"_ObjCurve"
                    ob_collection = find_collection(bpy.context, ob)


                    areas = [area for screen in context.workspace.screens for area in screen.areas if area.type == "OUTLINER"]#VIEW3D
                    for area in areas:
                        space = area.spaces[0]
                        #space.use_filter_children = False
                        space.show_restrict_column_select = True
                        space.show_restrict_column_viewport = True
                        space.show_restrict_column_render = True
                        #bpy.context.space_data.overlay.show_face_orientation = True


                    if "1GenLine" in ob.name:
                        Skin001.show_viewport = True
                        Skin001.show_render = True

                    if Source_ARROW_x0 not in bpy.data.objects:
                        bpy.ops.object.empty_add(type='SINGLE_ARROW', align='WORLD', location=(0, 0, 0), rotation=(0, 1.5708, 0), scale=(1, 1, 1))
                        bpy.ops.object.transforms_to_deltas(mode='ALL')
                        bpy.context.object.name = Source_ARROW_x0
                        bpy.context.object.hide_render = True

                        move_object(Source_ARROW_x0,ob.name)

                    if Target_ARROW_x0 not in bpy.data.objects:
                        bpy.ops.object.empty_add(type='SINGLE_ARROW', align='WORLD', location=(10, 0, 0), rotation=(0, 1.5708, 0), scale=(1, 1, 1))#
                        bpy.ops.object.transforms_to_deltas(mode='ALL')
                        bpy.context.object.name = Target_ARROW_x0
                        bpy.context.object.hide_render = True

                        move_object(Target_ARROW_x0,ob.name)


                    if Source_ARROW_x1 not in bpy.data.objects:
                        bpy.ops.object.empty_add(type='SINGLE_ARROW', align='WORLD', location=(0, 0, 0), rotation=(0, -1.5708, 0), scale=(1, 1, 1))
                        bpy.ops.object.transforms_to_deltas(mode='ALL')
                        bpy.context.object.name = Source_ARROW_x1
                        bpy.context.object.hide_render = True

                        move_object(Source_ARROW_x1,ob.name)

                    if Target_ARROW_x1 not in bpy.data.objects:
                        bpy.ops.object.empty_add(type='SINGLE_ARROW', align='WORLD', location=(-10, 0, 0), rotation=(0, -1.5708, 0), scale=(1, 1, 1))#
                        bpy.ops.object.transforms_to_deltas(mode='ALL')
                        bpy.context.object.name = Target_ARROW_x1
                        bpy.context.object.hide_render = True

                        move_object(Target_ARROW_x1,ob.name)


                    if Source_ARROW_y0 not in bpy.data.objects:
                        bpy.ops.object.empty_add(type='SINGLE_ARROW', align='WORLD', location=(0, 0, 0), rotation=(-1.5708, 0, 0), scale=(1, 1, 1))
                        bpy.ops.object.transforms_to_deltas(mode='ALL')
                        bpy.context.object.name = Source_ARROW_y0
                        bpy.context.object.hide_render = True

                        move_object(Source_ARROW_y0,ob.name)

                    if Target_ARROW_y0 not in bpy.data.objects:
                        bpy.ops.object.empty_add(type='SINGLE_ARROW', align='WORLD', location=(0, 10, 0), rotation=(-1.5708, 0, 0), scale=(1, 1, 1))#
                        bpy.ops.object.transforms_to_deltas(mode='ALL')
                        bpy.context.object.name = Target_ARROW_y0
                        bpy.context.object.hide_render = True

                        move_object(Target_ARROW_y0,ob.name)

                    if Source_ARROW_y1 not in bpy.data.objects:
                        bpy.ops.object.empty_add(type='SINGLE_ARROW', align='WORLD', location=(0, 0, 0), rotation=(1.5708, 0, 0), scale=(1, 1, 1))
                        bpy.ops.object.transforms_to_deltas(mode='ALL')
                        bpy.context.object.name = Source_ARROW_y1
                        bpy.context.object.hide_render = True

                        move_object(Source_ARROW_y1,ob.name)


                    if Target_ARROW_y1 not in bpy.data.objects:
                        bpy.ops.object.empty_add(type='SINGLE_ARROW', align='WORLD', location=(0, -10, 0), rotation=(1.5708, 0, 0), scale=(1, 1, 1))#
                        bpy.ops.object.transforms_to_deltas(mode='ALL')
                        bpy.context.object.name = Target_ARROW_y1
                        bpy.context.object.hide_render = True

                        move_object(Target_ARROW_y1,ob.name)

                    if Source_ARROW_z0 not in bpy.data.objects:
                        bpy.ops.object.empty_add(type='SINGLE_ARROW', align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1))
                        bpy.ops.object.transforms_to_deltas(mode='ALL')
                        bpy.context.object.name = Source_ARROW_z0
                        bpy.context.object.hide_render = True

                        Source_z0=bpy.data.objects[Source_ARROW_z0]
                        Source_z0.parent = ob
                        Source_z0_collection = find_collection(bpy.context, Source_z0)
                        ob_collection.objects.link(Source_z0)
                        Source_z0_collection.objects.unlink(Source_z0)


                    if Target_ARROW_z0 not in bpy.data.objects:
                        bpy.ops.object.empty_add(type='SINGLE_ARROW', align='WORLD', location=(0, 0, 10), rotation=(0, 0, 0), scale=(1, 1, 1))#
                        bpy.ops.object.transforms_to_deltas(mode='ALL')
                        bpy.context.object.name = Target_ARROW_z0
                        bpy.context.object.hide_render = True

                        move_object(Target_ARROW_z0,ob.name)



                    if Source_ARROW_z1 not in bpy.data.objects:
                        bpy.ops.object.empty_add(type='SINGLE_ARROW', align='WORLD', location=(0, 0, 0), rotation=(3.1415926, 0, 0), scale=(1, 1, 1))
                        bpy.ops.object.transforms_to_deltas(mode='ALL')
                        bpy.context.object.name = Source_ARROW_z1
                        bpy.context.object.hide_render = True

                        Source_z1=bpy.data.objects[Source_ARROW_z1]
                        Source_z1.parent = ob
                        Source_z1_collection = find_collection(bpy.context, Source_z1)
                        ob_collection.objects.link(Source_z1)
                        Source_z1_collection.objects.unlink(Source_z1)


                    if Target_ARROW_z1 not in bpy.data.objects:
                        bpy.ops.object.empty_add(type='SINGLE_ARROW', align='WORLD', location=(0, 0, -10), rotation=(3.1415926, 0, 0), scale=(1, 1, 1))#
                        bpy.ops.object.transforms_to_deltas(mode='ALL')
                        bpy.context.object.name = Target_ARROW_z1
                        bpy.context.object.hide_render = True

                        Target_z1=bpy.data.objects[Target_ARROW_z1]
                        Target_z1.parent = ob
                        Target_z1_collection = find_collection(bpy.context, Target_z1)
                        ob_collection.objects.link(Target_z1)
                        Target_z1_collection.objects.unlink(Target_z1)

                    if ObjLattice not in bpy.data.objects:
                        bpy.ops.object.add(radius=10, type='LATTICE', enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
                        bpy.context.object.name = ObjLattice
                        bpy.context.object.data.points_u = 3
                        bpy.context.object.data.points_v = 3
                        bpy.context.object.data.points_w = 3
                        bpy.context.object.hide_render = True

                        Lattice=bpy.data.objects[ObjLattice]
                        Lattice.parent = ob
                        Lattice_collection = find_collection(bpy.context, Lattice)
                        ob_collection.objects.link(Lattice)
                        Lattice_collection.objects.unlink(Lattice)


                    if ObjBoolTarget not in bpy.data.objects:#要想使之不变化就使用父子级吧 设置它的材质关联
                        bpy.ops.mesh.primitive_cylinder_add(vertices=4, radius=1, depth=9, enter_editmode=False, align='WORLD', location=(0, 0, 1), rotation=(1.5708, 0.785398, 0), scale=(1, 1, 1))
                        bpy.context.object.name = ObjBoolTarget
                        bpy.context.object.hide_render = True
                        bpy.context.object.display_type = 'WIRE'
                        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
                        BoolObject=bpy.data.objects[ObjBoolTarget]

                        '''
                        if len(BoolObject.material_slots) <= 1:
                            mat0 = bpy.data.materials.get("PreM00")
                            mat1 = bpy.data.materials.get("PreM01")
                            mat2 = bpy.data.materials.get("PreM02")
                            mat3 = bpy.data.materials.get("PreM03")
                            mat4 = bpy.data.materials.get("PreM04")
                            BoolObject.data.materials.append(MatNew)
                            BoolObject.data.materials.append(mat1)
                            BoolObject.data.materials.append(mat2)
                            BoolObject.data.materials.append(mat3)
                            BoolObject.data.materials.append(mat4)
                        '''

                        BoolObject.parent = ob
                        BoolObject_collection = find_collection(bpy.context, BoolObject)
                        ob_collection.objects.link(BoolObject)
                        BoolObject_collection.objects.unlink(BoolObject)

                    if ObjBoolPlane not in bpy.data.objects:
                        bpy.ops.mesh.primitive_plane_add(size=16, enter_editmode=False, align='WORLD', location=(0, -5, 0), rotation=(1.5708, 0, 0), scale=(1, 1, 1))
                        bpy.context.object.name = ObjBoolPlane
                        bpy.context.object.hide_render = True
                        bpy.context.object.display_type = 'WIRE'
                        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

                        #bpy.ops.object.material_slot_add()
                        #bpy.ops.object.material_slot_add()
                        #bpy.ops.object.material_slot_add()
                        #bpy.ops.object.material_slot_add()
                        #bpy.ops.object.material_slot_add()

                        BoolPlane=bpy.data.objects[ObjBoolPlane]#可以在此之前添加实体化
                        BoolPlane.parent = ob
                        BoolPlane_collection = find_collection(bpy.context, BoolPlane)
                        ob_collection.objects.link(BoolPlane)
                        BoolPlane_collection.objects.unlink(BoolPlane)

                        '''
                        if len(BoolPlane.material_slots) <= 1:
                            mat0 = bpy.data.materials.get("PreM00")
                            mat1 = bpy.data.materials.get("PreM01")
                            mat2 = bpy.data.materials.get("PreM02")
                            mat3 = bpy.data.materials.get("PreM03")
                            mat4 = bpy.data.materials.get("PreM04")
                            BoolPlane.data.materials.append(mat0)
                            BoolPlane.data.materials.append(mat1)
                            BoolPlane.data.materials.append(mat2)
                            BoolPlane.data.materials.append(mat3)
                            BoolPlane.data.materials.append(mat4)
                        '''

                        #BoolPlane.data.materials[0] = mat0
                        #BoolPlane.data.materials[1] = mat1
                        #BoolPlane.data.materials[2] = mat2
                        #BoolPlane.data.materials[3] = mat3
                        #BoolPlane.data.materials[4] = mat4

                        BoolPlaneArray = BoolPlane.modifiers.new("BoolPlaneArray", "ARRAY")
                        BoolPlaneArray.fit_type = 'FIXED_COUNT'
                        BoolPlaneArray.count = 7
                        BoolPlaneArray.use_relative_offset = False
                        BoolPlaneArray.use_constant_offset = True
                        BoolPlaneArray.constant_offset_displace[0] = 0
                        BoolPlaneArray.constant_offset_displace[1] = 1.5


                    if ObjCurve not in bpy.data.objects:
                        bpy.ops.curve.primitive_bezier_circle_add(radius=10, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
                        bpy.context.object.name = ObjCurve
                        bpy.context.object.hide_render = True

                        Curve=bpy.data.objects[ObjCurve]
                        Curve.parent = ob
                        Curve_collection = find_collection(bpy.context, Curve)
                        ob_collection.objects.link(Curve)
                        Curve_collection.objects.unlink(Curve)
                        Curve.select_set(False)

                    if "DisplaceTexture" not in bpy.data.textures:
                        DisplaceTexture = bpy.data.textures.new("DisplaceTexture", 'VORONOI')
                        DisplaceTexture.distance_metric = 'CHEBYCHEV'
                        Displace052.texture = DisplaceTexture

                    Bool003_01Uniun.operation = 'UNION'
                    Bool003_01Uniun.object = bpy.data.objects[ObjBoolTarget]

                    Bool005_02Uniun.operation = 'UNION'#'DIFFERENCE'
                    Bool005_02Uniun.object = bpy.data.objects[ObjBoolTarget]

                    Bool016_03Intersect.operation = 'INTERSECT'
                    Bool016_03Intersect.object = bpy.data.objects[ObjBoolTarget]

                    Bool018_04Uniun.operation = 'UNION'
                    Bool018_04Uniun.object = bpy.data.objects[ObjBoolTarget]

                    Bool038_05Uniun.operation = 'UNION'
                    Bool038_05Uniun.object = bpy.data.objects[ObjBoolTarget]

                    Bool062_06Difference.operation = 'DIFFERENCE'
                    Bool062_06Difference.object = bpy.data.objects[ObjBoolTarget]

                    Warp010_x0.object_from = bpy.data.objects[Source_ARROW_x0]
                    Warp010_x0.object_to = bpy.data.objects[Target_ARROW_x0]
                    Warp011_x1.object_from = bpy.data.objects[Source_ARROW_x1]
                    Warp011_x1.object_to = bpy.data.objects[Target_ARROW_x1]
                    Warp012_y0.object_from = bpy.data.objects[Source_ARROW_y0]
                    Warp012_y0.object_to = bpy.data.objects[Target_ARROW_y0]
                    Warp013_y1.object_from = bpy.data.objects[Source_ARROW_y1]
                    Warp013_y1.object_to = bpy.data.objects[Target_ARROW_y1]
                    Warp014_z0.object_from = bpy.data.objects[Source_ARROW_z0]
                    Warp014_z0.object_to = bpy.data.objects[Target_ARROW_z0]
                    Warp015_z1.object_from = bpy.data.objects[Source_ARROW_z1]
                    Warp015_z1.object_to = bpy.data.objects[Target_ARROW_z1]

                    Warp021_x0.object_from = bpy.data.objects[Source_ARROW_x0]
                    Warp021_x0.object_to = bpy.data.objects[Target_ARROW_x0]
                    Warp022_x1.object_from = bpy.data.objects[Source_ARROW_x1]
                    Warp022_x1.object_to = bpy.data.objects[Target_ARROW_x1]
                    Warp023_y0.object_from = bpy.data.objects[Source_ARROW_y0]
                    Warp023_y0.object_to = bpy.data.objects[Target_ARROW_y0]
                    Warp024_y1.object_from = bpy.data.objects[Source_ARROW_y1]
                    Warp024_y1.object_to = bpy.data.objects[Target_ARROW_y1]
                    Warp025_z0.object_from = bpy.data.objects[Source_ARROW_z0]
                    Warp025_z0.object_to = bpy.data.objects[Target_ARROW_z0]
                    Warp026_z1.object_from = bpy.data.objects[Source_ARROW_z1]
                    Warp026_z1.object_to = bpy.data.objects[Target_ARROW_z1]

                    Warp053_x0.object_from = bpy.data.objects[Source_ARROW_x0]
                    Warp053_x0.object_to = bpy.data.objects[Target_ARROW_x0]
                    Warp054_x1.object_from = bpy.data.objects[Source_ARROW_x1]
                    Warp054_x1.object_to = bpy.data.objects[Target_ARROW_x1]
                    Warp055_y0.object_from = bpy.data.objects[Source_ARROW_y0]
                    Warp055_y0.object_to = bpy.data.objects[Target_ARROW_y0]
                    Warp056_y1.object_from = bpy.data.objects[Source_ARROW_y1]
                    Warp056_y1.object_to = bpy.data.objects[Target_ARROW_y1]
                    Warp057_z0.object_from = bpy.data.objects[Source_ARROW_z0]
                    Warp057_z0.object_to = bpy.data.objects[Target_ARROW_z0]
                    Warp058_z1.object_from = bpy.data.objects[Source_ARROW_z1]
                    Warp058_z1.object_to = bpy.data.objects[Target_ARROW_z1]



                    Curve045.show_viewport = False
                    Curve045.show_render = False
                    Curve045.deform_axis = 'NEG_Y'
                    Curve045.object = bpy.data.objects[ObjCurve]

                    Curve061.show_viewport = False
                    Curve061.show_render = False
                    Curve061.deform_axis = 'NEG_Z'
                    Curve061.object = bpy.data.objects[ObjCurve]

                    Lattice042.show_viewport = False
                    Lattice042.show_render = False
                    Lattice042.object = bpy.data.objects[ObjLattice]

                    Shrinkwrap039.show_viewport = False#V
                    Shrinkwrap039.show_render = False
                    Shrinkwrap039.wrap_method = 'TARGET_PROJECT'
                    Shrinkwrap039.wrap_mode = 'OUTSIDE'
                    Shrinkwrap039.target = bpy.data.objects[ObjBoolTarget]
                    Shrinkwrap039.offset = 0.5#随便

                    Bevel065.show_viewport = False
                    Bevel065.show_render = False
                    Bevel065.affect = 'VERTICES'
                    Bevel065.offset_type = 'PERCENT'
                    Bevel065.width_pct = 33

                    Decimate044.show_viewport = False
                    Decimate044.show_render = False

                    Bevel046.show_viewport = False
                    Bevel046.show_render = False
                    Bevel046.affect = 'VERTICES'
                    Bevel046.offset_type = 'PERCENT'
                    Bevel046.width_pct = 10#随便吧

                    Shrinkwrap047.show_viewport = False
                    Shrinkwrap047.show_render = False
                    Shrinkwrap047.wrap_method = 'NEAREST_SURFACEPOINT'
                    Shrinkwrap047.wrap_mode = 'ON_SURFACE'
                    Shrinkwrap047.target = bpy.data.objects[ObjBoolTarget]
                    Shrinkwrap047.offset = 0.3#随便



                    Edgesplit048.show_viewport = False
                    Edgesplit048.show_render = False
                    Edgesplit048.use_edge_angle = True
                    Edgesplit048.use_edge_sharp = True
                    Edgesplit048.split_angle = 0.0523599

                    Solidify049.show_viewport = False
                    Solidify049.show_render = False
                    Solidify049.solidify_mode = 'NON_MANIFOLD'
                    Solidify049.nonmanifold_thickness_mode = 'EVEN'
                    Solidify049.nonmanifold_boundary_mode = 'NONE'
                    Solidify049.thickness = 1.4
                    Solidify049.offset = 1
                    Solidify049.nonmanifold_merge_threshold = 0.02
                    Solidify049.use_rim_only = True
                    Solidify049.use_rim = True



                    Bool050.show_viewport = False
                    Bool050.show_render = False
                    Bool050.operation = 'DIFFERENCE'

                    Curve068.show_viewport = False
                    Curve068.show_render = False
                    Curve068.object = bpy.data.objects[ObjCurve]

                    Curve077.show_viewport = False
                    Curve077.show_render = False
                    Curve077.object = bpy.data.objects[ObjCurve]

                    Bool085.show_viewport = False
                    Bool085.show_render = False
                    Bool085.operation = 'DIFFERENCE'

                    Bevel086.show_viewport = False
                    Bevel086.show_render = False
                    Bevel086.affect = 'VERTICES'
                    Bevel086.offset_type = 'PERCENT'
                    Bevel086.width_pct = 10#随便变动


                    Lattice088.show_viewport = False
                    Lattice088.show_render = False
                    Lattice088.object = bpy.data.objects[ObjLattice]

                    Bool090.show_viewport = False
                    Bool090.show_render = False#关联Bevel094 需要调整
                    Bool090.operation = 'DIFFERENCE'
                    Bool090.object = bpy.data.objects[ObjBoolPlane]

                    Bool095.show_viewport = True#实在不行有洞就向上一级直到Bool085
                    Bool095.show_render = True#A打开直线
                    #if bpy.app.version >= (2, 92, 0):
                        #Bool095.operation = 'INTERSECT'
                    #else:
                    Bool095.operation = 'DIFFERENCE'
                    Bool095.object = bpy.data.objects[ObjBoolPlane]

                    Bool107.show_viewport = False
                    Bool107.show_render = False

                    Array108.show_viewport = False
                    Array108.show_render = False
                    Array108.fit_type = 'FIT_LENGTH'
                    Array108.fit_length = 61
                    Array108.relative_offset_displace[0] = 2

                    Curve109.show_viewport = False
                    Curve109.show_render = False
                    Curve109.object = bpy.data.objects[ObjCurve]
                    Curve109.deform_axis = 'POS_X'



                    Simpledeform110.show_viewport = False
                    Simpledeform110.show_render = False
                    Simpledeform110.deform_method = 'TWIST'
                    Simpledeform110.angle = -0.523599

                    Simpledeform110.deform_axis = 'Z'

                    Simpledeform111.show_viewport = False
                    Simpledeform111.show_render = False
                    Simpledeform111.deform_method = 'TAPER'
                    Simpledeform111.factor = 0.5
                    Simpledeform111.deform_axis = 'Z'

                    Simpledeform112.show_viewport = False
                    Simpledeform112.show_render = False
                    Simpledeform112.deform_method = 'STRETCH'
                    Simpledeform112.factor = 0.1
                    Simpledeform112.deform_axis = 'Z'

                    Cast113.show_viewport = False
                    Cast113.show_render = False

                    Mirror114.mirror_object = bpy.data.objects[ObjLattice]



                    if amProperty.MOD_BOOLEAN_Bool == True:
                        Bool003_01Uniun.show_viewport = True
                        Bool003_01Uniun.show_render = True
                        Bool005_02Uniun.show_viewport = True
                        Bool005_02Uniun.show_render = True
                        Bool016_03Intersect.show_viewport = True
                        Bool016_03Intersect.show_render = True
                        Bool018_04Uniun.show_viewport = True
                        Bool018_04Uniun.show_render = True
                        Bool038_05Uniun.show_viewport = True
                        Bool038_05Uniun.show_render = True
                        Bool062_06Difference.show_viewport = True
                        Bool062_06Difference.show_render = True

                    if amProperty.MOD_WARP_Bool == True:
                        Warp010_x0.show_viewport = True
                        Warp010_x0.show_render = True
                        Warp011_x1.show_viewport = True
                        Warp011_x1.show_render = True
                        Warp012_y0.show_viewport = True
                        Warp012_y0.show_render = True
                        Warp013_y1.show_viewport = True
                        Warp013_y1.show_render = True
                        Warp014_z0.show_viewport = True
                        Warp014_z0.show_render = True
                        Warp015_z1.show_viewport = True
                        Warp015_z1.show_render = True

                        Warp021_x0.show_viewport = True
                        Warp021_x0.show_render = True
                        Warp022_x1.show_viewport = True
                        Warp022_x1.show_render = True
                        Warp023_y0.show_viewport = True
                        Warp023_y0.show_render = True
                        Warp024_y1.show_viewport = True
                        Warp024_y1.show_render = True
                        Warp025_z0.show_viewport = True
                        Warp025_z0.show_render = True
                        Warp026_z1.show_viewport = True
                        Warp026_z1.show_render = True

                        Warp053_x0.show_viewport = True
                        Warp053_x0.show_render = True
                        Warp054_x1.show_viewport = True
                        Warp054_x1.show_render = True
                        Warp055_y0.show_viewport = True
                        Warp055_y0.show_render = True
                        Warp056_y1.show_viewport = True
                        Warp056_y1.show_render = True
                        Warp057_z0.show_viewport = True
                        Warp057_z0.show_render = True
                        Warp058_z1.show_viewport = True
                        Warp058_z1.show_render = True

                    if amProperty.MOD_CURVE_Bool == True:
                        Curve045.show_viewport = True
                        Curve045.show_render = True
                        Curve061.show_viewport = True
                        Curve061.show_render = True

                    if amProperty.MOD_LATTICE_Bool == True:
                        Lattice042.show_viewport = True
                        Lattice042.show_render = True

                    if amProperty.MOD_ARRAY_Bool == True:
                        Array008.show_viewport = True
                        Array008.show_render = True			
                        Array033.show_viewport = True
                        Array033.show_render = True					
                        Array067.show_viewport = True
                        Array067.show_render = True					
                        Array076.show_viewport = True
                        Array076.show_render = True
                        Array028.show_viewport = True
                        Array028.show_render = True

                    if amProperty.MOD_SCREW_Bool == True:
                        Screw034.show_viewport = True
                        Screw034.show_render = True

                    if amProperty.MOD_TRIANGULATE_Bool == True:
                        Triangulate066.show_viewport = True
                        Triangulate066.show_render = True

                        Triangulate096.show_viewport = True
                        Triangulate096.show_render = True

                        Triangulate102.show_viewport = True
                        Triangulate102.show_render = True

                    if amProperty.MOD_SIMPLEDEFORM_Bool == True:
                        Simpledeform029.show_viewport = True
                        Simpledeform029.show_render = True
                        Simpledeform030.show_viewport = True
                        Simpledeform030.show_render = True
                        Simpledeform031.show_viewport = True
                        Simpledeform031.show_render = True

                        Simpledeform072.show_viewport = True
                        Simpledeform072.show_render = True

                        Simpledeform006.show_viewport = True
                        Simpledeform006.show_render = True

                        Simpledeform035.show_viewport = True
                        Simpledeform035.show_render = True
                        Simpledeform036.show_viewport = True
                        Simpledeform036.show_render = True

                        Simpledeform037.show_viewport = True
                        Simpledeform037.show_render = True

                        Simpledeform070.show_viewport = True
                        Simpledeform070.show_render = True

                        Simpledeform071.show_viewport = True
                        Simpledeform071.show_render = True

                        Simpledeform078.show_viewport = True
                        Simpledeform078.show_render = True

                        Simpledeform079.show_viewport = True
                        Simpledeform079.show_render = True

                        Simpledeform080.show_viewport = True
                        Simpledeform080.show_render = True

                        Simpledeform069.show_viewport = True
                        Simpledeform069.show_render = True

                        Simpledeform073.show_viewport = True
                        Simpledeform073.show_render = True

                        Simpledeform074.show_viewport = True
                        Simpledeform074.show_render = True

                        Simpledeform081.show_viewport = True
                        Simpledeform081.show_render = True

                        Simpledeform082.show_viewport = True
                        Simpledeform082.show_render = True

                        Simpledeform083.show_viewport = True
                        Simpledeform083.show_render = True

                    if amProperty.MOD_MIRROR_Bool == True:
                        Mirror106.show_viewport = True
                        Mirror106.show_render = True

                        #Mirror114.show_viewport = True
                        #Mirror114.show_render = True

                    if amProperty.RandomMaterialBool == True:
                        for i in range(0,len(ob.material_slots)):
                            ob.active_material_index = i
                            MatOld = ob.active_material
                            MatNew = MatOld.copy()
                            MatNew.name=MatNew.name[:-4]+"_"+ob.name
                            ob.data.materials[i] = MatNew
                            if len(BoolObject.material_slots) <= (len(ob.material_slots)-1):
                                BoolObject.data.materials.append(MatNew)
                            if len(BoolPlane.material_slots) <= (len(ob.material_slots)-1):
                                BoolPlane.data.materials.append(MatNew)
                            #xv=random.uniform(0, sampleProperty.xvMax)
                            if i == 0:#从这里设置材质参数
                                bpy.data.materials[MatNew.name].node_tree.nodes["PreMColor"].inputs[1].default_value = (random.uniform(0, 0.9), random.uniform(0, 0.7), random.uniform(0, 1), 1)
                                bpy.data.materials[MatNew.name].node_tree.nodes["PreMColor"].inputs[2].default_value = (random.uniform(0, 1), random.uniform(0, 0.9), random.uniform(0, 0.8), 1)
                                #bpy.data.materials["PreM00_立方体"].node_tree.nodes["混合"].inputs[1].default_value = (0.821436, 0.069368, 0.819111, 1)
                                #bpy.data.materials["PreM00_立方体"].node_tree.nodes["混合"].inputs[2].default_value = (0.0137551, 0.321451, 0.516982, 1)
                            
                            if i == 1:
                                bpy.data.materials[MatNew.name].node_tree.nodes["PreMColor"].inputs[1].default_value = (random.uniform(0, 0.3), random.uniform(0, 0.3), random.uniform(0, 0.3), 1)
                                bpy.data.materials[MatNew.name].node_tree.nodes["PreMColor"].inputs[2].default_value = (random.uniform(0.2, 0.8), random.uniform(0.2, 0.8), random.uniform(0.2, 0.8), 1)

                            if i == 2:
                                bpy.data.materials[MatNew.name].node_tree.nodes["PreMColor"].inputs[0].default_value = (random.uniform(0, 0.05), random.uniform(0, 0.05), random.uniform(0, 0.05), 1)

                            if i == 3:
                                bpy.data.materials[MatNew.name].node_tree.nodes["PreMColor"].inputs[1].default_value = (random.uniform(0, 0.5), random.uniform(0, 0.5), random.uniform(0, 0.5), 1)
                                bpy.data.materials[MatNew.name].node_tree.nodes["PreMColor"].inputs[2].default_value = (random.uniform(0.4, 1), random.uniform(0.4, 1), random.uniform(0.4, 1), 1)
                            
                            if i == 4:
                                bpy.data.materials[MatNew.name].node_tree.nodes["PreMColor"].inputs[0].default_value = (random.uniform(0, 0.4), random.uniform(0, 0.4), random.uniform(0, 0.4), 1)
                                bpy.data.materials[MatNew.name].node_tree.nodes["PreMColor"].inputs[17].default_value = (random.uniform(0, 0.8), random.uniform(0, 0.8), random.uniform(0, 0.8), 1)
                                #bpy.data.materials["PreM04_立方体"].node_tree.nodes["原理化BSDF"].inputs[17].default_value = (0.0183155, 0.253049, 0.253049, 1)


                    else:
                        for i in range(0,len(ob.material_slots)):
                            ob.active_material_index = i
                            MatOld = ob.active_material
                            if len(BoolObject.material_slots) <= (len(ob.material_slots)-1):
                                BoolObject.data.materials.append(MatOld)
                            if len(BoolPlane.material_slots) <= (len(ob.material_slots)-1):
                                BoolPlane.data.materials.append(MatOld)


                elif amProperty.GenMechEnum =='Helmet':
                    ob.modifiers.clear()

                    Skin001 = ob.modifiers.new("1_Skin", "SKIN")
                    Array002 = ob.modifiers.new("2_$$$Array$$$", "ARRAY")
                    Displace003 = ob.modifiers.new("3_Displace", "DISPLACE")
                    Displace004 = ob.modifiers.new("4_Displace", "DISPLACE")
                    Cast005 = ob.modifiers.new("5_Cast", "CAST")
                    Displace006 = ob.modifiers.new("6_Displace", "DISPLACE")
                    Bevel007 = ob.modifiers.new("7_Bevel", "BEVEL")
                    Displace08 = ob.modifiers.new("8_Displace", "DISPLACE")
                    Wave009 = ob.modifiers.new('9_Wave', 'WAVE')
                    Wireframe010 = ob.modifiers.new('10_Wireframe', 'WIREFRAME')
                    Screw011 = ob.modifiers.new("11_Screw", "SCREW")
                    Remesh012 = ob.modifiers.new("121Remesh","REMESH")
                    Displace013 = ob.modifiers.new("Displace013", "DISPLACE")
                    Bool014 = ob.modifiers.new("Bool014++++++++++", "BOOLEAN")
                    Decimate015 = ob.modifiers.new("Decimate015", "DECIMATE")
                    Build016 = ob.modifiers.new("Build016", "BUILD")
                    Displace017 = ob.modifiers.new("Displace017", "DISPLACE")
                    Smooth018 = ob.modifiers.new("Smooth018", "SMOOTH")
                    Displace019 = ob.modifiers.new("Displace019", "DISPLACE")
                    Subsurf020 = ob.modifiers.new("Subsurf020", "SUBSURF")
                    Decimate021 = ob.modifiers.new("Decimate021", "DECIMATE")
                    Displace022 = ob.modifiers.new("Displace022", "DISPLACE")
                    Smooth023 = ob.modifiers.new("Smooth023", "SMOOTH")
                    Decimate024 = ob.modifiers.new("Decimate024", "DECIMATE")
                    Screw025 = ob.modifiers.new("Screw025", "SCREW")
                    Bool026 = ob.modifiers.new("Bool026++++++++++", "BOOLEAN")
                    Simpledeform027 = ob.modifiers.new("27_&&&&Simpledeform", "SIMPLE_DEFORM")
                    Simpledeform028 = ob.modifiers.new("28_&&&&Simpledeform", "SIMPLE_DEFORM")
                    Simpledeform029 = ob.modifiers.new("29_&&&&Simpledeform", "SIMPLE_DEFORM")
                    Edgesplit030 = ob.modifiers.new("Edgesplit030", "EDGE_SPLIT")
                    Displace031 = ob.modifiers.new("Displace031", "DISPLACE")
                    Screw032 = ob.modifiers.new("Screw032", "SCREW")
                    Decimate033 = ob.modifiers.new("Decimate033", "DECIMATE")
                    Displace034 = ob.modifiers.new("Displace034", "DISPLACE")
                    Smooth035 = ob.modifiers.new("Smooth035", "SMOOTH")
                    Wave036 = ob.modifiers.new('Wave036', 'WAVE')
                    Ocean037 = ob.modifiers.new('Ocean037', 'OCEAN')
                    Cast038 = ob.modifiers.new("Cast038", "CAST")
                    Displace039 = ob.modifiers.new("Displace039", "DISPLACE")
                    Bool040 = ob.modifiers.new("Bool040++++++++++", "BOOLEAN")
                    Cast041 = ob.modifiers.new("Cast041", "CAST")
                    Simpledeform042 = ob.modifiers.new("42_&&&&Simpledeform", "SIMPLE_DEFORM")
                    Remesh043 = ob.modifiers.new("Remesh043","REMESH")
                    Simpledeform070 = ob.modifiers.new("70_&&&&Simpledeform", "SIMPLE_DEFORM")
                    Smooth044 = ob.modifiers.new("Smooth044", "SMOOTH")
                    Laplaciansmooth45 = ob.modifiers.new("Laplaciansmooth45", "LAPLACIANSMOOTH")
                    Bool046 = ob.modifiers.new("Bool046++++++++++", "BOOLEAN")
                    Cast047 = ob.modifiers.new("Cast047", "CAST")
                    Cast048 = ob.modifiers.new("Cast048", "CAST")
                    Simpledeform049 = ob.modifiers.new("049_&&&&Simpledeform", "SIMPLE_DEFORM")
                    Simpledeform050 = ob.modifiers.new("050_&&&&Simpledeform", "SIMPLE_DEFORM")
                    Simpledeform051 = ob.modifiers.new("051_&&&&Simpledeform", "SIMPLE_DEFORM")
                    Simpledeform052 = ob.modifiers.new("052_&&&&Simpledeform", "SIMPLE_DEFORM")
                    Simpledeform053 = ob.modifiers.new("053_&&&&Simpledeform", "SIMPLE_DEFORM")
                    Simpledeform054 = ob.modifiers.new("054_&&&&Simpledeform", "SIMPLE_DEFORM")
                    Bool055 = ob.modifiers.new("Bool055++++++++++", "BOOLEAN")
                    Decimate056 = ob.modifiers.new("Decimate056", "DECIMATE")
                    Bevel057 = ob.modifiers.new("Bevel057", "BEVEL")
                    Triangulate058 = ob.modifiers.new("Triangulate058", "TRIANGULATE")
                    Edgesplit059 = ob.modifiers.new("Edgesplit059", "EDGE_SPLIT")
                    Solidify60 = ob.modifiers.new("Solidify60", "SOLIDIFY")
                    Solidify61 = ob.modifiers.new("Solidify61", "SOLIDIFY")
                    Mirror062 = ob.modifiers.new('Mirror062', 'MIRROR')
                    Array063 = ob.modifiers.new("63_$$$Array$$$", "ARRAY")
                    Curve064 = ob.modifiers.new("Curve064", "CURVE")
                    Simpledeform065 = ob.modifiers.new("65_&&&&Simpledeform", "SIMPLE_DEFORM")
                    Simpledeform066 = ob.modifiers.new("66_&&&&Simpledeform", "SIMPLE_DEFORM")
                    Simpledeform067 = ob.modifiers.new("67_&&&&Simpledeform", "SIMPLE_DEFORM")
                    Cast068 = ob.modifiers.new("Cast068", "CAST")
                    Mirror069 = ob.modifiers.new('Mirror069', 'MIRROR')


                    for mod in ob.modifiers:
                        mod.show_viewport = False
                        mod.show_render = False

                    Array002.show_on_cage = True
                    Array002.show_in_editmode = True
                    Array002.show_viewport = True
                    Array002.show_render = True
                    Array002.count = 2
                    Array002.use_relative_offset = True
                    Array002.relative_offset_displace[0] = 0
                    Array002.relative_offset_displace[2] = 0.4

                    Displace003.show_on_cage = True
                    Displace003.show_in_editmode = True
                    Displace003.show_viewport = True
                    Displace003.show_render = True
                    Displace003.strength = 5
                    Displace003.mid_level = 0.5

                    Displace004.show_on_cage = True
                    Displace004.show_in_editmode = True
                    Displace004.show_viewport = True
                    Displace004.show_render = True
                    Displace004.strength = 1
                    Displace004.mid_level = 0.5

                    Cast005.show_on_cage = True
                    Cast005.show_in_editmode = True
                    Cast005.show_viewport = True
                    Cast005.show_render = True
                    Cast005.cast_type = 'CYLINDER'
                    Cast005.use_x = True
                    Cast005.use_y = True
                    Cast005.use_z = True
                    Cast005.factor = -0.78
                    Cast005.radius = 5.2
                    Cast005.size = 5.7
                    Cast005.use_radius_as_size = True

                    Displace006.show_on_cage = True
                    Displace006.show_in_editmode = True
                    Displace006.show_viewport = True
                    Displace006.show_render = True
                    Displace006.strength = 1.3
                    Displace006.mid_level = 0.5

                    Bevel007.show_in_editmode = True
                    Bevel007.show_viewport = True
                    Bevel007.show_render = True
                    Bevel007.affect = 'EDGES'
                    Bevel007.offset_type = 'OFFSET'
                    Bevel007.width = 0.5
                    Bevel007.segments = 1
                    Bevel007.use_clamp_overlap = True
                    Bevel007.loop_slide = True
                    Bevel007.material = 2

                    Displace08.show_in_editmode = True
                    Displace08.show_viewport = True
                    Displace08.show_render = True
                    Displace08.strength = 1.3
                    Displace08.mid_level = 0.5

                    Wave009.show_in_editmode = True
                    Wave009.show_viewport = True
                    Wave009.show_render = True
                    Wave009.use_cyclic = True
                    Wave009.falloff_radius = 0
                    Wave009.height = 0.5
                    Wave009.width = 1.5
                    Wave009.narrowness = 1.5
                    Wave009.time_offset = 2.6
                    Wave009.lifetime = 0
                    Wave009.damping_time = 1
                    Wave009.speed = 0.25

                    Wireframe010.thickness = 0.375
                    Wireframe010.offset = 0
                    Wireframe010.use_boundary = True
                    Wireframe010.use_replace = False
                    Wireframe010.use_even_offset = False
                    Wireframe010.use_relative_offset = True
                    Wireframe010.material_offset = 1

                    Screw011.angle = 1.46957
                    Screw011.screw_offset = 0
                    Screw011.iterations = 1
                    Screw011.axis = 'X'
                    Screw011.steps = 8
                    Screw011.render_steps = 8


                    Remesh012.show_in_editmode = True
                    Remesh012.show_viewport = True
                    Remesh012.show_render = True
                    Remesh012.mode = 'SMOOTH'
                    Remesh012.octree_depth = 4
                    Remesh012.scale = 0.8986
                    Remesh012.use_smooth_shade = False

                    Displace013.show_in_editmode = True
                    Displace013.show_viewport = True
                    Displace013.show_render = True
                    Displace013.strength = 1
                    Displace013.mid_level = 0.5

                    Decimate015.decimate_type = 'COLLAPSE'
                    Decimate015.ratio = 0.404
                    Decimate015.use_collapse_triangulate = False
                    Decimate015.use_symmetry = False

                    Build016.show_viewport = True
                    Build016.show_render = True
                    Build016.frame_start = -1
                    Build016.frame_duration = 1
                    Build016.use_reverse = False
                    Build016.use_random_order = True
                    Build016.seed = 12


                    Displace017.show_in_editmode = True
                    Displace017.show_viewport = True
                    Displace017.show_render = True
                    Displace017.strength = 1
                    Displace017.mid_level = 0.5

                    Smooth018.show_in_editmode = True
                    Smooth018.show_viewport = True
                    Smooth018.show_render = True
                    Smooth018.use_x = True
                    Smooth018.use_y = True
                    Smooth018.use_z = True
                    Smooth018.factor = 1
                    Smooth018.iterations = 1

                    Displace019.show_in_editmode = True
                    Displace019.show_viewport = True
                    Displace019.show_render = True
                    Displace019.strength = 1
                    Displace019.mid_level = 0.5

                    Subsurf020.render_levels = 1

                    Decimate021.decimate_type = 'COLLAPSE'
                    Decimate021.ratio = 0.404
                    Decimate021.use_collapse_triangulate = False
                    Decimate021.use_symmetry = False

                    Displace022.show_in_editmode = True
                    Displace022.show_viewport = True
                    Displace022.show_render = True
                    Displace022.strength = 1
                    Displace022.mid_level = 0.5

                    Smooth023.show_in_editmode = True
                    Smooth023.show_viewport = True
                    Smooth023.show_render = True
                    Smooth023.use_x = True
                    Smooth023.use_y = True
                    Smooth023.use_z = True
                    Smooth023.factor = 1
                    Smooth023.iterations = 1

                    Decimate024.show_viewport = True
                    Decimate024.show_render = True
                    Decimate024.decimate_type = 'COLLAPSE'
                    Decimate024.ratio = 0.429715
                    Decimate024.use_collapse_triangulate = False

                    Screw025.show_in_editmode = True
                    Screw025.show_viewport = True
                    Screw025.show_render = True
                    Screw025.angle = 1.5708
                    Screw025.screw_offset = 5
                    Screw025.iterations = 2
                    Screw025.axis = 'Z'
                    Screw025.steps = 8
                    Screw025.render_steps = 8
                    Screw025.use_merge_vertices = False

                    Simpledeform027.show_in_editmode = True
                    Simpledeform027.show_viewport = True
                    Simpledeform027.show_render = True
                    Simpledeform027.deform_method = 'TWIST'
                    Simpledeform027.angle = 0.969986
                    Simpledeform027.deform_axis = 'X'

                    Simpledeform028.deform_method = 'TWIST'
                    Simpledeform028.angle = 0.942478
                    Simpledeform028.deform_axis = 'Y'

                    Simpledeform029.deform_method = 'TWIST'#或bend弯曲
                    Simpledeform029.angle = 0.696386
                    Simpledeform029.deform_axis = 'Y'

                    Edgesplit030.show_in_editmode = True
                    Edgesplit030.show_viewport = True
                    Edgesplit030.show_render = True
                    Edgesplit030.use_edge_angle = True
                    Edgesplit030.split_angle = 0.47822
                    Edgesplit030.use_edge_sharp = True

                    Displace031.strength = 1.1
                    Displace031.mid_level = 0.5

                    Screw032.angle = 1.6057
                    Screw032.screw_offset = 0
                    Screw032.iterations = 1
                    Screw032.axis = 'Y'
                    Screw032.steps = 8
                    Screw032.render_steps = 8

                    Decimate033.decimate_type = 'COLLAPSE'
                    Decimate033.ratio = 0.14

                    Displace034.strength = 1.1
                    Displace034.mid_level = 0.46

                    Smooth035.show_in_editmode = True
                    Smooth035.show_viewport = True
                    Smooth035.show_render = True
                    Smooth035.use_x = True
                    Smooth035.use_y = True
                    Smooth035.use_z = True
                    Smooth035.factor = 3

                    Wave036.show_viewport = True
                    Wave036.show_render = True
                    Wave036.use_x = True
                    Wave036.use_y = True
                    Wave036.use_cyclic = False
                    Wave036.falloff_radius = 0
                    Wave036.height = 0.5
                    Wave036.width = 1.5
                    Wave036.narrowness = 1.5
                    Wave036.time_offset = 3.4
                    Wave036.lifetime = 0
                    Wave036.damping_time = 1
                    Wave036.speed = 0.25

                    Ocean037.geometry_mode = 'DISPLACE'
                    Ocean037.resolution = 5#分辨率
                    Ocean037.time = 2.49#时间
                    Ocean037.depth = 200#深度
                    Ocean037.size = 1.07##尺寸
                    Ocean037.spatial_size = 54###空间尺寸
                    Ocean037.random_seed = 0##随机种
                    Ocean037.wave_scale = 1#wave_scale->size 缩放影响尺寸 0不动
                    Ocean037.wave_scale_min = 0.01#最小波浪
                    Ocean037.choppiness = 1#翻滚度
                    Ocean037.wind_velocity = 30#风速 小的时候才能变
                    Ocean037.wave_alignment = 0#对齐 打开下两选项
                    Ocean037.wave_direction = 0#方向
                    Ocean037.damping = 0.5#阻尼

                    Cast038.show_in_editmode = True
                    Cast038.show_viewport = True
                    Cast038.show_render = True
                    Cast038.use_x = True
                    Cast038.use_y = True
                    Cast038.use_z = True
                    Cast038.cast_type = 'CYLINDER'
                    Cast038.factor = 0.278158
                    Cast038.radius = 0
                    Cast038.size = 0
                    Cast038.use_radius_as_size = True

                    Displace039.show_in_editmode = True
                    Displace039.show_viewport = True
                    Displace039.show_render = True
                    Displace039.strength = 1
                    Displace039.mid_level = 0.5

                    Cast041.show_in_editmode = True
                    Cast041.show_viewport = True
                    Cast041.show_render = True
                    Cast041.use_x = True
                    Cast041.use_y = True
                    Cast041.use_z = True
                    Cast041.cast_type = 'CYLINDER'
                    Cast041.factor = 0.324562
                    Cast041.radius = 0
                    Cast041.size = 0
                    Cast041.use_radius_as_size = True

                    Simpledeform042.show_in_editmode = True
                    Simpledeform042.show_viewport = True
                    Simpledeform042.show_render = True
                    Simpledeform042.deform_method = 'TWIST'
                    Simpledeform042.angle = 0.969986
                    Simpledeform042.deform_axis = 'X'

                    Remesh043.show_in_editmode = True
                    Remesh043.show_viewport = True
                    Remesh043.show_render = True
                    Remesh043.mode = 'SMOOTH'
                    Remesh043.octree_depth = 4
                    Remesh043.scale = 0.9
                    Remesh043.use_remove_disconnected = True
                    Remesh043.threshold = 1
                    Remesh043.use_smooth_shade = True

                    Simpledeform070.show_render = True
                    Simpledeform070.deform_method = 'STRETCH'
                    Simpledeform070.factor = 0
                    Simpledeform070.deform_axis = 'Z'

                    Smooth044.use_x = False
                    Smooth044.use_y = False
                    Smooth044.use_z = True#两短一长选最长，平滑一部分就好
                    Smooth044.factor = 2
                    Smooth044.iterations = 1

                    Laplaciansmooth45.show_in_editmode = True
                    Laplaciansmooth45.show_viewport = True
                    Laplaciansmooth45.show_render = True
                    Laplaciansmooth45.iterations = 1
                    Laplaciansmooth45.use_x = True
                    Laplaciansmooth45.use_y = True
                    Laplaciansmooth45.use_z = True
                    Laplaciansmooth45.lambda_factor = 0.25
                    Laplaciansmooth45.lambda_border = 0.1
                    Laplaciansmooth45.use_volume_preserve = True
                    Laplaciansmooth45.use_normalized = True

                    Cast047.show_in_editmode = True
                    Cast047.show_viewport = True
                    Cast047.show_render = True
                    Cast047.use_x = True
                    Cast047.use_y = True
                    Cast047.use_z = True
                    Cast047.cast_type = 'CUBOID'
                    Cast047.factor = 0.349905
                    Cast047.radius = 0
                    Cast047.size = 0
                    Cast047.use_radius_as_size = True

                    Cast048.show_in_editmode = True
                    Cast048.show_viewport = True
                    Cast048.show_render = True
                    Cast048.cast_type = 'SPHERE'
                    Cast048.use_z = True
                    Cast048.use_x = False
                    Cast048.use_y = False

                    Cast048.factor = 0.349907
                    Cast048.radius = 0
                    Cast048.size = 0
                    Cast048.use_radius_as_size = True

                    Simpledeform049.show_in_editmode = True
                    Simpledeform049.show_viewport = True
                    Simpledeform049.show_render = True
                    Simpledeform049.deform_method = 'TWIST'
                    Simpledeform049.angle = 0.942061
                    Simpledeform049.deform_axis = 'Y'

                    Simpledeform050.show_in_editmode = True
                    Simpledeform050.show_viewport = True
                    Simpledeform050.show_render = True
                    Simpledeform050.deform_method = 'BEND'
                    Simpledeform050.angle = 0.942061
                    Simpledeform050.deform_axis = 'X'

                    Simpledeform051.show_in_editmode = True
                    Simpledeform051.show_viewport = True
                    Simpledeform051.show_render = True
                    Simpledeform051.deform_method = 'TAPER'
                    Simpledeform051.factor = 0.9
                    Simpledeform051.deform_axis = 'X'

                    Simpledeform052.deform_method = 'TAPER'
                    Simpledeform052.factor = 1.6
                    Simpledeform052.deform_axis = 'X'

                    Simpledeform053.deform_method = 'STRETCH'
                    Simpledeform053.factor = 0.4
                    Simpledeform053.deform_axis = 'X'

                    Simpledeform054.deform_method = 'TWIST'
                    Simpledeform054.angle = -1.8326
                    Simpledeform054.deform_axis = 'X'

                    Decimate056.show_viewport = True
                    Decimate056.show_render = True
                    Decimate056.decimate_type = 'DISSOLVE'
                    Decimate056.angle_limit = 0.0872665
                    Decimate056.delimit = {'NORMAL', 'MATERIAL', 'SEAM', 'SHARP', 'UV'}
                    Decimate056.use_dissolve_boundaries = True

                    Bevel057.show_in_editmode = True
                    Bevel057.show_viewport = True
                    Bevel057.show_render = True
                    Bevel057.affect = 'EDGES'
                    Bevel057.offset_type = 'OFFSET'
                    Bevel057.width = 0.1
                    Bevel057.segments = 1
                    Bevel057.limit_method = 'ANGLE'
                    Bevel057.angle_limit = 0.436332
                    Bevel057.use_clamp_overlap = True
                    Bevel057.loop_slide = True
                    Bevel057.material = 2

                    Edgesplit059.use_edge_angle = True
                    Edgesplit059.split_angle = 0.261799
                    Edgesplit059.use_edge_sharp = True

                    Solidify60.show_in_editmode = True
                    Solidify60.show_viewport = True
                    Solidify60.show_render = True
                    Solidify60.solidify_mode = 'EXTRUDE'
                    Solidify60.thickness = 0.1
                    Solidify60.offset = 1
                    Solidify60.use_even_offset = False
                    Solidify60.use_rim = True
                    Solidify60.use_rim_only = True
                    Solidify60.material_offset_rim = 3

                    Triangulate058.show_render = True
                    Edgesplit059.show_render = True
                    Solidify61.show_render = True

                    Solidify61.solidify_mode = 'EXTRUDE'
                    Solidify61.thickness = -0.05
                    Solidify61.offset = -1
                    Solidify61.use_even_offset = False
                    Solidify61.use_rim = True
                    Solidify61.use_rim_only = True
                    Solidify61.material_offset_rim = 1

                    Mirror062.show_in_editmode = True
                    Mirror062.show_viewport = True
                    Mirror062.show_render = True
                    Mirror062.use_axis[0] = True
                    Mirror062.use_bisect_axis[0] = True
                    Mirror062.use_bisect_flip_axis[0] = True

                    Simpledeform065.show_in_editmode = True
                    Simpledeform065.show_viewport = True
                    Simpledeform065.show_render = True
                    Simpledeform065.deform_method = 'TAPER'
                    Simpledeform065.factor = 0.7
                    Simpledeform065.deform_axis = 'Z'

                    Simpledeform066.deform_method = 'STRETCH'
                    Simpledeform066.factor = 0.2
                    Simpledeform066.deform_axis = 'Z'

                    Simpledeform067.deform_method = 'BEND'
                    Simpledeform067.angle = -0.785398
                    Simpledeform067.deform_axis = 'Z'

                    Cast068.use_y = True
                    Cast068.use_z = True
                    Cast068.factor = -0.235582
                    Cast068.radius = 0
                    Cast068.size = 0
                    Cast068.use_radius_as_size = True

                    ob.data.use_auto_smooth = True
                    ob.data.auto_smooth_angle = 0.523599

                    if amProperty.RandomMaterialBool == True:
                        for i in range(0,len(ob.material_slots)):
                            ob.active_material_index = i
                            MatOld = ob.active_material
                            MatNew = MatOld.copy()
                            MatNew.name=MatNew.name[:-4]+"_"+ob.name
                            ob.data.materials[i] = MatNew
                            if i == 0:#从这里设置材质参数
                                bpy.data.materials[MatNew.name].node_tree.nodes["PreMColor"].inputs[1].default_value = (random.uniform(0, 0.9), random.uniform(0, 0.7), random.uniform(0, 1), 1)
                                bpy.data.materials[MatNew.name].node_tree.nodes["PreMColor"].inputs[2].default_value = (random.uniform(0, 1), random.uniform(0, 0.9), random.uniform(0, 0.8), 1)
                            
                            if i == 1:
                                bpy.data.materials[MatNew.name].node_tree.nodes["PreMColor"].inputs[1].default_value = (random.uniform(0, 0.3), random.uniform(0, 0.3), random.uniform(0, 0.3), 1)
                                bpy.data.materials[MatNew.name].node_tree.nodes["PreMColor"].inputs[2].default_value = (random.uniform(0.2, 0.8), random.uniform(0.2, 0.8), random.uniform(0.2, 0.8), 1)

                            if i == 2:
                                bpy.data.materials[MatNew.name].node_tree.nodes["PreMColor"].inputs[0].default_value = (random.uniform(0, 0.05), random.uniform(0, 0.05), random.uniform(0, 0.05), 1)

                            if i == 3:
                                bpy.data.materials[MatNew.name].node_tree.nodes["PreMColor"].inputs[1].default_value = (random.uniform(0, 0.5), random.uniform(0, 0.5), random.uniform(0, 0.5), 1)
                                bpy.data.materials[MatNew.name].node_tree.nodes["PreMColor"].inputs[2].default_value = (random.uniform(0.4, 1), random.uniform(0.4, 1), random.uniform(0.4, 1), 1)
                            
                            if i == 4:
                                bpy.data.materials[MatNew.name].node_tree.nodes["PreMColor"].inputs[0].default_value = (random.uniform(0, 0.4), random.uniform(0, 0.4), random.uniform(0, 0.4), 1)
                                bpy.data.materials[MatNew.name].node_tree.nodes["PreMColor"].inputs[17].default_value = (random.uniform(0, 0.8), random.uniform(0, 0.8), random.uniform(0, 0.8), 1)


            for mod in ob.modifiers:
                mod.show_expanded = False
                mod.show_in_editmode = False
                if (mod.type =='BOOLEAN') and bpy.app.version >= (2, 92, 0):
                    mod.solver ='FAST'

        if len(OBJNameList) != 0:
            NumCount=count(0, 1)
            bpy.ops.object.select_all(action='DESELECT')
            for OBJName in OBJNameList:

                ob= bpy.data.objects[OBJName]
                bpy.context.view_layer.objects.active = ob

                #bpy.data.objects[OBJName].select_set(True)
                #NumOBJ=len(OBJModEndList)
                Num=int(next(NumCount))
                start = int(OBJModEndList[Num])+1
                end= int(OBJModEndList[Num+1])-1
                #Modparam[4+int(next(ModCount))]
                #OBJModEndList[]
                #else:
                ob.modifiers.clear()
                #ob.constraints.clear()
                amProperty.GenMechEnum = amProperty.GenMechName
                #FolderPath=os.path.dirname(__file__)+'\\Preset\\'
                #with open(FolderPath + amProperty.GenMechEnum + ".txt") as f:
                f = open(File, encoding='utf-8')#f = open(File)
                for OBJline in islice(f,start,end):
                    Modparam = OBJline.split("|")#####split
                    Conparam = OBJline.split("|")
                    ConPreType=Conparam[1]
                    ConType=ConPreType[4:]

                    i=0
                    if Modparam[1] == "SKIN":#Type
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.branch_smoothing=float(Modparam[5])
                        Mod.branch_smoothing=str_to_bool(Modparam[6])
                        Mod.branch_smoothing=str_to_bool(Modparam[7])
                        Mod.branch_smoothing=str_to_bool(Modparam[8])
                        Mod.branch_smoothing=str_to_bool(Modparam[9])
                    elif Modparam[1] == "CAST":#Type
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.cast_type= real_str(Modparam[5])
                        Mod.use_x = str_to_bool(Modparam[6])
                        Mod.use_y = str_to_bool(Modparam[7])
                        Mod.use_z = str_to_bool(Modparam[8])
                        Mod.factor = float(Modparam[9])
                        Mod.radius = float(Modparam[10])
                        Mod.size = float(Modparam[11])
                        Mod.use_radius_as_size = str_to_bool(Modparam[12])
                        Mod.vertex_group = real_str(Modparam[13])
                        Mod.invert_vertex_group = str_to_bool(Modparam[14])
                        Mod.object = str_to_obj(Modparam[15])
                        Mod.use_transform = str_to_bool(Modparam[16])
                    elif Modparam[1] == "BOOLEAN":#real_str str_to_obj str_to_bool (Modparam[4+int(next(ModCount))])
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        
                        Mod.operation=real_str(Modparam[4+int(next(ModCount))])#int(next(ModCount))
                        Mod.object = str_to_obj(Modparam[4+int(next(ModCount))])
                        Mod.double_threshold = float(Modparam[4+int(next(ModCount))])
                        if (bpy.app.version >= (2, 92, 0)) and (len(Modparam)>=10):
                            Mod.solver =Modparam[4+int(next(ModCount))]
                            Mod.use_self = str_to_bool(Modparam[4+int(next(ModCount))])

                    elif Modparam[1] == "REMESH":#real_str str_to_obj str_to_bool float int
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        
                        Mod.mode=real_str(Modparam[4+int(next(ModCount))])#int(next(ModCount))
                        Mod.octree_depth = int(Modparam[4+int(next(ModCount))])
                        Mod.scale = float(Modparam[4+int(next(ModCount))])
                        Mod.use_remove_disconnected = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.threshold = float(Modparam[4+int(next(ModCount))])
                        Mod.use_smooth_shade = str_to_bool(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == "SIMPLE_DEFORM":#real_str str_to_obj str_to_bool float int
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        
                        Mod.deform_method=real_str(Modparam[4+int(next(ModCount))])
                        Mod.angle = float(Modparam[4+int(next(ModCount))])
                        Mod.origin = str_to_obj(Modparam[4+int(next(ModCount))])
                        Mod.deform_axis = real_str(Modparam[4+int(next(ModCount))])
                        Mod.limits[0] = float(Modparam[4+int(next(ModCount))])
                        Mod.limits[1] = float(Modparam[4+int(next(ModCount))])
                        Mod.lock_x = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.lock_y = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.lock_z = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.vertex_group=real_str(Modparam[4+int(next(ModCount))])
                        Mod.invert_vertex_group = str_to_bool(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == "DISPLACE":#Type real_str str_to_obj str_to_bool (Modparam[4+int(next(ModCount))])
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        
                        Mod.texture=str_to_obj(Modparam[4+int(next(ModCount))])#int(next(ModCount))
                        Mod.direction = real_str(Modparam[4+int(next(ModCount))])
                        Mod.space = real_str(Modparam[4+int(next(ModCount))])
                        Mod.strength = float(Modparam[4+int(next(ModCount))])
                        Mod.mid_level = float(Modparam[4+int(next(ModCount))])
                        Mod.vertex_group = real_str(Modparam[4+int(next(ModCount))])
                        Mod.invert_vertex_group = str_to_bool(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == "ARRAY":#real_str str_to_obj str_to_bool float int
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        
                        Mod.fit_type=real_str(Modparam[4+int(next(ModCount))])
                        Mod.count = int(Modparam[4+int(next(ModCount))])
                        Mod.use_relative_offset = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.relative_offset_displace[0] = float(Modparam[4+int(next(ModCount))])
                        Mod.relative_offset_displace[1] = float(Modparam[4+int(next(ModCount))])
                        Mod.relative_offset_displace[2] = float(Modparam[4+int(next(ModCount))])
                        Mod.use_constant_offset = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.constant_offset_displace[0] = float(Modparam[4+int(next(ModCount))])
                        Mod.constant_offset_displace[1] = float(Modparam[4+int(next(ModCount))])
                        Mod.constant_offset_displace[2] = float(Modparam[4+int(next(ModCount))])
                        Mod.use_object_offset = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.offset_object = str_to_obj(Modparam[4+int(next(ModCount))])
                        Mod.use_merge_vertices = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.merge_threshold = float(Modparam[4+int(next(ModCount))])
                        Mod.use_merge_vertices_cap = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.offset_u = float(Modparam[4+int(next(ModCount))])
                        Mod.offset_v = float(Modparam[4+int(next(ModCount))])
                        Mod.start_cap = str_to_obj(Modparam[4+int(next(ModCount))])
                        Mod.end_cap = str_to_obj(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == 'WARP':#real_str str_to_obj str_to_bool float int
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        
                        Mod.object_from = str_to_obj(Modparam[4+int(next(ModCount))])
                        Mod.object_to = str_to_obj(Modparam[4+int(next(ModCount))])
                        Mod.use_volume_preserve = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.strength = float(Modparam[4+int(next(ModCount))])
                        Mod.vertex_group = real_str(Modparam[4+int(next(ModCount))])
                        Mod.invert_vertex_group = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.falloff_type = real_str(Modparam[4+int(next(ModCount))])
                        Mod.falloff_radius= float(Modparam[4+int(next(ModCount))])
                        Mod.texture = str_to_obj(Modparam[4+int(next(ModCount))])
                        Mod.texture_coords =  real_str(Modparam[4+int(next(ModCount))])#real_str(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == "WIREFRAME":#real_str str_to_obj str_to_bool float int
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        
                        Mod.thickness = float(Modparam[4+int(next(ModCount))])
                        Mod.offset = float(Modparam[4+int(next(ModCount))])
                        Mod.use_boundary = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_replace = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_even_offset = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_relative_offset = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_crease = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.crease_weight = float(Modparam[4+int(next(ModCount))])
                        Mod.material_offset = int(Modparam[4+int(next(ModCount))])
                        Mod.vertex_group = real_str(Modparam[4+int(next(ModCount))])
                        Mod.invert_vertex_group = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.thickness_vertex_group = float(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == "SCREW":#real_str str_to_obj str_to_bool float int
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        
                        Mod.angle = float(Modparam[4+int(next(ModCount))])
                        Mod.screw_offset = float(Modparam[4+int(next(ModCount))])
                        Mod.iterations = int(Modparam[4+int(next(ModCount))])
                        Mod.axis = real_str(Modparam[4+int(next(ModCount))])
                        Mod.object = str_to_obj(Modparam[4+int(next(ModCount))])
                        Mod.use_object_screw_offset = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.steps = int(Modparam[4+int(next(ModCount))])
                        Mod.render_steps = int(Modparam[4+int(next(ModCount))])
                        Mod.use_merge_vertices = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.merge_threshold = float(Modparam[4+int(next(ModCount))])
                        Mod.use_stretch_u = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_stretch_v = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_smooth_shade = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_normal_calculate = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_normal_flip = str_to_bool(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == "SHRINKWRAP":#real_str str_to_obj str_to_bool float int
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.wrap_method = real_str(Modparam[4+int(next(ModCount))])
                        Mod.wrap_mode = real_str(Modparam[4+int(next(ModCount))])
                        Mod.target = str_to_obj(Modparam[4+int(next(ModCount))])
                        Mod.offset = float(Modparam[4+int(next(ModCount))])
                        Mod.vertex_group = real_str(Modparam[4+int(next(ModCount))])
                        Mod.invert_vertex_group = str_to_bool(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == "WAVE":#real_str str_to_obj str_to_bool float int Mod.invert_vertex_group
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.use_x = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_y = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_cyclic = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_normal = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_normal_x = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_normal_y = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_normal_z = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.falloff_radius = float(Modparam[4+int(next(ModCount))])
                        Mod.height = float(Modparam[4+int(next(ModCount))])
                        Mod.width = float(Modparam[4+int(next(ModCount))])
                        Mod.narrowness = float(Modparam[4+int(next(ModCount))])
                        Mod.vertex_group = real_str(Modparam[4+int(next(ModCount))])
                        Mod.invert_vertex_group = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.start_position_object = str_to_obj(Modparam[4+int(next(ModCount))])
                        Mod.start_position_x = float(Modparam[4+int(next(ModCount))])
                        Mod.start_position_y = float(Modparam[4+int(next(ModCount))])
                        Mod.time_offset = float(Modparam[4+int(next(ModCount))])
                        Mod.lifetime = float(Modparam[4+int(next(ModCount))])
                        Mod.damping_time = float(Modparam[4+int(next(ModCount))])
                        Mod.speed = float(Modparam[4+int(next(ModCount))])
                        Mod.texture = str_to_obj(Modparam[4+int(next(ModCount))])
                        Mod.texture_coords = real_str(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == "LAPLACIANSMOOTH":#real_str str_to_obj str_to_bool float int Mod.invert_vertex_group
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        
                        Mod.iterations = int(Modparam[4+int(next(ModCount))])
                        Mod.use_x = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_y = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_z = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.lambda_factor = float(Modparam[4+int(next(ModCount))])
                        Mod.lambda_border = float(Modparam[4+int(next(ModCount))])
                        Mod.use_volume_preserve = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_normalized = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.vertex_group = real_str(Modparam[4+int(next(ModCount))])
                        Mod.invert_vertex_group = str_to_bool(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == "LATTICE":#real_str str_to_obj str_to_bool float int Mod.invert_vertex_group
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        
                        Mod.object = str_to_obj(Modparam[4+int(next(ModCount))])
                        Mod.vertex_group = real_str(Modparam[4+int(next(ModCount))])
                        Mod.invert_vertex_group = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.strength = float(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == "BEVEL":#real_str str_to_obj str_to_bool float int Mod.invert_vertex_group
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        
                        Mod.affect = real_str(Modparam[4+int(next(ModCount))])
                        Mod.offset_type = real_str(Modparam[4+int(next(ModCount))])
                        Mod.width_pct = float(Modparam[4+int(next(ModCount))])
                        Mod.segments = int(Modparam[4+int(next(ModCount))])
                        Mod.angle_limit = float(Modparam[4+int(next(ModCount))])
                        Mod.limit_method = real_str(Modparam[4+int(next(ModCount))])
                        Mod.vertex_group = real_str(Modparam[4+int(next(ModCount))])
                        Mod.invert_vertex_group = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.profile_type = real_str(Modparam[4+int(next(ModCount))])
                        Mod.profile = float(Modparam[4+int(next(ModCount))])
                        Mod.miter_outer = real_str(Modparam[4+int(next(ModCount))])
                        Mod.miter_inner = real_str(Modparam[4+int(next(ModCount))])
                        Mod.spread = float(Modparam[4+int(next(ModCount))])
                        Mod.vmesh_method = real_str(Modparam[4+int(next(ModCount))])
                        Mod.use_clamp_overlap = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.loop_slide = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.harden_normals = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.mark_seam = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.mark_sharp = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.material = int(Modparam[4+int(next(ModCount))])
                        Mod.face_strength_mode = real_str(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == "DECIMATE":#real_str str_to_obj str_to_bool float int Mod.invert_vertex_group
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        
                        Mod.decimate_type = real_str(Modparam[4+int(next(ModCount))])
                        Mod.ratio = float(Modparam[4+int(next(ModCount))])
                        Mod.use_symmetry = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.symmetry_axis = real_str(Modparam[4+int(next(ModCount))])
                        Mod.use_collapse_triangulate = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.vertex_group = real_str(Modparam[4+int(next(ModCount))])
                        Mod.invert_vertex_group = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.vertex_group_factor = float(Modparam[4+int(next(ModCount))])
                        Mod.iterations = int(Modparam[4+int(next(ModCount))])
                        Mod.angle_limit = float(Modparam[4+int(next(ModCount))])
                        Mod.delimit = Dict_str(Modparam[4+int(next(ModCount))])#########################
                        Mod.use_dissolve_boundaries = str_to_bool(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == "CURVE":#real_str str_to_obj str_to_bool float int Mod.invert_vertex_group
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.object = str_to_obj(Modparam[4+int(next(ModCount))])
                        Mod.deform_axis = real_str(Modparam[4+int(next(ModCount))])
                        Mod.vertex_group = real_str(Modparam[4+int(next(ModCount))])
                        Mod.invert_vertex_group = str_to_bool(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == "EDGE_SPLIT":#real_str str_to_obj str_to_bool float int Mod.invert_vertex_group
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.use_edge_angle = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.split_angle = float(Modparam[4+int(next(ModCount))])
                        Mod.use_edge_sharp = str_to_bool(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == "SOLIDIFY":#real_str str_to_obj str_to_bool float int Mod.invert_vertex_group
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.solidify_mode = real_str(Modparam[4+int(next(ModCount))])
                        Mod.nonmanifold_thickness_mode = real_str(Modparam[4+int(next(ModCount))])
                        Mod.nonmanifold_boundary_mode = real_str(Modparam[4+int(next(ModCount))])
                        Mod.thickness = float(Modparam[4+int(next(ModCount))])
                        Mod.offset = float(Modparam[4+int(next(ModCount))])
                        Mod.nonmanifold_merge_threshold = float(Modparam[4+int(next(ModCount))])
                        Mod.use_rim = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_rim_only = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.vertex_group = real_str(Modparam[4+int(next(ModCount))])
                        Mod.invert_vertex_group = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.thickness_vertex_group = float(Modparam[4+int(next(ModCount))])
                        Mod.use_flat_faces = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_flip_normals = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.material_offset = int(Modparam[4+int(next(ModCount))])
                        Mod.material_offset_rim = int(Modparam[4+int(next(ModCount))])
                        Mod.bevel_convex = float(Modparam[4+int(next(ModCount))])
                        Mod.thickness_clamp = float(Modparam[4+int(next(ModCount))])
                        Mod.use_thickness_angle_clamp = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.shell_vertex_group = real_str(Modparam[4+int(next(ModCount))])
                        Mod.rim_vertex_group = real_str(Modparam[4+int(next(ModCount))])
                        Mod.use_even_offset = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_quality_normals = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.edge_crease_inner = float(Modparam[4+int(next(ModCount))])
                        Mod.edge_crease_outer = float(Modparam[4+int(next(ModCount))])
                        Mod.edge_crease_rim = float(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == 'SMOOTH':#real_str str_to_obj str_to_bool float int Mod.invert_vertex_group
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.use_x = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_y = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_z = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.factor = float(Modparam[4+int(next(ModCount))])
                        Mod.iterations = int(Modparam[4+int(next(ModCount))])
                        Mod.vertex_group = real_str(Modparam[4+int(next(ModCount))])
                        Mod.invert_vertex_group = str_to_bool(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == "SUBSURF":#real_str str_to_obj str_to_bool float int Mod.invert_vertex_group
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.subdivision_type = real_str(Modparam[4+int(next(ModCount))])
                        Mod.levels = int(Modparam[4+int(next(ModCount))])
                        Mod.render_levels = int(Modparam[4+int(next(ModCount))])
                        Mod.show_only_control_edges = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.show_only_control_edges = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.quality = int(Modparam[4+int(next(ModCount))])
                        Mod.uv_smooth = real_str(Modparam[4+int(next(ModCount))])
                        Mod.use_creases = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_custom_normals = str_to_bool(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == "TRIANGULATE":#real_str str_to_obj str_to_bool float int Mod.invert_vertex_group
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.quad_method = real_str(Modparam[4+int(next(ModCount))])
                        Mod.ngon_method = real_str(Modparam[4+int(next(ModCount))])
                        Mod.min_vertices = int(Modparam[4+int(next(ModCount))])
                        Mod.keep_custom_normals = str_to_bool(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == "WELD":#real_str str_to_obj str_to_bool float int Mod.invert_vertex_group
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.merge_threshold = float(Modparam[4+int(next(ModCount))])
                        if bpy.app.version >= (2, 92, 0):
                            Mod.mode = Modparam[4+int(next(ModCount))]
                        else:
                            next(ModCount)
                        Mod.vertex_group = real_str(Modparam[4+int(next(ModCount))])
                        Mod.invert_vertex_group = str_to_bool(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == "MIRROR":#real_str str_to_obj str_to_bool float int Mod.invert_vertex_group
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.use_axis[0] = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_axis[1] = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_axis[2] = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_bisect_axis[0] = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_bisect_axis[1] = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_bisect_axis[2] = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_bisect_flip_axis[0] = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_bisect_flip_axis[1] = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_bisect_flip_axis[2] = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.mirror_object = str_to_obj(Modparam[4+int(next(ModCount))])
                        Mod.use_clip = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_mirror_merge = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.merge_threshold = float(Modparam[4+int(next(ModCount))])
                        Mod.use_mirror_u = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_mirror_v = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.mirror_offset_u = float(Modparam[4+int(next(ModCount))])
                        Mod.mirror_offset_v = float(Modparam[4+int(next(ModCount))])
                        Mod.offset_u = float(Modparam[4+int(next(ModCount))])
                        Mod.offset_v = float(Modparam[4+int(next(ModCount))])
                        Mod.use_mirror_vertex_groups = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_mirror_udim = str_to_bool(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == "BUILD":#real_str str_to_obj str_to_bool float int Mod.invert_vertex_group
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.frame_start = float(Modparam[4+int(next(ModCount))])
                        Mod.frame_duration = float(Modparam[4+int(next(ModCount))])
                        Mod.use_reverse = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_random_order = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.seed = int(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == "OCEAN":#real_str str_to_obj str_to_bool float int Mod.invert_vertex_group
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.geometry_mode = real_str(Modparam[4+int(next(ModCount))])
                        Mod.repeat_x = int(Modparam[4+int(next(ModCount))])
                        Mod.repeat_y = int(Modparam[4+int(next(ModCount))])
                        Mod.resolution = int(Modparam[4+int(next(ModCount))])
                        Mod.time = float(Modparam[4+int(next(ModCount))])
                        Mod.depth = float(Modparam[4+int(next(ModCount))])
                        Mod.size = float(Modparam[4+int(next(ModCount))])
                        Mod.spatial_size = int(Modparam[4+int(next(ModCount))])
                        Mod.random_seed = int(Modparam[4+int(next(ModCount))])
                        Mod.use_normals = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.wave_scale = float(Modparam[4+int(next(ModCount))])
                        Mod.wave_scale_min = float(Modparam[4+int(next(ModCount))])
                        Mod.choppiness = float(Modparam[4+int(next(ModCount))])
                        Mod.wind_velocity = float(Modparam[4+int(next(ModCount))])
                        Mod.wave_alignment = float(Modparam[4+int(next(ModCount))])
                        Mod.wave_direction = float(Modparam[4+int(next(ModCount))])
                        Mod.damping = float(Modparam[4+int(next(ModCount))])
                        Mod.use_foam = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.foam_layer_name = real_str(Modparam[4+int(next(ModCount))])
                        Mod.foam_coverage = float(Modparam[4+int(next(ModCount))])
                        Mod.use_spray = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.spray_layer_name = real_str(Modparam[4+int(next(ModCount))])
                        Mod.invert_spray = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.spectrum = real_str(Modparam[4+int(next(ModCount))])
                        Mod.sharpen_peak_jonswap = float(Modparam[4+int(next(ModCount))])
                        Mod.fetch_jonswap = float(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == "HOOK":#real_str str_to_obj str_to_bool float int Mod.invert_vertex_group
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.object = str_to_obj(Modparam[4+int(next(ModCount))])
                        Mod.vertex_group = real_str(Modparam[4+int(next(ModCount))])
                        Mod.invert_vertex_group = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.strength = float(Modparam[4+int(next(ModCount))])
                        Mod.falloff_radius = int(Modparam[4+int(next(ModCount))])
                        Mod.use_falloff_uniform = str_to_bool(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == "CORRECTIVE_SMOOTH":#real_str str_to_obj str_to_bool float int Mod.invert_vertex_group
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.factor = float(Modparam[4+int(next(ModCount))])
                        Mod.iterations = int(Modparam[4+int(next(ModCount))])
                        Mod.scale = float(Modparam[4+int(next(ModCount))])
                        Mod.smooth_type = real_str(Modparam[4+int(next(ModCount))])
                        Mod.vertex_group = real_str(Modparam[4+int(next(ModCount))])
                        Mod.invert_vertex_group = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_only_smooth = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_pin_boundary = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.rest_source = real_str(Modparam[4+int(next(ModCount))])
                    elif (Modparam[1] == 'CLOTH') or (Modparam[1] == 'COLLISION') or (Modparam[1] == 'DYNAMIC_PAINT') or (Modparam[1] == 'FLUID') or (Modparam[1] == 'PARTICLE_SYSTEM') or (Modparam[1] == 'SOFT_BODY'):
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                    elif Modparam[1] == 'EXPLODE':
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.particle_uv = real_str(Modparam[4+int(next(ModCount))])
                        Mod.show_alive = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.show_dead = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.show_unborn = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_edge_cut = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_size = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.invert_vertex_group = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.vertex_group = real_str(Modparam[4+int(next(ModCount))])
                        Mod.protect = float(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == 'PARTICLE_INSTANCE':
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.object = str_to_obj(Modparam[4+int(next(ModCount))])
                        Mod.particle_system_index = int(Modparam[4+int(next(ModCount))])
                        Mod.use_normal = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_children = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_size = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.show_alive = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.show_dead = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.show_unborn = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.particle_amount = float(Modparam[4+int(next(ModCount))])
                        Mod.particle_offset = float(Modparam[4+int(next(ModCount))])
                        Mod.space = Modparam[4+int(next(ModCount))]
                        Mod.axis = Modparam[4+int(next(ModCount))]
                        Mod.use_path = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.position = float(Modparam[4+int(next(ModCount))])
                        Mod.random_position = float(Modparam[4+int(next(ModCount))])
                        Mod.rotation = float(Modparam[4+int(next(ModCount))])
                        Mod.random_rotation = float(Modparam[4+int(next(ModCount))])
                        Mod.use_preserve_shape = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.index_layer_name = Modparam[4+int(next(ModCount))]
                        Mod.value_layer_name = Modparam[4+int(next(ModCount))]
                    elif Modparam[1] == 'MULTIRES':
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.show_only_control_edges = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.subdivision_type = Modparam[4+int(next(ModCount))]
                        Mod.quality = int(Modparam[4+int(next(ModCount))])
                        Mod.uv_smooth = Modparam[4+int(next(ModCount))]
                        Mod.use_creases = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_custom_normals = str_to_bool(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == 'MASK':
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.mode = Modparam[4+int(next(ModCount))]
                        Mod.vertex_group = Modparam[4+int(next(ModCount))]
                        Mod.armature = str_to_obj(Modparam[4+int(next(ModCount))])
                        Mod.invert_vertex_group = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.threshold = float(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == 'ARMATURE':
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.object = str_to_obj(Modparam[4+int(next(ModCount))])
                        Mod.vertex_group = Modparam[4+int(next(ModCount))]
                        Mod.invert_vertex_group = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_deform_preserve_volume = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_multi_modifier = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_vertex_groups = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_bone_envelopes = str_to_bool(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == 'LAPLACIANDEFORM':
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.iterations = int(Modparam[4+int(next(ModCount))])
                        Mod.vertex_group = Modparam[4+int(next(ModCount))]
                        Mod.invert_vertex_group = str_to_bool(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == 'MESH_DEFORM':
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.object = str_to_obj(Modparam[4+int(next(ModCount))])
                        Mod.vertex_group = Modparam[4+int(next(ModCount))]
                        Mod.invert_vertex_group = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.precision = int(Modparam[4+int(next(ModCount))])
                        Mod.use_dynamic_bind = str_to_bool(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == 'SURFACE_DEFORM':
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.target = str_to_obj(Modparam[4+int(next(ModCount))])
                        Mod.falloff = float(Modparam[4+int(next(ModCount))])
                        Mod.strength = float(Modparam[4+int(next(ModCount))])
                        Mod.vertex_group = Modparam[4+int(next(ModCount))]
                        Mod.invert_vertex_group = str_to_bool(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == 'DATA_TRANSFER':
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.object = str_to_obj(Modparam[4+int(next(ModCount))])
                        Mod.use_object_transform = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.mix_mode = Modparam[4+int(next(ModCount))]
                        Mod.mix_factor = float(Modparam[4+int(next(ModCount))])
                        Mod.vertex_group = Modparam[4+int(next(ModCount))]
                        Mod.invert_vertex_group = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.use_vert_data = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.data_types_verts = Dict_str(Modparam[4+int(next(ModCount))])#{'VGROUP_WEIGHTS'}#
                        Mod.vert_mapping = Modparam[4+int(next(ModCount))]
                        Mod.layers_vgroup_select_src = Modparam[4+int(next(ModCount))]
                        Mod.layers_vgroup_select_dst = Modparam[4+int(next(ModCount))]
                        Mod.use_edge_data = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.data_types_edges = Dict_str(Modparam[4+int(next(ModCount))])#{'SEAM'}#
                        Mod.edge_mapping = Modparam[4+int(next(ModCount))]
                        Mod.use_loop_data = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.data_types_loops = Dict_str(Modparam[4+int(next(ModCount))])#{'VCOL'}#
                        Mod.loop_mapping = Modparam[4+int(next(ModCount))]
                        Mod.layers_vcol_select_src = Modparam[4+int(next(ModCount))]
                        Mod.layers_vcol_select_dst = Modparam[4+int(next(ModCount))]
                        Mod.layers_uv_select_src = Modparam[4+int(next(ModCount))]
                        Mod.layers_uv_select_dst = Modparam[4+int(next(ModCount))]
                        Mod.islands_precision = float(Modparam[4+int(next(ModCount))])
                        Mod.use_poly_data = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.data_types_polys = Dict_str(Modparam[4+int(next(ModCount))])#{'SMOOTH'}#
                        Mod.poly_mapping = Modparam[4+int(next(ModCount))]
                        Mod.use_max_distance = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.max_distance = float(Modparam[4+int(next(ModCount))])
                        Mod.ray_radius = float(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == 'MESH_CACHE':
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.cache_format = Modparam[4+int(next(ModCount))]
                        Mod.filepath = Modparam[4+int(next(ModCount))]
                        Mod.factor = float(Modparam[4+int(next(ModCount))])
                        Mod.deform_mode = Modparam[4+int(next(ModCount))]
                        Mod.interpolation = Modparam[4+int(next(ModCount))]
                        Mod.time_mode = Modparam[4+int(next(ModCount))]
                        Mod.play_mode = Modparam[4+int(next(ModCount))]
                        Mod.frame_start = float(Modparam[4+int(next(ModCount))])
                        Mod.frame_scale = float(Modparam[4+int(next(ModCount))])
                        Mod.eval_frame = float(Modparam[4+int(next(ModCount))])
                        Mod.forward_axis = Modparam[4+int(next(ModCount))]
                        Mod.up_axis = Modparam[4+int(next(ModCount))]
                        Mod.flip_axis = Dict_str(Modparam[4+int(next(ModCount))])#{'X', 'Y', 'Z'}##
                    elif Modparam[1] == 'MESH_SEQUENCE_CACHE':
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.read_data = Dict_str(Modparam[4+int(next(ModCount))])#{'VERT', 'POLY', 'UV', 'COLOR'}
                    elif Modparam[1] == 'NORMAL_EDIT':
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.mode = Modparam[4+int(next(ModCount))]
                        Mod.target = str_to_obj(Modparam[4+int(next(ModCount))])
                        Mod.use_direction_parallel = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.mix_mode = Modparam[4+int(next(ModCount))]
                        Mod.mix_factor = float(Modparam[4+int(next(ModCount))])
                        Mod.vertex_group = Modparam[4+int(next(ModCount))]
                        Mod.invert_vertex_group = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.mix_limit = float(Modparam[4+int(next(ModCount))])
                        Mod.offset[0] = float(Modparam[4+int(next(ModCount))])
                        Mod.offset[1] = float(Modparam[4+int(next(ModCount))])
                        Mod.offset[2] = float(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == 'WEIGHTED_NORMAL':
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.mode = Modparam[4+int(next(ModCount))]
                        Mod.weight = float(Modparam[4+int(next(ModCount))])
                        Mod.thresh = float(Modparam[4+int(next(ModCount))])
                        Mod.keep_sharp = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.face_influence = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.vertex_group = Modparam[4+int(next(ModCount))]
                        Mod.invert_vertex_group = str_to_bool(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == 'UV_PROJECT':
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.uv_layer = Modparam[4+int(next(ModCount))]
                        Mod.aspect_x = float(Modparam[4+int(next(ModCount))])
                        Mod.aspect_y = float(Modparam[4+int(next(ModCount))])
                        Mod.scale_x = float(Modparam[4+int(next(ModCount))])
                        Mod.scale_y = float(Modparam[4+int(next(ModCount))])
                        Mod.projector_count = float(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == 'UV_WARP':
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.uv_layer = Modparam[4+int(next(ModCount))]
                        Mod.center[0] = float(Modparam[4+int(next(ModCount))])
                        Mod.center[1] = float(Modparam[4+int(next(ModCount))])
                        Mod.axis_u = Modparam[4+int(next(ModCount))]
                        Mod.axis_v = Modparam[4+int(next(ModCount))]
                        Mod.object_from = str_to_obj(Modparam[4+int(next(ModCount))])
                        Mod.object_to = str_to_obj(Modparam[4+int(next(ModCount))])
                        Mod.vertex_group = Modparam[4+int(next(ModCount))]
                        Mod.invert_vertex_group = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.offset[0] = float(Modparam[4+int(next(ModCount))])
                        Mod.offset[1] = float(Modparam[4+int(next(ModCount))])
                        Mod.scale[0] = float(Modparam[4+int(next(ModCount))])
                        Mod.scale[1] = float(Modparam[4+int(next(ModCount))])
                        Mod.rotation = float(Modparam[4+int(next(ModCount))])
                    elif Modparam[1] == 'VERTEX_WEIGHT_EDIT':
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.vertex_group = Modparam[4+int(next(ModCount))]
                        Mod.default_weight = float(Modparam[4+int(next(ModCount))])
                        Mod.use_add = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.add_threshold = float(Modparam[4+int(next(ModCount))])
                        Mod.use_remove = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.remove_threshold = float(Modparam[4+int(next(ModCount))])
                        Mod.normalize = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.falloff_type = Modparam[4+int(next(ModCount))]
                        Mod.invert_falloff = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.mask_constant = float(Modparam[4+int(next(ModCount))])
                        Mod.mask_vertex_group = Modparam[4+int(next(ModCount))]
                        Mod.invert_mask_vertex_group = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.mask_tex_use_channel = Modparam[4+int(next(ModCount))]
                        Mod.mask_tex_mapping = Modparam[4+int(next(ModCount))]
                        Mod.mask_tex_map_object = str_to_obj(Modparam[4+int(next(ModCount))])
                        Mod.mask_tex_uv_layer = Modparam[4+int(next(ModCount))]
                    elif Modparam[1] == 'VERTEX_WEIGHT_MIX':
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.vertex_group_a = Modparam[4+int(next(ModCount))]
                        Mod.vertex_group_b = Modparam[4+int(next(ModCount))]
                        Mod.default_weight_a = float(Modparam[4+int(next(ModCount))])
                        Mod.default_weight_b = float(Modparam[4+int(next(ModCount))])
                        Mod.mix_set = Modparam[4+int(next(ModCount))]
                        Mod.mix_mode = Modparam[4+int(next(ModCount))]
                        Mod.normalize = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.mask_constant = float(Modparam[4+int(next(ModCount))])
                        Mod.mask_vertex_group = Modparam[4+int(next(ModCount))]
                        Mod.invert_mask_vertex_group = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.mask_tex_use_channel = Modparam[4+int(next(ModCount))]
                        Mod.mask_tex_mapping = Modparam[4+int(next(ModCount))]
                        Mod.mask_tex_map_object = str_to_obj(Modparam[4+int(next(ModCount))])
                        Mod.mask_tex_uv_layer = Modparam[4+int(next(ModCount))]
                    elif Modparam[1] == 'VERTEX_WEIGHT_PROXIMITY':
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.vertex_group = Modparam[4+int(next(ModCount))]
                        Mod.target = str_to_obj(Modparam[4+int(next(ModCount))])
                        Mod.proximity_mode = Modparam[4+int(next(ModCount))]
                        Mod.proximity_geometry = Dict_str(Modparam[4+int(next(ModCount))])#{'VERTEX', 'EDGE', 'FACE'}
                        Mod.min_dist = float(Modparam[4+int(next(ModCount))])
                        Mod.max_dist = float(Modparam[4+int(next(ModCount))])
                        Mod.normalize = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.falloff_type = Modparam[4+int(next(ModCount))]
                        Mod.invert_falloff = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.mask_constant = float(Modparam[4+int(next(ModCount))])
                        Mod.mask_vertex_group = Modparam[4+int(next(ModCount))]
                        Mod.invert_mask_vertex_group = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.mask_tex_use_channel = Modparam[4+int(next(ModCount))]
                        Mod.mask_tex_mapping = Modparam[4+int(next(ModCount))]
                        Mod.mask_tex_map_object = str_to_obj(Modparam[4+int(next(ModCount))])
                        Mod.mask_tex_uv_layer = Modparam[4+int(next(ModCount))]
                    elif (Modparam[1] == 'VOLUME_TO_MESH') and (bpy.app.version >= (2, 92, 0)):
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])
                        Mod.object = str_to_obj(Modparam[4+int(next(ModCount))])
                        Mod.grid_name = Modparam[4+int(next(ModCount))]
                        Mod.resolution_mode = Modparam[4+int(next(ModCount))]
                        Mod.threshold = float(Modparam[4+int(next(ModCount))])
                        Mod.adaptivity = float(Modparam[4+int(next(ModCount))])
                        Mod.use_smooth_shade = str_to_bool(Modparam[4+int(next(ModCount))])
                        Mod.voxel_amount = int(Modparam[4+int(next(ModCount))])
                        Mod.voxel_size = float(Modparam[4+int(next(ModCount))])
                    elif (Modparam[1] == 'NODES') and (bpy.app.version >= (2, 92, 0)):
                        ModCount=count(1, 1)
                        Mod = ob.modifiers.new(Modparam[0],Modparam[1])
                        Mod.show_viewport = str_to_bool(Modparam[2])
                        Mod.show_render = str_to_bool(Modparam[3])

                        Mod.node_group=bpy.data.node_groups[Modparam[4+int(next(ModCount))]]
                        Mod.name+='__'+Mod.node_group.name
                        Mod.node_group.use_fake_user = str_to_bool(Modparam[4+int(next(ModCount))])



                    if ConType == 'CAMERA_SOLVER':
                        ConCount=count(1, 1)
                        Con = ob.constraints.new(ConType)
                        Con.name=Conparam[0]
                        Con.mute = str_to_bool(Conparam[2])

                        Con.use_active_clip=str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.influence=float(Conparam[2+int(next(ConCount))])

                    elif ConType == 'FOLLOW_TRACK':
                        ConCount=count(1, 1)
                        Con = ob.constraints.new(ConType)
                        Con.name=Conparam[0]
                        Con.mute = str_to_bool(Conparam[2])

                        Con.use_active_clip=str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.use_3d_position=str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.use_undistorted_position=str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.frame_method=Conparam[2+int(next(ConCount))]
                        Con.camera=to_Obj(Conparam[2+int(next(ConCount))])
                        Con.depth_object=to_Obj(Conparam[2+int(next(ConCount))])
                        Con.influence=float(Conparam[2+int(next(ConCount))])

                    elif ConType == 'OBJECT_SOLVER':
                        ConCount=count(1, 1)
                        Con = ob.constraints.new(ConType)
                        Con.name=Conparam[0]
                        Con.mute = str_to_bool(Conparam[2])

                        Con.use_active_clip=str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.camera=to_Obj(Conparam[2+int(next(ConCount))])
                        Con.influence=float(Conparam[2+int(next(ConCount))])

                    elif ConType == 'COPY_LOCATION':
                        ConCount=count(1, 1)
                        Con = ob.constraints.new(ConType)
                        Con.name=Conparam[0]
                        Con.mute = str_to_bool(Conparam[2])

                        Con.target = to_Obj(Conparam[2+int(next(ConCount))])
                        Con.subtarget = Conparam[2+int(next(ConCount))]
                        Con.use_x = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.use_y = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.use_z = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.invert_x = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.invert_y = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.invert_z = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.use_offset = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.target_space = Conparam[2+int(next(ConCount))]
                        Con.owner_space = Conparam[2+int(next(ConCount))]
                        Con.space_object = to_Obj(Conparam[2+int(next(ConCount))])
                        Con.space_subtarget = Conparam[2+int(next(ConCount))]
                        Con.influence = float(Conparam[2+int(next(ConCount))])

                    elif ConType == 'COPY_ROTATION':
                        ConCount=count(1, 1)
                        Con = ob.constraints.new(ConType)
                        Con.name=Conparam[0]
                        Con.mute = str_to_bool(Conparam[2])

                        Con.target = to_Obj(Conparam[2+int(next(ConCount))])
                        Con.subtarget = Conparam[2+int(next(ConCount))]
                        Con.euler_order = Conparam[2+int(next(ConCount))]
                        Con.use_x = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.use_y = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.use_z = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.invert_x = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.invert_y = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.invert_z = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.mix_mode = Conparam[2+int(next(ConCount))]
                        Con.target_space = Conparam[2+int(next(ConCount))]
                        Con.owner_space = Conparam[2+int(next(ConCount))]
                        Con.space_object = to_Obj(Conparam[2+int(next(ConCount))])
                        Con.space_subtarget = Conparam[2+int(next(ConCount))]
                        Con.influence = float(Conparam[2+int(next(ConCount))])

                    elif ConType == 'COPY_SCALE':
                        ConCount=count(1, 1)
                        Con = ob.constraints.new(ConType)
                        Con.name=Conparam[0]
                        Con.mute = str_to_bool(Conparam[2])

                        Con.target = to_Obj(Conparam[2+int(next(ConCount))])
                        Con.subtarget = Conparam[2+int(next(ConCount))]
                        Con.use_x = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.use_y = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.use_z = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.power = float(Conparam[2+int(next(ConCount))])
                        Con.use_make_uneleliform = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.use_offset = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.use_add = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.target_space = Conparam[2+int(next(ConCount))]
                        Con.owner_space = Conparam[2+int(next(ConCount))]
                        Con.space_object = to_Obj(Conparam[2+int(next(ConCount))])
                        Con.space_subtarget = Conparam[2+int(next(ConCount))]
                        Con.influence = float(Conparam[2+int(next(ConCount))])

                    elif ConType == 'COPY_TRANSFORMS':
                        ConCount=count(1, 1)
                        Con = ob.constraints.new(ConType)
                        Con.name=Conparam[0]
                        Con.mute = str_to_bool(Conparam[2])

                        Con.target = to_Obj(Conparam[2+int(next(ConCount))])
                        Con.subtarget = Conparam[2+int(next(ConCount))]
                        Con.mix_mode = Conparam[2+int(next(ConCount))]
                        Con.target_space = Conparam[2+int(next(ConCount))]
                        Con.owner_space = Conparam[2+int(next(ConCount))]
                        Con.space_object = to_Obj(Conparam[2+int(next(ConCount))])
                        Con.space_subtarget = Conparam[2+int(next(ConCount))]
                        Con.influence = float(Conparam[2+int(next(ConCount))])

                    elif ConType == 'LIMIT_DISTANCE':
                        ConCount=count(1, 1)
                        Con = ob.constraints.new(ConType)
                        Con.name=Conparam[0]
                        Con.mute = str_to_bool(Conparam[2])

                        Con.target = to_Obj(Conparam[2+int(next(ConCount))])
                        Con.subtarget = Conparam[2+int(next(ConCount))]
                        Con.distance = float(Conparam[2+int(next(ConCount))])
                        Con.limit_mode = Conparam[2+int(next(ConCount))]
                        Con.use_transform_limit = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.target_space = Conparam[2+int(next(ConCount))]
                        Con.owner_space = Conparam[2+int(next(ConCount))]
                        Con.space_object = to_Obj(Conparam[2+int(next(ConCount))])
                        Con.space_subtarget = Conparam[2+int(next(ConCount))]
                        Con.influence = float(Conparam[2+int(next(ConCount))])

                    elif (ConType=='LIMIT_LOCATION') or (ConType=='LIMIT_SCALE'):
                        ConCount=count(1, 1)
                        Con = ob.constraints.new(ConType)
                        Con.name=Conparam[0]
                        Con.mute = str_to_bool(Conparam[2])

                        Con.use_min_x = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.use_min_y = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.use_min_z = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.use_max_x = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.use_max_y = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.use_max_z = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.use_transform_limit = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.min_x = float(Conparam[2+int(next(ConCount))])
                        Con.min_y = float(Conparam[2+int(next(ConCount))])
                        Con.min_z = float(Conparam[2+int(next(ConCount))])
                        Con.max_x = float(Conparam[2+int(next(ConCount))])
                        Con.max_y = float(Conparam[2+int(next(ConCount))])
                        Con.max_z = float(Conparam[2+int(next(ConCount))])
                        Con.owner_space = Conparam[2+int(next(ConCount))]
                        Con.space_object = to_Obj(Conparam[2+int(next(ConCount))])
                        Con.space_subtarget = Conparam[2+int(next(ConCount))]
                        Con.influence = float(Conparam[2+int(next(ConCount))])

                    elif ConType == 'LIMIT_ROTATION':
                        ConCount=count(1, 1)
                        Con = ob.constraints.new(ConType)
                        Con.name=Conparam[0]
                        Con.mute = str_to_bool(Conparam[2])

                        Con.use_limit_x = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.use_limit_y = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.use_limit_z = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.min_x = float(Conparam[2+int(next(ConCount))])
                        Con.max_x = float(Conparam[2+int(next(ConCount))])
                        Con.min_y = float(Conparam[2+int(next(ConCount))])
                        Con.max_y = float(Conparam[2+int(next(ConCount))])
                        Con.min_z = float(Conparam[2+int(next(ConCount))])
                        Con.max_z = float(Conparam[2+int(next(ConCount))])
                        Con.use_transform_limit = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.owner_space = Conparam[2+int(next(ConCount))]
                        Con.space_object = to_Obj(Conparam[2+int(next(ConCount))])
                        Con.space_subtarget = Conparam[2+int(next(ConCount))]
                        Con.influence = float(Conparam[2+int(next(ConCount))])

                    elif ConType == 'MAINTAIN_VOLUME':
                        ConCount=count(1, 1)
                        Con = ob.constraints.new(ConType)
                        Con.name=Conparam[0]
                        Con.mute = str_to_bool(Conparam[2])

                        Con.mode = Conparam[2+int(next(ConCount))]
                        Con.free_axis = Conparam[2+int(next(ConCount))]
                        Con.volume = float(Conparam[2+int(next(ConCount))])
                        Con.owner_space = Conparam[2+int(next(ConCount))]
                        Con.space_object = to_Obj(Conparam[2+int(next(ConCount))])
                        Con.space_subtarget = Conparam[2+int(next(ConCount))]
                        Con.influence = float(Conparam[2+int(next(ConCount))])

                    elif ConType == 'TRANSFORM':
                        ConCount=count(1, 1)
                        Con = ob.constraints.new(ConType)
                        Con.name=Conparam[0]
                        Con.mute = str_to_bool(Conparam[2])

                        Con.target = to_Obj(Conparam[2+int(next(ConCount))])
                        Con.subtarget = Conparam[2+int(next(ConCount))]
                        Con.use_motion_extrapolate = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.target_space = Conparam[2+int(next(ConCount))]
                        Con.owner_space = Conparam[2+int(next(ConCount))]
                        Con.space_object = to_Obj(Conparam[2+int(next(ConCount))])
                        Con.space_subtarget = Conparam[2+int(next(ConCount))]
                        Con.influence = float(Conparam[2+int(next(ConCount))])

                        Con.map_from = Conparam[2+int(next(ConCount))]
                        Con.from_min_x = float(Conparam[2+int(next(ConCount))])
                        Con.from_max_x = float(Conparam[2+int(next(ConCount))])
                        Con.from_min_y = float(Conparam[2+int(next(ConCount))])
                        Con.from_max_y = float(Conparam[2+int(next(ConCount))])
                        Con.from_min_z = float(Conparam[2+int(next(ConCount))])
                        Con.from_max_z = float(Conparam[2+int(next(ConCount))])
                        Con.from_rotation_mode = Conparam[2+int(next(ConCount))]
                        Con.from_min_x_rot = float(Conparam[2+int(next(ConCount))])
                        Con.from_max_x_rot = float(Conparam[2+int(next(ConCount))])
                        Con.from_min_y_rot = float(Conparam[2+int(next(ConCount))])
                        Con.from_max_y_rot = float(Conparam[2+int(next(ConCount))])
                        Con.from_min_z_rot = float(Conparam[2+int(next(ConCount))])
                        Con.from_max_z_rot = float(Conparam[2+int(next(ConCount))])
                        Con.from_min_x_scale = float(Conparam[2+int(next(ConCount))])
                        Con.from_max_x_scale = float(Conparam[2+int(next(ConCount))])
                        Con.from_min_y_scale = float(Conparam[2+int(next(ConCount))])
                        Con.from_max_y_scale = float(Conparam[2+int(next(ConCount))])
                        Con.from_min_z_scale = float(Conparam[2+int(next(ConCount))])
                        Con.from_max_z_scale = float(Conparam[2+int(next(ConCount))])

                        Con.map_to = Conparam[2+int(next(ConCount))]
                        Con.map_to_x_from = Conparam[2+int(next(ConCount))]
                        Con.map_to_y_from = Conparam[2+int(next(ConCount))]
                        Con.map_to_z_from = Conparam[2+int(next(ConCount))]
                        Con.to_min_x = float(Conparam[2+int(next(ConCount))])
                        Con.to_max_x = float(Conparam[2+int(next(ConCount))])
                        Con.to_min_y = float(Conparam[2+int(next(ConCount))])
                        Con.to_max_y = float(Conparam[2+int(next(ConCount))])
                        Con.to_min_z = float(Conparam[2+int(next(ConCount))])
                        Con.to_max_z = float(Conparam[2+int(next(ConCount))])
                        Con.mix_mode = float(Conparam[2+int(next(ConCount))])
                        Con.to_euler_order = Conparam[2+int(next(ConCount))]
                        Con.map_to_x_from = Conparam[2+int(next(ConCount))]
                        Con.map_to_y_from = Conparam[2+int(next(ConCount))]
                        Con.map_to_z_from = Conparam[2+int(next(ConCount))]
                        Con.to_min_x_rot = float(Conparam[2+int(next(ConCount))])
                        Con.to_max_x_rot = float(Conparam[2+int(next(ConCount))])
                        Con.to_min_y_rot = float(Conparam[2+int(next(ConCount))])
                        Con.to_max_y_rot = float(Conparam[2+int(next(ConCount))])
                        Con.to_min_z_rot = float(Conparam[2+int(next(ConCount))])
                        Con.to_max_z_rot = float(Conparam[2+int(next(ConCount))])
                        Con.mix_mode_rot = Conparam[2+int(next(ConCount))]
                        Con.map_to_x_from = Conparam[2+int(next(ConCount))]
                        Con.map_to_y_from = Conparam[2+int(next(ConCount))]
                        Con.map_to_z_from = Conparam[2+int(next(ConCount))]
                        Con.to_min_x_scale = float(Conparam[2+int(next(ConCount))])
                        Con.to_max_x_scale = float(Conparam[2+int(next(ConCount))])
                        Con.to_min_y_scale = float(Conparam[2+int(next(ConCount))])
                        Con.to_max_y_scale = float(Conparam[2+int(next(ConCount))])
                        Con.to_min_z_scale = float(Conparam[2+int(next(ConCount))])
                        Con.to_max_z_scale = float(Conparam[2+int(next(ConCount))])
                        Con.mix_mode_scale = Conparam[2+int(next(ConCount))]

                    elif ConType == 'TRANSFORM_CACHE':
                        ConCount=count(1, 1)
                        Con = ob.constraints.new(ConType)
                        Con.name=Conparam[0]
                        Con.mute = str_to_bool(Conparam[2])

                        Con.influence = float(Conparam[2+int(next(ConCount))])

                    elif ConType == 'CLAMP_TO':
                        ConCount=count(1, 1)
                        Con = ob.constraints.new(ConType)
                        Con.name=Conparam[0]
                        Con.mute = str_to_bool(Conparam[2])

                        Con.target = to_Obj(Conparam[2+int(next(ConCount))])
                        Con.main_axis = Conparam[2+int(next(ConCount))]
                        Con.use_cyclic = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.influence = float(Conparam[2+int(next(ConCount))])

                    elif ConType == 'DAMPED_TRACK':
                        ConCount=count(1, 1)
                        Con = ob.constraints.new(ConType)
                        Con.name=Conparam[0]
                        Con.mute = str_to_bool(Conparam[2])

                        Con.target = to_Obj(Conparam[2+int(next(ConCount))])
                        Con.subtarget = Conparam[2+int(next(ConCount))]
                        Con.track_axis = Conparam[2+int(next(ConCount))]
                        Con.influence = float(Conparam[2+int(next(ConCount))])

                    elif ConType == 'LOCKED_TRACK':
                        ConCount=count(1, 1)
                        Con = ob.constraints.new(ConType)
                        Con.name=Conparam[0]
                        Con.mute = str_to_bool(Conparam[2])

                        Con.target = to_Obj(Conparam[2+int(next(ConCount))])
                        Con.subtarget = Conparam[2+int(next(ConCount))]
                        Con.track_axis = Conparam[2+int(next(ConCount))]
                        Con.lock_axis = Conparam[2+int(next(ConCount))]
                        Con.influence = float(Conparam[2+int(next(ConCount))])

                    elif ConType == 'STRETCH_TO':
                        ConCount=count(1, 1)
                        Con = ob.constraints.new(ConType)
                        Con.name=Conparam[0]
                        Con.mute = str_to_bool(Conparam[2])

                        Con.target = to_Obj(Conparam[2+int(next(ConCount))])
                        Con.subtarget = Conparam[2+int(next(ConCount))]
                        Con.rest_length = float(Conparam[2+int(next(ConCount))])
                        Con.bulge = float(Conparam[2+int(next(ConCount))])
                        Con.use_bulge_min = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.use_bulge_max = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.bulge_min = float(Conparam[2+int(next(ConCount))])
                        Con.bulge_max = float(Conparam[2+int(next(ConCount))])
                        Con.bulge_smooth = float(Conparam[2+int(next(ConCount))])
                        Con.volume = Conparam[2+int(next(ConCount))]
                        Con.keep_axis = Conparam[2+int(next(ConCount))]
                        Con.influence = float(Conparam[2+int(next(ConCount))])

                    elif ConType == 'TRACK_TO':
                        ConCount=count(1, 1)
                        Con = ob.constraints.new(ConType)
                        Con.name=Conparam[0]
                        Con.mute = str_to_bool(Conparam[2])

                        Con.target = to_Obj(Conparam[2+int(next(ConCount))])
                        Con.subtarget = Conparam[2+int(next(ConCount))]
                        Con.track_axis = Conparam[2+int(next(ConCount))]
                        Con.up_axis = Conparam[2+int(next(ConCount))]
                        Con.use_target_z = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.target_space = Conparam[2+int(next(ConCount))]
                        Con.owner_space = Conparam[2+int(next(ConCount))]
                        Con.space_object = to_Obj(Conparam[2+int(next(ConCount))])
                        Con.space_subtarget = Conparam[2+int(next(ConCount))]
                        Con.influence = float(Conparam[2+int(next(ConCount))])

                    elif ConType == 'ACTION':
                        ConCount=count(1, 1)
                        Con = ob.constraints.new(ConType)
                        Con.name=Conparam[0]
                        Con.mute = str_to_bool(Conparam[2])

                        Con.target = to_Obj(Conparam[2+int(next(ConCount))])
                        Con.subtarget = Conparam[2+int(next(ConCount))]
                        Con.use_eval_time = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.eval_time = float(Conparam[2+int(next(ConCount))])
                        Con.mix_mode = Conparam[2+int(next(ConCount))]
                        Con.influence = float(Conparam[2+int(next(ConCount))])
                        Con.transform_channel = Conparam[2+int(next(ConCount))]
                        Con.target_space = Conparam[2+int(next(ConCount))]
                        Con.space_object = to_Obj(Conparam[2+int(next(ConCount))])
                        Con.space_subtarget = Conparam[2+int(next(ConCount))]
                        Con.min = float(Conparam[2+int(next(ConCount))])
                        Con.max = float(Conparam[2+int(next(ConCount))])
                        Con.use_bone_object_action = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.frame_start = int(Conparam[2+int(next(ConCount))])
                        Con.frame_end = int(Conparam[2+int(next(ConCount))])

                    elif ConType == 'ARMATURE':
                        ConCount=count(1, 1)
                        Con = ob.constraints.new(ConType)
                        Con.name=Conparam[0]
                        Con.mute = str_to_bool(Conparam[2])

                        Con.use_deform_preserve_volume = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.use_bone_envelopes = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.influence = float(Conparam[2+int(next(ConCount))])

                    elif ConType == 'CHILD_OF':
                        ConCount=count(1, 1)
                        Con = ob.constraints.new(ConType)
                        Con.name=Conparam[0]
                        Con.mute = str_to_bool(Conparam[2])

                        Con.target = to_Obj(Conparam[2+int(next(ConCount))])
                        Con.subtarget = Conparam[2+int(next(ConCount))]
                        Con.use_location_x = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.use_location_y = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.use_location_z = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.use_rotation_x = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.use_rotation_y = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.use_rotation_z = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.use_scale_x = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.use_scale_y = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.use_scale_z = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.influence = float(Conparam[2+int(next(ConCount))])

                    elif ConType == 'FLOOR':
                        ConCount=count(1, 1)
                        Con = ob.constraints.new(ConType)
                        Con.name=Conparam[0]
                        Con.mute = str_to_bool(Conparam[2])

                        Con.target = to_Obj(Conparam[2+int(next(ConCount))])
                        Con.subtarget = Conparam[2+int(next(ConCount))]
                        Con.offset = float(Conparam[2+int(next(ConCount))])
                        Con.floor_location = Conparam[2+int(next(ConCount))]
                        Con.use_rotation = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.target_space = Conparam[2+int(next(ConCount))]
                        Con.owner_space = Conparam[2+int(next(ConCount))]
                        Con.space_object = to_Obj(Conparam[2+int(next(ConCount))])
                        Con.space_subtarget = Conparam[2+int(next(ConCount))]
                        Con.influence = float(Conparam[2+int(next(ConCount))])

                    elif ConType == 'FOLLOW_PATH':
                        ConCount=count(1, 1)
                        Con = ob.constraints.new(ConType)
                        Con.name=Conparam[0]
                        Con.mute = str_to_bool(Conparam[2])

                        Con.target = to_Obj(Conparam[2+int(next(ConCount))])
                        Con.offset = float(Conparam[2+int(next(ConCount))])
                        Con.forward_axis = Conparam[2+int(next(ConCount))]
                        Con.up_axis = Conparam[2+int(next(ConCount))]
                        Con.use_fixed_location = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.use_curve_radius = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.use_curve_follow = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.influence = float(Conparam[2+int(next(ConCount))])

                    elif ConType == 'PIVOT':
                        ConCount=count(1, 1)
                        Con = ob.constraints.new(ConType)
                        Con.name=Conparam[0]
                        Con.mute = str_to_bool(Conparam[2])

                        Con.target = to_Obj(Conparam[2+int(next(ConCount))])
                        Con.subtarget = Conparam[2+int(next(ConCount))]
                        Con.offset[0] = float(Conparam[2+int(next(ConCount))])
                        Con.offset[1] = float(Conparam[2+int(next(ConCount))])
                        Con.offset[2] = float(Conparam[2+int(next(ConCount))])
                        Con.rotation_range = Conparam[2+int(next(ConCount))]
                        Con.influence = float(Conparam[2+int(next(ConCount))])

                    elif ConType == 'SHRINKWRAP':
                        ConCount=count(1, 1)
                        Con = ob.constraints.new(ConType)
                        Con.name=Conparam[0]
                        Con.mute = str_to_bool(Conparam[2])

                        Con.target = to_Obj(Conparam[2+int(next(ConCount))])
                        Con.distance = float(Conparam[2+int(next(ConCount))])
                        Con.shrinkwrap_type = Conparam[2+int(next(ConCount))]
                        Con.project_axis_space = Conparam[2+int(next(ConCount))]
                        Con.project_limit = float(Conparam[2+int(next(ConCount))])
                        Con.use_project_opposite = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.cull_face = Conparam[2+int(next(ConCount))]
                        Con.use_invert_cull = str_to_bool(Conparam[2+int(next(ConCount))])#
                        Con.wrap_mode = Conparam[2+int(next(ConCount))]
                        Con.use_track_normal = str_to_bool(Conparam[2+int(next(ConCount))])
                        Con.track_axis = Conparam[2+int(next(ConCount))]
                        Con.influence = float(Conparam[2+int(next(ConCount))])

                for mod in ob.modifiers:
                    mod.show_expanded = False
                    mod.show_in_editmode = False



        '''
        if len(DriversList)>0:#测试打印
            print(DriversList)
            print(DriversList[0])
            print(DriversList[0][1])
        '''
        if len(DriversList)>0:
            for DriverLine in DriversList:
                DriverCount=count(1, 1)
                WeAddDiver=False
                SourceType=DriverLine[1]
                Source=DriverLine[2]
                SourceDataPath=DriverLine[3]
                SourceIndex=DriverLine[4]
                expType=DriverLine[5]
                exp=DriverLine[6]
                TargetNum=DriverLine[7]
                


                if SourceType=='OBJECT':
                    if Source in bpy.data.objects:
                        source=bpy.data.objects[Source]
                        WeAddDiver=True
                elif SourceType=='TEXTURE':
                    if Source in bpy.data.textures:
                        source=bpy.data.textures[Source]
                        WeAddDiver=True
                elif (SourceType=='NODETREE') and (bpy.app.version >= (2, 92, 0)):
                    if Source in bpy.data.node_groups:
                        source=bpy.data.node_groups[Source]
                        WeAddDiver=True

                if WeAddDiver==True:
                    if (int(SourceIndex) != 0) or ('.vector' in SourceDataPath):
                        d = source.driver_add( SourceDataPath, int(SourceIndex) ).driver
                    else:
                        d = source.driver_add( SourceDataPath ).driver
                    

                    d.type=expType
                    if d.type=='SCRIPTED':
                        d.expression = exp

                varnum=int(TargetNum)
                for var in range(varnum):
                    FuncType=DriverLine[7+int(next(DriverCount))]
                    FuncName=DriverLine[7+int(next(DriverCount))]
                    TargetType=DriverLine[7+int(next(DriverCount))]
                    targetName=DriverLine[7+int(next(DriverCount))]
                    TargetDataPath=DriverLine[7+int(next(DriverCount))]
                    transform_type=DriverLine[7+int(next(DriverCount))]
                    transform_space=DriverLine[7+int(next(DriverCount))]
                    #nextCount=7+int(next(DriverCount))
                    rotation_mode=DriverLine[7+int(next(DriverCount))]

                    if (TargetType=='OBJECT') and (targetName!=''):
                        if targetName in bpy.data.objects:
                            target=bpy.data.objects[targetName]
                            #TargetDiver=True
                    elif (TargetType=='TEXTURE') and (targetName!=''):
                        if targetName in bpy.data.textures:
                            target=bpy.data.textures[targetName]
                            #TargetDiver=True
                    elif (TargetType=='NODETREE') and (targetName!='') and (bpy.app.version >= (2, 92, 0)):
                        if targetName in bpy.data.node_groups:
                            target=bpy.data.node_groups[targetName]
                            #TargetDiver=True
                    else:
                        target=None
                        #WeAddDiver=False

                    v = d.variables.new()
                    v.name = FuncName
                    v.type = FuncType
                    if v.type== 'SINGLE_PROP':#SINGLE_PROP才会出现选择物体类型
                        v.targets[0].id_type   = TargetType
                        v.targets[0].id        = target
                        v.targets[0].data_path = TargetDataPath
                        v.targets[0].transform_type=transform_type
                        v.targets[0].transform_space=transform_space
                        v.targets[0].rotation_mode=rotation_mode

                    elif v.type=='TRANSFORMS':
                        v.targets[0].id        = target
                        v.targets[0].data_path = TargetDataPath
                        v.targets[0].transform_type=transform_type
                        v.targets[0].transform_space=transform_space
                        v.targets[0].rotation_mode=rotation_mode
                    
                    elif v.type=='ROTATION_DIFF':
                        Func2Type=DriverLine[7+int(next(DriverCount))]
                        Func2Name=DriverLine[7+int(next(DriverCount))]
                        Target2Type=DriverLine[7+int(next(DriverCount))]
                        target2Name=DriverLine[7+int(next(DriverCount))]
                        Target2DataPath=DriverLine[7+int(next(DriverCount))]
                        transform2_type=DriverLine[7+int(next(DriverCount))]
                        transform2_space=DriverLine[7+int(next(DriverCount))]
                        rotation2_mode=DriverLine[7+int(next(DriverCount))]

                        v.targets[0].id        = target

                        #target2Name=DriverLine[nextCount+4]
                        if target2Name in bpy.data.objects:
                            v.targets[1].id        = bpy.data.objects[target2Name]

                    elif v.type=='LOC_DIFF':
                        Func2Type=DriverLine[7+int(next(DriverCount))]
                        Func2Name=DriverLine[7+int(next(DriverCount))]
                        Target2Type=DriverLine[7+int(next(DriverCount))]
                        target2Name=DriverLine[7+int(next(DriverCount))]
                        Target2DataPath=DriverLine[7+int(next(DriverCount))]
                        transform2_type=DriverLine[7+int(next(DriverCount))]
                        transform2_space=DriverLine[7+int(next(DriverCount))]
                        rotation2_mode=DriverLine[7+int(next(DriverCount))]

                        v.targets[0].id        = target
                        v.targets[0].transform_space = transform_space

                        #target2Name=DriverLine[nextCount+4]
                        if target2Name in bpy.data.objects:
                            v.targets[1].id = bpy.data.objects[target2Name]
                        v.targets[1].transform_space = transform2_space






        if len(OBJNameList) != 0:
            for OBJName in OBJNameList:
        
                ob= bpy.data.objects[OBJName]
                name=amProperty.GenMechEnum.split('_')[0]
                ob.name=name+OBJName
                
                if (amProperty.RandomMaterialBool == True) and (ob.type=='MESH'):
                    for i in range(0,len(ob.material_slots)):
                        ob.active_material_index = i
                        MatOld = ob.active_material
                        MatNew = MatOld.copy()
                        MatNew.name=MatNew.name[:-4]+"_"+ob.name
                        ob.data.materials[i] = MatNew
                        if i == 0:#从这里设置材质参数
                            bpy.data.materials[MatNew.name].node_tree.nodes["PreMColor"].inputs[1].default_value = (random.uniform(0, 0.9), random.uniform(0, 0.7), random.uniform(0, 1), 1)
                            bpy.data.materials[MatNew.name].node_tree.nodes["PreMColor"].inputs[2].default_value = (random.uniform(0, 1), random.uniform(0, 0.9), random.uniform(0, 0.8), 1)

                        if i == 1:
                            bpy.data.materials[MatNew.name].node_tree.nodes["PreMColor"].inputs[1].default_value = (random.uniform(0, 0.3), random.uniform(0, 0.3), random.uniform(0, 0.3), 1)
                            bpy.data.materials[MatNew.name].node_tree.nodes["PreMColor"].inputs[2].default_value = (random.uniform(0.2, 0.8), random.uniform(0.2, 0.8), random.uniform(0.2, 0.8), 1) 
                        if i == 2:
                            bpy.data.materials[MatNew.name].node_tree.nodes["PreMColor"].inputs[0].default_value = (random.uniform(0, 0.05), random.uniform(0, 0.05), random.uniform(0, 0.05), 1) 
                        if i == 3:
                            bpy.data.materials[MatNew.name].node_tree.nodes["PreMColor"].inputs[1].default_value = (random.uniform(0, 0.5), random.uniform(0, 0.5), random.uniform(0, 0.5), 1)
                            bpy.data.materials[MatNew.name].node_tree.nodes["PreMColor"].inputs[2].default_value = (random.uniform(0.4, 1), random.uniform(0.4, 1), random.uniform(0.4, 1), 1)

                        if i == 4:
                            bpy.data.materials[MatNew.name].node_tree.nodes["PreMColor"].inputs[0].default_value = (random.uniform(0, 0.4), random.uniform(0, 0.4), random.uniform(0, 0.4), 1)
                            bpy.data.materials[MatNew.name].node_tree.nodes["PreMColor"].inputs[17].default_value = (random.uniform(0, 0.8), random.uniform(0, 0.8), random.uniform(0, 0.8), 1)
                





        
        amProperty.GenMechSkinResize =  (1,1,1)

        genLine_result = make_collection('2GenMech', bpy.context.collection)#bpy.data.collections["2GenMech"]#在这个合集中找到所有物体，修改这里的合集0AutoMech
        
        
        if (len(genLine_result.objects) > 12) and ((amProperty.GenMechEnum =='MechfyHigh') or (amProperty.GenMechEnum =='Mechfy')):#如果在当前Collection中有物体
            for childObject in genLine_result.objects:
        #for ob in sel:
                bpy.ops.object.mode_set(mode='OBJECT')#
                bpy.ops.object.select_all(action='DESELECT')
                childObject.select_set(True)
                bpy.context.view_layer.objects.active = childObject

                if 'neck_01' in childObject.name or 'hand_l' in childObject.name:
                    if bpy.context.mode =='OBJECT':
                        bpy.ops.object.mode_set(mode='EDIT')
                        #bpy.ops.mesh.select_all(action='SELECT')    
                        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT', action='TOGGLE')
                        bpy.ops.mesh.select_all(action='SELECT')
                        bpy.ops.transform.skin_resize(value=(0.6,0.6,0.6), mirror=True, use_proportional_edit=False, proportional_edit_falloff='RANDOM', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                        bpy.ops.transform.skin_resize(value=amProperty.GenMechSkinResize, mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                        #bpy.ops.transform.skin_resize(value=amProperty.GenMechSkinResize)
                        #bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE', action='TOGGLE')
                        bpy.ops.object.mode_set(mode='OBJECT')
                
                elif '_l' in childObject.name or 'head' in childObject.name or 'spine_01' in childObject.name:
                    if bpy.context.mode =='OBJECT':
                        bpy.ops.object.mode_set(mode='EDIT')
                        #bpy.ops.mesh.select_all(action='SELECT')
                        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT', action='TOGGLE')
                        bpy.ops.mesh.select_all(action='SELECT')
                        bpy.ops.transform.skin_resize(value=(0.8,0.8,0.8), mirror=True, use_proportional_edit=False, proportional_edit_falloff='RANDOM', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                        bpy.ops.transform.skin_resize(value=amProperty.GenMechSkinResize, mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                        #bpy.ops.transform.skin_resize(value=amProperty.GenMechSkinResize, mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                        #bpy.ops.transform.skin_resize(value=amProperty.GenMechSkinResize)
                        #bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE', action='TOGGLE')
                        bpy.ops.object.mode_set(mode='OBJECT')
                



        #bpy.context.view_layer.objects.active = ob#bpy.context.scene.objects.active = ob
        #ob.select_set(True)
        self.report({'INFO'}, "修改器生成成功。")
        return {'FINISHED'}

#'DATA_TRANSFER', 'MESH_CACHE', 'MESH_SEQUENCE_CACHE', 'NORMAL_EDIT', 'WEIGHTED_NORMAL', 'UV_PROJECT', 'UV_WARP', 'VERTEX_WEIGHT_EDIT', 
# 'VERTEX_WEIGHT_MIX', 'VERTEX_WEIGHT_PROXIMITY', 'ARRAY', 'BEVEL', 'BOOLEAN', 'BUILD', 'DECIMATE', 'EDGE_SPLIT', 'MASK', 'MIRROR', 18
# 'MULTIRES', 'REMESH', 'SCREW', 'SKIN', 'SOLIDIFY', 'SUBSURF', 'TRIANGULATE', 'WELD', 'WIREFRAME', 'ARMATURE', 'CAST', 'CURVE', 30
# 'DISPLACE', 'HOOK', 'LAPLACIANDEFORM', 'LATTICE', 'MESH_DEFORM', 'SHRINKWRAP', 'SIMPLE_DEFORM', 'SMOOTH', 'CORRECTIVE_SMOOTH', 39
# 'LAPLACIANSMOOTH', 'SURFACE_DEFORM', 'WARP', 'WAVE', 'CLOTH', 'COLLISION', 'DYNAMIC_PAINT', 'EXPLODE', 'FLUID', 'OCEAN', 49
# 'PARTICLE_INSTANCE', 'PARTICLE_SYSTEM', 'SOFT_BODY', 'SURFACE', 'SIMULATION',54-1 SIMULATION