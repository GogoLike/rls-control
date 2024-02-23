# Import the library
import adi
import numpy as np
import matplotlib.pyplot as plt

# Create a device interface
sdr = adi.ad9364("ip:192.168.70.60")

sample_rate = 0.6e6  # Hz
center_freq = 433.5e6 # Hz
num_samps = 10000   # number of samples returned per call to rx()

sdr.gain_control_mode_chan0 = 'manual'

sdr.tx_rf_bandwidth = int(sample_rate)
sdr.tx_lo = int(center_freq)
sdr.tx_hardwaregain_chan0 = -80.0

sdr.rx_hardwaregain_chan0 = 0.0 # dB
sdr.rx_lo = int(center_freq)
sdr.sample_rate = int(sample_rate)
sdr.rx_rf_bandwidth = int(sample_rate) # filter width, just set it to the same as sample rate for now
sdr.rx_buffer_size = num_samps

num_symbols = 1000
x_int = np.array([np.mod(_, 2) for _ in range(num_symbols)]) # 0 to 2
x_degrees = x_int*360/2
x_radians = x_degrees*np.pi/180.0 # sin() and cos() takes in radians
x_symbols = np.cos(x_radians) + 1j*np.sin(x_radians)
samples_tx = np.repeat(x_symbols, 16)
samples_tx *= 2**14 # The PlutoSDR expects samples to be between -2^14 and +2^14, not -1 and +1 like some SDRs

sdr.tx_cyclic_buffer = True # Enable cyclic buffers
sdr.tx(samples_tx)

samples_rx = sdr.rx() # receive samples off Pluto

# Stop transmitting
sdr.tx_destroy_buffer()

plt.plot(samples_rx[:1000])
plt.show()

fft_samp = np.fft.fftshift(np.fft.fft(samples_rx))

plt.plot(fft_samp)
plt.show()