import serial
import subprocess
import os
import signal

ser = serial.Serial('/dev/ttyACM0',9600)
s = [0]

process = False
screen = False


def init(self):
        # Initialize pygame and display a blank screen.
        pygame.display.init()
        pygame.font.init()
        pygame.mouse.set_visible(False)
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        """Render a blank screen filled with the background color."""
        screen.fill(self._bgcolor)
        pygame.display.update()


def quit(self):
    pygame.quit()

def play(filename):
    global process
    args = ['omxplayer']
    args.append('-b')
    args.append('-r')
    args.append(filename)
    process = subprocess.Popen(args,stdout=open(os.devnull, 'wb'),close_fds=True)
    
def stop(self):
    global process
    if process is not None and process.returncode is None:
            # There are a couple processes used by omxplayer, so kill both
            # with a pkill command.
            subprocess.call(['pkill', '-9', 'omxplayer'])
    


def is_playing(self):
        global process
        """Return true if the video player is running, false otherwise."""
        if process is None:
            return False
        process.poll()
        return process.returncode is None

              



init

signal.signal(signal.SIGTERM, quit)

while True:
	command = str(ser.readline())
	print (command)
	if "play" in command :
	  print("play")
	  play('00003.MTS')
	  
	if "stop" in command :
	  print("stop")
	  stop("stop")
