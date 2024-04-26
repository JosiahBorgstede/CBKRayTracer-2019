import numpy as np
import matplotlib.pyplot as plt
import math
import random

import tracer.ray as ray
import tracer.camera as camera
import tracer.hitable as hitable
import tracer.surfaces as surfaces
import tracer.material as material
import tracer.texture as texture
import tracer.sah_bvh as sah_bvh
import tracer.triangle as triangle
import tracer.translations as translations
   

def makeScene():
    nx = 500 # Number of x pixels
    ny = 500# Number of y pixels
    ns = 1 #Number of z pixels

    #Camera
    cam = camera.Camera(np.array([278, 278, -800]), np.array([278, 278, 0]), \
                        np.array([0, -1, 0]), 40.0, nx/ny) # Make a camera

    # This makes a list of hitable objects we can collide with
    world = hitable.HitableList()
#canoe cam:look from 0, 0, 3 to 0, 0, 0
    #Textures
    colorLayer1 = texture.Marble(100, np.array([0.5493, 0.8322, 1]),\
                                 np.array([0.5145, 0.7090, 1]))
    colorLayer2 = texture.Marble(20, np.array([0.3804, 0.5530, 1.0]),\
                                 np.array([0.3252, 0.5068, 1.0]))
    colorLayer3 = texture.Marble(20, np.array([0.4263, 0.4341, 0.7792]),\
                                 np.array([0.4064, 0.5548, 1.0]))
    lightColor = texture.ConstantTexture(np.array([1, 1, 1]))
    green = texture.ConstantTexture(np.array([0.4, 1.0, 0.5]))
    black = texture.ConstantTexture(np.array([0.0, 0.0, 0.0]))
    wood = texture.Wood(0.5)
    

##    #Shapes
##    layerOne = surfaces.XZ_Rect(np.array([-100, 0.5, -1000]), np.array([100, 0.5, 12]), material.Dielectric(colorLayer1, 1.2))
##    layerTwo = surfaces.XZ_Rect(np.array([-100, 0.7, -1000]), np.array([100, 0.7, 12]), material.Dielectric(colorLayer2, 1.0))
##    layerThree = surfaces.XZ_Rect(np.array([-100, 1.0, -1000]), np.array([100, 0.5, 12]), material.Dielectric(colorLayer3, 1.0))
##    layerFour = surfaces.XZ_Rect(np.array([-100, 1.0, -1000]), np.array([100, 1, 12]), material.Metal(colorLayer3, 0.3))
##    sphere1 = surfaces.Sphere(np.array([0, 0, -1]), 0.5, material.Diffuse(wood))
##    box1 = surfaces.Box(np.array([0, -0.5, -1.5]), np.array([3, 0.5, -0.5]), material.Diffuse(wood))
##    sphere2 = surfaces.Sphere(np.array([3.25, 0, -1]), 0.5, material.Diffuse(wood))
##    spherenot1 = surfaces.Sphere(np.array([0.5, -0.5, -1]), 0.5, material.Diffuse(green))
##    boxnot1 = surfaces.Box(np.array([0.5, -1, -1.5]), np.array([2.5, 0, -0.5]), material.Diffuse(green))
##    spherenot2 = surfaces.Sphere(np.array([2.75, -0.5, -1]), 0.5, material.Diffuse(green))
##    connect = surfaces.Connected(box1, sphere1)
##    connect2 = surfaces.Connected(connect, sphere2)
##    connectnot = surfaces.Connected(boxnot1, spherenot1)
##    connectnot2 = surfaces.Connected(connectnot, spherenot2)
##    canoe = surfaces.Removal(connect2, connectnot2)
#    sphere = surfaces.Sphere(np.array([0, 0, 0]), 0.5, material.Diffuse(texture.Marble(5)))
 #   ground = surfaces.Sphere(np.array([0, 1000, 0]), 999, material.Diffuse(green))
    
    
    
    #Lights
 #   lightOne = surfaces.Sphere(np.array([0, -1, 0]), 0.5, material.Boring(lightColor))
#    lightTwo = surfaces.Sphere(np.array([0, -1, 3]), 0.5, material.Boring(lightColor))
#    lightThree = surfaces.Sphere(np.array([0, 0, -0.5]), 0.5, material.Boring(lightColor))
#    sun = surfaces.Sphere(np.array([400, -700, -1000]), 150, material.Boring(lightColor))

 #   canoeTwo = translations.translate(canoe, np.array([-1, 0, 0]))
    
    
##    #World Append
##    world.append(sun)
##    world.append(layerOne)
##    world.append(layerTwo)
##    world.append(layerThree)
##    world.append(layerFour)
##    #world.append(canoeTwo)
##    world.append(canoe)
#    world.append(sphere)
 #   world.append(ground)

    #textures
    red = texture.ConstantTexture(np.array([0.65, 0.05, 0.05]))
    white = texture.ConstantTexture(np.array([0.73, 0.73, 0.73]))
    green = texture.ConstantTexture(np.array([0.12, 0.45, 0.15]))
    light = texture.ConstantTexture(np.array([1.0, 1.0, 1.0]))
    

    #objects
    left = surfaces.YZ_Rect(np.array([555, 0, 0]), np.array([555, 555, 555]),\
                            material.Diffuse(red))
    right = surfaces.YZ_Rect(np.array([0, 0, 0]), np.array([0, 555, 555]), material.Diffuse(green))
    light = surfaces.XZ_Rect(np.array([213, 554, 227]), np.array([343, 554, 332]), material.Boring(light))
    floor = surfaces.XZ_Rect(np.array([0, 0, 0]), np.array([555, 0, 555]), material.Diffuse(white))
    roof = surfaces.XZ_Rect(np.array([0, 555, 0]), np.array([555, 555, 555]), material.Diffuse(white))
    back = surfaces.XY_Rect(np.array([0, 0, 555]), np.array([555, 555, 555]), material.Diffuse(white))
    box1 = surfaces.Box(np.array([265, 0, 65]), np.array([430, 165, 230]), material.Diffuse(white))
    box2 = surfaces.Box(np.array([130, 0, 295]), np.array([295, 330, 460]), material.Diffuse(white))
    sphere = surfaces.Sphere(np.array([347.5, 82.5, 147.5]), 82.5, material.Dielectric(white, 1.1))


    #append
    world.append(left)
    world.append(right)
    world.append(floor)
    world.append(roof)
    world.append(back)
    world.append(light)
    #world.append(box1)
    world.append(box2)
    world.append(sphere)
    
                                                        
    
    world = sah_bvh.SAH_BVH(world.hitables)
    lights = [light] #This makes a list of lights for defining lights
    return nx, ny, ns, cam, world, lights
