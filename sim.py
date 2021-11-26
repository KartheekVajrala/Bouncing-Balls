# importing Libraries

import pygame
from pygame.locals import *
import random
from OpenGL.GL import *
from OpenGL.GLU import *
from utilities import *

# User Parameters

L = 1                    # Length of the box
N = 20                  # Number of balls
initial_radius = 0          # Initial radius of the balls
final_volume_frac = 0.7     # Fraction of the volume of the box at end
save_location = True        # Save the location of the balls
hardCollision = True
increase_radius_hard = True

def Cube():
    '''
    Using OpenGL to draw a cube edges
    '''
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glColor3fv((0,0,0))
            glVertex3fv(verticies[vertex])
    glEnd()

def Sphere(ball):
    '''
    Using OpenGL to draw a sphere
    ball is an object from the class Ball in ultilities.py
    '''
    glPushMatrix()
    sphere = gluNewQuadric()
    glTranslatef(ball.pos.x,ball.pos.y,ball.pos.z) #Move to the place
    glColor3fv((1,0,0)) #Put color
    gluSphere(sphere, ball.radius, 16, 8) #Draw sphere
    glPopMatrix()
    # Also need to draw the images of cubes
    for img in ball.images:
        if img != None:
            Sphere(img)

def remove_images(balls):
    '''
    Removing uneccessary images that are not needed.
    '''
    for ball in balls:
        ball.images = []

def save_balls(balls):
    '''
    Save balls location in a locations.txt file
    '''
    with open('locations.txt','w') as f:
        for ball in balls:
            f.write(str(ball.radius) +" , " + str(ball.pos.x) + ' , ' + str(ball.pos.y) + ' , ' + str(ball.pos.z) + '\n')
            for img in ball.images:
                f.write(str(img.radius) +" , " + str(img.pos.x) + ' , ' + str(img.pos.y) + ' , ' + str(img.pos.z) + '\n')
    return

def main():
    # pygame Initialization
    pygame.init()
    display = (800,600)                                                     # Display size
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)                      # Rendering OpenGL in pygame
    
    # opengl Initialization
    gluPerspective(45, (display[0]/display[1]), 1, 50.0)
    glTranslatef(-0.5, -0.5, -4)                                            # Move the camera to the required position
    glRotatef(-20, 0, 1, 0)                                                 # Rotate the camera to the required position

    # Initialize the balls with random positions and velocities
    balls = []  
    for i in range(N):
            rand_x = random.uniform(0.1,0.9)
            rand_y = random.uniform(0.1,0.9)
            rand_z = random.uniform(0.1,0.9)
            rand_x_vel = random.uniform(-0.1,0.1)
            rand_y_vel = random.uniform(-0.1,0.1)
            rand_z_vel = random.uniform(-0.1,0.1)
            balls.append(Ball(Vector3(rand_x,rand_y,rand_z), Vector3(rand_x_vel,rand_y_vel,rand_z_vel), initial_radius))

    # Main Loop
    while True:
        for event in pygame.event.get():                       # Check for events and if quit is pressed exit the code
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # glRotatef(1, 0, 1, 0)

        # Computaion of Algorithm
        if not hardCollision:
        
            tc, particles1 = Calculate_tc(balls,N)                 # Calculate the time of collision (Algorithm 4.2)
            tr, particles2 = Calculate_tr(balls,N,L)                # Calculate the time of reflection (Algorithm 4.3)
            del_t = 0.01
            del_t = min(tc,0.03)
            # Update the position and radius of the balls
            for ball in balls:
                ball.update(del_t)
                ball.update_radius(del_t)
            # Change the position of Balls
            if del_t == tc:                                         
                vel_i,vel_j = collosion_balls(particles1)
                particles1[0].vel = vel_i
                particles1[1].vel = vel_j
            
            generate_images(balls,L)                                
            collision_wall(balls)
            
        # For in case of reflection generate the images of the balls
        else :
            hard_collision(balls,L)
            del_t = 0.05
            Calculate_tc(balls,N)
            for ball in balls:
                ball.update(del_t)
                if increase_radius_hard:
                    ball.update_radius(del_t)
            

        # Calculate the volume fraction of the box
        volume = N*(4/3)*3.14*balls[0].radius**3
        volume_frac = volume/(L**3)         

        # Condition for stopping the Simulation                    
        if volume_frac > final_volume_frac: 
            print("Program ended")

            # If locations are to be Saved.
            if save_location:
                save_balls(balls)
            pygame.quit()
            quit()
            break

        # For Rendering and Visualization using OpenGl
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE )
        glClearColor(1, 1, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    
        for ball in balls:
            # Rendering the Balls
            Sphere(ball)
        # Rendering the Box
        Cube()

        remove_images(balls)
        pygame.display.flip()
        
        pygame.time.wait(10)


main()