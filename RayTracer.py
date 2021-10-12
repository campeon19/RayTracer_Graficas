# Ray Tracer Engine
# Christian Perez 19710
# Graficas por Computador


from gl import Raytracer, V3
from obj import Obj, Texture, EnvMap, _color
from figures import AABB, REFLECTIVE, TRANSPARENT, PointLight, Sphere, Material, AmbientLight, DirectionalLight, Triangle2

# width = 1920
# height = 1080

width = 128
height = 128


rtx = Raytracer(width, height)

# MATERIALES

stone = Material(diffuse=(0.5451, 0.549, 0.4784), spec=64)
grass = Material(diffuse=(0.4, 1, 0), spec=128)
brick = Material(diffuse=(0.8, 0.25, 0.25), spec=32)
yellow = Material(diffuse=(1, 1, 0), spec=32)
brown = Material(diffuse=(0.588, 0.294, 0), spec=32)

redBall = Material(diffuse=(1, 0, 0), spec=64, matType=REFLECTIVE)
greenBall = Material(diffuse=(0, 1, 0), spec=64, matType=REFLECTIVE)
blueBall = Material(diffuse=(0, 0, 1), spec=64, matType=REFLECTIVE)
# star = Material(diffuse=(1, 1, 0), spec=128, matType=REFLECTIVE)


glass = Material(spec=64, ior=1.5, matType=TRANSPARENT)

mirror = Material(spec=128, matType=REFLECTIVE)

gift1 = Material(texture=Texture('Assets/gift-texture1.bmp'))
gift2 = Material(texture=Texture('Assets/gift2.bmp'))
gift3 = Material(texture=Texture('Assets/gift3.bmp'))
gift4 = Material(texture=Texture('Assets/gift4.bmp'))
tree = Material(texture=Texture('Assets/tree3.bmp'))
tronco = Material(texture=Texture('Assets/tronco.bmp'))


# LIGHT AND ENVIRONMENT MAP

rtx.glClearColor(0.2, 0.6, 0.8)
rtx.glClear()
rtx.envmap = EnvMap('Assets/envmap3.bmp')

rtx.ambLight = AmbientLight(strength=0.1)
rtx.dirLight = DirectionalLight(direction=V3(1, -1, -2), intensity=0.5)
rtx.pointLights.append(PointLight(position=V3(0, 2, 0), intensity=0.5))
rtx.pointLights.append(PointLight(position=V3(-5, 2.5, 0), intensity=0.8))


# OBJECTS

# Regalos en el suelo
rtx.scene.append(AABB(V3(-1, -2.5, -6), V3(2, 1, 1), gift1))
rtx.scene.append(AABB(V3(1.5, -2.7, -6), V3(0.7, 0.7, 0.7), gift4))
rtx.scene.append(AABB(V3(4.5, -2.7, -6), V3(0.7, 0.7, 0.7), gift3))

# Regalos en la Repiza
rtx.scene.append(AABB(V3(-3, -1, -7), V3(6, 0.1, 0.5), brown))
rtx.scene.append(AABB(V3(-5, -0.55, -7), V3(1, 0.7, 0.2), gift1))
rtx.scene.append(AABB(V3(-3.5, -0.5, -7), V3(0.7, 1, 0.5), gift2))
rtx.scene.append(AABB(V3(-2.3, -0.3, -7), V3(0.7, 1.5, 0.5), gift3))
rtx.scene.append(AABB(V3(-1, -0.72, -7), V3(1, 0.4, 0.5), gift4))

# Arbol
rtx.scene.append(
    Triangle2(V3(1, -2.5, -7), V3(6, -2.5, -7), V3(3.5, 4, -7), tree))
rtx.scene.append(AABB(V3(3.5, -3, -7), V3(0.7, 1, 0.01), tronco))

# Adornos en el arbol
rtx.scene.append(Sphere(V3(3, -1.9, -6), 0.2, greenBall))
rtx.scene.append(Sphere(V3(4.4, -1.5, -6), 0.2, redBall))
rtx.scene.append(Sphere(V3(3, -1, -6), 0.2, blueBall))
rtx.scene.append(Sphere(V3(1.6, -1.7, -6), 0.2, blueBall))
rtx.scene.append(Sphere(V3(2.1, -0.7, -6), 0.2, redBall))
rtx.scene.append(Sphere(V3(3.9, -0.4, -6), 0.2, greenBall))
rtx.scene.append(Sphere(V3(2.9, 0, -6), 0.2, redBall))
rtx.scene.append(Sphere(V3(3.7, 0.5, -6), 0.2, blueBall))
rtx.scene.append(Sphere(V3(2.3, 1, -6), 0.2, greenBall))
rtx.scene.append(Sphere(V3(3.3, 1.3, -6), 0.2, redBall))
rtx.scene.append(Sphere(V3(3, 2, -6), 0.2, blueBall))
rtx.scene.append(Sphere(V3(2.1, 0.1, -6), 0.2, greenBall))

# Estrella
rtx.scene.append(
    Triangle2(V3(2.7, 3, -6), V3(3.3, 3, -6), V3(3, 3.5, -6), yellow))
rtx.scene.append(
    Triangle2(V3(2.7, 3.3, -6), V3(3, 2.8, -6),  V3(3.3, 3.3, -6), yellow))

# Esferas Reflectivas y Refractivas
rtx.scene.append(Sphere(V3(-3, 2, -5), 0.7, glass))
rtx.scene.append(Sphere(V3(-3.7, -2.1, -5), 0.5, mirror))

# Renderizar escena final
rtx.glRender()
rtx.glFinish('Pruebas.bmp')
