import cmath as cm
import numpy as np
import matplotlib.pyplot as plt
import wave
import scipy.io.wavfile as read_wav
import note_info as notes

# roots of unity
def omega(p, q):
    return cm.exp((2.0 * cm.pi * 1j * q) / p)

# fix for fft_custom if signal length is not a power of 2
def pad(signal):
    k = 0
    while 2**k < len(signal):
        k += 1
    return signal + ([0] * (2**k - len(signal)))

# custom fft in python
def fft(signal):
    n = len(signal)
    if n == 1:
        return signal
    else:
        f_even    = fft([signal[i] for i in range(0, n, 2)])
        f_odd     = fft([signal[i] for i in range(1, n, 2)])
        combined  = [0] * n
        
        for m in range(n/2):
            combined[m] = f_even[m] + omega(n, -m) * f_odd[m]
            combined[m + n/2] = f_even[m] - omega(n, -m) * f_odd[m]
        return combined

# find norm of complex number
norm = lambda x: cm.polar(x)[0]

# fft from numpy library
def fft(signal):
    transformed_signal = np.fft.fft(signal)
    return [norm(x) for x in transformed_signal]

# binary search to find frequency for max freq for hearing (22kHz)
def binary_search(lst, val, low, high):
    if (high <= low):
        return low
    middle = low + (high - low) / 2
    if (lst[middle] == val):
        return middle
    elif (lst[middle] < val):
        return binary_search(lst, val, middle + 1, high)
    else:
        return binary_search(lst, val, low, middle)

# read audio file
audio_file = 'trumpet/trumpet-G3.wav'

w = wave.open(audio_file)

'''
# meta data
print "channels: ", w.getnchannels()
print "sample width: ", w.getsampwidth()
print "frame rate: ", w.getframerate()
print "number of frames: ", w.getnframes()
print (w.getframerate()/w.getnframes())
print "channels: ", w.getnchannels()
'''

np.set_printoptions(threshold=100)
file_info =  read_wav.read(audio_file)[1]

chs = []
#print file_info

# run fft on first channel if there are multiple
if (w.getnchannels() == 1):
    corr = fft(file_info)
else:   
    for i in range(w.getnchannels()):
        chs.append(map(lambda x: x[i], file_info))
    corr = fft(chs[0])

# get actual frequencies that will be mapped to coefficients
convert_fps = float(w.getframerate())/float(w.getnframes())
freqs = map(lambda x: x * convert_fps, range(len(corr)))

# truncate factors for normal notes
upper_limit = binary_search(freqs, notes.splits[-1], 0, len(freqs))
lower_limit = binary_search(freqs, notes.splits[0], 0, len(freqs))

# truncate
corr = np.asarray(corr[lower_limit:upper_limit])
freqs = np.asarray(freqs[lower_limit:upper_limit])

mean = np.mean(corr)
std = np.std(corr)

# isolate potential peaks using mean and std
peak_corr = []
peak_freqs = []
for i, f in np.ndenumerate(corr):
    if (f > mean + std):
        peak_corr.append(corr[i])
        peak_freqs.append(freqs[i])

# find notes based on frequencies and peaks
note_indices = []
index = 0
magnitudes = [0] * len(notes.freqs)
for i, s in enumerate(notes.splits[1:]):
    max = 0
    while (peak_freqs[index] < s ):
        if (peak_corr[index] > max):
            max = peak_corr[index]
        index = index + 1
        if (index >= len(peak_freqs)):
            break
    if (index >= len(peak_freqs)):
        break
    magnitudes[i] = max

# print notes that are present
for i, m in enumerate(magnitudes):
    if (m > 0):
        print notes.info[i][0],
print


print peak_freqs[0:10]
print peak_corr[0:10]
   
plt.figure(figsize=(16,4))
plt.xlim(xmax = 1500)
plt.plot(peak_freqs, peak_corr)
