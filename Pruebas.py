# Ray Tracer Engine
# Christian Perez 19710
# Graficas por Computador


from gl import Raytracer, V3
from obj import Obj, Texture, EnvMap, _color
from figures import AABB, REFLECTIVE, TRANSPARENT, PointLight, Sphere, Material, AmbientLight, DirectionalLight, Triangle2

width = 256
height = 256

rtx = Raytracer(width, height)

# MATERIALES

stone = Material(diffuse=(0.5451, 0.549, 0.4784), spec=64)
grass = Material(diffuse=(0.4, 1, 0), spec=128)
brick = Material(diffuse=(0.8, 0.25, 0.25), spec=32)
yellow = Material(diffuse=(1, 1, 0), spec=32)
brown = Material(diffuse=(0.588, 0.294, 0), spec=32)

glass = Material(spec=64, ior=1.5, matType=TRANSPARENT)

mirror = Material(spec=128, matType=REFLECTIVE)

gift1 = Material(texture=Texture('Assets/gift-texture1.bmp'))
redBall = Material(diffuse=(1, 0, 0), spec=64, matType=REFLECTIVE)

# LIGHT AND ENVIRONMENT MAP

rtx.envmap = EnvMap('Assets/envmap1.bmp')

rtx.ambLight = AmbientLight(strength=0.1)
rtx.dirLight = DirectionalLight(direction=V3(1, -1, -2), intensity=0.5)
rtx.pointLights.append(PointLight(position=V3(0, 2, 0), intensity=0.5))


rtx.scene.append(Sphere(V3(0, 0, -8), 1, redBall))
# rtx.scene.append(AABB(V3(2, 0, -6), V3(1, 1, 1), gift1))
# rtx.scene.append(Triangle2(V3(-2, 0, -7), V3(2, 0, -7), V3(0, 4, -7), stone))

# Renderizar escena final
rtx.glRender()
rtx.glFinish('Pruebas.bmp')
