# Christian Daniel Perez De Leon 19710

from numpy.core.numeric import cross
from gl import V3
import matematica as mate
from numpy import arctan2, arccos

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2

WHITE = (1, 1, 1)


class DirectionalLight(object):
    def __init__(self, direction=V3(0, -1, 0), intensity=1, color=WHITE):
        self.direction = mate.normalizar3D(direction)
        self.intensity = intensity
        self.color = color


class AmbientLight(object):
    def __init__(self, strength=0, color=WHITE):
        self.strength = strength
        self.color = color

    def getColor(self):
        return (self.strength * self.color[0] / 255,
                self.strength * self.color[1] / 255,
                self.strength * self.color[2] / 255)


class PointLight(object):
    # Luz con punto de origen que va en todas direcciones
    def __init__(self, position=V3(0, 0, 0), intensity=1, color=WHITE):
        self.position = position
        self.intensity = intensity
        self.color = color


class Material(object):
    def __init__(self, diffuse=WHITE, spec=1, ior=1, texture=None, matType=OPAQUE):
        self.diffuse = diffuse
        self.spec = spec
        self.matType = matType
        self.ior = ior
        self.texture = texture


class Intersect(object):
    def __init__(self, distance, point, normal, texCoords, sceneObject):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.sceneObject = sceneObject
        self.texCoords = texCoords


class Sphere(object):
    def __init__(self, center, radius, material=Material()):
        self.center = center
        self.radius = radius
        self.material = material

    def ray_intersect(self, orig, dir):

        L = mate.restaVect(self.center, orig)
        l = mate.normalizar3D(L)

        tca = mate.productoPunto(L, dir)

        d = (mate.productoPunto(L, L) - tca**2)
        if d > self.radius ** 2:
            return None

        thc = (self.radius**2 - d) ** 0.5
        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1

        if t0 < 0:
            return None

        # P = O + t * D
        hit = mate.sumaVec(orig, mate.multVectorxEscalar(dir, t0))
        normal = mate.restaVect(hit, self.center)
        normal = mate.normalizar3D(normal)

        u = 1 - ((arctan2(normal[2], normal[0]) / (2 * mate.pi)) + 0.5)
        v = arccos(-normal[1]) / mate.pi

        uvs = (u, v)

        return Intersect(distance=t0,
                         point=hit,
                         normal=normal,
                         texCoords=uvs,
                         sceneObject=self)


class Plane(object):
    def __init__(self, position, normal, material=Material()):
        self.position = position
        self.normal = normal
        self.material = material

    def ray_intersect(self, orig, dir):
        denom = mate.productoPunto(dir, self.normal)

        if abs(denom) > 0.0001:
            num = mate.productoPunto(mate.restaVect(
                self.position, orig), self.normal)
            t = num / denom
            if t > 0:
                hit = mate.sumaVec(orig, mate.multVectorxEscalar(dir, t))

                return Intersect(distance=t,
                                 point=hit,
                                 normal=self.normal,
                                 texCoords=None,
                                 sceneObject=self)

        return None


class AABB(object):

    def __init__(self, position, size, material=Material()):
        self.position = position
        self.size = size
        self.material = material
        self.planes = []

        self.boundsMin = [0, 0, 0]
        self.boundsMax = [0, 0, 0]

        halfSizeX = size[0] / 2
        halfSizeY = size[1] / 2
        halfSizeZ = size[2] / 2

        # Sides
        self.planes.append(
            Plane(mate.sumaVec(position, V3(halfSizeX, 0, 0)), V3(1, 0, 0), material))
        self.planes.append(
            Plane(mate.sumaVec(position, V3(-halfSizeX, 0, 0)), V3(-1, 0, 0), material))

        # Up and down
        self.planes.append(
            Plane(mate.sumaVec(position, V3(0, halfSizeY, 0)), V3(0, 1, 0), material))
        self.planes.append(
            Plane(mate.sumaVec(position, V3(0, -halfSizeY, 0)), V3(0, -1, 0), material))

        # Front and Back
        self.planes.append(
            Plane(mate.sumaVec(position, V3(0, 0, halfSizeZ)), V3(0, 0, 1), material))
        self.planes.append(
            Plane(mate.sumaVec(position, V3(0, 0, -halfSizeZ)), V3(0, 0, -1), material))

        # Bounds
        epsilon = 0.001
        for i in range(3):
            self.boundsMin[i] = self.position[i] - (epsilon + self.size[i]/2)
            self.boundsMax[i] = self.position[i] + (epsilon + self.size[i]/2)

    def ray_intersect(self, orig, dir):
        intersect = None
        t = float('inf')

        uvs = None

        for plane in self.planes:
            planeInter = plane.ray_intersect(orig, dir)
            if planeInter is not None:
                if planeInter.point[0] >= self.boundsMin[0] and planeInter.point[0] <= self.boundsMax[0]:
                    if planeInter.point[1] >= self.boundsMin[1] and planeInter.point[1] <= self.boundsMax[1]:
                        if planeInter.point[2] >= self.boundsMin[2] and planeInter.point[2] <= self.boundsMax[2]:
                            if planeInter.distance < t:
                                t = planeInter.distance
                                intersect = planeInter

                                u, v = 0, 0

                                if abs(plane.normal[0]) > 0:
                                    u = (
                                        planeInter.point[1] - self.boundsMin[1]) / (self.boundsMax[1] - self.boundsMin[1])
                                    v = (
                                        planeInter.point[2] - self.boundsMin[2]) / (self.boundsMax[2] - self.boundsMin[2])

                                elif abs(plane.normal[1]) > 0:
                                    u = (
                                        planeInter.point[0] - self.boundsMin[0]) / (self.boundsMax[0] - self.boundsMin[0])
                                    v = (
                                        planeInter.point[2] - self.boundsMin[2]) / (self.boundsMax[2] - self.boundsMin[2])

                                elif abs(plane.normal[2]) > 0:
                                    u = (
                                        planeInter.point[0] - self.boundsMin[0]) / (self.boundsMax[0] - self.boundsMin[0])
                                    v = (
                                        planeInter.point[1] - self.boundsMin[1]) / (self.boundsMax[1] - self.boundsMin[1])

                                uvs = (u, v)

        if intersect is None:
            return None

        return Intersect(distance=intersect.distance,
                         point=intersect.point,
                         normal=intersect.normal,
                         texCoords=uvs,
                         sceneObject=self)


# class Triangle(object):
#     def __init__(self, center, size, material=Material()):
#         self.size = size
#         self.material = material
#         center2 = [center[0], center[1] * -1, center[2]]
#         self.center = center2

#         self.boundsMin = [0, 0, 0]
#         self.boundsMax = [0, 0, 0]

#         d = size/2

#         self.v0 = [self.center[0], self.center[1] + d, self.center[2]]
#         self.v1 = [self.center[0] - d, self.center[1] - d, self.center[2]]
#         self.v2 = [self.center[0] + d, self.center[1] - d, self.center[2]]

#         epsilon = 0.001
#         for i in range(3):
#             self.boundsMin[i] = self.center[i] - (epsilon + d)
#             self.boundsMax[i] = self.center[i] + (epsilon + d)

#     def ray_intersect(self, orig, dir):

#         A = mate.restaVect(self.v1, self.v0)
#         B = mate.restaVect(self.v2, self.v0)
#         N = mate.productoCruz3D(A, B)

#         N = mate.normalizar3D(N)

#         NdotRayDirection = mate.productoPunto(N, dir)

#         if(abs(NdotRayDirection) < 0.001):
#             return None

#         D = mate.productoPunto(N, self.v0)

#         t = (mate.productoPunto(N, orig) + D) / NdotRayDirection

#         if t < 0:
#             return None

#         # P = mate.sumaVec(orig, mate.multVect(t, dir))
#         P = mate.multVect(mate.sumaVec(orig, t), dir)

#         edge0 = mate.restaVect(self.v1, self.v0)
#         edge1 = mate.restaVect(self.v2, self.v1)
#         edge2 = mate.restaVect(self.v0, self.v2)

#         c0 = mate.restaVect(P, self.v0)
#         c1 = mate.restaVect(P, self.v1)
#         c2 = mate.restaVect(P, self.v2)

#         cross0 = mate.productoCruz3D(edge0, c0)
#         cross1 = mate.productoCruz3D(edge1, c1)
#         cross2 = mate.productoCruz3D(edge2, c2)

#         if (mate.productoPunto(N, cross0)) < 0:
#             return None

#         if (mate.productoPunto(N, cross1)) < 0:
#             return None

#         if (mate.productoPunto(N, cross2)) < 0:
#             return None

#         hit = mate.sumaVec(orig, mate.multVect(dir, t))

#         return Intersect(distance=t,
#                          point=hit,
#                          normal=N,
#                          texCoords=None,
#                          sceneObject=self)


class Triangle2(object):
    def __init__(self, v0, v1, v2, material=Material()):
        self.material = material
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2

    def ray_intersect(self, orig, dir):

        A = mate.restaVect(self.v1, self.v0)
        B = mate.restaVect(self.v2, self.v0)
        N = mate.productoCruz3D(A, B)

        denom = mate.productoPunto(N, N)

        NdotRayDirection = mate.productoPunto(N, dir)

        if(abs(NdotRayDirection) < 0.001):
            return None

        d = mate.productoPunto(N, self.v0)

        t = (mate.productoPunto(N, orig) + d) / NdotRayDirection

        if t < 0:
            return None

        # P = mate.sumaVec(orig, mate.multVect(t, dir))
        P = mate.multVect(mate.sumVectorxEscalar(orig, t), dir)

        edge0 = mate.restaVect(self.v1, self.v0)
        edge1 = mate.restaVect(self.v2, self.v1)
        edge2 = mate.restaVect(self.v0, self.v2)

        c0 = mate.restaVect(P, self.v0)
        c1 = mate.restaVect(P, self.v1)
        c2 = mate.restaVect(P, self.v2)

        cross0 = mate.productoCruz3D(edge0, c0)
        cross1 = mate.productoCruz3D(edge1, c1)
        cross2 = mate.productoCruz3D(edge2, c2)

        u = mate.productoPunto(N, cross1) / denom
        v = mate.productoPunto(N, cross2) / denom

        if (mate.productoPunto(N, cross0)) < 0:
            return None

        if (mate.productoPunto(N, cross1)) < 0:
            return None

        if (mate.productoPunto(N, cross2)) < 0:
            return None

        hit = mate.sumaVec(orig, mate.multVectorxEscalar(dir, t))

        uvs = (u, v)

        N = mate.normalizar3D(N)

        return Intersect(distance=t,
                         point=hit,
                         normal=N,
                         texCoords=uvs,
                         sceneObject=self)
