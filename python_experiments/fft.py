import cmath as cm
import numpy as np
import matplotlib.pyplot as plt
import wave
import scipy.io.wavfile as read_wav

def omega(p, q):
    return cm.exp((2.0 * cm.pi * 1j * q) / p)

def pad(signal):
    k = 0
    while 2**k < len(signal):
        k += 1
    return signal + ([0] * (2**k - len(signal)))

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

def ifft(signal):
    time_signal = fft([x.conjugate() for x in signal])
    return [x.conjugate()/len(signal) for x in time_signal]

norm = lambda x: cm.polar(x)[0]

def fft_custom(signal):
    transformedSignal = np.array(fft(pad(signal)))
    
    plt.plot([norm(x) for x in transformedSignal])
    plt.show()
    
    cleanedSignal = ifft(transformedSignal)
    return np.array(cleanedSignal, dtype=np.float64)


def fft_clean(signal):
    transformedSignal = np.fft.fft(signal)
    
    cleanedSignal = np.fft.ifft(transformedSignal)
    return np.array(cleanedSignal, dtype=np.float64)

def fft(signal):
    transformedSignal = np.fft.fft(signal)
    return [norm(x) for x in transformedSignal]


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
    
audio_file = 'trumpet/trumpet-G5.wav'

w = wave.open(audio_file)
'''
print "channels: ", w.getnchannels()
print "sample width: ", w.getsampwidth()
print "frame rate: ", w.getframerate()
print "number of frames: ", w.getnframes()
print (w.getframerate()/w.getnframes())
'''
print "channels: ", w.getnchannels()
np.set_printoptions(threshold=100)
file_info =  read_wav.read(audio_file)[1]

chs = []
print file_info

if (w.getnchannels() == 1):
    freqs = fft(file_info)
else:   
    for i in range(w.getnchannels()):
        chs.append(map(lambda x: x[i], file_info))
    freqs = fft(chs[0])


convert_fps = float(w.getframerate())/float(w.getnframes())
fps = map(lambda x: x * convert_fps, range(len(freqs)))

upper_limit = binary_search(fps, 3000, 0, len(fps))

plt.figure(figsize=(16,4))
plt.plot(fps[0:upper_limit], freqs[0:upper_limit])
