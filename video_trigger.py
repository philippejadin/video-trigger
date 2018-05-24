# Copyright 2018 Philippe Jadin
# Inspired by adafruit video_looper :
# Copyright 2015 Adafruit Industries.
# Author: Tony DiCola
# License: GNU GPLv3, see LICENSE.txt


import ConfigParser
import importlib
import os
import re
import sys
import signal
import time
import serial
import subprocess

import pygame


class VideoTrigger(object):

    def __init__(self, config_path):
        """Create an instance of the main video trigger application class. Must
        pass path to a valid video trigger ini configuration file.
        """
        # Load the configuration.
        self._config = ConfigParser.SafeConfigParser()
        if len(self._config.read(config_path)) == 0:
            raise RuntimeError('Failed to find configuration file at {0}, is the application properly installed?'.format(config_path))
        self._console_output = self._config.getboolean('video_trigger', 'console_output')
 
        self._debug_enabled = self._config.getboolean('video_trigger', 'debug')
              
        
        self._running = False
        self._process_omxplayer = False
        self._process_hello_video = False
        self._process_audio = False
        self._is_playing = False
        self._is_showing = False
        self._text_pos = 20
        
        self._keyboard_control = self._config.getboolean('video_trigger', 'keyboard_control')
        
        # Initialize pygame and display a blank screen.
        pygame.display.init()
        pygame.font.init()
        
        self._small_font = pygame.font.Font(None, 20)
        self._big_font   = pygame.font.Font(None, 250)
        
        self._bgcolor = map(int, self._config.get('video_trigger', 'bgcolor') \
                                             .translate(None, ',') \
                                             .split())
        self._fgcolor = map(int, self._config.get('video_trigger', 'fgcolor') \
                                             .translate(None, ',') \
                                             .split())
        
        
        
        pygame.mouse.set_visible(False)
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        
        if self._config.getboolean('video_trigger', 'full_screen'):
            self._screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        else:
            self._screen = pygame.display.set_mode(size, pygame.RESIZABLE)
            
        self._blank_screen()   
        
        try:
            self._serial = serial.Serial('/dev/ttyACM0',9600)
        except:
            self._print_text('ERROR : Cannot open serial line, exiting in 5 seconds')
            time.sleep(5)
            self.quit()
        
        self._running  = True
       
        
    
    def _debug(self, message):
        if self._debug_enabled: 
            self._print_console(message)
            self._print_text(message)
        

    def _print_console(self, message):
        """Print message to standard output if console output is enabled."""
        if self._console_output:
            print(message)

    def _blank_screen(self):
        """Render a blank screen filled with the background color."""
        self._screen.fill(self._bgcolor)
        pygame.display.update()

   
    
    def _print_text(self, message):
        text = self._small_font.render(message, 1, self._fgcolor)
        w,h = self._screen.get_size()
        self._text_pos = self._text_pos + 20
        if (self._text_pos > h):
            self._text_pos = 20
            
        self._screen.blit(text, (20,self._text_pos))
        pygame.display.update()
    
    def _stop(self):
        # stop omxplayer
        if self._process_omxplayer :
            self._process_omxplayer.terminate()
            subprocess.call(['pkill', '-9', 'omxplayer'])
        
        # stop hello video
        if self._process_hello_video :
            self._process_hello_video.terminate()
        
        # stop aplay
        if self._process_audio :
            self._process_audio.terminate()
        
        # clear image
        if self._is_showing :
            self._blank_screen()
            self._is_showing = False
            
   

    
    def run(self):
        """Main program loop.  Will never return!"""
        self._debug('Video Trigger v1')
        self._debug('Debug enabled')
        
        
        while self._running:
            # Listen to an arduino command and act accordingly
            if (self._serial.inWaiting()>0): #if incoming bytes are waiting to be read from the serial input buffer
                command = str(self._serial.readline())
                self._debug('Serial command received : ' + command.strip())
                
                items = command.split(" ")
                action = items[0].strip()
                
                # We handle loop and play similarly, the difference is just a single argument on the command line players
                if (action == "play") or (action == "loop") :                                           
                    # tester synchro video et son et vitesse lecture simulatane depuis cle usb
                                       
                    # kill previous process
                    self._stop()
                    
                    # get filename
                    # check the file exists and play it else error
                    file = "/home/pi/" + items[1].strip()
                    
                    filename, file_extension = os.path.splitext(file)
                    
                    self._debug('Playing : ' + file)
                    
                    self._is_playing = True
                    
                    if (os.path.isfile(file)):
                        
                        # use omxplayer for mp4
                        if (file_extension == '.mp4'):
                            args = ['omxplayer']
                            args.extend(['--audio_fifo', '0'])
                            args.extend(['--video_fifo', '0'])
                            args.extend(['--audio_queue', '0.4'])
                            args.extend(['--video_queue', '0.4'])
                            args.extend(['--threshold', '0'])
                            args.append('--no-osd')
                            
                            if (action == 'loop'):
                                args.append('--loop')
                        
                            args.append(file)
                            self._process_omxplayer = subprocess.Popen(args, stdout=open(os.devnull, 'wb'), close_fds=True)
                            self._is_playing_omxplayer = True
                            
                        # use hello video for h264
                        elif (file_extension == '.h264'):
                            args = ['hello_video.bin']
                            if (action == 'loop'):
                                args.append('--loop')
                                
                            args.append(file)
                            self._process_hello_video= subprocess.Popen(args, stdout=open(os.devnull, 'wb'), close_fds=True)
                            self._is_playing_hello_video = True
                        
                        # use audio player for wav
                        elif (file_extension == '.wav'):
                            args = ['aplay']
                            args.append(file)
                            self._process_audio = subprocess.Popen(args, stdout=open(os.devnull, 'wb'), close_fds=True)
                            self._is_playing_audio = True
                        
                        # use pygame for png's
                        elif (file_extension == '.png'):
                            image = pygame.image.load(file)
                            self._screen.blit(image, (0,0))
                            pygame.display.update()
                            self._is_showing = True
                        
                        else:
                            self._print_text('Unknown file extension : ' + file_extension)
                            time.sleep(5)
                            
                            
                    else:
                        self._debug('File not found ' + file)
                        time.sleep(1)
                        
                
                    
                    
                if "stop" in command :
                    self._debug('Stoping')
                    self._stop()
                    
                
                    
            
            # Event handling for key press, if keyboard control is enabled
            if self._keyboard_control:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        # If pressed key is ESC quit program
                        if event.key == pygame.K_ESCAPE:
                            self.quit()
            # Give the CPU some time to do other tasks.
            time.sleep(0.002)

    def quit(self):
        """Shut down the program"""
        self._running = False
        self._stop()
        pygame.quit()

    def signal_quit(self, signal, frame):
        """Shut down the program, meant to by called by signal handler."""
        self.quit()


# Main entry point.
if __name__ == '__main__':
    print('Starting Video Trigger.')
    # Default config path to /boot.
    config_path = '/boot/video_trigger.ini'
    # Override config path if provided as parameter.
    if len(sys.argv) == 2:
        config_path = sys.argv[1]
    # Create video trigger.
    videotrigger = VideoTrigger(config_path)
    # Configure signal handlers to quit on TERM or INT signal.
    signal.signal(signal.SIGTERM, videotrigger.signal_quit)
    signal.signal(signal.SIGINT, videotrigger.signal_quit)
    # Run the main loop.
    videotrigger.run()
    