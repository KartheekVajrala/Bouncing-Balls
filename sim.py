import pygame
from pygame.locals import *
import random
from OpenGL.GL import *
from OpenGL.GLU import *
from utilities import *

L = 1
N = 50
initial_radius = 0
final_volume_frac = 0.7

def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glColor3fv((0,0,0))
            glVertex3fv(verticies[vertex])
    glEnd()

def Sphere(ball):
    glPushMatrix()
    sphere = gluNewQuadric()
    glTranslatef(ball.pos.x,ball.pos.y,ball.pos.z) #Move to the place
    glColor3fv((1,0,0)) #Put color
    gluSphere(sphere, ball.radius, 16, 8) #Draw sphere
    glPopMatrix()
    for img in ball.images:
        if img != None:
            Sphere(img)

def remove_images(balls):
    for b,ball in enumerate(balls):
        for i,img in enumerate(ball.images):
            if img == None:
                continue
            if i==0:
                if ball.pos.x > ball.radius:
                    ball.images[i] = None
                if ball.pos.x < -ball.radius:
                    balls[b] = ball.images[i]
                    break
            if i==1:
                if ball.pos.y > ball.radius:
                    ball.images[i] = None
                if ball.pos.y < -ball.radius:
                    balls[b] = ball.images[i]
                    break
            if i==2:
                if ball.pos.z > ball.radius:
                    ball.images[i] = None
                if ball.pos.z < -ball.radius:
                    balls[b] = ball.images[i]
                    break
            if i==3:
                if ball.pos.x < L - ball.radius:
                    ball.images[i] = None
                if ball.pos.x > L + ball.radius:
                    balls[b] = ball.images[i]
                    break
            if i==4:
                if ball.pos.y < L - ball.radius:
                    ball.images[i] = None
                if ball.pos.y > L + ball.radius:
                    balls[b] = ball.images[i]
                    break
            if i==5:
                if ball.pos.z < L - ball.radius:
                    ball.images[i] = None
                if ball.pos.z > L + ball.radius:
                    balls[b] = ball.images[i]
                    break
        

def main():
    # pygame Initialization
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    
    # opengl Initialization
    gluPerspective(45, (display[0]/display[1]), 1, 50.0)
    glTranslatef(-0.5, -0.5, -5)
    glRotatef(-20, 0, 1, 0)

    # Initialize the balls
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # glRotatef(1, 0, 1, 0)

        # Computaion of Algorithm

        tc, particles1 = Calculate_tc(balls,N)
        tr, particles2 = Calculate_tr(balls,N,L)
        del_t = 0.01
        del_t = min(tc,0.03)
        for ball in balls:
            ball.update(del_t)
            ball.update_radius(del_t)
        if del_t == tc:
            vel_i,vel_j = collosion_balls(particles1)
            particles1[0].vel = vel_i
            particles1[1].vel = vel_j
        # if del_t == tr:
        #     generate_images(balls)
        generate_images(balls,L)
        collision_wall(balls)
        remove_images(balls)
        volume = N*(4/3)*3.14*balls[0].radius**3
        volume_frac = volume/(L**3)
        if volume_frac > final_volume_frac:
            print("Program ended")
            break

        # Visualization
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE )
        glClearColor(1, 1, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    
        for ball in balls:
            
            Sphere(ball)
            
        Cube()
        pygame.display.flip()
        
        pygame.time.wait(10)


main()