import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    print symbols
    for command in commands:
        op = command['op']
        args = command['args']

        if op == 'move':
            t = make_translate(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]

        if op == 'rotate':
            theta = float(args[1]) * (math.pi / 180)
            if args[0] == 'x':
                t = make_rotX(theta)
            elif args[0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]
        if op == 'scale':
            t = make_scale(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]
        if op == 'line':
            add_edge( tmp,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), float(args[5]) )
            matrix_mult( cs[-1], tmp )
            draw_lines(tmp, screen, zbuffer, color)
            tmp = []
        if op == 'sphere':
            if command['cs'] == None:
                cs = stack
            else:
                cs = command['cs']


            if command['constants'] == None:
                const = ".white"
            else:
                const = command['constants']


            add_sphere(tmp,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step_3d)
            matrix_mult( cs[-1], tmp )
            #print(screen)
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, const)

            tmp = []
        if op == 'box':
            if command['cs'] == None:
                cs = stack
            else:
                cs = command['cs']

            if command['constants'] == None:
                const = ".white"
            else:
                const = command['constants']
            add_box(tmp,
                    float(args[0]), float(args[1]), float(args[2]),
                    float(args[3]), float(args[4]), float(args[5]))
            matrix_mult( cs[-1], tmp )
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, const)
            tmp = []
        if op == 'torus':
            if command['cs'] == None:
                cs = stack
            else:
                cs = command['cs']


            if command['constants'] == None:
                const = ".white"
            else:
                const = command['constants']
            add_torus(tmp,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), step_3d)
            matrix_mult( cs[-1], tmp )
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, const)
            tmp = []


        if op == 'push':
            stack.append( [x[:] for x in stack[-1]] )
        if op == 'pop':
            stack.pop()
        if op == 'display':
            display(screen)
        if op == 'save':
            save_extension(screen, args[0]+".png")
        print command
