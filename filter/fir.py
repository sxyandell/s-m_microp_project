# Source - https://stackoverflow.com/a
# Posted by piercus, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-16, License - CC BY-SA 4.0
# low pass filter code! running average, which I think is simplified case of FIR... can mess around and maybe hardcode the taps

import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import math
import contextlib

cutOffFrequency = 1200.0
fname = 'filter/Beethoven - Ode To Joy ｜ EASY Piano Tutorial.wav'
outname = f'filter/filteredOde_{cutOffFrequency}.wav'

# from http://stackoverflow.com/questions/13728392/moving-average-or-running-mean
def running_mean(x, windowSize):
  cumsum = np.cumsum(np.insert(x, 0, 0)) 
  return (cumsum[windowSize:] - cumsum[:-windowSize]) / windowSize

# from http://stackoverflow.com/questions/2226853/interpreting-wav-data/2227174#2227174
def interpret_wav(raw_bytes, n_frames, n_channels, sample_width, interleaved = True):

    if sample_width == 1:
        dtype = np.uint8 # unsigned char
    elif sample_width == 2:
        dtype = np.int16 # signed 2-byte short
    else:
        raise ValueError("Only supports 8 and 16 bit audio formats.")

    channels = np.frombuffer(raw_bytes, dtype=dtype)

    if interleaved:
        # channels are interleaved, i.e. sample N of channel M follows sample N of channel M-1 in raw data
        channels.shape = (n_frames, n_channels)
        channels = channels.T
    else:
        # channels are not interleaved. All samples from channel M occur before all samples from channel M-1
        channels.shape = (n_channels, n_frames)

    return channels

with contextlib.closing(wave.open(fname,'rb')) as spf:
    sampleRate = spf.getframerate()
    ampWidth = spf.getsampwidth()
    nChannels = spf.getnchannels()
    nFrames = spf.getnframes()

    # Extract Raw Audio from multi-channel Wav File
    signal = spf.readframes(nFrames*nChannels)
    spf.close()
    channels = interpret_wav(signal, nFrames, nChannels, ampWidth, True)

    # get window size
    # from http://dsp.stackexchange.com/questions/9966/what-is-the-cut-off-frequency-of-a-moving-average-filter
    freqRatio = (cutOffFrequency/sampleRate)
    N = int(math.sqrt(0.196196 + freqRatio**2)/freqRatio)
    print(N) # 16 taps

    # Use moviung average (only on first channel)
    filtered = running_mean(channels[0], N).astype(channels.dtype)

    wav_file = wave.open(outname, "w")
    wav_file.setparams((1, ampWidth, sampleRate, nFrames, spf.getcomptype(), spf.getcompname()))
    wav_file.writeframes(filtered.tobytes('C'))
    wav_file.close()



# from numpy import cos, sin, pi, absolute, arange
# from scipy.signal import kaiserord, lfilter, firwin, freqz
# from matplotlib.pyplot import figure, clf, plot, xlabel, ylabel, xlim, ylim, title, grid, axes, show
# import soundfile as sf
# import sounddevice as sd
# import numpy as np


# audio_file_path = "filter/Beethoven - Ode To Joy ｜ EASY Piano Tutorial.wav"
# recording, Fs = sf.read(audio_file_path)
# original_signal = recording.flatten()

# #------------------------------------------------
# # Create a signal for demonstration.
# #------------------------------------------------

# sample_rate = 9700 # 9.7 kHz
# nsamples = 400
# t = arange(nsamples) / sample_rate
# x = cos(2*pi*0.5*t) + 0.2*sin(2*pi*2.5*t+0.1) + \
#         0.2*sin(2*pi*15.3*t) + 0.1*sin(2*pi*16.7*t + 0.1) + \
#             0.1*sin(2*pi*23.45*t+.8)


# #------------------------------------------------
# # Create a FIR filter and apply it to x.
# #------------------------------------------------

# # The Nyquist rate of the signal.
# nyq_rate = sample_rate / 2.0

# # The desired width of the transition from pass to stop,
# # relative to the Nyquist rate.  We'll design the filter
# # with a 20 Hz transition width.
# width = 400/nyq_rate

# # The desired attenuation in the stop band, in dB.
# ripple_db = 30.0

# # # Compute the order and Kaiser parameter for the FIR filter.
# N, beta = kaiserord(ripple_db, width)

# # number of taps 
# N = 115

# # The cutoff frequency of the filter.
# cutoff_hz = 2000

# # Use firwin with a Kaiser window to create a lowpass FIR filter.
# # taps = firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
# taps = firwin(N, cutoff_hz, pass_zero=False, fs=sample_rate)


# # freqs = [0, 100e3, 110e3, 190e3, 200e3, 300e3, 310e3, 500e3]
# # gains = [1, 1,     0,     0,     0.5,   0.5,   0,     0]
# # taps = firwin2(101, freqs, gains, fs=sample_rate)

# print(taps)

# # Use lfilter to filter x with the FIR filter.
# filtered_x = lfilter(taps, 1.0, x)

# #------------------------------------------------
# # Plot the FIR filter coefficients.
# #------------------------------------------------

# figure(1)
# plot(taps, 'bo-', linewidth=2)
# title('Filter Coefficients (%d taps)' % N)
# grid(True)


# # -------------------------------------------------------------
# # Step 3: Apply Filter to Recorded Audio
# # -------------------------------------------------------------
# orig = original_signal / np.max(np.abs(original_signal))  # normalize
# filtered = lfilter(taps, 1.0, orig)  # use lfilter for efficiency

# # Save filtered audio
# filtered_file = "Recording_filtered.wav"
# sf.write(filtered_file, filtered, Fs)
# print(f"Filtered audio saved as '{filtered_file}'")





# -------------------------------------------------------------
# Step 4: Playback
# -------------------------------------------------------------
# print("▶ Playing INPUT Audio...")
# sd.play(orig, sample_rate)
# sd.wait()

# print("▶ Playing FILTERED Audio...")
# sd.play(filtered, sample_rate)
# sd.wait()


# #------------------------------------------------
# # Plot the magnitude response of the filter.
# #------------------------------------------------

# figure(2)
# clf()
# w, h = freqz(taps, worN=8000)
# plot((w/pi)*nyq_rate, absolute(h), linewidth=2)
# xlabel('Frequency (Hz)')
# ylabel('Gain')
# title('Frequency Response')
# ylim(-0.05, 1.05)
# grid(True)

# # Upper inset plot.
# ax1 = axes([0.42, 0.6, .45, .25])
# plot((w/pi)*nyq_rate, absolute(h), linewidth=2)
# xlim(0,8.0)
# ylim(0.9985, 1.001)
# grid(True)

# # Lower inset plot
# ax2 = axes([0.42, 0.25, .45, .25])
# plot((w/pi)*nyq_rate, absolute(h), linewidth=2)
# xlim(12.0, 20.0)
# ylim(0.0, 0.0025)
# grid(True)

# #------------------------------------------------
# # Plot the original and filtered signals.
# #------------------------------------------------

# # The phase delay of the filtered signal.
# delay = 0.5 * (N-1) / sample_rate

# figure(3)
# # Plot the original signal.
# plot(t, x)
# # Plot the filtered signal, shifted to compensate for the phase delay.
# plot(t-delay, filtered_x, 'r-')
# # Plot just the "good" part of the filtered signal.  The first N-1
# # samples are "corrupted" by the initial conditions.
# plot(t[N-1:]-delay, filtered_x[N-1:], 'g', linewidth=4)

# xlabel('t')
# grid(True)

# show()