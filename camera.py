import pyrr
from math import sin, cos, radians
from enum import Enum

# Default camera properties
POSITION = pyrr.Vector3([0.0, 0.0, 10.0])
UP = pyrr.Vector3([0.0, 1.0, 0.0])
YAW = -90.0
PITCH = 0.0
FRONT = pyrr.Vector3([0.0, 0.0, -1.0])
CAMERA_SPEED = 25.0
INPUT_SENSITIVITY = 0.1
ZOOM = 45.0  # is this fov?
ZOOM_MAX = 90.0
ZOOM_MIN = 1

CAMERA_DIRECTIONS = Enum('directions', 'FORWARD BACKWARD LEFT RIGHT UP DOWN')


class Camera:
    def __init__(self, position=POSITION, up=UP, yaw=YAW, pitch=PITCH, front=FRONT, camera_speed=CAMERA_SPEED, input_sensitivity=INPUT_SENSITIVITY, zoom=ZOOM):
        self.position = position
        self.world_up = up
        self.yaw = yaw
        self.pitch = pitch
        self.front = front
        self.camera_speed = camera_speed
        self.input_sensitivity = input_sensitivity
        self.zoom = zoom

        self.update_camera_vectors()

    def update_camera_vectors(self):
        # Calculate new front vector
        front = pyrr.Vector3()
        front.x = cos(radians(self.yaw)) * cos(radians(self.pitch))
        front.y = sin(radians(self.pitch))
        front.z = sin(radians(self.yaw)) * cos(radians(self.pitch))
        self.front = pyrr.vector.normalise(front)
        # Also recalculate right and up vectors
        self.right = pyrr.vector.normalise(pyrr.vector3.cross(self.front, self.world_up))
        self.up = pyrr.vector.normalise(pyrr.vector3.cross(self.right, self.front))

    def move_camera(self, direction, amount):
        # Should we pass in amount or delta time?
        velocity = self.camera_speed * amount
        if direction == CAMERA_DIRECTIONS.FORWARD:
            self.position += self.front * velocity
        elif direction == CAMERA_DIRECTIONS.BACKWARD:
            self.position -= self.front * velocity
        elif direction == CAMERA_DIRECTIONS.LEFT:
            self.position -= self.right * velocity
        elif direction == CAMERA_DIRECTIONS.RIGHT:
            self.position += self.right * velocity
        elif direction == CAMERA_DIRECTIONS.UP:
            raise NotImplementedError
        elif direction == CAMERA_DIRECTIONS.DOWN:
            raise NotImplementedError

    def rotate_camera(self, x, y, constrain_pitch=True):
        # Process x,y input and rotate camera accordingly.
        x *= self.input_sensitivity
        y *= self.input_sensitivity

        self.yaw += x
        self.pitch += y

        if constrain_pitch:
            self.pitch = max(min(self.pitch, 90), 0)

        self.update_camera_vectors()

    def zoom_camera(self, y):
        self.zoom += y
        self.zoom = max(min(self.zoom, ZOOM_MAX), ZOOM_MIN)

    def get_view_matrix(self):
        return self._look_at(self.position, self.position + self.front, self.world_up)

    def _look_at(self, position, target, world_up):
        zaxis = pyrr.vector.normalise(position - target)
        xaxis = pyrr.vector.normalise(pyrr.vector3.cross(pyrr.vector.normalise(world_up), zaxis))
        # Might be able to do cross with ^ operator
        yaxis = pyrr.vector3.cross(zaxis, xaxis)

        translation = pyrr.Matrix44.identity()
        translation[3][0] = -position.x
        translation[3][1] = -position.y
        translation[3][2] = -position.z

        rotation = pyrr.Matrix44.identity()
        rotation[0][0] = xaxis[0]
        rotation[1][0] = xaxis[1]
        rotation[2][0] = xaxis[2]
        rotation[0][1] = yaxis[0]
        rotation[1][1] = yaxis[1]
        rotation[2][1] = yaxis[2]
        rotation[0][2] = zaxis[0]
        rotation[1][2] = zaxis[1]
        rotation[2][2] = zaxis[2]

        return rotation * translation
