import adi

import numpy as np
import matplotlib.pyplot as plt


# Create a device interface
sdr = adi.ad9364("ip:192.168.70.60")

sample_rate = 60e6  # Hz
center_freq = 5.1e9 # Hz
num_samps = 10000   # number of samples returned per call to rx()

sdr.gain_control_mode_chan0 = 'manual'

sdr.rx_hardwaregain_chan0 = 0.0 # dB
sdr.rx_lo = int(center_freq)
sdr.sample_rate = int(sample_rate)
sdr.rx_rf_bandwidth = int(sample_rate) # filter width, just set it to the same as sample rate for now
sdr.rx_buffer_size = num_samps

sdr.tx_rf_bandwidth = int(sample_rate) # filter cutoff, just set it to the same as sample rate
sdr.tx_lo = int(center_freq)
sdr.tx_hardwaregain_chan0 = -80 # Increase to increase tx power, valid range is -90 to 0 dB

t = np.arange(num_samps)/sample_rate
samples = 0.5*np.exp(2.0j*np.pi*100e3*t) # Simulate a sinusoid of 100 kHz, so it should show up at 915.1 MHz at the receiver
samples *= 2**14 # The PlutoSDR expects samples to be between -2^14 and +2^14, not -1 and +1 like some SDRs

samples_rx = sdr.rx() # receive samples off Pluto

fft_rx = np.fft.fftshift(np.fft.fft(samples_rx))

plt.plot(fft_rx)
plt.show()