# from pyglet.gl import GL_QUADS
# from pyglet.graphics import Batch
from chunk import Chunk


def cube_vertices(x, y, z, n):
    """ Return the vertices of the cube at position x, y, z with size 2*n.

    """
    return [
        x - n, y + n, z - n, x - n, y + n, z + n, x + n, y + n, z + n, x + n, y + n, z - n,  # top
        x - n, y - n, z - n, x + n, y - n, z - n, x + n, y - n, z + n, x - n, y - n, z + n,  # bottom
        x - n, y - n, z - n, x - n, y - n, z + n, x - n, y + n, z + n, x - n, y + n, z - n,  # left
        x + n, y - n, z + n, x + n, y - n, z - n, x + n, y + n, z - n, x + n, y + n, z + n,  # right
        x - n, y - n, z + n, x + n, y - n, z + n, x + n, y + n, z + n, x - n, y + n, z + n,  # front
        x + n, y - n, z - n, x - n, y - n, z - n, x - n, y + n, z - n, x + n, y + n, z - n,  # back
    ]


class World:
    def __init__(self):
        # # Build a map. A map is a collection of all loaded blocks.
        # self.map = {}
        # # Might be able to do this with dict comp?
        # for x in range(10):
        #     for y in range(10):
        #         for z in range(10):
        #             self.map[(x, y, z)] = self.gen_world_block((x, y, z))

        # self.batch = Batch()
        # vertex_data = cube_vertices(0, 0, 0, 0.5)
        # self.batch.add(24, GL_QUADS, None,
        #                ('v3f/static', vertex_data))
        self.chunk = Chunk((0, 0, 0))
        print("chunk made")

    def gen_world_block(self, world_coords):
        """
        Given (x,y,z) world coordinates, generates the block at that position.
        """
        # Simple height function for now
        # Assumes unchanging world. will have to make this read from save later
        x, y, z = world_coords
        return y < 2

    def get_world_block(self, world_coords):
        """
        Given (x,y,z) world coordinates, gets the block at that position from the map.
        Let's us abstract away from block storage method.
        """
        return self.map[world_coords]
