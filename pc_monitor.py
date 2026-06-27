import time
import json
import datetime
import psutil
import serial

SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 115200

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to RP2350 on {SERIAL_PORT}")
except Exception as e:
    print(f"Connection error: {e}")
    exit()

# Initialize network counters for delta calculation
old_net = psutil.net_io_counters()

while True:
    # Date & Heure
    now = datetime.datetime.now().strftime("%H:%M:%S")

    # CPU & RAM
    cpu_per = psutil.cpu_percent(interval=0.5)
    # Température (Dépend du matériel, peut nécessiter des ajustements sous Windows)
    try:
        temps = psutil.sensors_temperatures()
        cpu_temp = temps['coretemp'][0].current if 'coretemp' in temps else 0
    except:
        cpu_temp = 0 # Alternative simplifiée si non supporté en natif

    ram = psutil.virtual_memory()

    # Processus
    proc_count = len(psutil.pids())

    # Réseau (Calcul du débit)
    new_net = psutil.net_io_counters()
    sent = (new_net.bytes_sent - old_net.bytes_sent) / 1024 / 0.5 # KB/s
    recv = (new_net.bytes_recv - old_net.bytes_recv) / 1024 / 0.5 # KB/s
    old_net = new_net

    # Formatage des données en JSON (simple à décoder)
    data = {
        "time": now,
        "cpu": f"{cpu_per}%",
        "temp": f"{cpu_temp}°C" if cpu_temp else "N/A",
        "ram": f"{ram.percent}%",
        "proc": proc_count,
        "up": f"{sent:.1f}K",
        "down": f"{recv:.1f}K"
    }

    # Envoi via le port Série
    payload = json.dumps(data) + "\n"
    ser.write(payload.encode('utf-8'))

    time.sleep(0.5) # Mise à jour toutes les secondes (0.5s d'intervalle CPU + pause)