import pyglet
from pyglet.gl import *
from shader import Shader
import ctypes

class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shader = Shader('vs.glsl', 'fs.glsl')
        self.vertices = (GLfloat * 9)(*[
            -0.5, -0.5, 0.0,
            0.5, -0.5, 0.0,
            0.0, 0.5, 0.0,
        ])

        self.VBO = GLuint()
        self.VAO = GLuint()
        glGenVertexArrays(1, self.VAO)
        glGenBuffers(1, self.VBO)
        glBindVertexArray(self.VAO)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, ctypes.sizeof(self.vertices), self.vertices, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * ctypes.sizeof(ctypes.c_float), None)
        glEnableVertexAttribArray(0)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
    
    def on_draw(self):
        #self.clear()
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        self.shader.use()
        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        
        #self.flip()
    
    def on_resize(self, width, height):
        glViewport(0, 0, width, height)

config = pyglet.gl.Config(double_buffer=True,
                          #depth_size=24,
                          major_version=3,
                          minor_version=2,
                          #forward_compatible=True,
)
window = Window(config=config)
pyglet.app.run()