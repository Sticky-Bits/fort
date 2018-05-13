from pyglet.app import run
from pyglet.gl import (GL_CULL_FACE, GL_DONT_CARE,
                       GL_FOG, GL_FOG_COLOR, GL_FOG_END, GL_FOG_HINT,
                       GL_FOG_MODE, GL_FOG_START, GL_LINEAR, GLfloat,
                       glClearColor, glEnable, glFogf, glFogfv, glFogi, glHint)

from window import Window


def setup_fog():
    glEnable(GL_FOG)
    glFogfv(GL_FOG_COLOR, (GLfloat * 4)(0.5, 0.69, 1.0, 1))
    glHint(GL_FOG_HINT, GL_DONT_CARE)
    glFogi(GL_FOG_MODE, GL_LINEAR)
    glFogf(GL_FOG_START, 20.0)
    glFogf(GL_FOG_END, 60.0)


def setup():
    glClearColor(0.5, 0.69, 1.0, 1)
    glEnable(GL_CULL_FACE)
    setup_fog()


def main():
    window = Window(width=800, height=600, caption='fort', resizable=True)
    window.set_exclusive_mouse(True)
    #setup()
    run()


if __name__ == '__main__':
    main()
