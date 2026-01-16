import threading
import serial
import time
from tqdm import tqdm


class Arduino:
    def __init__(self):
        self._arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=1)
        self._arduino.flush()
        self._latest_values = ''
        self._stop = threading.Event()
        self._worker = threading.Thread(target=self._update_values, daemon=True)
        self._worker.start()

    def _update_values(self) -> None:
        while not self._stop.is_set():
            if self._arduino.in_waiting > 0:
                data = self._arduino.read_until(b'\n')
                try:
                    data = data.decode('ascii').strip()
                    self._latest_values = data
                except Exception:
                    continue
            time.sleep(0.001)

    @property
    def value(self) -> str:
        return self._latest_values

    def stop(self):
        self._stop.set()

    def debug(self) -> None:
        reads = []
        index = {}
        sent_anomalies = []
        for _ in tqdm(range(1000)):
            values = []
            while True:
                if self._arduino.in_waiting > 0:
                    data = self._arduino.read_until(b'\n')
                    try:
                        data = data.decode('ascii')
                        data = data.replace('<', '')
                        data = data.replace('>', '')
                        data = data.replace('\n', '')
                        if not 0 < int(data) < 1024:
                            continue
                        data = (float(data) / 1023) * self._Vref
                        values.append(data)
                    except Exception:
                        sent_anomalies.append(data)
                        continue
                    if len(values) == 1000:
                        reads.append(values)
                        break
                time.sleep(0.001)
            time.sleep(0.01)
        anomalies = []
        for i, read in enumerate(reads):
            for j, value in enumerate(read):
                if not 2 < value < 3:
                    anomalies.append(value)
                    index[i] = j
        print(f'Number of sent anomalies: {len(sent_anomalies)}')
        print(f'Sent anomalies: {sent_anomalies}')
        print(f'Number of anomalies: {len(anomalies)}')
        print(f'Anomalies: {anomalies}')
        if len(reads) + len(values) <= 100:
            for read in reads:
                print(read)
        print(f'Indexes: {index}')
