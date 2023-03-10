#!/usr/bin/python
import time
import os
import glob
from itertools import repeat
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
import threading
from datetime import datetime

# ** Temperature Selection ** 0 = Fahrenheit, 1 = Celsius **
temp_selection = 0

# ** Calibration **
#TA
cal_TA = 1.9
cal_T1 = -3
cal_T2 = 0

probe_TA = '28-8000003203d6'
probe_T1 = '28-0305949722d7'
probe_T2 = '28-031394976a24'

# GPIO Setup
ledPinF = 22
ledPinC = 27
# buttonPin = 14
GPIO.setup(ledPinF, GPIO.OUT)
GPIO.setup(ledPinC, GPIO.OUT)
# GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# States
# ledStateRed = GPIO.LOW
# ledStateGreen = GPIO.LOW
# lstBtnState = int
# cntbtnState = GPIO.input(buttonPin)
# GPIO.output(ledPinRed, ledStateRed)
# GPIO.output(ledPinGreen, ledStateGreen)

# Raspberry Pi pin configuration:
lcd_rs = 26
lcd_en = 19
lcd_d4 = 13
lcd_d5 = 6
lcd_d6 = 5
lcd_d7 = 21
lcd_backlight = 4

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2

# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)

# 18B20 Temp. Probe
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'

# TA
device_folder_TA = glob.glob(base_dir + probe_TA)[0]
device_file_TA = device_folder_TA + '/w1_slave'
# T1
device_folder_T1 = glob.glob(base_dir + probe_T1)[0]
device_file_T1 = device_folder_T1 + '/w1_slave'
# T2
device_folder_T2 = glob.glob(base_dir + probe_T2)[0]
device_file_T2 = device_folder_T2 + '/w1_slave'


# TA
def read_temp_raw_TA():
    f = open(device_file_TA, 'r')
    lines = f.readlines()
    f.close()
    return lines

# T1


def read_temp_raw_T1():
    f = open(device_file_T1, 'r')
    lines = f.readlines()
    f.close()
    return lines

# T2


def read_temp_raw_T2():
    f = open(device_file_T2, 'r')
    lines = f.readlines()
    f.close()
    return lines

# CELSIUS CALCULATION
# Calibrated


def read_temp_c_TA():
    lines = read_temp_raw_TA()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw_TA()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        # TEMP_STRING IS THE SENSOR OUTPUT, MAKE SURE IT'S AN INTEGER TO DO THE MATH
        temp_c = (int(temp_string) / 1000.0) + cal_TA
        # temp_c = str(round(temp_c, 1)) # ROUND THE RESULT TO 1 PLACE AFTER THE DECIMAL, THEN CONVERT IT TO A STRING
        return temp_c

# Calibrated


def read_temp_c_T1():
    lines = read_temp_raw_T1()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw_T1()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        # TEMP_STRING IS THE SENSOR OUTPUT, MAKE SURE IT'S AN INTEGER TO DO THE MATH
        temp_c = (int(temp_string) / 1000.0) + cal_T1
        # temp_c = str(round(temp_c, 1)) # ROUND THE RESULT TO 1 PLACE AFTER THE DECIMAL, THEN CONVERT IT TO A STRING
        return temp_c

def read_temp_c_T2():
    lines = read_temp_raw_T2()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw_T2()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        # TEMP_STRING IS THE SENSOR OUTPUT, MAKE SURE IT'S AN INTEGER TO DO THE MATH
        temp_c = int(temp_string) / 1000.0 + cal_T2
        # temp_c = str(round(temp_c, 1)) # ROUND THE RESULT TO 1 PLACE AFTER THE DECIMAL, THEN CONVERT IT TO A STRING
        return temp_c


# FAHRENHEIT CALCULATION
def read_temp_f_TA():
    lines = read_temp_raw_TA()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw_TA()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        # TEMP_STRING IS THE SENSOR OUTPUT, MAKE SURE IT'S AN INTEGER TO DO THE MATH
        temp_f = ((int(temp_string) / 1000.0) + 1.9) * 9.0 / 5.0 + 32.0
        # temp_f = str(round(temp_f, 1)) # ROUND THE RESULT TO 1 PLACE AFTER THE DECIMAL, THEN CONVERT IT TO A STRING
        return temp_f

# Calibrated -10C


def read_temp_f_T1():
    lines = read_temp_raw_T1()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw_T1()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        # TEMP_STRING IS THE SENSOR OUTPUT, MAKE SURE IT'S AN INTEGER TO DO THE MATH
        temp_f = ((int(temp_string) / 1000.0) - 3) * 9.0 / 5.0 + 32.0
        # temp_f = str(round(temp_f, 1)) # ROUND THE RESULT TO 1 PLACE AFTER THE DECIMAL, THEN CONVERT IT TO A STRING
        return temp_f


def read_temp_f_T2():
    lines = read_temp_raw_T2()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw_T2()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        # TEMP_STRING IS THE SENSOR OUTPUT, MAKE SURE IT'S AN INTEGER TO DO THE MATH
        temp_f = (int(temp_string) / 1000.0) * 9.0 / 5.0 + 32.0
        # temp_f = str(round(temp_f, 1)) # ROUND THE RESULT TO 1 PLACE AFTER THE DECIMAL, THEN CONVERT IT TO A STRING
        return temp_f


while True:
    # print("TA " + str(read_temp_c_TA()) + "C")
    # print("T1 " + str(read_temp_c_T1()) + "C")
    # print("T2 " + str(read_temp_c_T2()) + "C")
    # print("reload")

    # lcd.message(repeat(" ", 1))
    # lcd.message("%s" %time.strftime("%H:%M"))
    # lcd.message("%s" %time.strftime("%m/%d"))
    lcd.clear()
    lcd.message(datetime.today().strftime("%I:%M%p"))
    lcd.message(repeat(" ", 1))
    if temp_selection == 1:
        GPIO.output(ledPinF, GPIO.LOW)
        GPIO.output(ledPinC, GPIO.HIGH)
        lcd.message("T1: " + str(round(read_temp_c_T1())) + chr(223) + "C")
    else:
        GPIO.output(ledPinF, GPIO.HIGH)
        GPIO.output(ledPinC, GPIO.LOW)
        lcd.message("T1: " + str(round(read_temp_f_T1())) + chr(223) + "F")
    lcd.message(" ")
    lcd.message("\n")
    if temp_selection == 1:
        lcd.message("A: " + str(round(read_temp_c_TA())) + chr(223) + "C")
    else:
        lcd.message("A: " + str(round(read_temp_f_TA())) + chr(223) + "F")
    lcd.message(repeat(" ", 1))
    if temp_selection == 1:
        lcd.message("T2: " + str(round(read_temp_c_T2())) + chr(223) + "C")
    else:
        lcd.message("T2: " + str(round(read_temp_f_T2())) + chr(223) + "F")
    time.sleep(60.0)