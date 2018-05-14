from pyglet.gl import glUseProgram, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER
from OpenGL.GL.shaders import compileProgram, compileShader


class Shader:
    """
    Shader class. Call with a relative system path to vertex and fragment shader source files.
    The shader will load and compile. Call Shader.use() to use. (glUseProgram)
    """
    def __init__(self, vertex_path, fragment_path, geometry_path=None):
        with open(vertex_path) as f:
            self.vertex_shader_source = f.readlines()
        with open(fragment_path) as f:
            self.fragment_shader_source = f.readlines()
        if geometry_path:
            raise NotImplementedError
            # with open(geometry_path) as f:
            #     self.geometry_shader_source = f.readlines()

        self.shader = compileProgram(compileShader(self.vertex_shader_source, GL_VERTEX_SHADER),
                                     compileShader(self.fragment_shader_source, GL_FRAGMENT_SHADER))

    def use(self):
        glUseProgram(self.shader)

    # Utility uniform functions
    def set_bool(self):
        raise NotImplementedError

    def set_int(self):
        raise NotImplementedError

    def set_float(self):
        raise NotImplementedError

    def set_vec2(self):
        raise NotImplementedError

    def set_vec3(self):
        raise NotImplementedError

    def set_vec4(self):
        raise NotImplementedError

    def set_mat3(self):
        raise NotImplementedError

    def set_mat4(self):
        raise NotImplementedError
