
import base64
import numpy as np
from tcam import TCam
from array import array
from PIL import Image
import RPi.GPIO as GPIO
import time

IP = "192.168.4.1"

GPIO.setmode(GPIO.BOARD)

button_pin = 11

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

COUNTER = 1


def convert(img):

    dimg = base64.b64decode(img["radiometric"])
    ra = array('H', dimg)
    return np.array(ra).reshape((120,160))


def update(file_name):
	image = convert(tcam.get_image())
	frame_image = Image.fromarray(image)
	
	frame_image.save(file_name)
	print(f'saved_file: {file_name}')


if __name__ == '__main__':
	 tcam = TCam()
	 tcam.connect(IP)
	 print('Connected')
	 try:
		 while True:
			 if GPIO.input(button_pin) == GPIO.HIGH:
				 print('button pressed')
				 outfile = f'-o thermal_im_{str(COUNTER).zfill(4)}.tif'
				 update(outfile)
				 COUNTER += 1
				 time.sleep(0.2)
	 
	 except KeyboardInterrupt:
		 tcam.shutdown()
 
