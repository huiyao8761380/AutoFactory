import bpy
import bmesh


#Reface
def ReSetConstraints(AddSubtarget,Bone):
    bone = Bone
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
    bone = Bone
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
    bone = Bone
    bc = bone.constraints.new('COPY_ROTATION')
    #bc.type == 'STRETCH_TO'
    #bc.name=bone.name
    bc.target = bpy.context.object
    bc.subtarget = Subtarget#lip.T.L.002
    bc.influence = Influence
    bc.target_space = Space
    bc.owner_space = Space

def ScaleConstraints(Bone,Subtarget,Influence = 1,Space = 'LOCAL',UseOffset = False):
    bone = Bone
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
    bone = Bone
    bc = bone.constraints.new('COPY_TRANSFORMS')
    #bc.type == 'STRETCH_TO'
    #bc.name=bone.name
    bc.target = bpy.context.object
    bc.subtarget = Subtarget#lip.T.L.002
    bc.influence = Influence
    bc.target_space = Space
    bc.owner_space = Space

def LimitDistance(Bone,Subtarget,Influence,Distance = 0,Space = 'WORLD'):
    bone = Bone
    bc = bone.constraints.new('LIMIT_DISTANCE')
    bc.target = bpy.context.object
    bc.subtarget = Subtarget#lip.T.L.002
    bc.influence = Influence
    bc.target_space = Space
    bc.owner_space = Space
    bc.distance = Distance#3.416

def RemoveConstraints(Bone):
    bone = Bone
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





#UE4Type
def MakeSureSelectOneLayer(layer):#确保选中该骨骼层级
    for i in range(31):
        #bpy.ops.pose.select_all(action='SELECT')
        bpy.context.object.data.layers[i] = False
    bpy.context.object.data.layers[layer] = True

    for i in range(31):
        bpy.context.object.data.layers[i] = False
    bpy.context.object.data.layers[layer] = True


def SelectBone(bone):#选择该层级的骨骼及子级

    bpy.ops.armature.select_all(action='DESELECT')
    SelectBone=bpy.context.object.data.edit_bones[bone]

    SelectBone.select_head = True
    SelectBone.select_tail = True
    SelectBone.select = True

    bpy.context.object.data.edit_bones.active = SelectBone #GOOD!
    

def Select2Bone(SecondBone,ActiveBone):

    SelectBone(ActiveBone)
    Select2Bone=bpy.context.object.data.edit_bones[SecondBone]

    Select2Bone.select_head = True
    Select2Bone.select_tail = True
    Select2Bone.select = True

def DuplicateMove():#复制骨骼到空层级

    #bpy.ops.armature.select_all(action='DESELECT')#'SELECT'
    #SelectBone(bone)
    bpy.ops.armature.duplicate_move(ARMATURE_OT_duplicate={"do_flip_names":False}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
    bpy.ops.armature.bone_layers(layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False))




#ReBone
def SetBoneParent(SecondBone,ActiveBone):

    SelectBone(ActiveBone)
    BoneChild=bpy.context.object.data.edit_bones[SecondBone]

    BoneChild.select_head = True
    BoneChild.select_tail = True
    BoneChild.select = True

    bpy.ops.armature.parent_set(type='OFFSET')#指向活跃骨骼为父级
    bpy.ops.armature.select_all(action='DESELECT')

def CleanBoneParent(ActiveBone):
    SelectBone(ActiveBone)
    bpy.ops.armature.parent_clear(type='CLEAR')


class OneClickAddUE4Rig(bpy.types.Operator):
    bl_idname = "am.oneclickaddue4rig"
    bl_label = "One Click Add UE4Rig"
    bl_description = "通过调用Rigify一键生成UE4格式的绑定骨骼。" 
    bl_options = {'REGISTER'}

    def execute(self, context):

        bpy.ops.am.rigrename()
        bpy.ops.am.rigreface()
        bpy.ops.am.ue4typebone()
        bpy.ops.am.rebone()
        bpy.ops.am.repose()

        self.report({'INFO'}, "One Click Add UE4Rig")
        return {'FINISHED'}


class RemoveIKBoneGroup(bpy.types.Operator):
    bl_idname = "am.removeikbonegroup"
    bl_label = "Remove IKBone Group"
    bl_description = "选择Ctrl+P自动绑定好的模型，删除IK顶点组的权重。" 
    bl_options = {'REGISTER'}

    def execute(self, context):
        #执行顺序5 点击绑定好的人体模型清理含有ik昵称的顶点组ik权重
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')


        ob = bpy.context.edit_object

        avg = ob.vertex_groups.active
        for vg in ob.vertex_groups:
            ob.vertex_groups.active = vg
            if vg.name.find("ik_") != -1:
                bpy.ops.object.vertex_group_remove_from()
        ob.vertex_groups.active = avg

        bpy.ops.object.mode_set(mode='OBJECT')

        self.report({'INFO'}, "Remove OBJ IKBone Group")
        return {'FINISHED'}


class RigMechByName(bpy.types.Operator):
    bl_idname = "am.rigmechbyname"
    bl_label = "Rig Mech By Name"
    bl_description = "选择要绑定的非合并物体，并选择骨骼为活动项，如果顶点组名称包含在该物体名称则生成权重,适合机械类绑定。" 
    bl_options = {'REGISTER'}

    def execute(self, context):
        amProperty = bpy.context.scene.amProperties
        sel=bpy.context.selected_objects
        Rig=bpy.context.active_object
        if amProperty.FakeRigBool ==False:
            bpy.ops.object.parent_set(type='ARMATURE_NAME')
            Rig.select_set(False)
            for ob in sel:
                if ob.name != Rig.name:
                    Rig.select_set(False)
                    ob.select_set(True)
                    bpy.context.view_layer.objects.active = ob
                    
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT', action='TOGGLE')

                    me = ob.data

                    #bm = bmesh.from_edit_mesh(me)
                    #设置你的顶点索引值
                    #v_index = 0 

                    #遍历顶点组
                    for group in ob.vertex_groups:
                        
                        #将当前顶点组设置为活动的_.
                        if group.name in ob.name:
                            bpy.ops.object.vertex_group_set_active(group=str(group.name))

                        # 选择活动顶点组
                            bpy.ops.object.vertex_group_select()

                        #获取当前选择的所有顶点(可能不用)
                            #vertices = [v for v in bm.verts if (v.select and not v.hide)]


                            bpy.ops.mesh.select_all(action='SELECT')#选择所有顶点

                            bpy.ops.object.vertex_group_assign()#赋予
                        #顶点的迭代 vertex iteration(可能不用)
                            '''
                            for vertex in vertices:
                                if vertex.index ==  v_index:
                                    print("Vertex ", v_index, " is in ", group.name)        
                            '''
                        #取消选择当前顶点组        
                            bpy.ops.object.vertex_group_deselect()

                    bmesh.update_edit_mesh(me, True)
        elif amProperty.FakeRigBool ==True:
            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode='POSE')
            MakeSureSelectOneLayer(23)
            bpy.ops.pose.select_all(action='SELECT')
            SelBone=bpy.context.selected_pose_bones
            '''
            for ob in sel:
                #if ob.name != Rig.name:
                ob.select_set(True)
                for bone in SelBone:
                    if bone.name in ob.name:
                        bpy.ops.object.parent_set(type='BONE')
                ob.select_set(False)
                    #Rig.select_set(True)
                    
            #bpy.context.view_layer.objects.active = Rig
            '''
            bpy.ops.pose.select_all(action='DESELECT')
            for bone in SelBone:
                Rig.data.bones[bone.name].select =False
            for bone in SelBone:
                Rig.data.bones[bone.name].select =False
                #if ob.name != Rig.name:
                for ob in sel:
                    
                    if (bone.name in ob.name) and ('ik' not in bone.name):
                        ob.select_set(True)
                        Rig.data.bones[bone.name].select =True#bpy.context.object.data.bones['Upperarm_l'].select=True
                        Rig.data.bones.active=Rig.data.bones[bone.name]#bpy.context.object.data.bones.active
                        #bone.select =True
                        bpy.ops.object.parent_set(type='BONE')
                    ob.select_set(False)
                    Rig.data.bones[bone.name].select =False
                


        bpy.ops.object.mode_set(mode='OBJECT')

        self.report({'INFO'}, "Rig Mech By Name")
        return {'FINISHED'}