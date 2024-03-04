from PyQt5.QtCore import QObject, QThread
from PyQt5 import QtCore
import adi
import json
import numpy as np

class RX_Worker(QThread):
    def __init__(self, sdr, rx_data, parent=None):
        super(RX_Worker, self).__init__()

        self.sdr = sdr
        self.rx_data = rx_data

    def run(self):
        if self.sdr is None:
            print(f"Bad rx data:\nsdr: {self.sdr}\ndata: {self.rx_data}")
            return -1
        else:
            self.rx_data = self.sdr.rx()
        return 0
    
    def get_rx(self):
        return self.rx_data

class TX_Worker(QThread):
    def __init__(self, sdr, tx_data, parent=None):
        super(TX_Worker, self).__init__()

        self.sdr = sdr
        self.tx_data = tx_data

    def run(self):
        if self.sdr is None or self.tx_data is None:
            print(f"Bad tx data:\nsdr: {self.sdr}\ndata: {self.tx_data}")
            return -1
        else:
            self.sdr.tx(self.tx_data)
        return 0

class SDRCtrl(QObject): 
    def __init__(self, parent=None):
        json_data = json.load(open("config.json"))

        self.sdr = adi.ad9364(json_data["sdr_ip"])

        self.sample_rate = int(json_data["sample_rate_MHz"] * 1e6)
        self.center_freq = int(json_data["center_freq_MHz"] * 1e6)
        self.num_samps = int(json_data["num_samples"])

        self.sdr.gain_control_mode_chan0 = 'manual'
        self.sdr.rx_hardwaregain_chan0 = json_data["rx_gain_dB"]
        self.sdr.tx_hardwaregain_chan0 = json_data["tx_gain_dB"]

        self.sdr.sample_rate = self.sample_rate

        self.sdr.rx_rf_bandwidth = self.sample_rate
        self.sdr.tx_rf_bandwidth = self.sample_rate

        self.sdr.rx_lo = self.center_freq
        self.sdr.tx_lo = self.center_freq

        self.sdr.rx_buffer_size = self.num_samps

        self.tx_buffer = None
        self.rx_buffer = None

        self.tx_worker = TX_Worker(self.sdr, self.tx_buffer)
        self.rx_worker = RX_Worker(self.sdr, self.rx_buffer)

        self.start_rx_only_signal = QtCore.pyqtSignal()
        self.start_rx_tx_signal = QtCore.pyqtSignal()

        self.start_rx_only_signal.connect(self.rx_worker.start)

        self.start_rx_tx_signal.connect(self.rx_worker.start)
        self.start_rx_tx_signal.connect(self.tx_worker.start)

        self.rx_worker.finished.connect(self.rx_finished)

    @QtCore.pyqtSlot()
    def rx_finished(self):
        self.rx_buffer = self.rx_worker.get_rx()
    
    def get_rx(self) -> np.array:
        return self.rx_buffer
    
    def set_tx(self, tx_data: np.array) -> None:
        self.tx_buffer = tx_data

    def rx_only(self) -> None:
        self.start_rx_only_signal.emit()

    def rx_tx(self) -> None:
        self.start_rx_tx_signal.emit()