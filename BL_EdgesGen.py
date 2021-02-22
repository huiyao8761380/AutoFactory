import bpy
import random

from . BL_Tool import *
from bpy.types import Operator,PropertyGroup
from bpy.props import FloatProperty, PointerProperty,StringProperty
#import numpy as np
#from random import random, randint 这代码也是看起来人模狗样的啊
#scene = bpy.context.scene
class EdgesGen:
    def __init__(self,name,BaseMin,BaseMax,vNumber,location):#,xu,yu,zu,xv,yv,zv
        if name is None:
            name = "EdgesGen"
        self.name = name
        #调参数区
        self.BaseMin = BaseMin#-5
        self.BaseMax = BaseMax#5
        self.vNumber = vNumber#10

        self.ENumber = self.vNumber - 1
        self.location = location

        self.verts = []
        self.edges = []
        self.faces = []

    def add_EdgeMesh(self):#默认位置location=(0,0,0)
        verts = self.random_verts()    #Define vertices and faces
        edges = self.random_edges()
        faces = [] #faces = [(0,1,2,3)]

        col_name="0AutoMech"#1设置集合名字

        MyMesh = bpy.data.meshes.new(self.name)#Name in edit mesh
        MyObject = bpy.data.objects.new(self.name, MyMesh)#name in object
        
        cube_collection = find_collection(bpy.context, MyObject)#2通过函数find_collection制作合集
        new_collection = make_collection(col_name,cube_collection)#3NEW col 将合集交给1GenLine

        col = bpy.data.collections.get(col_name)#4
        col.objects.link(MyObject)
        bpy.context.view_layer.objects.active = MyObject
        MyObject.select_set(True)#选择生成的所有物体
        MyMesh.from_pydata(verts, edges, faces)#Create mesh
        MyObject.location = self.location#Set location and scene of object
        MyMesh.update(calc_edges=True)#

    def random_verts(self):#把上面的变量传进来
        rand_verts = []
        amProperty = bpy.context.scene.amProperties
        sampleProperty = bpy.context.scene.AMOldPropertyGroup

        #if amProperty.GenLineEnum == 'GenLineOnly':
        if sampleProperty.edgeXYZ == True:
            xu=random.uniform(sampleProperty.xuMin,0)
            yu=random.uniform(sampleProperty.yuMin,0)
            zu=random.uniform(sampleProperty.zuMin,0)

            xv=random.uniform(0, sampleProperty.xvMax)
            yv=random.uniform(0, sampleProperty.yvMax)
            zv=random.uniform(0, sampleProperty.zvMax)
        else:
            xu=random.uniform(self.BaseMin,0)#暂不传值
            yu=random.uniform(self.BaseMin,0)
            zu=random.uniform(self.BaseMin,0)

            xv=random.uniform(0, self.BaseMax)
            yv=random.uniform(0, self.BaseMax)
            zv=random.uniform(0, self.BaseMax)

        x_u,y_u,z_u = self.BaseMin+xu,self.BaseMin+yu,self.BaseMin+zu
        x_v,y_v,z_v = self.BaseMax+xv,self.BaseMax+yv,self.BaseMax+zv
        for v in range(self.vNumber):
        #random.uniform(1,5.0) random.randint(self.BaseMin, self.BaseMax) random.random()
            x = random.uniform(x_u,x_v)
            y = random.uniform(y_u,y_v)
            z = random.uniform(z_u,z_v)
            rand_verts.append((x,y,z))
        #print("rand_verts: ")
        #print(rand_verts)
        self.verts = rand_verts    #old_verts = random.shuffle(old_verts)
        return self.verts
        
    def random_edges(self):
        rand_edges = []
        for e in range(self.ENumber):
            u = e
            v = u + 1
            rand_edges.append((u,v))
        #print(rand_edges)
        self.edges = rand_edges
        return self.edges
        
