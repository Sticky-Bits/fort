from ctypes import sizeof

from pyglet.gl import (GL_ARRAY_BUFFER, GL_FALSE, GL_FLOAT, GL_STATIC_DRAW,
                       GLfloat, GLuint, glBindBuffer, glBindVertexArray,
                       glBufferData, glEnableVertexAttribArray, glGenBuffers,
                       glGenVertexArrays, glVertexAttribPointer)

CHUNK_SIZE = 16


class Chunk:
    def __init__(self, position):
        self.verticies = []
        self.voxels = {}
        self.chunk_position = position
        self.world_position = tuple([x * CHUNK_SIZE for x in position])
        self.vbo = GLuint()
        self.vao = GLuint()
        self.gen_voxels()
        self.gen_vertices()

    def gen_voxels(self):
        for x in range(CHUNK_SIZE):
            for y in range(CHUNK_SIZE):
                for z in range(CHUNK_SIZE):
                    if y < 2:
                        self.voxels[(x, y, z)] = True
                    else:
                        self.voxels[(x, y, z)] = False

    def gen_vertices(self):
        # Just make a cube for now
        self.vertices = (GLfloat * 9)(*[
            -0.5, -0.5, 0.0,
            0.5, -0.5, 0.0,
            0.0, 0.5, 0.0,
        ])
        glGenVertexArrays(1, self.vao)
        glGenBuffers(1, self.vbo)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, sizeof(self.vertices), self.vertices, GL_STATIC_DRAW)

        glBindVertexArray(self.vao)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat), 0)
        glEnableVertexAttribArray(0)

    def delete_buffers(self):
        raise NotImplementedError
