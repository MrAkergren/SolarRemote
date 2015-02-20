#import serial
import tty, sys, termios

class ReadChar():
    def __enter__(self):
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)
        tty.setraw(sys.stdin.fileno())
        return sys.stdin.read(1)
    def __exit__(self, type, value, traceback):
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)

#ser = serial.Serial('/dev/ttyUSB0', 38400, timeout = 0)
#os.system("stty -echo")
def test():	
	print("Parans Panel Remote")
	print("Enter command:")

	while True:
		with ReadChar() as rc:
			cmd = ord(rc)
		if not cmd >= 48 and not cmd <= 57:
			print("Illegal command")
		if cmd == 48:	#0
			raise SystemExit
		if cmd == 56:	#8
			print("run u")
		if cmd == 50:	#2
			print("run d")
		if cmd == 52:	#4
			print("run l")
		if cmd == 54:	#6
			print("run r")
		if cmd == 53:	#5
			print("run s")
		if cmd == 55:	#7
			print("date")

if __name__ == "__main__":
    test()