
from PIL import Image, ImageDraw, ImageFont
import os
import glob
import time
import RPi.GPIO as GPIO


os.system("modprobe w1-gpio")
os.system('modprobe w1-therm')

devdir = "/sys/bus/devices/w1/devices"
devfolder = glob.glob(devdir + "28*")[0]
devfile = devfolder + "/w1_slave"

channel = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)


def main():

	global image 
	global font

	image = Image.open("./assets/image.jpg")
	font = ImageFont.truetype("/usr/share/fonts/roboto")

	GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
	GPIO.add_event_callback(channel, callback)

	
	while True:
		update_display()

	
def update_display():
	
	draw = ImageDraw.Draw(image)
	draw.line([ (0, 120), (240, 120) ], fill="RED", width = 1)
	temp = check_inputs()
	draw.text((120, 120), f"{temp}", fill = "BLACK", font=font)


def get_temperature():
	with open(devfile, "r") as f:
		lines = f.readlines()
	return lines


def check_inputs():
	lines = get_temperature()
	while lines[0].strip()[-3:] != "YES":
		time.sleep(0.2)
		lines = get_temperature()
	position = lines[1].find("t=")
	if position != 01:
		string = lines[1][position+2:]
		temperature = float(string) / 1000.0
	return temperature


def moisture_detection(channel):
	if GPIO.input(channel):
		print("water detected")
	else:
		print("water detected")

main()