import pyglet
from pyglet.gl import *
from shader import Shader
from ctypes import sizeof

window = pyglet.window.Window(800, 600, "OpenGL")

# stuff

shader = Shader('vert.glsl', 'frag.glsl')

vertices = (GLfloat*9)(*[
    -0.5, -0.5, 0.0,
    0.5, -0.5, 0.0,
    0.0, 0.5, 0.0,
])

vao = GLuint()
vbo = GLuint()
glGenVertexArrays(1, vao)
glGenBuffers(1, vbo)
glBindVertexArray(vao)

glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW)

glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat), 0)
glEnableVertexAttribArray(0)

glBindBuffer(GL_ARRAY_BUFFER, 0)

glBindVertexArray(0)

@window.event
def on_draw():
    glClearColor(0.2, 0.3, 0.3, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    shader.use()
    glBindVertexArray(vao)
    glDrawArrays(GL_TRIANGLES, 0, 3)


@window.event
def on_key_press(symbol, modifiers):
    pass


@window.event
def on_key_release(symbol, modifiers):
    print(symbol)


def update(dt):
    pass


pyglet.clock.schedule(update)

pyglet.app.run()
