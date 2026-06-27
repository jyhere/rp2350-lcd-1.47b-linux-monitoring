# Changelog

## 1.1 (2026-06-27)

- Scaled text rendering (2× larger via `write_text()`)
- Display orientation flip via `FLIPPED` constant in `main.py`
- Auto-reconnect in `pc_monitor.py` when Pico is unplugged/replugged
- Removed unsupported `°` character from temperature display
- Added `write_text(str, x, y, size, color)` to LCD class

## 1.0 (2026-06-27)

- Initial release
- PC monitoring over USB serial
- LCD driver for Waveshare RP2350-LCD-1.47-B
