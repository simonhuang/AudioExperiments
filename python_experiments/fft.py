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
    
    plt.plot([norm(x) for x in transformedSignal[0:8000]])
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
    
audio_file = 'violin_notes/g_4.wav'

w = wave.open(audio_file)
'''
print "channels: ", w.getnchannels()
print "sample width: ", w.getsampwidth()
print "frame rate: ", w.getframerate()
print "number of frames: ", w.getnframes()
print (w.getframerate()/w.getnframes())
'''

np.set_printoptions(threshold=100)
file_info =  read_wav.read(audio_file)[1]
ch1 = map(lambda x: x[0], file_info)
ch2 = map(lambda x: x[1], file_info)

freqs = fft(ch1)
convert_fps = float(w.getframerate())/float(w.getnframes())
fps = map(lambda x: x * convert_fps, range(len(freqs)))
plt.plot(freqs)
