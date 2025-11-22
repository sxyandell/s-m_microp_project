#- Audio Signal Filtering by Sudiksha Shailesh Sawant -

import numpy as np
import sounddevice as sd
import scipy.signal as signal
import matplotlib.pyplot as plt
import math
import soundfile as sf
import wave
import contextlib

def design_fir_lpf(fpass, fstop, fs, numtaps):
    nyquist = fs / 2

    bands = [0, fpass, fstop, nyquist]
    desired = [1, 0]
    taps = signal.remez(numtaps, bands, desired, fs=fs)
    return taps
def apply_filter(x, h):
    return signal.lfilter(h, 1.0, x)
def mse_psnr(original, filtered):
    min_len = min(len(original), len(filtered))
    original = original[:min_len]
    filtered = filtered[:min_len]
    mse = np.mean((original - filtered) ** 2)
    if mse == 0:
        psnr = float('inf')
    else:
        psnr = 20 * math.log10(np.max(np.abs(original)) / math.sqrt(mse))
    return mse, psnr
# NEW: Function to plot FIR filter frequency response
def plot_filter_response(h, fs, fpass, fstop):
    w, H = signal.freqz(h, worN=8000)
    freqs = w * fs / (2 * np.pi)
    plt.figure(figsize=(8, 4))
    plt.plot(freqs, np.abs(H), 'b', linewidth=1.5, label="FIR LPF Response")
    plt.axvline(fpass, color='g', linestyle='--', label="Passband Edge")
    plt.axvline(fstop, color='r', linestyle='--', label="Stopband Edge")
    plt.title("FIR Low Pass Filter Frequency Response")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    plt.show()

# === MAIN EXPERIMENT ===
cutOffFreqs = [200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600]
# cutOffFreqs = [400]
cutOffFrequency = 400
numtaps = 51
audio_file_path = "filter/Beethoven - Ode To Joy ｜ EASY Piano Tutorial.wav"
recording, Fs = sf.read(audio_file_path)
x = recording.flatten()
x = x / np.max(np.abs(x))
# [taps_200, taps_400, taps_600, taps_800, taps_1000, taps_1200, taps_1400] = [[], [], [], [], [], [], []]
# tapsarr = [taps_200, taps_400, taps_600, taps_800, taps_1000, taps_1200, taps_1400]
tapsarr = [[] for i in range(numtaps)]
print(f"tapsarr: {tapsarr}")

for i in range(len(cutOffFreqs)):
    cutOffFrequency = cutOffFreqs[i]
    Fpass = cutOffFrequency
    Fstop = Fpass + 500
    freqRatio = (cutOffFrequency/Fs)

    nyq_rate = Fs / 2.0

    # 5 Hz transition width.
    width = 450.0/nyq_rate
    # The desired attenuation in the stop band, in dB.
    ripple_db = 15
    # Compute the order and Kaiser parameter for the FIR filter.
    N, beta = signal.kaiserord(ripple_db, width)
    # The cutoff frequency of the filter.
    # print(N)
    # Use firwin with a Kaiser window to create a lowpass FIR filter.
    # h = signal.firwin(numtaps, cutOffFrequency/nyq_rate, window=('kaiser', beta))
    h = signal.firwin(numtaps, cutOffFrequency/nyq_rate, pass_zero = 'lowpass')

    # N = int(math.sqrt(0.196196 + freqRatio**2)/freqRatio)
    # b, a = signal.butter(numtaps, cutOffFrequency, 'low', fs=44000)
    # print(f"a = {a}")
    # print(f"b = {b}")
    # h = design_fir_lpf(Fpass, Fstop, Fs, numtaps)
    # print(f"taps: {h}")
    # print(np.sum(h))

    # hnew = h*(1/np.sum(h))
    # print(hnew)
    # print(np.sum(hnew))
    y = apply_filter(x, h)
    # y = signal.lfilter(b, a, x)
    filtered_file_path = f'filter/filteredOde_{cutOffFrequency}.wav'
    # print(f"saving to {filtered_file_path}")
    # sf.write(filtered_file_path, y[::2], Fs)

    # plt.figure(i)
    # w, h = signal.freqz(h, worN=8000)
    # plt.subplot(3, 1, 1); plt.title("Frequency response for Filter"); plt.ylabel('Gain'); plt.xlabel('Frequency'); plt.plot(np.log((w/np.pi)*(Fs/2)), np.log(abs(h)), linewidth=2)
    # plt.subplot(3, 1, 2); plt.title("Original Signal"); plt.plot(np.log(np.fft.rfftfreq(len(x), 1 / Fs)), -20*np.log(np.abs(np.fft.rfft(x))), 'g'); plt.xlabel('Freq (Hz)'); plt.ylabel('|original|')
    # plt.subplot(3, 1, 3); plt.title("Filtered Signal, python lib"); plt.plot(np.log(np.fft.rfftfreq(len(y), 1 / Fs)), -20*np.log(np.abs(np.fft.rfft(y))), 'r'); plt.xlabel('Freq (Hz)'); plt.ylabel('|library filtered|')

    for i in range(numtaps):
        tapsarr[i].append(h[i].round(decimals=5).item())
        
plt.show()

taplabels = []
# print(tapsarr)
# for taplist in tapsarr:
for i in range(numtaps):
    # print(taplist)
    plt.scatter(cutOffFreqs, tapsarr[i])
    # (a, b, c, d) = np.polyfit(cutOffFreqs, tapsarr[i], 3)
    # (a, b) = np.polyfit(cutOffFreqs, tapsarr[i], 1)
    (a, b, c) = np.polyfit(cutOffFreqs, tapsarr[i], 2)
    # print(a)
    # print(b)
    # print(c)
    # print(d)
    # plt.plot(cutOffFreqs, [a*freq for freq in cutOffFreqs] + b)
    plt.plot(cutOffFreqs, [(a*freq**2 + b*freq + c) for freq in cutOffFreqs] + b)

    # plt.plot(cutOffFreqs, [(a*freq**3 + b*freq**2 + c*freq + d) for freq in cutOffFreqs])

    # plt.text(1, max(tapsarr[i]) - i, f'tap = {a}*cutOffFreq + {b}')
    # plt.plot(tapsarr[i])
    # print(cutOffFreqs)
    # print(taplist)
    # print(f"taps b{i} accross freqs: {tapsarr[i]}")
    # print(f"b{i}: tap = {a}*cutOffFreq**3 + {b}*cutOffFreq**2 + {c}*cutOffFreq + {d}")
    # print(f"b{i}: tap = {a}*cutOffFreq + {b}")
    print(f"taps[{i}] = {a}*cutOffFreq**2 + {b}*cutOffFreq + {c}")

    # taplabels.append(f"b{i}")
    taplabels.append(f"tap = {a}*cutOffFreq + {b}")
    
print(cutOffFreqs)
# taplabels = [f"b{i}" for i in range(numtaps)]
# print(taplabels)
# plt.legend(taplabels)
# plt.legend(['tap1', 'tap2', 'tap3', 'tap4', 'tap5', 'tap6', 'tap7'])
plt.xlabel('cutoff frequency (Hz)')
plt.ylabel('taps (b_i)')
plt.show()





# #     # order = 4  # Filter order
# #     # cutoff = 800  # Cutoff frequency in Hz
# b, a = signal.butter(numtaps, cutOffFrequency, 'low', fs=44000)
# arr = signal.butter(numtaps, cutOffFrequency, 'low', fs=44000, output='sos') 
# print(b)
# print(a)
# print(arr)


# # Plot signals
# plt.figure(figsize=(10, 6))
# plt.subplot(3, 1, 1); plt.title(f"Case {case} - Original Signal"); plt.plot(x, 'r')
# plt.subplot(3, 1, 2); plt.title("Noisy Signal"); plt.plot(x)
# plt.subplot(3, 1, 3); plt.title("Filtered Signal"); plt.plot(y, 'g')
# plt.tight_layout()
# plt.show()


# # Source - https://stackoverflow.com/a
# # Posted by piercus, modified by community. See post 'Timeline' for change history
# # Retrieved 2025-11-16, License - CC BY-SA 4.0
# # low pass filter code! running average, which I think is simplified case of FIR... can mess around and maybe hardcode the taps

# import matplotlib.pyplot as plt
# import numpy as np
# import wave
# import sys
# import math
# import contextlib
# from scipy.signal import kaiserord, lfilter, firwin, freqz
# # np.set_printoptions(threshold=9000)

# cutOffFrequency = 800.0
# fname = 'filter/Beethoven - Ode To Joy ｜ EASY Piano Tutorial.wav'
# outname = f'filter/filteredOde_{cutOffFrequency}.wav'

# # from http://stackoverflow.com/questions/13728392/moving-average-or-running-mean
# def running_mean(x, windowSize):
#   cumsum = np.cumsum(np.insert(x, 0, 0)) 
#   print(cumsum[windowSize:])
#   print(cumsum[:-windowSize])
#   return (cumsum[windowSize:] - cumsum[:-windowSize]) / windowSize

# # from http://stackoverflow.com/questions/2226853/interpreting-wav-data/2227174#2227174
# def interpret_wav(raw_bytes, n_frames, n_channels, sample_width, interleaved = True):

#     if sample_width == 1:
#         dtype = np.uint8 # unsigned char
#     elif sample_width == 2:
#         dtype = np.int16 # signed 2-byte short
#     else:
#         raise ValueError("Only supports 8 and 16 bit audio formats.")

#     channels = np.frombuffer(raw_bytes, dtype=dtype)

#     if interleaved:
#         # channels are interleaved, i.e. sample N of channel M follows sample N of channel M-1 in raw data
#         channels.shape = (n_frames, n_channels)
#         channels = channels.T
#     else:
#         # channels are not interleaved. All samples from channel M occur before all samples from channel M-1
#         channels.shape = (n_channels, n_frames)

#     return channels

# with contextlib.closing(wave.open(fname,'rb')) as spf:
#     # sampleRate = 44000;
#     sampleRate = spf.getframerate()
#     print(f'sample rate: {sampleRate}')
#     ampWidth = spf.getsampwidth()
#     nChannels = spf.getnchannels()
#     nFrames = spf.getnframes()

#     # Extract Raw Audio from multi-channel Wav File
#     signal = spf.readframes(nFrames*nChannels)
#     spf.close()
#     channels = interpret_wav(signal, nFrames, nChannels, ampWidth, True)


#     # # get window size
#     # # from http://dsp.stackexchange.com/questions/9966/what-is-the-cut-off-frequency-of-a-moving-average-filter
#     # freqRatio = (cutOffFrequency/sampleRate)
#     # N = int(math.sqrt(0.196196 + freqRatio**2)/freqRatio)
#     # print(N) # 16 taps

#     # # Use moviung average (only on first channel)
#     # filtered = running_mean(channels[0], N).astype(channels.dtype)
#     # print(filtered)
    
#     nyq_rate = sampleRate/2;
#     width = nyq_rate/2;
#     # # The desired attenuation in the stop band, in dB.
#     ripple_db = 30.0
#     # # Compute the order and Kaiser parameter for the FIR filter.
#     N, beta = kaiserord(ripple_db, width)
#     # number of taps 
#     N = 115
#     # The cutoff frequency of the filter.
#     cutoff_hz = 2000
#     # Use firwin with a Kaiser window to create a lowpass FIR filter.
#     taps = firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
#     print(taps)
#     print(len(taps))
#     print(N)
#     # filtered = lfilter(taps, 1.0, channels[0]) / max(abs(max(channels[0])),abs(min(channels[0])))
#     orig = channels[0] / np.max(np.abs(channels[0]))  # normalize
#     filtered = lfilter(taps, 1.0, orig)  # use lfilter for efficiency
#     print(len(channels[0]))
#     # Source - https://stackoverflow.com/a

#     # order = 4  # Filter order
#     # cutoff = 800  # Cutoff frequency in Hz
    # b, a = signal.butter(order, cutoff, 'low', fs=1000)

#     # # Apply the filter
#     # filtered_sig = signal.filtfilt(b, a, orig)


#     plt.figure(1)
#     plt.plot(orig)

#     plt.figure(2)
#     plt.plot(filtered)

#     plt.show()

#     # N=16
#     # taps = firwin(16, cutOffFrequency, pass_zero=False, fs=sampleRate)

#     wav_file = wave.open(outname, "w")
#     wav_file.setparams((1, ampWidth, sampleRate, nFrames, spf.getcomptype(), spf.getcompname()))
#     wav_file.writeframes(filtered.tobytes('C'))
#     wav_file.close()



# # from numpy import cos, sin, pi, absolute, arange
# # from scipy.signal import kaiserord, lfilter, firwin, freqz
# # from matplotlib.pyplot import figure, clf, plot, xlabel, ylabel, xlim, ylim, title, grid, axes, show
# # import soundfile as sf
# # import sounddevice as sd
# # import numpy as np


# # audio_file_path = "filter/Beethoven - Ode To Joy ｜ EASY Piano Tutorial.wav"
# # recording, Fs = sf.read(audio_file_path)
# # original_signal = recording.flatten()

# # #------------------------------------------------
# # # Create a signal for demonstration.
# # #------------------------------------------------

# # sample_rate = 9700 # 9.7 kHz
# # nsamples = 400
# # t = arange(nsamples) / sample_rate
# # x = cos(2*pi*0.5*t) + 0.2*sin(2*pi*2.5*t+0.1) + \
# #         0.2*sin(2*pi*15.3*t) + 0.1*sin(2*pi*16.7*t + 0.1) + \
# #             0.1*sin(2*pi*23.45*t+.8)


# # #------------------------------------------------
# # # Create a FIR filter and apply it to x.
# # #------------------------------------------------

# # # The Nyquist rate of the signal.
# # nyq_rate = sample_rate / 2.0

# # # The desired width of the transition from pass to stop,
# # # relative to the Nyquist rate.  We'll design the filter
# # # with a 20 Hz transition width.
# # width = 400/nyq_rate

# # # The desired attenuation in the stop band, in dB.
# # ripple_db = 30.0

# # # # Compute the order and Kaiser parameter for the FIR filter.
# # N, beta = kaiserord(ripple_db, width)

# # # number of taps 
# # N = 115

# # # The cutoff frequency of the filter.
# # cutoff_hz = 2000

# # # Use firwin with a Kaiser window to create a lowpass FIR filter.
# # # taps = firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
# # taps = firwin(N, cutoff_hz, pass_zero=False, fs=sample_rate)


# # # freqs = [0, 100e3, 110e3, 190e3, 200e3, 300e3, 310e3, 500e3]
# # # gains = [1, 1,     0,     0,     0.5,   0.5,   0,     0]
# # # taps = firwin2(101, freqs, gains, fs=sample_rate)

# # print(taps)

# # # Use lfilter to filter x with the FIR filter.
# # filtered_x = lfilter(taps, 1.0, x)

# # #------------------------------------------------
# # # Plot the FIR filter coefficients.
# # #------------------------------------------------

# # figure(1)
# # plot(taps, 'bo-', linewidth=2)
# # title('Filter Coefficients (%d taps)' % N)
# # grid(True)


# # # -------------------------------------------------------------
# # # Step 3: Apply Filter to Recorded Audio
# # # -------------------------------------------------------------
# # orig = original_signal / np.max(np.abs(original_signal))  # normalize
# # filtered = lfilter(taps, 1.0, orig)  # use lfilter for efficiency

# # # Save filtered audio
# # filtered_file = "Recording_filtered.wav"
# # sf.write(filtered_file, filtered, Fs)
# # print(f"Filtered audio saved as '{filtered_file}'")





# # -------------------------------------------------------------
# # Step 4: Playback
# # -------------------------------------------------------------
# # print("▶ Playing INPUT Audio...")
# # sd.play(orig, sample_rate)
# # sd.wait()

# # print("▶ Playing FILTERED Audio...")
# # sd.play(filtered, sample_rate)
# # sd.wait()


# # #------------------------------------------------
# # # Plot the magnitude response of the filter.
# # #------------------------------------------------

# # figure(2)
# # clf()
# # w, h = freqz(taps, worN=8000)
# # plot((w/pi)*nyq_rate, absolute(h), linewidth=2)
# # xlabel('Frequency (Hz)')
# # ylabel('Gain')
# # title('Frequency Response')
# # ylim(-0.05, 1.05)
# # grid(True)

# # # Upper inset plot.
# # ax1 = axes([0.42, 0.6, .45, .25])
# # plot((w/pi)*nyq_rate, absolute(h), linewidth=2)
# # xlim(0,8.0)
# # ylim(0.9985, 1.001)
# # grid(True)

# # # Lower inset plot
# # ax2 = axes([0.42, 0.25, .45, .25])
# # plot((w/pi)*nyq_rate, absolute(h), linewidth=2)
# # xlim(12.0, 20.0)
# # ylim(0.0, 0.0025)
# # grid(True)

# # #------------------------------------------------
# # # Plot the original and filtered signals.
# # #------------------------------------------------

# # # The phase delay of the filtered signal.
# # delay = 0.5 * (N-1) / sample_rate

# # figure(3)
# # # Plot the original signal.
# # plot(t, x)
# # # Plot the filtered signal, shifted to compensate for the phase delay.
# # plot(t-delay, filtered_x, 'r-')
# # # Plot just the "good" part of the filtered signal.  The first N-1
# # # samples are "corrupted" by the initial conditions.
# # plot(t[N-1:]-delay, filtered_x[N-1:], 'g', linewidth=4)

# # xlabel('t')
# # grid(True)

# # show()