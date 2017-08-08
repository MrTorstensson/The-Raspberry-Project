# Released by rdb under the Unlicense (unlicense.org)
# Based on information from:
# https://www.kernel.org/doc/Documentation/input/joystick-api.txt
# Modified to work as a joystick control driver (MrTorstensson)

import os, struct, array
from fcntl import ioctl
from time import sleep
from _thread import *

class Xbox_One:
    """ Xbox One controller driver that will set up all buttons and Throttles """
    """ and keep latest value for all of them in a callable dictionary        """
  
    def __init__(self, JS = "/dev/input/js0"):
        """ JS = Gamepad device location in Kernel """
        # We'll store the states here.
        self.Key_states = {}
        self.axis_map = []
        self.button_map = []

        # These constants were borrowed from linux/input.h and modified for the names on the Xbox One control
        axis_names = {
            0x00 : 'lx',
            0x01 : 'ly',
            0x02 : 'lt',
            0x03 : 'rx',
            0x04 : 'ry',
            0x05 : 'rt',
            0x06 : 'throttle',
            0x07 : 'rudder',
            0x08 : 'wheel',
            0x09 : 'gas',
            0x0a : 'brake',
            0x10 : 'hat0x',
            0x11 : 'hat0y',
            0x12 : 'hat1x',
            0x13 : 'hat1y',
            0x14 : 'hat2x',
            0x15 : 'hat2y',
            0x16 : 'hat3x',
            0x17 : 'hat3y',
            0x18 : 'pressure',
            0x19 : 'distance',
            0x1a : 'tilt_x',
            0x1b : 'tilt_y',
            0x1c : 'tool_width',
            0x20 : 'volume',
            0x28 : 'misc',
        }

        button_names = {
            0x120 : 'trigger',
            0x121 : 'thumb',
            0x122 : 'thumb2',
            0x123 : 'top',
            0x124 : 'top2',
            0x125 : 'pinkie',
            0x126 : 'base',
            0x127 : 'base2',
            0x128 : 'base3',
            0x129 : 'base4',
            0x12a : 'base5',
            0x12b : 'base6',
            0x12f : 'dead',
            0x130 : 'a',
            0x131 : 'b',
            0x132 : 'c',
            0x133 : 'x',
            0x134 : 'y',
            0x135 : 'z',
            0x136 : 'lb',
            0x137 : 'rb',
            0x138 : 'tl2',
            0x139 : 'tr2',
            0x13a : 'select',
            0x13b : 'start',
            0x13c : 'Xbox',
            0x13d : 'thumbl',
            0x13e : 'thumbr',
            #Pads
            0x220 : 'dpad_up',
            0x221 : 'dpad_down',
            0x222 : 'dpad_left',
            0x223 : 'dpad_right',
            # XBox 360 controller uses these codes.
            0x2c0 : 'dpad_left',
            0x2c1 : 'dpad_right',
            0x2c2 : 'dpad_up',
            0x2c3 : 'dpad_down',
        }

        # Check if joystick device exists
        if (not os.path.exists(JS)):
            print('Game controller not found (%s), is it connected?' % JS)
            exit()

        # Open the joystick device.
        print('Opening %s...' % JS)
        self.jsdev = open(JS, 'rb')

        # Get the device name.
        buf = array.array('B', [0] * 64)
        ioctl(self.jsdev, 0x80006a13 + (0x10000 * len(buf)), buf) # JSIOCGNAME(len)
        js_name = buf.tostring()
        print('Device name: %s' % js_name)

        # Get number of axes and buttons.
        buf = array.array('B', [0])
        ioctl(self.jsdev, 0x80016a11, buf) # JSIOCGAXES
        num_axes = buf[0]
        buf = array.array('B', [0])
        ioctl(self.jsdev, 0x80016a12, buf) # JSIOCGBUTTONS
        num_buttons = buf[0]

        # Get the axis map.
        buf = array.array('B', [0] * 0x40)
        ioctl(self.jsdev, 0x80406a32, buf) # JSIOCGAXMAP
        for axis in buf[:num_axes]:
            axis_name = axis_names.get(axis, 'unknown(0x%02x)' % axis)
            self.axis_map.append(axis_name)
            self.Key_states[axis_name] = 0.0

        # Get the button map.
        buf = array.array('H', [0] * 200)
        ioctl(self.jsdev, 0x80406a34, buf) # JSIOCGBTNMAP
        for btn in buf[:num_buttons]:
            btn_name = button_names.get(btn, 'unknown(0x%03x)' % btn)
            self.button_map.append(btn_name)
            self.Key_states[btn_name] = 0

        print('%d axes found: %s' % (num_axes, ', '.join(self.axis_map)))
        print('%d buttons found: %s' % (num_buttons, ', '.join(self.button_map)))

        self.Running = True
        start_new_thread(self.UpdateThread,())

    def UpdateThread(self):
        # Main event loop
        while self.Running:
            evbuf = self.jsdev.read(8)
            if evbuf:
                time, value, type, number = struct.unpack('IhBB', evbuf)
                if type & 0x80:
                    True
                # If Button
                elif type & 0x01:
                    # Xbox button will disconnect
                    if self.button_map[number] == 'Xbox':
                        print('%s:%s' %('Disconnect', 'Exit'))
                        self.Running = False
                        break
                    self.Key_states[self.button_map[number]] = value
                    #print('%s:%s' %(self.button_map[number], self.Key_states[self.button_map[number]]))
                #If Throttle
                elif type & 0x02:
                    value = value/32676.0
                    self.Key_states[self.axis_map[number]] = value
                    #print('%s:%s' %(self.axis_map[number], self.Key_states[self.axis_map[number]]))
        print("Xbox_One update stopped, Reinitialize controller to start update")
        exit()


    def close(self):
        self.Running = False
        self.jsdev.close()

        
