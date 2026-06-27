import sys
import select
import json
from machine import Pin, SPI, PWM
import framebuf
import time

DC = 16
CS = 17
SCLK = 18
MOSI = 19
RST = 20
BL = 21
FLIPPED = True


class LCD_1inch47(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 320
        self.height = 172
        self.flipped = False

        self.cs = Pin(CS, Pin.OUT)
        self.rst = Pin(RST, Pin.OUT)

        self.cs(1)
        self.spi = SPI(0, 100000_000, polarity=0, phase=0,
                       sck=Pin(SCLK), mosi=Pin(MOSI), miso=None)
        self.dc = Pin(DC, Pin.OUT)
        self.dc(1)

        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        self.set_orientation(FLIPPED)

    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        self.rst(1)
        self.rst(0)
        self.rst(1)

        self.write_cmd(0x36)
        self.write_data(0x70)

        self.write_cmd(0x3A)
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x13)

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F)

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        self.write_data(0xF0)
        self.write_data(0x00)
        self.write_data(0x04)
        self.write_data(0x04)
        self.write_data(0x05)
        self.write_data(0x29)
        self.write_data(0x33)
        self.write_data(0x3E)
        self.write_data(0x38)
        self.write_data(0x12)
        self.write_data(0x12)
        self.write_data(0x28)
        self.write_data(0x30)

        self.write_cmd(0xE1)
        self.write_data(0xF0)
        self.write_data(0x07)
        self.write_data(0x0A)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x07)
        self.write_data(0x28)
        self.write_data(0x33)
        self.write_data(0x3E)
        self.write_data(0x36)
        self.write_data(0x14)
        self.write_data(0x14)
        self.write_data(0x29)
        self.write_data(0x23)

        self.write_cmd(0x21)
        self.write_cmd(0x11)
        self.write_cmd(0x29)

    def set_orientation(self, flipped):
        self.flipped = flipped
        self.write_cmd(0x36)
        self.write_data(0xB0 if flipped else 0x70)

    def write_text(self, s, x, y, size, color):
        tw = len(s) * 8
        temp = bytearray(tw * 8 * 2)
        fb = framebuf.FrameBuffer(temp, tw, 8, framebuf.RGB565)
        fb.fill(0)
        fb.text(s, 0, 0, 0xFFFF)
        for ty in range(8):
            for tx in range(tw):
                idx = (ty * tw + tx) * 2
                if temp[idx] or temp[idx + 1]:
                    self.fill_rect(x + tx * size, y + ty * size, size, size, color)

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0x3F)

        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x22)
        self.write_data(0x00)
        self.write_data(0xCD)

        self.write_cmd(0x2C)

        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)


pwm = PWM(Pin(BL))
pwm.freq(1000)
pwm.duty_u16(32768)

lcd = LCD_1inch47()

lcd.fill(0xFFFF)
lcd.show()
time.sleep(0.3)
lcd.fill(0x0000)
lcd.show()

WHITE = 0xFFFF
BLACK = 0x0000
RED = 0x07E0
GREEN = 0x001F
BLUE = 0xF800
GRAY = 0x8410

print("RP2350 initialized and listening...")

while True:
    if select.select([sys.stdin], [], [], 0.05)[0]:
        line = sys.stdin.readline().strip()
        try:
            stats = json.loads(line)

            lcd.fill(BLACK)

            lcd.write_text("=== PC MONITOR ===", 16, 2, 2, BLUE)
            lcd.write_text("TIME: " + stats['time'], 10, 22, 2, WHITE)
            lcd.write_text("CPU: " + stats['cpu'] + "  " + stats['temp'], 10, 48, 2, GREEN)
            lcd.write_text("RAM: " + stats['ram'], 10, 66, 2, GREEN)
            lcd.write_text("PROC: " + str(stats['proc']), 10, 92, 2, WHITE)
            lcd.write_text("NET DL: " + stats['down'] + "/s", 10, 110, 2, RED)
            lcd.write_text("NET UP: " + stats['up'] + "/s", 10, 128, 2, RED)

            lcd.hline(0, 42, 320, GRAY)
            lcd.hline(0, 86, 320, GRAY)

            lcd.show()

        except Exception:
            pass
