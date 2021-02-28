import os
'''
folder_path = 'C:/Users/Administrator/AppData/Roaming/Blender Foundation/Blender/2.90/scripts/addons/AutoMech/Preset'

#path = folder_path.replace("/", "/")
path = os.path.realpath(folder_path)#soft os.path.abspath
os.startfile(path)




for filename in os.listdir(os.getcwd()):
   #with open(os.path.join(os.getcwd(), filename), 'r')
   print(os.path.join(os.getcwd(), filename))
  
   
FileList=''
for filename in os.listdir(os.getcwd()):
   #with open(os.path.join(os.getcwd(), filename), 'r')
   FileList+=' '+filename
print(FileList)



FileList=[]
for file in os.listdir(os.getcwd()):
   #with open(os.path.join(os.getcwd(), filename), 'r')
    filename=file.split('.', 1)
    if len(filename[0]) < 1:
        FileList.append(filename[1])
    else:
        FileList.append(filename[0])
print(len(FileList))
'''

#for i in FileList:
    #print(i)
    
FileList=[]
enum_items = [
        ('MechPro', 'MechPro', "Multiple Modifier"),
        ('Helmet', "Helmet", "GenMech low poly procedural helmet mesh."),
        ('Mechfy', "Mechfy", "Created by Emiliano Colantoni for the first time")
    ]
    
FolderPath=os.path.dirname(__file__)+'//Preset//'
for file in os.listdir(FolderPath):
    filename=file.split('.', 1)
    if len(filename[0]) < 1:
        FileList.append(filename[1])
    else:
        FileList.append(filename[0])
for name in FileList:
    enum_items.append((name, name, ""))
#print(name, name, "")
print(enum_items)
