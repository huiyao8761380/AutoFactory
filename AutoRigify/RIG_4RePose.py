import bpy
#执行顺序4 Armature姿态模式



class RePose(bpy.types.Operator):
    bl_idname = "am.repose"
    bl_label = "RePose"
    bl_description = "切换Rig到姿态模式重新设置各个骨骼约束。" 
    bl_options = {'REGISTER'}

    def execute(self, context):

        bpy.ops.object.mode_set(mode='OBJECT')#
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.select_all(action='SELECT')
        for bone in bpy.context.selected_pose_bones:
            # Create a list of all the copy location constraints on this bone
            copyTransformsConstraints = [ a for a in bone.constraints if a.type == 'COPY_TRANSFORMS' ]
            DampedTrackConstraints = [ b for b in bone.constraints if b.type == 'DAMPED_TRACK' ]
            StretchToConstraints = [ c for c in bone.constraints if c.type == 'STRETCH_TO' ]
            
            # Iterate over all the bone's copy location constraints and delete them all

            for a in copyTransformsConstraints:
                bone.constraints.remove( a ) # Remove constraint
            for b in DampedTrackConstraints:
                bone.constraints.remove( b ) # Remove constraint
            for c in StretchToConstraints:
                bone.constraints.remove( c ) # Remove constraint



        for bone in bpy.context.selected_pose_bones:
            bc = bone.constraints.new('COPY_TRANSFORMS')
            
            bc.target = bpy.context.object

            bc.name = bone.name
            
            if "DEF-feet_" in bone.name:
                bc.name=bone.name[:-9]
                OldBoneName = bone.name[14:-4]
            
            if "DEF-palm" in bone.name:
                bc.name=bone.name[:-9]
                OldBoneName = bone.name[8:-4]
                
            if "DEF-thumb" in bone.name:
                bc.name=bone.name[:-9]
                OldBoneName = bone.name[9:-4]
                
            if "DEF-f_index" in bone.name:
                bc.name=bone.name[:-9]
                OldBoneName = bone.name[11:-4]
                
            if "DEF-f_middle" in bone.name:
                bc.name=bone.name[:-9]
                OldBoneName = bone.name[12:-4]
                
            if "DEF-f_ring" in bone.name:
                bc.name=bone.name[:-9]
                OldBoneName = bone.name[10:-4]
                
            if "DEF-f_pinky" in bone.name:
                bc.name=bone.name[:-9]
                OldBoneName = bone.name[11:-4]

            #if "root" in bone.name:

            

            
            bone.name = bone.name.replace(".", "_")
            
            
            if "00" in bone.name:
                bone.name = bone.name[:-4]
            elif "_01" in bone.name:
                bone.name = bone.name[:-4]


            if "DEF-feet_" in bone.name:
                OldBoneName = bc.name + OldBoneName#DEF-feet.pinky.
            elif "DEF-palm" in bone.name:
                OldBoneName = bc.name + OldBoneName
            elif "DEF-thumb" in bone.name:
                OldBoneName = bc.name + OldBoneName
            elif "DEF-f_" in bone.name:
                OldBoneName = bc.name + OldBoneName
            
            else:
                OldBoneName = bone.name.replace("_", ".")
            
            
            
            if "teeth" in bone.name:
                OldBoneName = OldBoneName.replace("ORG-", "ORG-")
            elif "eye" in bone.name:
                OldBoneName = OldBoneName.replace("ORG-", "ORG-")
            else:
                OldBoneName = OldBoneName.replace("ORG-", "DEF-")
                
            #OldBoneName = OldBoneName[:-1]

            
            if "root" in bone.name:
                bc.subtarget = "root"#bone.name[:-4]
                if "root.001" in bc.name:
                    bone.name ="ik_hand_root"
                    bpy.context.object.pose.bones["ik_hand_root"].bone_group = None
                    rootbone = bpy.context.object.data.bones["ik_hand_root"]
                    rootbone.use_deform = True
                    rootbone.envelope_distance = 0
                    rootbone.envelope_weight = 0
                    rootbone.use_envelope_multiply = True
                    rootbone.head_radius = 0
                    rootbone.tail_radius = 0
                elif "root.002" in bc.name:
                    bone.name ="ik_foot_root"
                    bpy.context.object.pose.bones["ik_foot_root"].bone_group = None
                    rootbone = bpy.context.object.data.bones["ik_foot_root"]
                    rootbone.use_deform = True
                    rootbone.envelope_distance = 0
                    rootbone.envelope_weight = 0
                    rootbone.use_envelope_multiply = True
                    rootbone.head_radius = 0
                    rootbone.tail_radius = 0
            elif "DEF-hand" in bc.name:
                bc.subtarget = bc.name[:-4]
                if "hand.r.002" in bc.name:
                    bc.subtarget = "hand_ik.r"
                    bone.name ="ik_hand_r"
                    handbone = bpy.context.object.data.bones["ik_hand_r"]
                    handbone.use_deform = True
                    handbone.envelope_distance = 0
                    handbone.envelope_weight = 0
                    handbone.use_envelope_multiply = True
                    handbone.head_radius = 0
                    handbone.tail_radius = 0
                elif "hand.r.003" in bc.name:
                    bc.subtarget = "hand_ik.r"
                    bone.name ="ik_hand_gun"
                    handbone = bpy.context.object.data.bones["ik_hand_gun"]
                    handbone.use_deform = True
                    handbone.envelope_distance = 0
                    handbone.envelope_weight = 0
                    handbone.use_envelope_multiply = True
                    handbone.head_radius = 0
                    handbone.tail_radius = 0
                elif "hand.l.002" in bc.name:
                    bc.subtarget = "hand_ik.l"
                    bone.name ="ik_hand_l"
                    handbone = bpy.context.object.data.bones["ik_hand_l"]
                    handbone.use_deform = True
                    handbone.envelope_distance = 0
                    handbone.envelope_weight = 0
                    handbone.use_envelope_multiply = True
                    handbone.head_radius = 0
                    handbone.tail_radius = 0
            elif "DEF-foot" in bc.name:
                bc.subtarget = bc.name[:-4]
                if "foot.r.002" in bc.name:
                    bc.subtarget = "foot_ik.r"
                    bone.name ="ik_foot_r"
                    footbone = bpy.context.object.data.bones["ik_foot_r"]
                    footbone.use_deform = True
                    footbone.envelope_distance = 0
                    footbone.envelope_weight = 0
                    footbone.use_envelope_multiply = True
                    footbone.head_radius = 0
                    footbone.tail_radius = 0
                elif "foot.l.002" in bc.name:
                    bc.subtarget = "foot_ik.l"
                    bone.name ="ik_foot_l"
                    footbone = bpy.context.object.data.bones["ik_foot_l"]
                    footbone.use_deform = True
                    footbone.envelope_distance = 0
                    footbone.envelope_weight = 0
                    footbone.use_envelope_multiply = True
                    footbone.head_radius = 0
                    footbone.tail_radius = 0
            else:
                bc.subtarget = OldBoneName #从这里开始复制变换
            #bc.name = bone.name
            
            if "neck" in bone.name:
                bc.subtarget = bc.name[:-4].replace("ORG-", "DEF-") +'.01'
                if "neck" and ".001" in bone.name:
                    bc.subtarget = bc.name[:-4].replace("ORG-", "DEF-")+'.02'
            
            
            elif "spine" in bone.name:
                if "spine.00" not in bone.name:
                    bc.subtarget = bc.name[:-4].replace("ORG-", "DEF-")+".01"
                elif "spine.001" in bone.name:
                    bc.subtarget = bc.name[:-4].replace("ORG-", "DEF-")+".02"
                elif "spine.002" in bone.name:
                    bc.subtarget = bc.name[:-4].replace("ORG-", "DEF-")+".03"
                    
            elif "DEF-head"in bone.name:
                bc.subtarget = bc.name[:-4].replace("ORG-", "DEF-")
            elif "DEF-pelvis" in bone.name:
                bc.subtarget = bc.name[:-4].replace("ORG-", "DEF-")
            elif "ORG-face" in bone.name:
                bc.subtarget = bc.name[:-4]
            elif "ORG-jaw.001" in bone.name:
                bc.subtarget = bc.name[:-4].replace("ORG-", "DEF-")
                
                
            elif "ORG-tongue" in bone.name:
                if "ORG-tongue.003" in bone.name:
                    bc.subtarget = bc.name[:-4].replace("ORG-", "DEF-")
                elif "ORG-tongue.004" in bone.name:
                    bc.subtarget = bc.name[:-4].replace("ORG-", "DEF-")+".001"
                elif "ORG-tongue.005" in bone.name:
                    bc.subtarget = bc.name[:-4].replace("ORG-", "DEF-")+".002"
                    
            elif "ORG-chin" in bone.name:
                if "ORG-chin.002" in bone.name:
                    bc.subtarget = bc.name[:-4].replace("ORG-", "DEF-")
                elif "ORG-chin.003" in bone.name:
                    bc.subtarget = bc.name[:-4].replace("ORG-", "DEF-")+".001"

            elif "ORG-nose" in bone.name:
                if "ORG-nose.005" in bone.name:
                    bc.subtarget = bc.name[:-4].replace("ORG-", "DEF-")
                elif "ORG-nose.007" in bone.name:
                    bc.subtarget = bc.name[:-4].replace("ORG-", "DEF-")+".001"
                elif "ORG-nose.006" in bone.name:
                    bc.subtarget = bc.name[:-4].replace("ORG-", "DEF-")+".002"
                elif "ORG-nose.008" in bone.name:
                    bc.subtarget = bc.name[:-4].replace("ORG-", "DEF-")+".003"
                elif "ORG-nose.009" in bone.name:
                    bc.subtarget = bc.name[:-4].replace("ORG-", "DEF-")+".004"

                elif "L.005" in bc.name:
                    bc.subtarget = bc.name[:-4].replace("ORG-", "DEF-") + ".001"
                elif "R.005" in bc.name:
                    bc.subtarget = bc.name[:-4].replace("ORG-", "DEF-") + ".001"
                elif "L.004" in bc.name:
                    bc.subtarget = bc.name[:-4].replace("ORG-", "DEF-") + ".002"
                elif "R.004" in bc.name:
                    bc.subtarget = bc.name[:-4].replace("ORG-", "DEF-") + ".002"
                    
            elif "ORG-jaw_L" in bone.name:
                if "ORG-jaw_L.001" in bone.name:
                    bc.subtarget = "DEF-jaw.L"
                else:
                    bc.subtarget = "DEF-jaw.L.001"
                    
            elif "ORG-jaw_R" in bone.name:
                if "ORG-jaw_R.001" in bone.name:
                    bc.subtarget = "DEF-jaw.R"
                else:
                    bc.subtarget = "DEF-jaw.R.001"
                    
                    
                if "root.001" in bone.name:
                    bone.name = bone.name.replace("root.001", "ik_hand_root")#ik
                if "root.002" in bone.name:
                    bone.name = bone.name.replace("root.002", "ik_foot_root")

            elif "cheek.T." in bc.name:#++++++++++++++++++++++
                if "005" in bc.name:
                    bc.subtarget = bc.name[:-4].replace("ORG-", "DEF-") + ".001"
                elif "004" in bc.name:
                    bc.subtarget = bc.name[:-4].replace("ORG-", "DEF-") + ".002"

            elif "cheek.B." in bc.name:
                if ".005" in bc.name:
                    bc.subtarget = bc.name[:-4].replace("ORG-", "DEF-") + ".001"

                elif ".004" in bc.name:
                    bc.subtarget = bc.name[:-4].replace("ORG-", "DEF-") + ".002"

            elif "lip.T." in bc.name:
                if ".005" in bc.name:
                    bc.subtarget = bc.name[:-4].replace("ORG-", "DEF-") + ".001"

                elif ".004" in bc.name:
                    bc.subtarget = bc.name[:-4].replace("ORG-", "DEF-") + ".002"

            elif "lip.B." in bc.name:
                if ".005" in bc.name:
                    bc.subtarget = bc.name[:-4].replace("ORG-", "DEF-") + ".001"

                elif ".004" in bc.name:
                    bc.subtarget = bc.name[:-4].replace("ORG-", "DEF-") + ".002"

        #DEF-lip.T.

            '''


            elif "ORG-tongue" in bone.name:
                bc.subtarget = bc.name[:-4]
            '''
            





        for bone in bpy.context.selected_pose_bones:
            if "ORG" in bone.name:
                bone.name = bone.name.replace("ORG", "UE4")
            elif "DEF" in bone.name:
                bone.name = bone.name.replace("DEF", "UE4")
                

            if '-f_' in bone.name:
                bone.name = bone.name.replace("-f_", "-")

            if '_l' in bone.name:           
                bone.name = bone.name.replace("_l", "_L")   
            if '_r' in bone.name:
                bone.name = bone.name.replace("_r", "_R")

            if "ik_" in bone.name:
                bone.name=bone.name.lower()
            else:
                bone.name = bone.name[4:].capitalize()

            if ".00" in bone.name:
                bone.name=bone.name[:-4]
                if ".00" in bone.name:
                    bone.name=bone.name[:-4]

            if ".001" in bone.name:
                bone.name=bone.name.replace(".001", ".01")
            if ".002" in bone.name:
                bone.name=bone.name.replace(".002", ".02")
            if ".003" in bone.name:
                bone.name=bone.name.replace(".003", ".03")
            if ".004" in bone.name:
                bone.name=bone.name.replace(".004", ".04")
            if ".005" in bone.name:
                bone.name=bone.name.replace(".005", ".05")


            bone.name=bone.name.replace(".00", ".0")
            if ".00" in bone.name:
                bone.name=bone.name[:-4]
                if ".00" in bone.name:
                    bone.name=bone.name[:-4]

            bone.name=bone.name.replace(".00", ".0")
            if ".00" in bone.name:
                bone.name=bone.name[:-4]
                if ".00" in bone.name:
                    bone.name=bone.name[:-4]

            bone.name=bone.name.replace(".00", ".0")
            if ".00" in bone.name:
                bone.name=bone.name[:-4]

            bone.name=bone.name.replace(".00", ".0")
            if ".00" in bone.name:
                bone.name=bone.name[:-4]

            bone.name=bone.name.replace(".00", ".0")
            bone.name=bone.name.replace(".00", ".0")
            bone.name=bone.name.replace(".00", ".0")



        for bone in bpy.context.object.data.bones:
            #if bone.name == 'root':#骨骼名称为Armature时才会删掉
                #bone.name='FakeRoot'

            if bone.name == 'Thigh_l.01':
                bone.name='thigh_twist_01_l'
            if bone.name == 'Thigh_r.01':
                bone.name='thigh_twist_01_r'

            if bone.name == 'Calf_l.01':
                bone.name='calf_twist_01_l'
            if bone.name == 'Calf_r.01':
                bone.name='calf_twist_01_r'

            if bone.name == 'Upperarm_l.01':
                bone.name='upperarm_twist_01_l'
            if bone.name == 'Upperarm_r.01':
                bone.name='upperarm_twist_01_r'

            if bone.name == 'Lowerarm_l.01':
                bone.name='lowerarm_twist_01_l'
            if bone.name == 'Lowerarm_r.01':
                bone.name='lowerarm_twist_01_r'

            if bone.name == 'Spine.02':
                bone.name='spine_03'
            if bone.name == 'Spine.01':
                bone.name='spine_02'
            if bone.name == 'Spine':
                bone.name='spine_01'

        bpy.ops.object.mode_set(mode='OBJECT')#

        self.report({'INFO'}, "RePose")
        return {'FINISHED'}