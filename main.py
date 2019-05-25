from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OBJLoader import *
from math import sin, cos, sqrt
import time
import random
import pygame


class GameState:
    currState = 1
    MAIN_MENU = 0
    PLAY = 1
    COLLISION = 2
    GAME_OVER = 3
    QUIT = 4
    collisionTime = 0

    @staticmethod
    def processState():
        if GameState.currState == GameState.QUIT:
            exit(0)
        if GameState.currState == GameState.GAME_OVER:
            BarrierGenerator.clean()
            BarrierGenerator.init()
            Score.clean()
            Ball.clean()
            GameState.currState = GameState.PLAY
        Lights.update()
        Sky.draw()
        Road.draw()
        Ball.update()
        BarrierGenerator.draw()
        Score.update()

class Lights:
    @staticmethod
    def update():

        # updating top light
        lightPos = [0, 20, Ball.ballZ - 30, 0]
        lightAmb = [abs(cos(Ball.ballZ / 100)) ** 2, abs(cos(45 + Ball.ballZ / 100)) ** 2, abs(sin(Ball.ballZ / 100)), 1]
        lightDiff = [abs(cos(Ball.ballZ / 100)), abs(cos(45 + Ball.ballZ / 100)), abs(sin(Ball.ballZ / 100)), 1]
        lightSpec = [abs(cos(Ball.ballZ / 100)), abs(cos(45 + Ball.ballZ / 100)), abs(sin(Ball.ballZ / 100)), 1]
        glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
        glLightfv(GL_LIGHT0, GL_AMBIENT, lightAmb)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, lightDiff)
        glLightfv(GL_LIGHT0, GL_SPECULAR, lightSpec)

        # updating lane lights
        lightPos = [Road.leftStripCenter, .01, Ball.ballZ - 3, 1]
        lightAmb = [Road.stripR, Road.stripG, Road.stripB, 1]
        lightDiff = [Road.stripR, Road.stripG, Road.stripB, 1]
        lightSpec = [Road.stripR, Road.stripG, Road.stripB, 1]
        glLightfv(GL_LIGHT1, GL_POSITION, lightPos)
        glLightfv(GL_LIGHT1, GL_AMBIENT, lightAmb)
        glLightfv(GL_LIGHT1, GL_DIFFUSE, lightDiff)
        glLightfv(GL_LIGHT1, GL_SPECULAR, lightSpec)
        lightPos = [Road.rightStripCenter, .01, Ball.ballZ - 3, 1]
        glLightfv(GL_LIGHT2, GL_POSITION, lightPos)
        glLightfv(GL_LIGHT2, GL_AMBIENT, lightAmb)
        glLightfv(GL_LIGHT2, GL_DIFFUSE, lightDiff)
        glLightfv(GL_LIGHT2, GL_SPECULAR, lightSpec)

    @staticmethod
    def adjust(i, j, k):
        glEnable(GL_LIGHT0) if i else glDisable(GL_LIGHT0)
        glEnable(GL_LIGHT1) if j else glDisable(GL_LIGHT1)
        glEnable(GL_LIGHT2) if k else glDisable(GL_LIGHT2)


class Score:
    currScore = 0
    highScore = 0
    @staticmethod
    def clean():
        Score.highScore = max(Score.highScore, Score.currScore)
        Score.currScore = 0

    @staticmethod
    def update():
        glDisable(GL_LIGHTING)
        glColor(1, 1, 1, .5)
        Score.drawText("Score: " + str(Score.currScore), 15, 670, .35)
        Score.drawText("High score: " + str(Score.highScore), 30, 645, .15, 2)
        if GameState.currState == GameState.COLLISION:
            if(Ball.scale == 0):
                glClearColor(0, 0, 0, 1)
                glClear(GL_COLOR_BUFFER_BIT)
                if Score.currScore > Score.highScore:
                    glColor3f(1, 0, 0)
                    Score.drawText("New High Score !", 300, Display.HEIGHT * 6 / 7, 0.6, 4)
                    glColor(1, 1, 1, .5)
                Score.drawText("Your Score : " + str(Score.currScore), 450 ,Display.HEIGHT * 3/4, 0.4, 2 )
                Score.drawText("Game Over", Display.WIDTH / 2 - 350, Display.HEIGHT / 2, 1, 8)
                glColor3f(0, 0.5, 0.7)
                Score.drawText("Press 'p' to play again", 500, Display.HEIGHT / 4, 0.15, 2)
            Road.stripR = 1
            Road.stripG = 0
            Road.stripB = 0
        glEnable(GL_LIGHTING)


    @staticmethod
    def drawText(string, xShift=0, yShift=0, scale=1, lineWidth=4):
        glLineWidth(lineWidth)
        Display.orthoProjection()
        glPushMatrix()
        glLoadIdentity()
        glTranslate(xShift, yShift, 0)
        glScale(scale, scale, 1)
        string = string.encode()
        for c in string:
            glutStrokeCharacter(GLUT_STROKE_ROMAN, c)
        glPopMatrix()
        Display.perProjection()

class Sky:
    width = height = 0
    centerX = 0
    centerY = 0
    length = 3500
    skyspeed = .3
    texture = None
    @staticmethod
    def init():
        Sky.texture = glGenTextures(1)
        imgLoad = pygame.image.load("Milkyway.JPG")
        imgRaw = pygame.image.tostring(imgLoad, "RGB", 1)
        Sky.width = imgLoad.get_width()
        Sky.height = imgLoad.get_height()
        glBindTexture(GL_TEXTURE_2D, Sky.texture)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, Sky.width, Sky.height, 0, GL_RGB, GL_UNSIGNED_BYTE, imgRaw)
        gluBuild2DMipmaps(GL_TEXTURE_2D, 3, Sky.width, Sky.height, GL_RGB, GL_UNSIGNED_BYTE, imgRaw)

    @staticmethod
    def draw():
        glDisable(GL_LIGHTING)
        glColor(1, 1, 1, 1)
        glBindTexture(GL_TEXTURE_2D, Sky.texture)
        glEnable(GL_TEXTURE_2D)
        glBegin(GL_QUADS)
        glTexCoord(Sky.centerX / Sky.width, Sky.centerY / Sky.height)
        glVertex(-500, -500, Ball.ballZ - 500)

        glTexCoord((Sky.centerX + Sky.length) / Sky.width, Sky.centerY / Sky.height)
        glVertex(500, -500, Ball.ballZ - 500)

        glTexCoord((Sky.centerX + Sky.length) / Sky.width, (Sky.centerY + Sky.length) / Sky.height)
        glVertex(500, 500, Ball.ballZ - 500)

        glTexCoord(Sky.centerX / Sky.width, (Sky.centerY + Sky.length) / Sky.height)
        glVertex(-500, 500, Ball.ballZ - 500)
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)
        Sky.centerX -= Sky.skyspeed
        glEnable(GL_LIGHTING)


class Ball:
    speed = .6
    ROT_SPEED = 8
    BALL_RADIUS = .98
    ballObj = None
    ballX = ballY = ballZ = 0
    ballRotX = ballRotZ = ballRotY = 0
    goRight = goLeft = goUp = False
    currX = 0
    maxHeight = 3.5
    v0 = sqrt(2 * 9.8 * maxHeight)
    jumpTime = 0
    ballDiff = [0.4, 0.4, 0.4, 1]
    ballSpec = [0.77, 0.77, 0.77, 1]
    ballShin = [5]
    scale = 1


    @staticmethod
    def init():
        Ball.ballObj = OBJ(b"ball.obj", swapyz=True)

    @staticmethod
    def clean():
        Ball.ballX = Ball.ballY = Ball.ballZ = 0
        Ball.ballRotX = Ball.ballRotZ = 0
        Ball.goRight = Ball.goLeft = Ball.goUp = False
        Ball.currX = 0
        Ball.scale = 1
        Ball.ballRotY = 0
        Ball.speed = 0.6

    @staticmethod
    def update():
        glPushMatrix()
        if GameState.currState == GameState.PLAY:
            if Ball.goRight:
                Ball.ballX += Ball.speed / 2
                Ball.ballRotZ -= Ball.ROT_SPEED
                if Ball.ballX >= Ball.currX:
                    Ball.goRight = False
                    Ball.ballX = Ball.currX
                    Ball.ballRotZ = 0
            if Ball.goLeft:
                Ball.ballX -= Ball.speed / 2
                Ball.ballRotZ += Ball.ROT_SPEED
                if Ball.ballX <= Ball.currX:
                    Ball.goLeft = False
                    Ball.ballX = Ball.currX
                    Ball.ballRotZ = 0
            if Ball.goUp:
                t = (time.time() - Ball.jumpTime) * 2.5
                Ball.ballY = Ball.v0 * t - .5 * 9.8 * (t ** 2)
                if Ball.ballY <= -0.00001:
                    Ball.ballY = 0
                    Ball.goUp = False

        glEnable(GL_COLOR_MATERIAL)
        Lights.adjust(1, 1, 1)
        glTranslate(Ball.ballX, Ball.ballY + Ball.BALL_RADIUS, Ball.ballZ)
        glRotate(Ball.ballRotX, 1, 0, 0)
        glRotate(Ball.ballRotZ, 0, 0, 1)
        glRotate(Ball.ballRotY, 0, 1, 0)
        glScale(Ball.scale, Ball.scale, Ball.scale)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, Ball.ballDiff)
        glMaterialfv(GL_FRONT, GL_SPECULAR, Ball.ballSpec)
        glMaterialfv(GL_FRONT, GL_SHININESS, Ball.ballShin)
        glCallList(Ball.ballObj.gl_list)
        glPopMatrix()
        glDisable(GL_COLOR_MATERIAL)
        if GameState.currState == GameState.PLAY:
            Ball.ballZ -= Ball.speed
            Ball.ballRotX -= Ball.ROT_SPEED
            Ball.speed = min(Ball.speed + 0.0001, 1)
        if GameState.currState == GameState.COLLISION:
            Ball.scale = max(0, Ball.scale - 0.02)
            Ball.ballRotY -= 10
            Ball.ballRotX = 0
            Ball.ballRotZ = 0


class Road:
    width = left = right = leftStripCenter = leftStripLeft = leftStripRight = \
    rightStripCenter = rightStripLeft = rightStripRight = stripR = stripG = stripB = 0
    laneColorDiff = [0.1, 0.1, 0.1, .88]
    laneColorSpec = [0.1, 0.1, 0.1, .8]
    laneColorShin = [5]

    @staticmethod
    def init(width, stripWidth):
        Road.width = width
        Road.left = -width / 2
        Road.right = width / 2
        Road.leftStripCenter = Road.left + width / 3
        Road.leftStripLeft = Road.leftStripCenter - stripWidth / 2
        Road.leftStripRight = Road.leftStripCenter + stripWidth / 2
        Road.rightStripCenter = Road.right - width / 3
        Road.rightStripLeft = Road.rightStripCenter - stripWidth / 2
        Road.rightStripRight = Road.rightStripCenter + stripWidth / 2
        Barrier.tracks = [-Road.width / 3, 0, Road.width / 3]

    @staticmethod
    def draw():
        Road.stripR = abs(sin(Ball.ballZ / 100))
        Road.stripG = abs(sin(45 + Ball.ballZ / 100))
        Road.stripB = abs(cos(Ball.ballZ / 100))

        glEnable(GL_COLOR_MATERIAL)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, Road.laneColorDiff)
        glMaterialfv(GL_FRONT, GL_SPECULAR, Road.laneColorSpec)
        glMaterialfv(GL_FRONT, GL_SHININESS, Road.laneColorShin)
        Lights.adjust(1, 1, 1)

        # lanes
        glColor(0, 0, 0, 1)

        # right lane
        glBegin(GL_POLYGON)
        glVertex(Road.right, 0, -1000 + Ball.ballZ)
        glVertex(Road.right, 0, 1000 + Ball.ballZ)
        glVertex(Road.rightStripRight, 0, 1000 + Ball.ballZ)
        glVertex(Road.rightStripRight, 0, -1000 + Ball.ballZ)
        glEnd()

        # mid lane
        glBegin(GL_POLYGON)
        glVertex(Road.rightStripLeft, 0, -1000 + Ball.ballZ)
        glVertex(Road.rightStripLeft, 0, 1000 + Ball.ballZ)
        glVertex(Road.leftStripRight, 0, 1000 + Ball.ballZ)
        glVertex(Road.leftStripRight, 0, -1000 + Ball.ballZ)
        glEnd()

        # left lane
        glBegin(GL_POLYGON)
        glVertex(Road.leftStripLeft, 0, -1000 + Ball.ballZ)
        glVertex(Road.leftStripLeft, 0, 1000 + Ball.ballZ)
        glVertex(Road.left, 0, 1000 + Ball.ballZ)
        glVertex(Road.left, 0, -1000 + Ball.ballZ)
        glEnd()


        # left strip line
        glColor(Road.stripR, Road.stripG, Road.stripB, .7)
        glBegin(GL_POLYGON)
        glVertex(Road.leftStripLeft, 0, -1000 + Ball.ballZ)
        glVertex(Road.leftStripLeft, 0, 1000 + Ball.ballZ)
        glVertex(Road.leftStripRight, 0, 1000 + Ball.ballZ)
        glVertex(Road.leftStripRight, 0, -1000 + Ball.ballZ)
        glEnd()

        # right strip line
        glBegin(GL_POLYGON)
        glVertex(Road.rightStripLeft, 0, -1000 + Ball.ballZ)
        glVertex(Road.rightStripLeft, 0, 1000 + Ball.ballZ)
        glVertex(Road.rightStripRight, 0, 1000 + Ball.ballZ)
        glVertex(Road.rightStripRight, 0, -1000 + Ball.ballZ)
        glEnd()
        glDisable(GL_COLOR_MATERIAL)


class BarrierGenerator:
    INIT_BARRIER_DENSITY = 40
    BARRIERS_RANGE = 450
    BARRIERS_START = 50
    MIN_DIST = 8
    barriers = []


    @staticmethod
    def init():
        barriersZ = []
        barriersZTaken=[]
        [barriersZ.append(random.randrange(BarrierGenerator.BARRIERS_START, BarrierGenerator.BARRIERS_START \
            + BarrierGenerator.BARRIERS_RANGE)) for i in range(0, BarrierGenerator.INIT_BARRIER_DENSITY)]
        barriersZ.sort()

        for i in range(len(barriersZ)):
            if len(barriersZTaken) > 0 and barriersZ[i] - barriersZTaken[-1] < BarrierGenerator.MIN_DIST:
                continue
            barriersZTaken.append(barriersZ[i])

        for i in range(len(barriersZTaken)):
            barrier = Barrier(-barriersZTaken[i])

            #prevents two successive barriers to be in the same track by generating a new Barrier object with a new randomly generated track value
            while len(BarrierGenerator.barriers) >= 1 and barrier.track == BarrierGenerator.barriers[-1].track:
                barrier = Barrier(-barriersZTaken[i])
            BarrierGenerator.barriers.append(barrier)


    @staticmethod
    def clean():
        BarrierGenerator.barriers.clear()

    @staticmethod
    def draw():
        Lights.adjust(1, 1, 1)
        glEnable(GL_COLOR_MATERIAL)
        [barrier.draw() for barrier in BarrierGenerator.barriers]
        glDisable(GL_COLOR_MATERIAL)


class Barrier:
    tracks = []
    OBS_HEIGHT = [2, 3.5]
    texture = None
    textureWidth = textureHeight = 0
    barrierDiff = [1, 1, 1, 0]
    barrierSpec = [1, 1, 1, 0]
    barrierShin = [0]
    y = 0

    def __init__(self, z):
        self.track = random.choice(Barrier.tracks)
        self.height = random.choice(Barrier.OBS_HEIGHT)
        self.z = z
        self.passedBallTime = -1
        self.barrierID = len(BarrierGenerator.barriers)

    def drawTexturedRect(self, coords):
        alpha = 1
        if self.passedBallTime > 0:
            alpha = max(1 - (time.time() - self.passedBallTime) * 2, 0)
        if GameState.currState == GameState.COLLISION:
            alpha = max(1 - (time.time() - GameState.collisionTime), 0)
        Barrier.barrierDiff[3] = alpha ** 3
        Barrier.barrierSpec[3] = alpha ** 3
        glMaterialfv(GL_FRONT, GL_DIFFUSE, Barrier.barrierDiff)
        glMaterialfv(GL_FRONT, GL_SPECULAR, Barrier.barrierSpec)
        glMaterialfv(GL_FRONT, GL_SHININESS, Barrier.barrierShin)
        glColor(1, 1, 1, alpha ** 3)
        glBindTexture(GL_TEXTURE_2D, Barrier.texture)
        glEnable(GL_TEXTURE_2D)
        glBegin(GL_QUADS)
        glTexCoord(0, 0)
        glVertex(coords[0][0], coords[0][1], coords[0][2])

        glTexCoord(1, 0)
        glVertex(coords[1][0], coords[1][1], coords[1][2])

        glTexCoord(1, 1)
        glVertex(coords[2][0], coords[2][1], coords[2][2])

        glTexCoord(0, 1)
        glVertex(coords[3][0], coords[3][1], coords[3][2])
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)

    def draw(self):
        glPushMatrix()
        glTranslate(self.track, self.y, self.z)

                    #coords[0] [0],[1],[2],
        self.drawTexturedRect([[-1, 0, 0], [1, 0, 0], [1, self.height, 0], [-1, self.height, 0]])      #front face rect
        self.drawTexturedRect([[1, 0, 0],  [1, self.height, 0], [1, self.height,  -2], [1, 0, -2]])     #right face rect
        self.drawTexturedRect([[-1, 0, 0], [-1, self.height, 0], [-1, self.height,  -2], [-1, 0, -2]]) #left face rect
        self.drawTexturedRect([[-1, self.height, 0], [1, self.height, 0], [1, self.height,  - 2], [-1, self.height, -2]])   #top face rect
        glPopMatrix()

        if self.collide():
            self.y -= 0.1
        if self.collide() and GameState.currState == GameState.PLAY:
            GameState.collisionTime = time.time()
            GameState.currState = GameState.COLLISION
        if Ball.ballZ + Ball.BALL_RADIUS < self.z and self.passedBallTime < 0:
            self.passedBallTime = time.time()
            Score.currScore += 1
        if self.z > Ball.ballZ + 30:
            self.z = Ball.ballZ - BarrierGenerator.BARRIERS_RANGE
            self.track = random.choice(Barrier.tracks)
            while self.track == BarrierGenerator.barriers[self.barrierID - 1].track:
                self.track = self.track = random.choice(Barrier.tracks)
            self.length = random.choice(Barrier.OBS_HEIGHT)
            self.passedBallTime = -1

    def collide(self):
        return self.segmentIntersect(Ball.ballX - Ball.BALL_RADIUS, Ball.ballX + Ball.BALL_RADIUS, self.track - 1, self.track + 1) \
            and self.segmentIntersect(Ball.ballY, Ball.ballY + Ball.BALL_RADIUS * 2, 0, self.height) \
            and self.segmentIntersect(Ball.ballZ - Ball.BALL_RADIUS, Ball.ballZ + Ball.BALL_RADIUS, self.z - 2, self.z)

    def segmentIntersect(self, l1, r1, l2, r2):
        return (l2 <= r1 and r2 >= l1) or (l1 <= r2 and r1 >= l2)

    @staticmethod
    def textureInit():
        Barrier.texture = glGenTextures(1)
        imgLoad = pygame.image.load("obs_texture.JPG")
        imgRaw = pygame.image.tostring(imgLoad, "RGBA", 1)
        Barrier.textureWidth = imgLoad.get_width()
        Barrier.textureHeight = imgLoad.get_height()
        glBindTexture(GL_TEXTURE_2D, Barrier.texture)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, Barrier.textureWidth, Barrier.textureHeight, 0, GL_RGBA, GL_UNSIGNED_BYTE, imgRaw)
        gluBuild2DMipmaps(GL_TEXTURE_2D, 4, Barrier.textureWidth, Barrier.textureHeight, GL_RGBA, GL_UNSIGNED_BYTE, imgRaw)

class Display:
    WIDTH = 1280
    HEIGHT = 720
    FPS = 60
    TITLE = b"Space Surfers"
    displayWinID = 0

    @staticmethod
    def init():
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowPosition(0, 0)
        glutInitWindowSize(Display.WIDTH, Display.HEIGHT)
        Display.displayWinID = glutCreateWindow(Display.TITLE)
        glColorMaterial(GL_FRONT, GL_AMBIENT)
        glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glutDisplayFunc(render)
        glutSpecialFunc(handleArrows)
        glutKeyboardFunc(handleKeyboard)
        Display.perProjection()
        Display.positionCamera()

    @staticmethod
    def perProjection():
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(35, Display.WIDTH / Display.HEIGHT, 1, 2500)
        glMatrixMode(GL_MODELVIEW)

    @staticmethod
    def orthoProjection():
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, Display.WIDTH, 0, Display.HEIGHT)
        glMatrixMode(GL_MODELVIEW)

    @staticmethod
    def positionCamera():
        glLoadIdentity()
        gluLookAt(0, 5.5, 15 + Ball.ballZ,
                  0, 0, Ball.ballZ - 5,
                  0, 1, 0)

def handleArrows(key, x, y):
    if GameState.currState == GameState.COLLISION:
        return
    if not Ball.goRight and not Ball.goLeft:
        if key == GLUT_KEY_LEFT and Ball.currX - Road.width / 3 > Road.left:
            Ball.currX -= Road.width / 3
            Ball.goLeft = True
        elif key == GLUT_KEY_RIGHT and Ball.currX + Road.width / 3 < Road.right:
            Ball.currX += Road.width / 3
            Ball.goRight = True
        if key == GLUT_KEY_UP and not Ball.goUp:
            Ball.jumpTime = time.time()
            Ball.goUp = True

def handleKeyboard(key, x, y):
    if key == b'q':
        GameState.currState = GameState.QUIT
    if key == b'p' and GameState.currState == GameState.COLLISION:
        GameState.currState = GameState.GAME_OVER


def render():
    print(Ball.ballRotZ)
    Display.positionCamera()
    glClearColor(1, 1, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    GameState.processState()
    glutSwapBuffers()

def timer(x):
    stTime = time.time()
    render()
    glutTimerFunc(max(int(1000 / Display.FPS - (time.time() - stTime) * 1000), 0), timer, 0)

def main():
    Display.init()
    Ball.init()
    Sky.init()
    Road.init(12, .5)
    BarrierGenerator.init()
    Barrier.textureInit()
    glutTimerFunc(0, timer, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()