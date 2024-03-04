from PyQt5.QtCore import QObject
from sdr_ctrl import SDRCtrl
import json

import numpy as np

class SignalCtrl(QObject):
    def __init__(self, parent=None) -> None:
        self.sdr_control = None

        json_data = json.load(open("config.json"))
        self.signals = {
            obj: 
            (
                json_data["signals"][obj]["name"],
                json_data["signals"][obj]["seq_type"],
                json_data["signals"][obj]["txt_path"]
            )
            for obj in json_data["signals"]
            }

        self.tx_signal = None
        self.rx_signal = None
    
    def set_tx(self, tx_signal: np.array) -> None:
        self.tx_signal = tx_signal
    
    def get_rx(self) -> np.array:
        self.rx_signal = self.sdr_control.get_rx()
    
    def set_tx_from_list(self, signal_name: str) -> None:
        pass

    def get_signal_list(self) -> dict:
        return self.signals
    
    def listen(self) -> int:
        if self.sdr_control is None:
            try:
                self.sdr_control = SDRCtrl()
            except:
                print("SDR Control can't create")
                return -1
        return 0

    def send_and_listen(self) -> int:
        if self.sdr_control is None:
            try:
                self.sdr_control = SDRCtrl()
            except:
                print("SDR Control can't create")
                return -1
        return 0

    def imitate(self, sigma: int, delay: int) -> None :
        noise_complex = np.random.normal(size=len(self.rx_signal))*np.exp(-1j*2*np.pi*np.random.randn(len(self.rx_signal)))
        noise_complex = sigma*noise_complex/(max(noise_complex.real) + 1j*max(noise_complex.imag))
