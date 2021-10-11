# Ray Tracer Engine
# Christian Perez 19710
# Graficas por Computador


from gl import Raytracer, V3
from obj import Obj, Texture, EnvMap, _color
from figures import AABB, REFLECTIVE, TRANSPARENT, PointLight, Sphere, Material, AmbientLight, DirectionalLight, Triangle, Triangle2

# width = 1080
# height = 540

width = 256
height = 156

# width = 300
# height = 512

# width = 600
# height = 1024

# width = 1000
# height = 1424

rtx = Raytracer(width, height)


# nieve = Material( diffuse = _color(0.9372,0.882,0.78))
# white = Material( diffuse = _color(1,1,1))
# black = Material( diffuse = _color(0,0,0))
carrot = Material(diffuse=(0.93, 0.57, 0.13))
stone = Material(diffuse=(0.5451, 0.549, 0.4784), spec=64)
# rojo = Material( diffuse = _color(1,0,0))
grass = Material(diffuse=(0.4, 1, 0), spec=128)
brick = Material(diffuse=(0.8, 0.25, 0.25), spec=32)


glass = Material(spec=64, ior=1.5, matType=TRANSPARENT)
glass2 = Material(spec=64, ior=1.8, matType=TRANSPARENT)

mirror = Material(spec=128, matType=REFLECTIVE)
mirror2 = Material(diffuse=(0, 0, 1), spec=64, matType=REFLECTIVE)

gift1 = Material(texture=Texture('Assets/gift-texture1.bmp'))


# rtx.scene.append( Sphere(V3(0,-3,-10), 2.3, nieve) )
# rtx.scene.append( Sphere(V3(0,0.8,-11), 2, nieve) )
# rtx.scene.append( Sphere(V3(0,3.7,-10), 1.4, nieve) )
# rtx.scene.append( Sphere(V3(0,-2.5,-8), 0.5, black) )
# rtx.scene.append( Sphere(V3(0,-0.7,-8), 0.35, black) )
# rtx.scene.append( Sphere(V3(0,1,-8), 0.3, black) )
# rtx.scene.append( Sphere(V3(0,3,-8), 0.3, carrot) )
# rtx.scene.append( Sphere(V3(0.3,3.5,-8), 0.15, white) )
# rtx.scene.append( Sphere(V3(-0.3,3.5,-8), 0.15, white) )
# rtx.scene.append( Sphere(V3(0.27,3.1,-7), 0.06, black) )
# rtx.scene.append( Sphere(V3(-0.27,3.1,-7), 0.06, black) )
# rtx.scene.append( Sphere(V3(0.2,2.35,-8), 0.1, stone) )
# rtx.scene.append( Sphere(V3(-0.2,2.35,-8), 0.1, stone) )
# rtx.scene.append( Sphere(V3(-0.5,2.55,-8), 0.1, stone) )
# rtx.scene.append( Sphere(V3(0.5,2.55,-8), 0.1, stone) )

rtx.glClearColor(0.2, 0.6, 0.8)
rtx.glClear()
rtx.envmap = EnvMap('Assets/envmap3.bmp')

rtx.ambLight = AmbientLight(strength=0.1)
rtx.dirLight = DirectionalLight(direction=V3(1, -1, -2), intensity=0.5)
rtx.pointLights.append(PointLight(position=V3(0, 2, 0), intensity=0.5))

# rtx.scene.append( Sphere(V3(-4,2,-8), 1, glass))
# rtx.scene.append( Sphere(V3(0,2,-8), 1, glass2))
# rtx.scene.append( Sphere(V3(4,2,-8), 1, mirror))
# rtx.scene.append( Sphere(V3(-4,-2,-8), 1, mirror2))
# rtx.scene.append( Sphere(V3(0,-2,-8), 1, carrot))
# rtx.scene.append( Sphere(V3(4,-2,-8), 1, grass))

# rtx.scene.append(AABB(V3(-1, -1, -5), V3(2, 1, 1), gift1))

# rtx.scene.append(Triangle(V3(0, 0, -5), 4, grass))
# rtx.scene.append(Sphere(V3(3.5, -1, -6), 0.5, mirror))
rtx.scene.append(
    Triangle2(V3(1, -1.5, -7), V3(6, -1.5, -7), V3(3.5, 4, -7), grass))
# rtx.scene.append(AABB(V3(4, -3.5, -7), V3(0.5, 1, 0.01), stone))

rtx.glRender()

rtx.glFinish('Pruebas.bmp')
