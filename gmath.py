import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 'location'
COLOR = 'color'
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, symbols, reflect ):
    print(light)
    n = normal[:]
    normalize(n)
    #normalize(light[LOCATION])
    normalize(view)
    r = symbols[reflect][1]

    a = calculate_ambient(ambient, r)
    d = calculate_diffuse(light, r, n)
    s = calculate_specular(light, r, view, n)

    i = [0, 0, 0]
    i[RED] = int(a[RED] + d[RED] + s[RED])
    i[GREEN] = int(a[GREEN] + d[GREEN] + s[GREEN])
    i[BLUE] = int(a[BLUE] + d[BLUE] + s[BLUE])
    limit_color(i)

    return i

def calculate_ambient(alight, reflect):
    a = [0, 0, 0]
    a[RED] = alight[RED] * reflect['red'][AMBIENT]
    a[GREEN] = alight[GREEN] * reflect['green'][AMBIENT]
    a[BLUE] = alight[BLUE] * reflect['blue'][AMBIENT]
    return a
#cycles through the dict. of lights!
def calculate_diffuse(light, reflect, normal):
    d = [0, 0, 0]
    for lights in light:
        ref=light[lights]
        #new location of light
        normalize(ref['location'])
        dot = dot_product( ref['location'], normal)

        dot = dot if dot > 0 else 0
        d[RED] = ref[COLOR][RED] * reflect['red'][DIFFUSE] * dot
        d[GREEN] = ref[COLOR][GREEN] * reflect['green'][DIFFUSE] * dot
        d[BLUE] = ref[COLOR][BLUE] * reflect['blue'][DIFFUSE] * dot
    return d

def calculate_specular(light, reflect, view, normal):
    s = [0, 0, 0]
    n = [0, 0, 0]
    for lights in light:
        ref=light[lights]
        normalize(ref['location'])
        result = 2 * dot_product(ref['location'], normal)
        n[0] = (normal[0] * result) - ref[LOCATION][0]
        n[1] = (normal[1] * result) - ref[LOCATION][1]
        n[2] = (normal[2] * result) - ref[LOCATION][2]

        result = dot_product(n, view)
        result = result if result > 0 else 0
        result = pow( result, SPECULAR_EXP )

        s[RED] = ref[COLOR][RED] * reflect['red'][SPECULAR] * result
        s[GREEN] = ref[COLOR][GREEN] * reflect['green'][SPECULAR] * result
        s[BLUE] = ref[COLOR][BLUE] * reflect['blue'][SPECULAR] * result
    return s

def limit_color(color):
    color[RED] = 255 if color[RED] > 255 else color[RED]
    color[GREEN] = 255 if color[GREEN] > 255 else color[GREEN]
    color[BLUE] = 255 if color[BLUE] > 255 else color[BLUE]

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
