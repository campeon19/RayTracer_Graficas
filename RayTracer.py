# Ray Tracer Engine
# Christian Perez 19710
# Graficas por Computador 


from gl import RayTracer, V3, _color
from obj import Obj, Texture
from figures import Sphere, Material

# width = 300
# height = 512

# width = 600
# height = 1024

width = 1000
height = 1424

rtx = RayTracer(width, height)

nieve = Material( diffuse = _color(0.9372,0.882,0.78))
white = Material( diffuse = _color(1,1,1))
black = Material( diffuse = _color(0,0,0))
carrot = Material( diffuse = _color(0.93,0.57,0.13))
stone = Material( diffuse = _color(0.5451,0.549,0.4784))
rojo = Material( diffuse = _color(1,0,0))

rtx.scene.append( Sphere(V3(0,-3,-10), 2.3, nieve) )
rtx.scene.append( Sphere(V3(0,0.8,-11), 2, nieve) )
rtx.scene.append( Sphere(V3(0,3.7,-10), 1.4, nieve) )
rtx.scene.append( Sphere(V3(0,-2.5,-8), 0.5, black) )
rtx.scene.append( Sphere(V3(0,-0.7,-8), 0.35, black) )
rtx.scene.append( Sphere(V3(0,1,-8), 0.3, black) )
rtx.scene.append( Sphere(V3(0,3,-8), 0.3, carrot) )
rtx.scene.append( Sphere(V3(0.3,3.5,-8), 0.15, white) )
rtx.scene.append( Sphere(V3(-0.3,3.5,-8), 0.15, white) )
rtx.scene.append( Sphere(V3(0.27,3.1,-7), 0.06, black) )
rtx.scene.append( Sphere(V3(-0.27,3.1,-7), 0.06, black) )
rtx.scene.append( Sphere(V3(0.2,2.35,-8), 0.1, stone) )
rtx.scene.append( Sphere(V3(-0.2,2.35,-8), 0.1, stone) )
rtx.scene.append( Sphere(V3(-0.5,2.55,-8), 0.1, stone) )
rtx.scene.append( Sphere(V3(0.5,2.55,-8), 0.1, stone) )
rtx.glRender()

rtx.glFinish('Pruebas.bmp')