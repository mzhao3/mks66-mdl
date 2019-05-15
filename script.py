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

        if op == 'sphere':
            if command['cs'] == None:
                cs = stack
            else:
                cs = command['cs']

            if command['constants']:
                if command['constants'] == None:
                    const = ".white"
                else:
                    const = command['constants']

            #     #blue green and red are not in the right order
            #     areflect = [symbols[const][1][x][0] for x in symbols[const][1]]
            #     dreflect = [symbols[const][1][x][1] for x in symbols[const][1]]
            #     sreflect = [symbols[const][1][x][2] for x in symbols[const][1]]
            #
            # #print(areflect)
            # #print(dreflect)
            # #print(sreflect)
            add_sphere(tmp,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step_3d)
            matrix_mult( cs[-1], tmp )
            #print(screen)
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, const)
            #split constants into a, s, d
            #constants name kar kdr ksr kag kdg ksg kab kdb ksb [r] [g] [b]

            polygons = []

        if op == 'push':
            stack.append( [x[:] for x in stack[-1]] )
        if op == 'pop':
            stack.pop()
        if op == 'display':
            display(screen)
        if op == 'save':
            save_extension(screen, args[0]+".png")
        print command
