#
# Thermostat.py – Completed Final Project Code
#

from time import sleep
from datetime import datetime
from statemachine import StateMachine, State
import board
import adafruit_ahtx0
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import serial
from gpiozero import Button, PWMLED
from threading import Thread
from math import floor

DEBUG = True

# I2C + Sensor
i2c = board.I2C()
thSensor = adafruit_ahtx0.AHTx0(i2c)

# UART
ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# LEDs
redLight = PWMLED(18)
blueLight = PWMLED(23)

# LCD Manager
class ManagedDisplay():
    def __init__(self):
        self.lcd_rs = digitalio.DigitalInOut(board.D17)
        self.lcd_en = digitalio.DigitalInOut(board.D27)
        self.lcd_d4 = digitalio.DigitalInOut(board.D5)
        self.lcd_d5 = digitalio.DigitalInOut(board.D6)
        self.lcd_d6 = digitalio.DigitalInOut(board.D13)
        self.lcd_d7 = digitalio.DigitalInOut(board.D26)

        self.lcd_columns = 16
        self.lcd_rows = 2
        self.lcd = characterlcd.Character_LCD_Mono(
            self.lcd_rs, self.lcd_en,
            self.lcd_d4, self.lcd_d5, self.lcd_d6, self.lcd_d7,
            self.lcd_columns, self.lcd_rows
        )
        self.lcd.clear()

    def cleanupDisplay(self):
        self.lcd.clear()
        self.lcd_rs.deinit()
        self.lcd_en.deinit()
        self.lcd_d4.deinit()
        self.lcd_d5.deinit()
        self.lcd_d6.deinit()
        self.lcd_d7.deinit()

    def clear(self):
        self.lcd.clear()

    def updateScreen(self, message):
        self.lcd.clear()
        self.lcd.message = message

screen = ManagedDisplay()

# STATE MACHINE
class TemperatureMachine(StateMachine):
    off = State(initial=True)
    heat = State()
    cool = State()

    setPoint = 72

    cycle = (
        off.to(heat) |
        heat.to(cool) |
        cool.to(off)
    )

    def on_enter_heat(self):
        blueLight.off()
        if DEBUG: print("* Changing state to heat")

    def on_exit_heat(self):
        redLight.off()

    def on_enter_cool(self):
        redLight.off()
        if DEBUG: print("* Changing state to cool")

    def on_exit_cool(self):
        blueLight.off()

    def on_enter_off(self):
        redLight.off()
        blueLight.off()
        if DEBUG: print("* Changing state to off")

    def processTempStateButton(self):
        if DEBUG: print("Cycling Temperature State")
        self.cycle()

    def processTempIncButton(self):
        if DEBUG: print("Increasing Set Point")
        self.setPoint += 1
        self.updateLights()

    def processTempDecButton(self):
        if DEBUG: print("Decreasing Set Point")
        self.setPoint -= 1
        self.updateLights()

    def updateLights(self):
        temp = floor(self.getFahrenheit())
        redLight.off()
        blueLight.off()

        if DEBUG:
            print(f"State: {self.current_state.id}")
            print(f"SetPoint: {self.setPoint}")
            print(f"Temp: {temp}")

        if self.is_off:
            return

        if self.is_heat:
            if temp < self.setPoint:
                redLight.pulse(fade_in_time=1, fade_out_time=1, background=True)
            else:
                redLight.on()
            return

        if self.is_cool:
            if temp > self.setPoint:
                blueLight.pulse(fade_in_time=1, fade_out_time=1, background=True)
            else:
                blueLight.on()
            return

    def run(self):
        Thread(target=self.manageMyDisplay).start()

    def getFahrenheit(self):
        t = thSensor.temperature
        return ((9/5) * t) + 32

    def setupSerialOutput(self):
        state = self.current_state.id
        temp = floor(self.getFahrenheit())
        output = f"{state},{temp},{self.setPoint}"
        return output

    endDisplay = False

    def manageMyDisplay(self):
        counter = 1
        altCounter = 1
        while not self.endDisplay:
            current_time = datetime.now()
            lcd_line_1 = current_time.strftime("%m/%d %H:%M:%S") + "\n"

            if altCounter < 6:
                temp = floor(self.getFahrenheit())
                lcd_line_2 = f"Temp: {temp:3d}F".ljust(16)
                altCounter += 1
            else:
                state = self.current_state.id
                lcd_line_2 = f"{state.upper():4s} SP:{self.setPoint:3d}".ljust(16)
                altCounter += 1
                if altCounter >= 11:
                    self.updateLights()
                    altCounter = 1

            screen.updateScreen(lcd_line_1 + lcd_line_2)

            if (counter % 30) == 0:
                ser.write((self.setupSerialOutput() + "\n").encode('utf-8'))
                counter = 1
            else:
                counter += 1

            sleep(1)

        screen.cleanupDisplay()

# Instantiate machine
tsm = TemperatureMachine()
tsm.run()

# BUTTONS
greenButton = Button(24)
greenButton.when_pressed = tsm.processTempStateButton

redButton = Button(25)
redButton.when_pressed = tsm.processTempIncButton

blueButton = Button(12)
blueButton.when_pressed = tsm.processTempDecButton

repeat = True

while repeat:
    try:
        sleep(30)
    except KeyboardInterrupt:
        print("Cleaning up. Exiting...")
        repeat = False
        tsm.endDisplay = True
        sleep(1)
