# RP2350 PC Monitor

Monitor PC resource usage (CPU, RAM, network, temps) on a Waveshare RP2350-LCD-1.47-B display.

![demo](https://img.shields.io/badge/status-working-brightgreen)

## Hardware

- **Board**: [Waveshare RP2350-LCD-1.47-B](https://www.waveshare.com/rp2350-lcd-1.47-b.htm) (RP2350 + 1.47" 172×320 ST7789V3 LCD)
- **Connection**: USB serial

## Features

- CPU usage & temperature
- RAM usage
- Active process count
- Network upload/download speed (KB/s)
- Timestamp

## Files

| File | Description |
|------|-------------|
| `main.py` | MicroPython firmware — drives the LCD, parses JSON over serial |
| `pc_monitor.py` | Python script — gathers PC metrics, sends JSON over USB serial |

## Pinout

| LCD Pin | GPIO |
|---------|------|
| DC | 16 |
| CS | 17 |
| SCLK | 18 |
| MOSI | 19 |
| RST | 20 |
| BL  | 21 (PWM) |

Uses **SPI0**.

## Setup

### 1. Flash MicroPython

Hold BOOTSEL while connecting the Pico 2, then copy the UF2:
https://micropython.org/download/RPI_PICO2/

### 2. Upload `main.py`

```bash
rshell -p /dev/ttyACM0 cp main.py /pyboard/main.py
```

### 3. Run the PC monitor

```bash
pip install pyserial psutil
python pc_monitor.py
```

## How it works

`pc_monitor.py` polls `psutil` every 0.5 s and sends a JSON line over USB serial:

```json
{"time":"14:32:01","cpu":"23%","temp":"45.0°C","ram":"67%","proc":312,"up":"0.5K","down":"1.2K"}
```

`main.py` parses the JSON and renders it on the LCD using `framebuf`.
