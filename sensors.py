#!/usr/bin/python
import time
import os
import glob
from itertools import repeat
import Adafruit_DHT
import Adafruit_CharLCD as LCD

# Raspberry Pi pin configuration:
lcd_rs        = 26 
lcd_en        = 19
lcd_d4        = 13
lcd_d5        = 6
lcd_d6        = 5
lcd_d7        = 21
lcd_backlight = 4

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)

# ** Temperature Selection ** 0 = Fahrenheit, 1 = Celsius **
temp_selection = 0

#18B20 Temp. Probe
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

#CELSIUS CALCULATION
def read_temp_c():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = int(temp_string) / 1000.0 # TEMP_STRING IS THE SENSOR OUTPUT, MAKE SURE IT'S AN INTEGER TO DO THE MATH
        # temp_c = str(round(temp_c, 1)) # ROUND THE RESULT TO 1 PLACE AFTER THE DECIMAL, THEN CONVERT IT TO A STRING
        return temp_c

#FAHRENHEIT CALCULATION
def read_temp_f():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_f = (int(temp_string) / 1000.0) * 9.0 / 5.0 + 32.0 # TEMP_STRING IS THE SENSOR OUTPUT, MAKE SURE IT'S AN INTEGER TO DO THE MATH
        # temp_f = str(round(temp_f, 1)) # ROUND THE RESULT TO 1 PLACE AFTER THE DECIMAL, THEN CONVERT IT TO A STRING
        return temp_f

    #DHT11 on Pin17
def read_temp_c_dht():
    humidity, temperature = Adafruit_DHT.read_retry(11, 17)
    temp_c_dht = int(temperature)
    # temp_c_dht = str(temperature)
    return temp_c_dht

def read_temp_f_dht():
    humidity, temperature = Adafruit_DHT.read_retry(11, 17)
    temp_f_dht = int(temperature) * 9.0 / 5.0 + 32.0 #C -> F
    # temp_f_dht = str(temp_f_dht)
    return temp_f_dht

def read_humidity():
    humidity, temperature = Adafruit_DHT.read_retry(11, 17)
    rh = int(humidity)
    return rh

while True:

    #DHT11 on Pin17
    humidity, temperature = Adafruit_DHT.read_retry(11, 17)

    #Temp & Humidity
    if temp_selection == 1:
        lcd.message("AT: " + str(round(read_temp_c_dht())) + chr(223) + "C")
    else:
        lcd.message("AT: " + str(round(read_temp_f_dht())) + chr(223) + "F")
    
    lcd.message(" ")
    lcd.message("RH: " + str(round(read_humidity())) + "%")

    lcd.message("\n")
    if temp_selection == 1:
        lcd.message("TT: " + str(round(read_temp_c())) + chr(223) + "C")
    else:
        lcd.message("TT: " + str(round(read_temp_f())) + chr(223) + "F")

    lcd.message(repeat(" ", 2))

    #Time
    lcd.message("%s" %time.strftime("%H:%M"))

    lcd.message(repeat(" ", 1))

    # C Output
    # lcd.message("Temp: " + read_temp_c() + chr(223) + "C" )
    # F Output
    # lcd.message("Temp: " + read_temp_f() + chr(223) + "F" )
    # lcd.message("\n")
    # lcd.message("Humidity: %d%%" % humidity)
    # lcd.message("   ")

    # print ("Time: %s" %time.strftime("%H:%M:%S"))
    # print (str(read_temp_c()) + "C")
    # print (str(round(read_temp_f(), 1)) + "F")
    # print ("DHT11: Temp: " + str(temperature) + " " + str(humidity) + "%")

    time.sleep(30)
