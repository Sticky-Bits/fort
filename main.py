from chunk import Chunk
from math import radians

import pyglet
import pyrr
from pyglet.gl import (GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST,
                       GL_FRONT_AND_BACK, GL_LINE, GL_TRIANGLES,
                       glBindVertexArray, glClear, glClearColor, glDrawArrays,
                       glEnable, glPolygonMode, glViewport)
from pyglet.window import Window

from camera import Camera
from shader import Shader

from pyglet.gl import *
import ctypes

# pyglet.options['shadow_window'] = False

# Specify config to get core opengl context
config = pyglet.gl.Config(
    double_buffer=True,
    # depth_size=24,
    major_version=3,
    minor_version=2,
    # forward_compatible=True,
)


class Window(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # glEnable(GL_DEPTH_TEST)
        self.shader = Shader('vs.glsl', 'fs.glsl')
        self.chunk = Chunk((0, 0, 0))
        self.camera = Camera()
        self.shader.use()
        self.shader.set_uniform("light.direction", pyrr.Vector3([-0.5, -1.0, -0.0]))
        self.shader.set_uniform("viewPos", self.camera.position)
        self.shader.set_uniform("light.ambient", pyrr.Vector3([0.2, 0.2, 0.2]))
        self.shader.set_uniform("light.diffuse", pyrr.Vector3([0.5, 0.5, 0.5]))
        self.shader.set_uniform("light.specular", pyrr.Vector3([1.0, 1.0, 1.0]))
        self.shader.set_uniform("material.shininess", 32.0)

    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass

    def on_draw(self):
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        self.projection = pyrr.matrix44.create_perspective_projection(radians(self.camera.zoom), self.width / self.height, 0.1, 1000.0)
        self.view = self.camera.get_view_matrix()
        self.shader.set_uniform("projection", self.projection)
        self.shader.set_uniform("view", self.view)

        # Draw!
        glBindVertexArray(self.chunk.vao)
        # Normally we'd translate before drawing a chunk
        model = pyrr.Matrix44()
        self.shader.set_uniform("model", model)
        glDrawArrays(GL_TRIANGLES, 0, len(self.chunk.vertices)//3)

        # swap buffers - may not be necessary with pyglet
        # self.flip()

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_resize(self, width, height):
        glViewport(0, 0, width, height)


window = Window(800, 600, "hey", config=config)

pyglet.app.run()
