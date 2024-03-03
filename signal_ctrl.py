from PyQt5.QtCore import QObject, QThread
from sdr_ctrl import SDRCtrl

import numpy as np

class SignalCtrl(QObject):
    def __init__(self, parent=None):
        sdr = SDRCtrl()
        tx_signal = np.array()
        rx_signal = np.array()