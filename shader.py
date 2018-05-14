from pyglet.gl import (GL_FALSE, GL_FRAGMENT_SHADER, GL_VERTEX_SHADER,
                       glAttachShader, glCompileShader, glCreateProgram,
                       glCreateShader, glDeleteShader, glGetUniformLocation,
                       glLinkProgram, glShaderSource, glUniform1f, glUniform1i,
                       glUniform3fv, glUniform4fv, glUniformMatrix3fv,
                       glUniformMatrix4fv, glUseProgram)
from pyrr.objects import Matrix33, Matrix44, Vector3, Vector4
from ctypes import c_float

from OpenGL.GL.shaders import compileProgram, compileShader

# Define types as constants in case we need to change libraries later
VECTOR3_TYPE = Vector3
VECTOR4_TYPE = Vector4
MATRIX3_TYPE = Matrix33
MATRIX4_TYPE = Matrix44


class Shader:
    """
    Shader class. Call with a relative system path to vertex and fragment shader source files.
    The shader will load and compile. Call Shader.use() to use. (glUseProgram)
    """
    def __init__(self, vertex_path, fragment_path, geometry_path=None):
        with open(vertex_path) as f:
            self.vertex_shader_source = f.readlines()
        with open(fragment_path) as f:
            self.fragment_shader_source = "".join(f.readlines())
        if geometry_path:
            raise NotImplementedError
            # with open(geometry_path) as f:
            #     self.geometry_shader_source = f.readlines()
        # use pyopengl shortcuts for now, not sure if I need to do this manually
        self.shader = compileProgram(compileShader(self.vertex_shader_source, GL_VERTEX_SHADER),
                                     compileShader(self.fragment_shader_source, GL_FRAGMENT_SHADER))

    def use(self):
        glUseProgram(self.shader)

    # Utility uniform functions
    def set_uniform(self, name, value):
        name = name.encode()
        valtype = type(value)
        if valtype == bool or valtype == int:
            glUniform1i(glGetUniformLocation(self.shader, name), int(value))
        elif valtype == float:
            glUniform1f(glGetUniformLocation(self.shader, name), value)
        # elif valtype == VECTOR2_TYPE:
        #     glUniform2fv(glGetUniformLocation(self.shader, name), 1, value)
        elif valtype == VECTOR3_TYPE:
            glUniform3fv(glGetUniformLocation(self.shader, name), 1, c_float(value[0]), c_float(value[1]), c_float(value[2]))
        elif valtype == VECTOR4_TYPE:
            glUniform4fv(glGetUniformLocation(self.shader, name), 1, c_float(value[0]), c_float(value[1]), c_float(value[2]), c_float(value[3]))
        elif valtype == MATRIX3_TYPE:
            glUniformMatrix3fv(glGetUniformLocation(self.shader, name), 1, GL_FALSE, c_float(value[0][0]))  # Should this be value[0][0]?
        elif valtype == MATRIX4_TYPE:
            glUniformMatrix4fv(glGetUniformLocation(self.shader, name), 1, GL_FALSE, c_float(value[0][0]))  # Should this be value[0][0]?

    def check_compile_errors(self):
        pass
