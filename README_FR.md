# RP2350 PC Monitor

Surveillez les ressources de votre PC (CPU, RAM, réseau, température) sur un écran Waveshare RP2350-LCD-1.47-B.

![status](https://img.shields.io/badge/status-fonctionnel-brightgreen)

## Matériel

- **Carte** : [Waveshare RP2350-LCD-1.47-B](https://www.waveshare.com/rp2350-lcd-1.47-b.htm) (RP2350 + écran 1.47" 172×320 ST7789V3)
- **Connexion** : USB série

## Fonctionnalités

- Utilisation et température du CPU
- Utilisation de la RAM
- Nombre de processus actifs
- Débit réseau montant/descendant (Ko/s)
- Horodatage

## Fichiers

| Fichier | Description |
|---------|-------------|
| `main.py` | Firmware MicroPython — pilote l'écran, parse le JSON reçu sur le port série |
| `pc_monitor.py` | Script Python côté PC — récupère les métriques système, envoie du JSON via USB série |

## Brochage

| Pin LCD | GPIO |
|---------|------|
| DC | 16 |
| CS | 17 |
| SCLK | 18 |
| MOSI | 19 |
| RST | 20 |
| BL  | 21 (PWM) |

Utilise le bus **SPI0**.

## Installation

### 1. Flasher MicroPython

Maintenez BOOTSEL en branchant le Pico 2, puis copiez le fichier UF2 :
https://micropython.org/download/RPI_PICO2/

### 2. Envoyer `main.py`

```bash
rshell -p /dev/ttyACM0 cp main.py /pyboard/main.py
```

### 3. Lancer le moniteur PC

```bash
pip install pyserial psutil
python pc_monitor.py
```

## Fonctionnement

`pc_monitor.py` interroge `psutil` toutes les 0,5 s et envoie une ligne JSON sur le port série USB :

```json
{"time":"14:32:01","cpu":"23%","temp":"45.0°C","ram":"67%","proc":312,"up":"0.5K","down":"1.2K"}
```

`main.py` parse le JSON et l'affiche sur l'écran via `framebuf`.
