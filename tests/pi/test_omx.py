import os
import subprocess
import time
import pygame
import serial

'''
arduino = serial.Serial('/dev/ttyACM0', 9600)

while 1 :
    arduino.readline()
'''


args = ['omxplayer']
args.append('-b')
args.append('00003.MTS')


pygame.display.init()
pygame.font.init()
pygame.mouse.set_visible(False)


print (subprocess.Popen(args,stdout=open(os.devnull, 'wb'),close_fds=True))


'''

#print (subprocess.check_output(args))
'''
