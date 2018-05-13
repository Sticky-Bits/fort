import math

from pyglet.clock import get_fps, schedule_interval
from pyglet.gl import (GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST,
                       GL_MODELVIEW, GL_PROJECTION, GL_TRIANGLES,
                       glBindVertexArray, glClear, glClearColor, glColor3d,
                       glDisable, glDrawArrays, glEnable, glLoadIdentity,
                       glMatrixMode, glOrtho, glRotatef, glTranslatef,
                       gluPerspective, glViewport)
from pyglet.text import Label
from pyglet.window import Window, key

from world import World

TICKS_PER_SECOND = 60
MOVEMENT_SPEED = 15
MOUSE_SENSITIVITY = 0.1


class Window(Window):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.world = World()
        self.exclusive = False

        self.rotation = (0, 0)
        self.position = (0, 0, -10)
        self.movement_direction = [0, 0]
        schedule_interval(self.update, 1.0 / TICKS_PER_SECOND)

        self.label = Label(
            '', font_name='Arial', font_size=18,
            x=10, y=self.height - 10, anchor_x='left', anchor_y='top',
            color=(0, 0, 0, 255))

    def set_exclusive_mouse(self, exclusive):
        """ If `exclusive` is True, the game will capture the mouse, if False
        the game will ignore the mouse.

        """
        super(Window, self).set_exclusive_mouse(exclusive)
        self.exclusive = exclusive

    def get_sight_vector(self):
        x, y = self.rotation
        # y ranges from -90 to 90, or -pi/2 to pi/2, so m ranges from 0 to 1 and
        # is 1 when looking ahead parallel to the ground and 0 when looking
        # straight up or down.
        m = math.cos(math.radians(y))
        # dy ranges from -1 to 1 and is -1 when looking straight down and 1 when
        # looking straight up.
        dy = math.sin(math.radians(y))
        dx = math.cos(math.radians(x - 90)) * m
        dz = math.sin(math.radians(x - 90)) * m
        return (dx, dy, dz)

    def get_motion_vector(self):
        if any(self.movement_direction):
            x, y = self.rotation
            movement_direction = math.degrees(math.atan2(*self.movement_direction))
            y_angle = math.radians(y)
            x_angle = math.radians(x + movement_direction)
            m = math.cos(y_angle)
            dy = math.sin(y_angle)
            if self.movement_direction[1]:
                # Moving left or right.
                dy = 0.0
                m = 1
            if self.movement_direction[0] > 0:
                # Moving backwards.
                dy *= -1
            # When you are flying up or down, you have less left and right
            # motion.
            dx = math.cos(x_angle) * m
            dz = math.sin(x_angle) * m
        else:
            dy = 0.0
            dx = 0.0
            dz = 0.0
        return (dx, dy, dz)

    def update(self, dt):
        speed = MOVEMENT_SPEED
        d = dt * speed  # distance covered this tick.
        dx, dy, dz = self.get_motion_vector()
        dx, dy, dz = dx * d, dy * d, dz * d
        x, y, z = self.position
        x += dx
        y += dy
        z += dz
        self.position = (x, y, z)

    def on_mouse_press(self, x, y, button, modifiers):
        self.set_exclusive_mouse(True)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.exclusive:
            x, y = self.rotation
            x, y = x + dx * MOUSE_SENSITIVITY, y + dy * MOUSE_SENSITIVITY
            y = max(-90, min(90, y))
            self.rotation = (x, y)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.W:
            self.movement_direction[0] -= 1
        elif symbol == key.S:
            self.movement_direction[0] += 1
        elif symbol == key.A:
            self.movement_direction[1] -= 1
        elif symbol == key.D:
            self.movement_direction[1] += 1
        elif symbol == key.ESCAPE:
            self.set_exclusive_mouse(False)

    def on_key_release(self, symbol, modifiers):
        if symbol == key.W:
            self.movement_direction[0] += 1
        elif symbol == key.S:
            self.movement_direction[0] -= 1
        elif symbol == key.A:
            self.movement_direction[1] += 1
        elif symbol == key.D:
            self.movement_direction[1] -= 1

    def set_2d(self):
        width, height = self.get_size()
        glDisable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set_3d(self):
        width, height = self.get_size()
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(65.0, width / float(height), 0.1, 60.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        x, y = self.rotation
        glRotatef(x, 0, 1, 0)
        glRotatef(-y, math.cos(math.radians(x)), 0, math.sin(math.radians(x)))
        x, y, z = self.position
        glTranslatef(-x, -y, -z)

    def on_draw(self):
        #self.clear()
        #self.set_3d()
        # Draw world stuff
        #glColor3d(1, 1, 1)
        # self.world.batch.draw()
        glClearColor(0.5, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glBindVertexArray(self.world.chunk.vao)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        #self.set_2d()
        #self.draw_label()
        # Draw UI stuff

    def draw_label(self):
        """ Draw the label in the top left of the screen.

        """
        x, y, z = self.position
        pitch, yaw = self.rotation
        self.label.text = '%02d (%.2f, %.2f, %.2f) - %.2f %.2f' % (
            get_fps(), x, y, z, pitch, yaw)
        self.label.draw()
