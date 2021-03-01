import bpy
from .RIG_Tool import *

#执行顺序1
#需要解决的问题：
#2。。lips.L编辑位置可能需要改变对其位置

#3 的lip.B.L/R.002 的父级为jaw 并指定lip.T.L/R.002约束 nose.005的父级指向face
#3 lip.T/B.L/R.002等需要复制lips.L的约束位置

#V29  DEF-li p.T.L.002 DEF-lip. B.L.002 DEF-chin.L 需要指定DEF-cheek.B.L约束

#V 30层的MCH-CTRL-cheek01.L/R.006 MCH-CTRL-cheek02.L/R.006 设置父级为ORG-face

#！！！需要DEF-lip.B.L R .002设置父级为lip.B.L R.002 需要调整嘴唇的拉伸
#删减后需要重新添加 两个嘴角的点

'''
def ReSetConstraints(AddSubtarget):
    StretchToConstraints = [ c for c in bone.constraints if c.type == 'STRETCH_TO' ]
    DampedTrackConstraints = [ b for b in bone.constraints if b.type == 'DAMPED_TRACK' ]

    for c in StretchToConstraints:
        bone.constraints.remove( c ) 

    for b in DampedTrackConstraints:
        b.subtarget = AddSubtarget
    bc = bone.constraints.new('STRETCH_TO')
    #bc.type == 'STRETCH_TO'
    bc.name=bone.name
    bc.target = bpy.context.object
    bc.subtarget = AddSubtarget

def LocConstraints(Bone,Subtarget,Influence,Space = 'LOCAL',Owner_Space='LOCAL',UseOffset = False,x=True,y=True,z=True,ix=False,iy=False,iz=False):
    bc = bone.constraints.new('COPY_LOCATION')
    #bc.type == 'STRETCH_TO'
    #bc.name=bone.name
    bc.target = bpy.context.object
    bc.subtarget = Subtarget#lip.T.L.002
    bc.influence = Influence
    bc.target_space = Space
    bc.owner_space = Owner_Space
    bc.use_offset = UseOffset
    bc.use_x = x
    bc.use_y = y
    bc.use_z = z
    bc.invert_x = ix
    bc.invert_y = iy
    bc.invert_z = iz

#bpy.ops.pose.constraint_add(type='COPY_ROTATION')
#bpy.ops.pose.constraint_add(type='COPY_SCALE')
def RotConstraints(Bone,Subtarget,Influence = 1,Space = 'LOCAL'):
    bc = bone.constraints.new('COPY_ROTATION')
    #bc.type == 'STRETCH_TO'
    #bc.name=bone.name
    bc.target = bpy.context.object
    bc.subtarget = Subtarget#lip.T.L.002
    bc.influence = Influence
    bc.target_space = Space
    bc.owner_space = Space

def ScaleConstraints(Bone,Subtarget,Influence = 1,Space = 'LOCAL',UseOffset = False):
    bc = bone.constraints.new('COPY_SCALE')
    #bc.type == 'STRETCH_TO'
    #bc.name=bone.name
    bc.target = bpy.context.object
    bc.subtarget = Subtarget#lip.T.L.002
    bc.influence = Influence
    bc.target_space = Space
    bc.owner_space = Space
    bc.use_offset = UseOffset

def TransformsConstraints(Bone,Subtarget,Influence,Space = 'LOCAL'):
    bc = bone.constraints.new('COPY_TRANSFORMS')
    #bc.type == 'STRETCH_TO'
    #bc.name=bone.name
    bc.target = bpy.context.object
    bc.subtarget = Subtarget#lip.T.L.002
    bc.influence = Influence
    bc.target_space = Space
    bc.owner_space = Space

def LimitDistance(Bone,Subtarget,Influence,Distance = 0,Space = 'WORLD'):
    bc = bone.constraints.new('LIMIT_DISTANCE')
    bc.target = bpy.context.object
    bc.subtarget = Subtarget#lip.T.L.002
    bc.influence = Influence
    bc.target_space = Space
    bc.owner_space = Space
    bc.distance = Distance#3.416

def RemoveConstraints(Bone):

    copyTransformsConstraints = [ a for a in bone.constraints if a.type == 'COPY_TRANSFORMS' ]
    DampedTrackConstraints = [ b for b in bone.constraints if b.type == 'DAMPED_TRACK' ]
    StretchToConstraints = [ c for c in bone.constraints if c.type == 'STRETCH_TO' ]
    LocationConstraints = [ d for d in bone.constraints if d.type == 'COPY_LOCATION' ]
    LimitDistanceConstraints = [ e for e in bone.constraints if e.type == 'LIMIT_DISTANCE' ]
    RotationConstraints = [ f for f in bone.constraints if f.type == 'COPY_ROTATION' ]
    ScaleConstraints = [ g for g in bone.constraints if g.type == 'COPY_SCALE' ]

    # Iterate over all the bone's copy location constraints and delete them all

    for a in copyTransformsConstraints:
        bone.constraints.remove( a ) # Remove constraint
    for b in DampedTrackConstraints:
        bone.constraints.remove( b ) # Remove constraint
    for c in StretchToConstraints:
        bone.constraints.remove( c ) 
    for d in LocationConstraints:
        bone.constraints.remove( d ) 
    for e in LimitDistanceConstraints:
        bone.constraints.remove( e ) 
    for f in RotationConstraints:
        bone.constraints.remove( f ) 
    for g in ScaleConstraints:
        bone.constraints.remove( g ) 
'''

class RigReFace(bpy.types.Operator):
    bl_idname = "am.rigreface"
    bl_label = "Rig ReFace"
    bl_description = "将materig生成的Rig再次重命名等相关操作。" 
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.object.type =='ARMATURE':

            if 'metarig' in bpy.context.object.name:
                bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
                bpy.ops.pose.rigify_generate()

            bpy.ops.object.mode_set(mode='OBJECT')
            #
            bpy.ops.object.mode_set(mode='POSE')
            MakeSureSelectOneLayer(29)
            bpy.ops.pose.select_all(action='SELECT')

            for bone in bpy.context.selected_pose_bones:


                if "DEF-nose." in bone.name:
                    if "DEF-nose.L" in bone.name:
                        if "L.001" in bone.name:
                            ReSetConstraints("nose.003",bone)
                        elif "L.002" in bone.name:
                            ReSetConstraints("DEF-nose.L.001",bone)
                        else:
                            ReSetConstraints("DEF-nose.L.002",bone)
                    if "DEF-nose.R" in bone.name:
                        if "R.001" in bone.name:
                            ReSetConstraints("nose.003",bone)
                        elif "R.002" in bone.name:
                            ReSetConstraints("DEF-nose.R.001",bone)
                        else:
                            ReSetConstraints("DEF-nose.R.002",bone)

                if "DEF-cheek.T." in bone.name:
                    if "L.002" in bone.name:
                        ReSetConstraints("nose.L",bone)
                    if "R.002" in bone.name:
                        ReSetConstraints("nose.R",bone)

                    if "L.001" in bone.name:
                        ReSetConstraints("DEF-cheek.T.L.002",bone)
                    if "R.001" in bone.name:
                        ReSetConstraints("DEF-cheek.T.R.002",bone)

                if "DEF-cheek.B." in bone.name:
                    if "L.002" in bone.name:
                        ReSetConstraints("brow.T.L",bone)
                    if "R.002" in bone.name:
                        ReSetConstraints("brow.T.R",bone)

                    if "L.001" in bone.name:
                        ReSetConstraints("cheek.B.L.002",bone)
                    if "R.001" in bone.name:
                        ReSetConstraints("cheek.B.R.002",bone)

                if "DEF-lip." in bone.name:
                    if "T.L.001" in bone.name:#这里需要重新指定生成的 lip.T.L.002
                        ReSetConstraints("lip.T.L.2",bone)#lip.T.L.001
                    if "T.R.001" in bone.name:
                        ReSetConstraints("lip.T.R.2",bone)#lip.T.R.001

                    if "B.L.001" in bone.name:
                        ReSetConstraints("lip.B.L.2",bone)#lip.B.L.001
                    if "B.R.001" in bone.name:
                        ReSetConstraints("lip.B.R.2",bone)#lip.B.R.001
                    '''
                    if "T.L.002" in bone.name:#以下应该指向def的 我又删掉T.L.002 了
                        ReSetConstraints("DEF-cheek.B.L")
                    if "T.R.002" in bone.name:
                        ReSetConstraints("DEF-cheek.B.R")

                    if "B.L.002" in bone.name:
                        ReSetConstraints("DEF-cheek.B.L")
                    if "B.R.002" in bone.name:
                        ReSetConstraints("DEF-cheek.B.R")
                    '''
                if "DEF-chin.L" in bone.name:
                    ReSetConstraints("DEF-cheek.B.L",bone)
                if "DEF-chin.R" in bone.name:
                    ReSetConstraints("DEF-cheek.B.R",bone)

            #切换到编辑模式修改31 root到face
            bpy.ops.object.mode_set(mode='EDIT')
            MakeSureSelectOneLayer(29)
            ob = bpy.context.object
            if ob.type == 'ARMATURE':
                armature = ob.data
            for bone in armature.edit_bones:
                if "DEF-lip.U.003" in bone.name: #fnmatch.fnmatchcase(bone.name, "DEF-lip.U.003"): 
                    armature.edit_bones.remove(bone)
                elif "DEF-lip.U.002" in bone.name:
                    armature.edit_bones.remove(bone)
                elif "DEF-lip.D.003" in bone.name:
                    armature.edit_bones.remove(bone)
                elif "DEF-lip.D.002" in bone.name:
                    armature.edit_bones.remove(bone)
                
                elif "DEF-cheek01.L.003" in bone.name:
                    bone.use_connect = False
                    bone.parent = bpy.context.object.data.edit_bones['ORG-face']
                elif "DEF-cheek01.R.003" in bone.name:
                    bone.use_connect = False
                    bone.parent = bpy.context.object.data.edit_bones['ORG-face']

                elif "DEF-cheek02.L.003" in bone.name:
                    bone.use_connect = False
                    bone.parent = bpy.context.object.data.edit_bones['ORG-face']
                elif "DEF-cheek02.R.003" in bone.name:
                    bone.use_connect = False
                    bone.parent = bpy.context.object.data.edit_bones['ORG-face']

                #elif "DEF-lip.B.L.002" in bone.name:#删
                    #bone.use_connect = False
                    #bone.parent = bpy.context.object.data.edit_bones['lip.B.L.002']
                #elif "DEF-lip.B.R.002" in bone.name:#删
                    #bone.use_connect = False
                    #bone.parent = bpy.context.object.data.edit_bones['lip.B.R.002']


            MakeSureSelectOneLayer(1)
            for bone in armature.edit_bones:
                if "lips.L" in bone.name:#
                    SelectBone("lips.L")
                    if bone.head[0] < 2.8635:
                        bpy.context.object.data.use_mirror_x = True
                        bpy.context.scene.tool_settings.use_snap = True
                        bpy.context.scene.tool_settings.snap_elements = {'VERTEX'}
                        bpy.ops.transform.translate(value=(0.611132, 0.420887, -0.0228424), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=0.0220949, use_proportional_connected=False, use_proportional_projected=False)
                        bpy.context.object.data.use_mirror_x = False
                        bpy.context.scene.tool_settings.use_snap = False

            MakeSureSelectOneLayer(2)
            for bone in armature.edit_bones:
                #bpy.context.object.data.use_mirror_x = True
                if "lip.B.L.2" in bone.name:#
                    armature.edit_bones.remove(bone)
                elif "lip.B.R.2" in bone.name:#
                    armature.edit_bones.remove(bone)
                elif "lip.T.L.2" in bone.name:#
                    armature.edit_bones.remove(bone)
                elif "lip.T.R.2" in bone.name:#
                    armature.edit_bones.remove(bone)

            bpy.context.object.data.use_mirror_x = True
            bpy.context.scene.tool_settings.use_snap = True
            bpy.context.scene.transform_orientation_slots[0].type = 'GLOBAL'
            bpy.context.scene.tool_settings.transform_pivot_point = 'ACTIVE_ELEMENT'
            bpy.context.scene.tool_settings.snap_elements = {'VERTEX'}
            bpy.context.scene.tool_settings.snap_target = 'ACTIVE'

            bpy.ops.armature.select_all(action='DESELECT')
            if "chin.L" in bpy.context.object.data.bones:
                SelectBone("chin.L")
                bpy.ops.armature.duplicate_move(ARMATURE_OT_duplicate={"do_flip_names":False}, TRANSFORM_OT_translate={"value":(-0.192229, -1.92778, 3.23282), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":0.0220949, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
                SelectBone("chin.L")
                bpy.ops.armature.duplicate_move(ARMATURE_OT_duplicate={"do_flip_names":False}, TRANSFORM_OT_translate={"value":(-0.168067, -2.13659, 3.4946), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":0.0220949, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})


            bpy.context.object.data.use_mirror_x = False
            bpy.context.scene.tool_settings.use_snap = False

            for bone in armature.edit_bones:
                if "chin.L.001" in bone.name:
                    bone.name = "lip.B.L.2"
                    bone.parent = bpy.context.object.data.edit_bones['MCH-jaw_master.002']

                elif "chin.R.001" in bone.name:
                    bone.name = "lip.B.R.2"
                    bone.parent = bpy.context.object.data.edit_bones['MCH-jaw_master.002']

                elif "chin.L.002" in bone.name:
                    bone.name = "lip.T.L.2"
                    bone.parent = bpy.context.object.data.edit_bones['MCH-jaw_master.002']

                elif "chin.R.002" in bone.name:
                    bone.name = "lip.T.R.2"
                    bone.parent = bpy.context.object.data.edit_bones['MCH-jaw_master.002']


            MakeSureSelectOneLayer(31)
            bpy.context.object.data.layers[29] = False
            bpy.context.object.data.layers[1] = False
            bpy.context.object.data.layers[2] = False
            bpy.ops.armature.select_all(action='SELECT')

            for bone in bpy.context.selected_bones:#bpy.context.edit_bones:
                if "ORG-lip.U" in bone.name:
                    bone.parent = bpy.context.object.data.edit_bones['ORG-face']
                if "ORG-lip.D" in bone.name:
                    bone.parent = bpy.context.object.data.edit_bones['ORG-face']
                if "ORG-cheek0" in bone.name:
                    bone.parent = bpy.context.object.data.edit_bones['ORG-face']

                if "ORG-cheek.B.L.002" in bone.name:
                    bone.parent = bpy.context.object.data.edit_bones[bone.name[4:]]
                if "ORG-cheek.B.R.002" in bone.name:
                    bone.parent = bpy.context.object.data.edit_bones[bone.name[4:]]

                if "ORG-cheek.T.L.002" in bone.name:
                    bone.parent = bpy.context.object.data.edit_bones[bone.name[4:]]
                if "ORG-cheek.T.R.002" in bone.name:
                    bone.parent = bpy.context.object.data.edit_bones[bone.name[4:]]

                if "ORG-nose.L.002" in bone.name:
                    bone.parent = bpy.context.object.data.edit_bones[bone.name[4:]]
                if "ORG-nose.R.002" in bone.name:
                    bone.parent = bpy.context.object.data.edit_bones[bone.name[4:]]

            bpy.ops.armature.select_all(action='DESELECT')

            MakeSureSelectOneLayer(30)
            bpy.context.object.data.layers[31] = False
            bpy.ops.armature.select_all(action='SELECT')
            #30层的MCH-CTRL-cheek01.L/R.006 MCH-CTRL-cheek02.L/R.006 设置父级为ORG-face
            for bone in armature.edit_bones:
                if "MCH-CTRL-cheek01.L.006" in bone.name:
                    bone.parent = bpy.context.object.data.edit_bones['ORG-face']
                if "MCH-CTRL-cheek02.L.006" in bone.name:
                    bone.parent = bpy.context.object.data.edit_bones['ORG-face']

                if "MCH-CTRL-cheek01.R.006" in bone.name:
                    bone.parent = bpy.context.object.data.edit_bones['ORG-face']
                if "MCH-CTRL-cheek02.R.006" in bone.name:
                    bone.parent = bpy.context.object.data.edit_bones['ORG-face']

            bpy.ops.armature.select_all(action='DESELECT')


            #3 的lip.B.L/R.002 的父级为jaw 
            MakeSureSelectOneLayer(2)
            bpy.context.object.data.layers[30] = False
            for bone in armature.edit_bones:
                #if "lip.B.L.002" in bone.name:
                    #if "DEF-" not in bone.name:
                        #bone.parent = bpy.context.object.data.edit_bones['ORG-face']
                #if "lip.B.R.002" in bone.name:
                    #if "DEF-" not in bone.name:
                        #bone.parent = bpy.context.object.data.edit_bones['ORG-face']
                if "nose.005" in bone.name:
                    bone.parent = bpy.context.object.data.edit_bones['ORG-face']
                if "nose.001" in bone.name:
                    bone.parent = bpy.context.object.data.edit_bones['nose_master']
                if "nose.003" in bone.name:
                    bone.parent = bpy.context.object.data.edit_bones['nose_master']
                if "chin.002" in bone.name:
                    bone.parent = bpy.context.object.data.edit_bones['chin.001']#

            #bpy.ops.armature.select_all(action='DESELECT')



            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.mode_set(mode='POSE')
            bpy.ops.pose.select_all(action='SELECT')
            for bone in bpy.context.selected_pose_bones:
            #3 lip.T/B.L/R.002等需要复制lips.L的约束位置 以下为层级3
                if "lip.T.L.2" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"lips.L",0.7)
                    LimitDistance(bone,"chin",0.3,5)
                elif "lip.T.R.2" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"lips.R",0.7)
                    LimitDistance(bone,"chin",0.3,5)

                elif "lip.B.L.2" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"lip.T.L.2",0.3)
                    LocConstraints(bone,"lips.L",0.7)
                    LimitDistance(bone,"chin",0.51,4.8)#,'LOCAL',False,False,True,True)
                elif "lip.B.R.2" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"lip.T.R.2",0.3)
                    LocConstraints(bone,"lips.R",0.7)
                    LimitDistance(bone,"chin",0.5,4.8)#,'LOCAL',False,False,True,True)

                #elif "chin.002" in bone.name:
                    #RemoveConstraints(bone)
                    #LocConstraints(bone,"lip.B",0.3)
                    #LocConstraints(bone,"tweak_lip.D.001",0.3)

                elif "chin.001" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"chin.002",0.4)
                    LocConstraints(bone,"chin",0.2)

                elif "cheek.B.L.001" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"lips.L",0.2)
                elif "cheek.B.R.001" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"lips.R",0.2)


                elif "cheek.T.L.001" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"cheek.B.L.001",0.1)
                    LocConstraints(bone,"cheek.B.L.002",0.3)
                elif "cheek.T.R.001" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"cheek.B.R.001",0.1)


                elif "cheek.T.L.002" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"lid.B.L.002",0.2)
                elif "cheek.T.R.002" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"lid.B.R.002",0.2)


                elif "nose.005" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"lip.T",0.2)
                elif "nose.004" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"nose.005",0.5)
                    LocConstraints(bone,"nose.003",0.6)
                elif "nose.003" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"nose.005",0.4)
                elif "nose.001" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"nose.002",0.1)
                    LocConstraints(bone,"nose",0.3)

                elif "nose.L.002" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"cheek01_ctrl.L.001",0.5)
                    LocConstraints(bone,"nose.L.001",1)
                    
                elif "nose.R.002" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"cheek01_ctrl.R.001",0.5)
                    LocConstraints(bone,"nose.R.001",1)

                elif "nose" in bone.name:
                    if "." not in bone.name:
                        RemoveConstraints(bone)
                        LocConstraints(bone,"nose.001",0.3)
                        LocConstraints(bone,"brow.T.L.003",0.3)
                        LocConstraints(bone,"brow.T.R.003",0.3)


                elif "brow.T.L" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"brow.T.L.001",0.1)
                elif "brow.R.L" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"brow.T.R.001",0.1)


                elif "lid.B.L" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"nose.L",0.3)
                elif "lid.B.R" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"nose.L",0.3)
            bpy.ops.pose.select_all(action='DESELECT')

            MakeSureSelectOneLayer(0)
            bpy.context.object.data.layers[2] = False
            bpy.ops.pose.select_all(action='SELECT')
            for bone in bpy.context.selected_pose_bones:
                if "cheek01_ctrl.L.001" in bone.name:#1
                    RemoveConstraints(bone)
                    LocConstraints(bone,"nose.L.001",0.5)
                    LocConstraints(bone,"lips.L",0.1,'LOCAL','WORLD',True,True,True,True,False,True,True)
                    LocConstraints(bone,"lips.L",0.4,'LOCAL','LOCAL',True,False,True,False,False,False,False)
                elif "cheek01_ctrl.R.001" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"nose.R.001",0.5)
                    LocConstraints(bone,"lips.R",0.1,'LOCAL','WORLD',True,True,True,True,False,True,True)
                    LocConstraints(bone,"lips.R",0.4,'LOCAL','LOCAL',True,False,True,False,False,False,False)

                elif "cheek02_ctrl.L.001" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"cheek03_ctrl.L",1,'POSE','POSE')
                elif "cheek02_ctrl.R.001" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"cheek03_ctrl.R",1,'POSE','POSE')#V

                elif "cheek01_ctrl.L" in bone.name:
                    RemoveConstraints(bone)
                    LimitDistance(bone,"chin.002",1,0.01)
                elif "cheek01_ctrl.R" in bone.name:
                    RemoveConstraints(bone)
                    LimitDistance(bone,"chin.002",1,0.01)

                elif "cheek02_ctrl.L" in bone.name:
                    RemoveConstraints(bone)
                    LimitDistance(bone,"chin.001",1,0.01)
                elif "cheek02_ctrl.R" in bone.name:
                    RemoveConstraints(bone)
                    LimitDistance(bone,"chin.001",1,0.01)

                elif "lip_ctrl.003" in bone.name:
                    RemoveConstraints(bone)
                    LimitDistance(bone,"lip.T",1,0.01)
                elif "lip_ctrl.001" in bone.name:
                    RemoveConstraints(bone)
                    LimitDistance(bone,"lip.B",1,0.01)

                elif "lip_ctrl.L.003" in bone.name:
                    RemoveConstraints(bone)
                    LimitDistance(bone,"tweak_lip.D.001",0.4,3.4)#3.4->0.03416
                    LimitDistance(bone,"lip.T.L.2",1,0.8)
                elif "lip_ctrl.R.003" in bone.name:
                    RemoveConstraints(bone)
                    LimitDistance(bone,"tweak_lip.D.001",0.4,3.4)
                    LimitDistance(bone,"lip.T.R.2",1,0.8)

                elif "lip_ctrl.L.001" in bone.name:
                    RemoveConstraints(bone)
                    LimitDistance(bone,"tweak_lip.D.001",0.4,2.6)#0.027247
                    LimitDistance(bone,"lip.B.L.2",1,0.8)
                elif "lip_ctrl.R.001" in bone.name:
                    RemoveConstraints(bone)
                    LimitDistance(bone,"tweak_lip.D.001",0.4,2.6)
                    LimitDistance(bone,"lip.B.R.2",1,0.8)

                elif "lip_ctrl.L.002" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"tweak_lip.U.001",1,'POSE','POSE')
                elif "lip_ctrl.R.002" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"tweak_lip.U.001",1,'POSE','POSE')#v

                elif "lip_ctrl.L" in bone.name:
                    if "00" not in bone.name:
                        RemoveConstraints(bone)
                        LimitDistance(bone,"tweak_lip.D.001",1,0.01)
                elif "lip_ctrl.R" in bone.name:
                    if "00" not in bone.name:
                        RemoveConstraints(bone)
                        LimitDistance(bone,"tweak_lip.D.001",1,0.01)

                elif "lip_ctrl" in bone.name:
                    if "." not in bone.name:
                        RemoveConstraints(bone)
                        LimitDistance(bone,"chin.002",1,0.01)
            bpy.ops.pose.select_all(action='DESELECT')


            MakeSureSelectOneLayer(1)
            bpy.context.object.data.layers[0] = False
            bpy.ops.pose.select_all(action='SELECT')
            for bone in bpy.context.selected_pose_bones:
                if "nose.L.001" in bone.name:#1
                    RemoveConstraints(bone)
                    LocConstraints(bone,"cheek01_ctrl.L.001",0.3)
                    #LocConstraints(bone,"nose.L.001",0.5)
                elif "nose.R.001" in bone.name:#1
                    RemoveConstraints(bone)
                    LocConstraints(bone,"cheek01_ctrl.R.001",0.3)

                elif "nose.002" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"nose.003",0.2)
                elif "cheek03_ctrl.R" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"cheek02_ctrl.R.001",1)

                elif "tweak_cheek01.R.001" in bone.name:
                    RemoveConstraints(bone)
                    LimitDistance(bone,"tweak_lip.D.R.001",1,1.2)
                elif "tweak_cheek01.L.001" in bone.name:
                    RemoveConstraints(bone)
                    LimitDistance(bone,"tweak_lip.D.L.001",1,1.2)


                elif "tweak_cheek01.L.002" in bone.name:#
                    RemoveConstraints(bone)
                    LocConstraints(bone,"lips.L",0.15,'LOCAL','WORLD',True,True,True,True,False,True,True)
                    LocConstraints(bone,"lips.L",0.6,'LOCAL','LOCAL',True,False,True,False,False,False,False)
                elif "tweak_cheek01.R.002" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"lips.R",0.15,'LOCAL','WORLD',True,True,True,True,False,True,True)
                    LocConstraints(bone,"lips.R",0.6,'LOCAL','LOCAL',True,False,True,False,False,False,False)

                elif "tweak_cheek01.L.003" in bone.name:#
                    RemoveConstraints(bone)
                    LocConstraints(bone,"lips.L",0.25,'LOCAL','WORLD',True,True,True,True,False,True,True)
                    LocConstraints(bone,"lips.L",0.8,'LOCAL','LOCAL',True,False,True,False,False,False,False)
                elif "tweak_cheek01.R.003" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"lips.R",0.25,'LOCAL','WORLD',True,True,True,True,False,True,True)
                    LocConstraints(bone,"lips.R",0.8,'LOCAL','LOCAL',True,False,True,False,False,False,False)

                elif "tweak_cheek01.L.004" in bone.name:#
                    RemoveConstraints(bone)
                    LocConstraints(bone,"lips.L",0.3,'LOCAL','WORLD',True,True,True,True,False,True,True)
                    LocConstraints(bone,"lips.L",1,'LOCAL','LOCAL',True,False,True,False,False,False,False)
                elif "tweak_cheek01.R.004" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"lips.R",0.3,'LOCAL','WORLD',True,True,True,True,False,True,True)
                    LocConstraints(bone,"lips.R",1,'LOCAL','LOCAL',True,False,True,False,False,False,False)

                elif "tweak_cheek01.L.005" in bone.name:#
                    RemoveConstraints(bone)
                    LocConstraints(bone,"lips.L",0.2,'LOCAL','WORLD',True,True,True,True,False,True,True)
                    LocConstraints(bone,"lips.L",0.8,'LOCAL','LOCAL',True,False,True,False,False,False,False)
                elif "tweak_cheek01.R.005" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"lips.R",0.2,'LOCAL','WORLD',True,True,True,True,False,True,True)
                    LocConstraints(bone,"lips.R",0.8,'LOCAL','LOCAL',True,False,True,False,False,False,False)




                elif "lip.B.L.001" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"lips.L",0.25)
                    #LocConstraints(bone,"jaw_master",0.2,'LOCAL',False,False,True,True)
                    LocConstraints(bone,"lip.B",0.5)
                    RotConstraints(bone,"lip.B",1)
                    ScaleConstraints(bone,"lip.B",1)
                elif "lip.B.R.001" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"lips.R",0.25)
                    #LocConstraints(bone,"jaw_master",0.2,'LOCAL',False,False,True,True)
                    LocConstraints(bone,"lip.B",0.5)
                    RotConstraints(bone,"lip.B",1)
                    ScaleConstraints(bone,"lip.B",1)

                elif "lip.T.L.001" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"lips.L",0.25)
                    LocConstraints(bone,"lip.T",0.75)
                    RotConstraints(bone,"lip.T",1)
                    ScaleConstraints(bone,"lip.T",1)
                elif "lip.T.R.001" in bone.name:
                    RemoveConstraints(bone)
                    LocConstraints(bone,"lips.R",0.25)
                    LocConstraints(bone,"lip.T",0.75)
                    RotConstraints(bone,"lip.T",1)
                    ScaleConstraints(bone,"lip.T",1)


            bpy.ops.pose.select_all(action='DESELECT')

            bpy.ops.object.mode_set(mode='OBJECT')

        self.report({'INFO'}, "Rig ReFace")
        return {'FINISHED'}

            #DuplicateMove()

            #for selec_bone in bpy.context.selected_bones:
                #if "face" not in bone.name:
                #Select2Bone(selec_bone.name,"ORG-face")

                #selec_bone.parent = bpy.context.object.data.edit_bones['ORG-face']

                #bpy.ops.armature.parent_set(type='OFFSET')
                #selec_bone




            #SelectBone("ORG-cheek02.L")
            #bpy.ops.armature.select_similar(type='CHILDREN')

            #SelectBone("ORG-cheek02.R")
            #bpy.ops.armature.select_similar(type='CHILDREN')
















#nose.L nose.R 细分(一分二) 得 nose.L.002 nose.R.002！镜像
#将整个nose往上移动，直到将nose.004(鼻子接近嘴唇的那部分）放置到nose.003（上一个父级之前的位置）
#nose.L.001 nose.R.001 指向 nose.002

#在nose.004后挤出 lip.U到lip.T.L模型中间位置 再细分
#在chin.001后挤出 lip.D到lip.B.L模型中间位置 再细分
#全选并复制lip.T.L子级 到 lip.U 尾部 做 lip.U.L 并命名

#全选并复制lip.B.L子级 到 lip.D 尾部 做 lip.D.L 并命名

#全选并复制lip.B.L子级 到 lip.D 头部 做 cheek01.L 并命名
#全选并复制lip.B.L子级 到 chin.001 头部 做 cheek02.L 并命名

#将cheek01.L.001尾部移动到 脸颊1 并细分为5个
#将cheek02.L.001尾部移动到 脸颊2 并细分为5个

#全选并复制lip.T.L子级 到 cheek02.L.005 尾部 做 cheek03.L 并命名
#将cheek02.L.001尾部移动到 脸颊3 并细分为6个

#将做好的骨骼进行镜像

# 以下操作先开启镜像

#cheek.T.L.001 细分 得cheek.T.L.002
#cheek.B.L.001 细分 得cheek.B.L.002

#lip.T.L.001 细分 得lip.T.L.002
#lip.B.L.001 细分 得lip. B.L.002


#还原DEF ORG位置