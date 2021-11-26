import math
from OpenGL.GL import images
import numpy as np

class Vector3:
    '''
    3D Vector class for use in physics simulations
    '''
    def __init__(self, x, y, z):
        self.x = x                                 # x coordinate
        self.y = y                                 # y coordinate
        self.z = z                                 # z coordinate
    
    def add(self, other):                             
        # Add two vectors
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    def sub(self, other):
        # Subtract two vectors
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    def mul(self, other):
        # Multiply vector by a scalar
        return Vector3(self.x * other, self.y * other, self.z * other)
    def div(self, other):
        # Divide vector by a scalar
        return Vector3(self.x / other, self.y / other, self.z / other)
    def dot(self, other):
        # Dot product of two vectors
        return self.x * other.x + self.y * other.y + self.z * other.z
    def cross(self, other):
        # Cross product of two vectors
        return Vector3(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z, self.x * other.y - self.y * other.x)
    def mag(self):
        # Magnitude of the vector
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    def distance(self, other):
        # Distance between two vectors
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)
    def norm(self):
        # Normalize the vector
        return Vector3(self.x / self.mag(), self.y / self.mag(), self.z / self.mag())
    def __str__(self):
        # String representation of the vector
        return "Vector3({}, {}, {})".format(self.x, self.y, self.z)

class Ball:
    '''
    Class for a ball in a 3D environment
    '''
    def __init__(self, pos, vel, radius):
        self.pos = pos                                # Position of the ball
        self.vel = vel                                # Velocity of the ball
        self.radius = radius                          # Radius of the ball
        self.a = 0.01                                 # Rate of change of radius
        self.images = [None for i in range(6)]        # Images of the ball
    
    def __str__(self):
        '''
        String representation of the ball
        '''
        return "Ball({}, {}, {})".format(self.pos, self.vel, self.radius)

    def update(self, dt):
        '''
        Update the ball's position and velocity
        '''
        self.pos = self.pos.add(self.vel.mul(dt))
    
    def update_radius(self, dt):
        '''
        Update the ball's radius
        '''
        self.radius = self.radius + self.a * dt

def Calculate_tc(balls,N):
    '''
    Algorithm 4.2 
    '''
    tc = float('inf')
    particles = []
    for i in range(N):
        for j in range(i+1,N):
            ball_i = balls[i]
            ball_j = balls[j]
            if i == j:                             # If it is the same ball
                continue
            elif ball_i.pos.distance(ball_j.pos) <= ball_i.radius + ball_j.radius:
                # If the balls are colliding
                if ball_i.vel.sub(ball_j.vel).dot(ball_i.pos.sub(ball_j.pos)) > 0:
                    # If the balls are moving away from each other
                    continue
                # Update the velocities of the balls
                vel_i,vel_j =  collosion_balls((ball_i, ball_j))
                ball_i.vel = vel_i
                ball_j.vel = vel_j
            else:
                # If the balls are not colliding
                # Equation 4.2 and 4.4 from the pdf
                r = ball_i.pos.sub(ball_j.pos)
                v = ball_i.vel.sub(ball_j.vel)
                a = v.dot(v)-(ball_i.a+ball_j.a)**2
                b = r.dot(v) - (ball_i.a+ball_j.a)*(ball_i.radius+ball_j.radius)
                c = r.dot(r) - (ball_i.radius+ball_j.radius)**2
                # Calculate the time of collision
                if (b<=0 or a<0) and (b-a*c)>0:
                    temp_tc = (-b - math.sqrt(b**2 - a*c))/a
                    if temp_tc < tc:
                        tc = temp_tc
                        particles = [ball_i, ball_j]
    return tc, particles

def collosion_balls(particles):
    '''
    Updating the Velocitites of the balls after a collision
    '''
    del_r = particles[0].vel.sub(particles[1].vel)
    u = del_r.div(del_r.mag())
    # from Algorithm 4.4 in pdf, formulas to Calculate the new velocities of the balls
    vel_i_parllel = u.mul(u.dot(particles[0].vel))
    vel_j_parllel = u.mul(u.dot(particles[1].vel))
    vel_i_perp = particles[0].vel.sub(vel_i_parllel)
    vel_j_perp = particles[1].vel.sub(vel_j_parllel)
    vel_i_new = vel_i_perp.add(vel_j_parllel.add(u.mul(particles[0].a+particles[1].a)))
    vel_j_new = vel_j_perp.add(vel_i_parllel.add(u.mul(particles[1].a+particles[0].a)))
    return vel_i_new, vel_j_new

def Calculate_tr(balls,N,L):
    '''
    Algorithm 4.2 
    '''
    tr = float('inf')
    particles = []
    # ms and ind can be neglected as they are not used in the algorithm
    ms = [0 for i in range(N)]
    ind = -1
    for i in range(N):
        ball_i = balls[i]
        if ball_i.pos.x > ball_i.radius:                                 # If the ball is not in the left wall
            temp_tr = (ball_i.pos.x - ball_i.radius)/(ball_i.vel.x-ball_i.a)  # Calculate the time of collision
            if temp_tr < tr:                                           # If the time of collision is less than the current time of collision
                tr = temp_tr                                          # Update the time of collision
                particles = [ball_i]                                 # Update the particles
                ms[i] += 1 
                ind = i
        if ball_i.pos.y > ball_i.radius:                                # If the ball is not in the bottom wall
            temp_tr = (ball_i.pos.y - ball_i.radius)/(ball_i.vel.y-ball_i.a) # Calculate the time of collision
            if temp_tr < tr:                                          # If the time of collision is less than the current time of collision
                tr = temp_tr                                         # Update the time of collision
                particles = [ball_i]                                # Update the particles
                ms[i] += 1 
                ind = i
        if ball_i.pos.z > ball_i.radius:                               # If the ball is not in the back wall
            temp_tr = (ball_i.pos.z - ball_i.radius)/(ball_i.vel.z-ball_i.a) 
            if temp_tr < tr:                                         
                tr = temp_tr                                       
                particles = [ball_i] 
                ms[i] += 1
                ind = i
        if ball_i.pos.x < 1-ball_i.radius:                            # If the ball is not in the right wall
            temp_tr = (L-ball_i.pos.x - ball_i.radius)/(ball_i.vel.x+ball_i.a)
            if temp_tr < tr:
                tr = temp_tr
                particles = [ball_i]
                ms[i] += 1
                ind = i
        if ball_i.pos.y < 1-ball_i.radius:                            # If the ball is not in the top wall
            temp_tr = (L-ball_i.pos.y - ball_i.radius)/(ball_i.vel.y+ball_i.a)
            if temp_tr < tr:
                tr = temp_tr
                particles = [ball_i]
                ms[i] += 1
                ind = i
        if ball_i.pos.z < 1-ball_i.radius:                            # If the ball is not in the front wall
            temp_tr = (L-ball_i.pos.z - ball_i.radius)/(ball_i.vel.z+ball_i.a)
            if temp_tr < tr:
                tr = temp_tr
                particles = [ball_i]
                ms[i] += 1
                ind = i
        # if len(ball_i.images) == 0:
        #     generate_images([ball_i],L)
    return tr, particles

def generate_images(balls,L):
    m = 0
    '''
    For each ball generating necessary images
    '''
    for ball in balls:
        x = 0       # How much the ball's image has moved in the x direction
        y = 0       # How much the ball's image has moved in the y direction
        z = 0       # How much the ball's image has moved in the z direction
        # Calculating the how many images are needed from algorithm 4.5 in pdf
        if ball.pos.x < ball.radius:              # If the ball is in the left side of the box
            m += 1                                # Add one wall
            x = L                                 # Set the x position of the image to the right side of the box
        if ball.pos.y < ball.radius:             # If the ball is in the bottom side of the box
            m += 1
            y = L
        if ball.pos.z < ball.radius:            # If the ball is in the back side of the box
            m += 1
            z = L
        if ball.pos.x > L-ball.radius:         # If the ball is in the right side of the box
            m += 1
            x = -L
        if ball.pos.y > L-ball.radius:        # If the ball is in the top side of the box
            m += 1
            y = -L
        if ball.pos.z > L-ball.radius:       # If the ball is in the front side of the box
            m += 1
            z = -L
        if m == 1:
            # If only one image is needed
            img = Ball(ball.pos.add(Vector3(x,y,z)), ball.vel, ball.radius)
            ball.images.append(img)
        elif m == 2:
            # If 3 images are needed
            if x == 0:
                # if not touching the left and right wall
                img1 = Ball(ball.pos.add(Vector3(0,y,0)), ball.vel, ball.radius)        # down image
                img2 = Ball(ball.pos.add(Vector3(0,0,z)), ball.vel, ball.radius)        # back image
                img3 = Ball(ball.pos.add(Vector3(0,y,z)), ball.vel, ball.radius)        # back-down image
            elif y == 0:
                # if not touching the top and bottom wall
                img1 = Ball(ball.pos.add(Vector3(x,0,0)), ball.vel, ball.radius)       # right image
                img2 = Ball(ball.pos.add(Vector3(x,0,z)), ball.vel, ball.radius)       # right-back image
                img3 = Ball(ball.pos.add(Vector3(0,0,z)), ball.vel, ball.radius)       # back image
            elif z == 0:
                # if not touching the front and back wall
                img1 = Ball(ball.pos.add(Vector3(x,y,0)), ball.vel, ball.radius)     # right-down image
                img2 = Ball(ball.pos.add(Vector3(0,y,0)), ball.vel, ball.radius)     # down image
                img3 = Ball(ball.pos.add(Vector3(x,0,0)), ball.vel, ball.radius)     # right image
            ball.images.append(img1)
            ball.images.append(img2)
            ball.images.append(img3)
        elif m == 3:
            # If 8 images are needed
            # Each corner has a ball' image total of 8 balls.
            img1 = Ball(ball.pos.add(Vector3(x,y,0)), ball.vel, ball.radius)
            img2 = Ball(ball.pos.add(Vector3(0,y,0)), ball.vel, ball.radius)
            img3 = Ball(ball.pos.add(Vector3(x,0,0)), ball.vel, ball.radius)
            img4 = Ball(ball.pos.add(Vector3(0,0,z)), ball.vel, ball.radius)
            img5 = Ball(ball.pos.add(Vector3(x,0,z)), ball.vel, ball.radius)
            img6 = Ball(ball.pos.add(Vector3(0,y,z)), ball.vel, ball.radius)
            img7 = Ball(ball.pos.add(Vector3(x,y,z)), ball.vel, ball.radius)
            ball.images.append(img1)
            ball.images.append(img2)
            ball.images.append(img3)
            ball.images.append(img4)
            ball.images.append(img5)
            ball.images.append(img6)
            ball.images.append(img7)


def collision_wall(balls,L=1):
    '''
    Updating Velocities of balls
    '''
    for ball in balls:
        if ball.pos.x < 0:                                  # If it goes beyond left wall
            ball.pos.x += L                                 # move to right wall

        if ball.pos.y < 0:                                  # If it goes beyond bottom wall
            ball.pos.y += L                                 # move to top wall

        if ball.pos.z < 0:                                 # If it goes beyond back wall
            ball.pos.z += L                                   # move to front wall

        if ball.pos.x > L:                                 # If it goes beyond right wall
            ball.pos.x -= L                                # move to left wall

        if ball.pos.y > L:                                # If it goes beyond top wall
            ball.pos.y -= L                               # move to bottom wall

        if ball.pos.z > L:                               # If it goes beyond front wall
            ball.pos.z -= L                              # move to back wall
        
    return

def hard_collision(balls,L):
    """
    Updating Velocities of balls
    """
    for ball in balls:
        if ball.pos.x > L - ball.radius:                 #right wall
            ball.pos.x = L - ball.radius                 
            ball.vel.x = -ball.vel.x                     #reflecting
        if ball.pos.x < ball.radius:                      #left wall
            ball.pos.x = ball.radius
            ball.vel.x = -ball.vel.x                     #reflecting
        if ball.pos.y > L - ball.radius:                  #top wall
            ball.pos.y = L - ball.radius
            ball.vel.y = -ball.vel.y                       #reflecting
        if ball.pos.y < ball.radius:                      #bottom wall
            ball.pos.y = ball.radius
            ball.vel.y = -ball.vel.y                       #reflecting
        if ball.pos.z > L - ball.radius:                   #back wall
            ball.pos.z = L - ball.radius
            ball.vel.z = -ball.vel.z                      #reflecting
        if ball.pos.z < ball.radius:                      #front wall
            ball.pos.z = ball.radius
            ball.vel.z = -ball.vel.z
    return

# Vertices of the Cube
verticies = (
    (1, 0, 0),
    (1, 1, 0),
    (0, 1, 0),
    (0, 0, 0),
    (1, 0, 1),
    (1, 1, 1),
    (0, 0, 1),
    (0, 1, 1)
    )

# Edges of the Cube
edges = (
    (0,1),                            # Here (0,1) is the edge between vertices 0 and 1 from above list
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )