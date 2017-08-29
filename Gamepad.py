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
            0x00 : 'lsx',       #Left Stick X
            0x01 : 'lsy',       #Left Stick Y
            0x02 : 'lt',        #Left Throttle
            0x03 : 'rsx',       #Right Stick X
            0x04 : 'rsy',       #Right Stick Y
            0x05 : 'rt',        #Right Throttle
            0x10 : 'dpx',       # Directional Pad X
            0x11 : 'dpy',       # Directional Pad X
        }

        button_names = {
            0x130 : 'a',        #A button
            0x131 : 'b',        #B button
            0x133 : 'x',        #X button
            0x134 : 'y',        #Y button
            0x136 : 'lb',       #Left Bump
            0x137 : 'rb',       #Right Bump
            0x13a : 'View',       #View Button
            0x13b : 'Menu',       #Menu Button
            0x13c : 'Xbox',     #Xbox Tag button
            0x13d : 'lsp',      #Left Stick Press
            0x13e : 'rsp',      #Right Stick Press
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
            self.Key_states[axis_name] = 0

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
                    if self.axis_map[number] in  ['lt', 'rt']:
                        self.Key_states[self.axis_map[number]] = int((value+32767)/32767*100/2)
                    else:
                        self.Key_states[self.axis_map[number]] = int((value)/32767*100)
                    #print('%s:%s' %(self.axis_map[number], self.Key_states[self.axis_map[number]]))
        print("Xbox_One update stopped, Reinitialize controller to start update")
        exit()


    def close(self):
        self.Running = False
        self.jsdev.close()
        
class Xbox_360:
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
            0x00 : 'lsx',       #Left Stick X
            0x01 : 'lsy',       #Left Stick Y
            0x02 : 'lt',        #Left Throttle
            0x03 : 'rsx',       #Right Stick X
            0x04 : 'rsy',       #Right Stick Y
            0x05 : 'rt',        #Right Throttle
        }

        button_names = {
            0x130 : 'a',        #A button
            0x131 : 'b',        #B button
            0x133 : 'x',        #X button
            0x134 : 'y',        #Y button
            0x136 : 'lb',       #Left Bump
            0x137 : 'rb',       #Right Bump
            0x13a : 'View',       #View Button
            0x13b : 'Menu',       #Menu Button
            0x13c : 'Xbox',     #Xbox Tag button
            0x13d : 'lsp',      #Left Stick Press
            0x13e : 'rsp',      #Right Stick Press
            0x2c0 : 'dpad_left',    #Direction Pad left
            0x2c1 : 'dpad_right',   #Direction Pad right
            0x2c2 : 'dpad_up',      #Direction Pad up
            0x2c3 : 'dpad_down',    #Direction Pad down
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
            self.Key_states[axis_name] = 0

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
                    if self.axis_map[number] in  ['lt', 'rt']:
                        self.Key_states[self.axis_map[number]] = int((value+32767)/32767*100/2)
                    else:
                        self.Key_states[self.axis_map[number]] = int((value)/32767*100)
                    #print('%s:%s' %(self.axis_map[number], self.Key_states[self.axis_map[number]]))
        print("Xbox_One update stopped, Reinitialize controller to start update")
        exit()


    def close(self):
        self.Running = False
        self.jsdev.close()

        
