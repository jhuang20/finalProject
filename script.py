import mdl
from display import *
from matrix import *
from draw import *

"""======== first_pass( commands ) ==========

  Checks the commands array for any animation commands
  (frames, basename, vary)

  Should set num_frames and basename if the frames
  or basename commands are present

  If vary is found, but frames is not, the entire
  program should exit.

  If frames is found, but basename is not, set name
  to some default value, and print out a message
  with the name being used.
  ==================== """
def first_pass( commands ):
    name = ''
    num_frames = 1
    for command in commands:
        if command['op'] == 'basename':
            name = command['args'][0]
        elif command['op'] == 'frames':
            num_frames = command['args'][0]
    return (name, num_frames)

"""======== second_pass( commands ) ==========

  In order to set the knobs for animation, we need to keep
  a seaprate value for each knob for each frame. We can do
  this by using an array of dictionaries. Each array index
  will correspond to a frame (eg. knobs[0] would be the first
  frame, knobs[2] would be the 3rd frame and so on).

  Each index should contain a dictionary of knob values, each
  key will be a knob name, and each value will be the knob's
  value for that frame.

  Go through the command array, and when you find vary, go
  from knobs[0] to knobs[frames-1] and add (or modify) the
  dictionary corresponding to the given knob with the
  appropirate value.
  ===================="""
def second_pass( commands, num_frames ):
    frames = [{} for i in range(int(num_frames)) ]
    for command in commands:
        print(command)
        if command['op']=="set":
            knob=command['knob']
            args = command['args']
            print(args)
            #sinit=args[1]
            #print(knob, args, init)
        if command['op'] == "vary":
            knob = command['knob']
            args = command['args']
            length = args[1] - args[0]
            velocity = args[3] - args[2]
            spe = velocity/length
            for i in range(int(length)):
                frames[int(i+args[0])][knob] = args[2] + spe * i

    return frames

def run(filename):
    """
    This function runs an mdl script
    """
    shading='default'
    p = mdl.parseFile(filename)
    lights={}
    if p:
        (commands, symbols) = p
        #print(p)
        #print(p)
        #print(commands)
        #print(symbols)
    else:
        print "Parsing failed."
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0,
              0,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'
    lights={}
    for cmd in symbols:
        if symbols[cmd][0]=='light':
            lights[cmd]=symbols[cmd][1]
    (name, num_frames) = first_pass(commands)
    frames = second_pass(commands, num_frames)
    (lights, ambient)=lights,[255,255,255]
    #print(lights)
    i = 0
    for frame in frames:
        symbols.update(frame)
        tmp = new_matrix()
        ident( tmp )
        stack = [ [x[:] for x in tmp] ]
        screen = new_screen()
        zbuffer = new_zbuffer()
        tmp = []
        master=[]
        step_3d = 600
        consts = ''
        coords = []
        coords1 = []

        for command in commands:
            c = command['op']
            args = command['args']
            knob_value = 1
            if c=='shading':
                #print(command['cs'])
                if command['shade_type']:
                    #print(tmp)
                    shading=command['shade_type']
                    #draw_polygons(tmp, screen, zbuffer, view, ambient, lights, symbols, reflect,command['shade_type'])
                else:
                    pass
            elif c=='mesh':
                print(c)
                #print(c, args)
                print(args[0])
                makeMesh(tmp,command['cs'])
                matrix_mult( stack[-1], tmp )
                if command['constants']:
                    reflect=command['constants']
                draw_polygons(tmp, screen, zbuffer, view, ambient, lights, symbols, reflect,shading)
            elif c == 'box':
                if command['constants']:
                    reflect = command['constants']
                add_box(tmp,args[0], args[1], args[2],args[3], args[4], args[5])
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, lights, symbols, reflect,shading)
                tmp = []
                reflect = '.white'
            elif c == 'sphere':
                if command['constants']:
                    reflect = command['constants']
                add_sphere(tmp,
                               args[0], args[1], args[2], args[3], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, lights, symbols, reflect,shading)
                tmp = []
                reflect = '.white'
            elif c == 'torus':
                if command['constants']:
                    reflect = command['constants']
                add_torus(tmp,args[0], args[1], args[2], args[3], args[4], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, lights, symbols, reflect,shading)
                tmp = []
                reflect = '.white'
            elif c == 'line':
                    add_edge(tmp,
                                     args[0], args[1], args[2], args[3], args[4], args[5])
                    matrix_mult( stack[-1], tmp )
                    draw_lines(tmp, screen, zbuffer, color)
                    tmp = []
            elif c == 'move':
                v=1
                if command['knob'] is not None:
                    v = symbols[command['knob']]
                tmp = make_translate(args[0] * v, args[1] * v, args[2] * v)
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'scale':
                v=1
                if command['knob'] is not None:
                    v = symbols[command['knob']]
                tmp = make_scale(args[0] * v, args[1] * v, args[2] * v)
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'rotate':
                v=1
                if command['knob'] is not None:
                    v = symbols[command['knob']]
                theta = args[1] * (math.pi/180)
                if args[0] == 'x':
                    tmp = make_rotX(theta*v)
                elif args[0] == 'y':
                    tmp = make_rotY(theta*v)
                else:
                    tmp = make_rotZ(theta * v)
                matrix_mult( stack[-1], tmp )
                stack[-1] = [ x[:] for x in tmp]
                tmp = []
            elif c == 'push':
                stack.append([x[:] for x in stack[-1]] )
            elif c == 'pop':
                stack.pop()
            elif c == 'display':
                display(screen)
            elif c == 'save':
                save_extension(screen, args[0])
        print('/anim/' + name + "%03d"%i)
        save_extension(screen, 'anim/' + name + "%03d"%i + '.gif')
        i += 1
        # end operation loop
    make_animation(name)
