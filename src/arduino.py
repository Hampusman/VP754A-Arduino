import threading
import serial
import time
from tqdm import tqdm


class Arduino:
    def __init__(self):
        self._arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=.1)
        self._Vref = 3.3
        self._Voq = 2.5
        self._current_value = 0.0
        self._g = 0
        self.stop = threading.Event()

    def start(self) -> None:
        print('Arduino started')
        while not self.stop.is_set():
            self._current_value = self._read()
        print('Arduino stopped.')

    def _read(self) -> float:
        values = []
        while True:
            if self._arduino.in_waiting > 0:
                data = self._arduino.read_until(b'\n')
                try:
                    data = data.decode('ascii')
                    data = data.replace('<', '')
                    data = data.replace('>', '')
                    data = data.replace('\n', '')
                    if not 0 <= int(data) <= 1023:
                        continue
                    data = (float(data) / 1023) * self._Vref
                    values.append(data)
                except Exception:
                    continue
                if len(values) == 10:
                    break
            time.sleep(0.001)
        return values[-1]

    @property
    def current_value(self) -> float:
        return self._current_value

    def _calculate_current(self, Vout: float) -> float:
        pass

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
