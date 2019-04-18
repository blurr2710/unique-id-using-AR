'''
 * Team Id: 1743
 * Author List: [abhinav vashisht,lovish mehta,manjeet singh]
 * Filename: 
 * Theme: eYRC thirsty crow 
 * Functions:issafe(),convert_to_list(),find_path_to_cell(),reset(),create_cells(),find_coords(),new_convert(),decode_angles(),
 * Global Variables:cells,sol,first_time,id_list,water_pitcher_id,pitcher_orientation
'''

import queue
import time
import serial
import numpy as np
import cv2
import cv2.aruco as aruco
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import pygame
from objloader import *
texture_background = None
camera_matrix = None
dist_coeff = None
global sol
global first_time
cap = cv2.VideoCapture(1)
global id_list
from collections import defaultdict
INVERSE_MATRIX = np.array([[ 1.0, 1.0, 1.0, 1.0],
                           [-1.0,-1.0,-1.0,-1.0],
                           [-1.0,-1.0,-1.0,-1.0],
                           [ 1.0, 1.0, 1.0, 1.0]])
################## Define Utility Functions Here #######################
"""
Function Name : getCameraMatrix()
Input: None
Output: camera_matrix, dist_coeff
Purpose: Loads the camera calibration file provided and returns the camera and
         distortion matrix saved in the calibration file.
"""
def getCameraMatrix():
        global camera_matrix, dist_coeff
        with np.load('camera.npz') as X:
                camera_matrix, dist_coeff, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]

        return camera_matrix,dist_coeff

########################################################################

############# Main Function and Initialisations ########################
"""
Function Name : main()
Input: None
Output: None
Purpose: Initialises OpenGL window and callback functions. Then starts the event
         processing loop.
"""        
def main():
        glutInit()
        getCameraMatrix()
        glutInitWindowSize(640, 480)
        glutInitWindowPosition(625, 100)
        glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH | GLUT_DOUBLE)
        window_id = glutCreateWindow("OpenGL")
        init__()
        init_gl()
        glutDisplayFunc(drawGLScene)
        glutIdleFunc(drawGLScene)
        glutMainLoop()

"""
Function Name : init_gl()
Input: None
Output: None
Purpose: Initialises various parameters related to OpenGL scene.
"""
def init__():
        global texture_background 
        global webcam
        global full
        global pot_list
        global manjeet
        global lovish
        global abhinav
        pot_list=[]
        pot=None
        webcam = cv2.VideoCapture(1)
def init_gl():
        global manjeet
        global lovish
        global abhinav
        global crow
        global texture_background
        global low
        global full
        global pot_list
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(33.7, 1.3, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_TEXTURE_2D)
        texture_background = glGenTextures(1)
        lovish=OBJ('Lovish.obj',swapyz=True)
        manjeet=OBJ('manjeet.obj',swapyz=True)
        abhinav=OBJ('ABHINAV.obj',swapyz=True)
"""
Function Name : resize()
Input: None
Output: None
Purpose: Initialises the projection matrix of OpenGL scene
"""
def resize(w,h):
        ratio = 1.0* w / h
        glMatrixMode(GL_PROJECTION)
        glViewport(0,0,w,h)
        gluPerspective(45, ratio, 0.1, 100.0)
def draw_aruco(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)
    parameters = aruco.DetectorParameters_create()
    corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters = parameters)
    img = aruco.drawDetectedMarkers(img, corners,ids)
    return img

"""
Function Name : drawGLScene()
Input: None
Output: None
Purpose: It is the main callback function which is called again and
         again by the event processing loop. In this loop, the webcam frame
         is received and set as background for OpenGL scene. ArUco marker is
         detected in the webcam frame and 3D model is overlayed on the marker
         by calling the overlay() function.
"""
def drawGLScene():
        global webcam
        global texture_background
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
 
        # get image from webcam
        ret,image = webcam.read()
        center=0
        if ret == True:
                draw_background(image)
                cam,dist=getCameraMatrix()
                ar_list=detect_markers(image,cam,dist)
                for i in ar_list:
                         if i[0] != 98:
                                overlay(image, ar_list, i[0],"texture_4.png",i[1])
                         center=i[1]
                if(ret==True):
                      frame=draw_aruco(image)
                      cv2.imshow("frame", frame)
                      cv2.waitKey(1)
        glutSwapBuffers()
########################################################################
######################## Aruco Detection Function ######################
"""
Function Name : detect_markers()
Input: img (numpy array)
Output: aruco list in the form [(aruco_id_1, centre_1, rvec_1, tvec_1),(aruco_id_2,
        centre_2, rvec_2, tvec_2), ()....]
Purpose: This function takes the image in form of a numpy array, camera_matrix and
         distortion matrix as input and detects ArUco markers in the image. For each
         ArUco marker detected in image, paramters such as ID, centre coord, rvec
         and tvec are calculated and stored in a list in a prescribed format. The list
         is returned as output for the function
"""
def detect_markers(img,camera_matrix,dist_coeff):
        
        aruco_list = []
        markerLength=100
        aruco_list=[]
        ######################## INSERT CODE HERE ########################
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        aruco_dict=aruco.Dictionary_get(aruco.DICT_5X5_250)
        parameters=aruco.DetectorParameters_create()
        corners,ids,_=aruco.detectMarkers(gray,aruco_dict,parameters=parameters)
        global c
        c=corners
        with np.load('camera.npz') as X:
              camera_matrix, dist_coeff,_,_=[X[i] for i in('mtx','dist','rvecs','tvecs')]
        rvec,tvec,_=aruco.estimatePoseSingleMarkers(corners,markerLength,camera_matrix,dist_coeff)
        if(np.all(ids!=None)):
             for j in range(len(ids)):
                  rvec1=rvec[j].reshape((1,1,3))
                  tvec1=tvec[j].reshape((1,1,3))
                  #for i in corners[j]:
                   #     x,y=i[j][0],i[j][1]
                   #     break
                  center1_x=corners[0][0][1][0]
                  center1_y=corners[0][0][1][1]
                  center2_x=corners[0][0][2][0]
                  center2_y=corners[0][0][2][1]
                  center_x=(center1_x+center2_x)/2
                  center_y=(center2_y+center1_y)/2
                  center=(int(center_x),int(center_y))
                  cor=(ids[j][0],center,rvec1,tvec1)
                  aruco_list.append(cor)
        ##################################################################
        return aruco_list
########################################################################


################# This is where the magic happens !! ###################
############### Complete these functions as  directed ##################
"""
Function Name : draw_background()
Input: img (numpy array)
Output: None
Purpose: Takes image as input and converts it into an OpenGL texture. That
         OpenGL texture is then set as background of the OpenGL scene
"""
def draw_background(image):
        bg_image = cv2.flip(image, 0)
        bg_image = Image.fromarray(bg_image)     
        ix = bg_image.size[0]
        iy = bg_image.size[1]
        bg_image = bg_image.tobytes("raw", "BGRX", 0, -1)
  
        # create background texture
        glBindTexture(GL_TEXTURE_2D, texture_background)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, bg_image)
        # draw background
        glBindTexture(GL_TEXTURE_2D, texture_background)
        glPushMatrix()
        glTranslatef(0.0,0.0,-10.0)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0); glVertex3f(-4.0, -3.0, 0.0)
        glTexCoord2f(1.0, 1.0); glVertex3f( 4.0, -3.0, 0.0)
        glTexCoord2f(1.0, 0.0); glVertex3f( 4.0,  3.0, 0.0)
        glTexCoord2f(0.0, 0.0); glVertex3f(-4.0,  3.0, 0.0)
        glEnd()
        glPopMatrix()
        return None

"""
Function Name : init_object_texture()
Input: Image file path
Output: None
Purpose: Takes the filepath of a texture file as input and converts it into OpenGL
         texture. The texture is then applied to the next object rendered in the OpenGL
         scene.
"""
def init_object_texture(image_filepath):
        im = Image.open(image_filepath)
        rgb_im = im.convert('RGB')
        image=rgb_im
        global texture_cube
        glEnable(GL_TEXTURE_2D)
        texture_cube = glGenTextures(1)
        ix = image.size[0]
        iy = image.size[1]
        image = image.tobytes("raw", "RGBX", 0, -1)
        glBindTexture(GL_TEXTURE_2D, texture_cube)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        return None

"""
Function Name : overlay()
Input: img (numpy array), aruco_list, aruco_id, texture_file (filepath of texture file)
Output: None
Purpose: Receives the ArUco information as input and overlays the 3D Model of a teapot
         on the ArUco marker. That ArUco information is used to
         calculate the rotation matrix and subsequently the view matrix. Then that view matrix
         is loaded as current matrix and the 3D model is rendered.

         Parts of this code are already completed, you just need to fill in the blanks. You may
         however add your own code in this function.
"""
####here data of final_path is sent to the robot
def overlay(img, ar_list, ar_id, texture_file,center):
        global lovish
        global manjeet
        for x in ar_list:
                if ar_id == x[0]:
                        centre, rvec, tvec = x[1], x[2], x[3]
        if len(ar_list)==0: 
                    return
                # build view matrix
        rmtx = cv2.Rodrigues(rvec)[0]
 
        view_matrix =np.array([[rmtx[0][0],rmtx[0][1],rmtx[0][2],tvec[0][0][0]/400],
                                [rmtx[1][0],rmtx[1][1],rmtx[1][2],tvec[0][0][1]/350],
                                [rmtx[2][0],rmtx[2][1],rmtx[2][2],tvec[0][0][2]/400],
                                [0.0       ,0.0       ,0.0       ,1.0    ]]) 
 
        view_matrix = view_matrix * INVERSE_MATRIX
        view_matrix = np.transpose(view_matrix)
        glPushMatrix()
        glLoadMatrixd(view_matrix)
        if(ar_id==10):
                 glCallList(manjeet.gl_list)
        if(ar_id==7):
            glCallList(lovish.gl_list)
        if(ar_id==6):
            glCallList(abhinav.gl_list)
        glPopMatrix()

########################################################################
if __name__ == "__main__":
        main()
        
