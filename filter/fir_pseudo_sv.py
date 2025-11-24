
import numpy as np
import sounddevice as sd
import scipy.signal as signal
import matplotlib.pyplot as plt
import soundfile as sf
import pandas as pd

# generate 7 taps for LPF based on cutoff frequency
# cutoff freq must be between 200 and 1600 Hz
def gettaps_old(freq):
    b06 = 0.00000383571428571*freq+0.248722857143
    b12345 = 0.0000171*freq-0.00238
    taps = [b06] + 5*[b12345] + [b06]
    return(taps)

def gettaps(cutOffFreq):
    taps = [0]*51
    taps[0] = 2.4114414996767963e-09*cutOffFreq**2 + -7.236308985132517e-06*cutOffFreq + 0.004511274725274724
    taps[1] = 1.9774563671622507e-09*cutOffFreq**2 + -6.737635746606334e-06*cutOffFreq + 0.004558340659340658
    taps[2] = 1.6213639301874615e-09*cutOffFreq**2 + -6.649169360051711e-06*cutOffFreq + 0.004963626373626372
    taps[3] = 1.2066095669036878e-09*cutOffFreq**2 + -6.7201115061409195e-06*cutOffFreq + 0.0056588461538461515
    taps[4] = 6.481092436974827e-10*cutOffFreq**2 + -6.776239495798323e-06*cutOffFreq + 0.006603999999999999
    taps[5] = -1.2605042016805994e-10*cutOffFreq**2 + -6.631680672268912e-06*cutOffFreq + 0.007740142857142854
    taps[6] = -1.1389786683904227e-09*cutOffFreq**2 + -6.159124111182947e-06*cutOffFreq + 0.009017060439560439
    taps[7] = -2.3846961861667595e-09*cutOffFreq**2 + -5.2671897220426785e-06*cutOffFreq + 0.010393884615384614
    taps[8] = -3.788380736910136e-09*cutOffFreq**2 + -3.952700387847461e-06*cutOffFreq + 0.011836516483516482
    taps[9] = -5.2408694246929445e-09*cutOffFreq**2 + -2.283220749838409e-06*cutOffFreq + 0.013339631868131871
    taps[10] = -6.601971557853891e-09*cutOffFreq**2 + -3.6930833872012435e-07*cutOffFreq + 0.014891675824175821
    taps[11] = -7.735374919198432e-09*cutOffFreq**2 + 1.6704605688428931e-06*cutOffFreq + 0.01648817582417584
    taps[12] = -8.486910148674832e-09*cutOffFreq**2 + 3.6500096961861395e-06*cutOffFreq + 0.01814094505494506
    taps[13] = -8.704670329670315e-09*cutOffFreq**2 + 5.3666208791208585e-06*cutOffFreq + 0.019864362637362635
    taps[14] = -8.31423723335483e-09*cutOffFreq**2 + 6.704555591467284e-06*cutOffFreq + 0.021650423076923088
    taps[15] = -7.282239819004503e-09*cutOffFreq**2 + 7.566245959922407e-06*cutOffFreq + 0.023491010989010973
    taps[16] = -5.589366515837072e-09*cutOffFreq**2 + 7.83728829993531e-06*cutOffFreq + 0.02538917582417582
    taps[17] = -3.3194085326437917e-09*cutOffFreq**2 + 7.5424353587588235e-06*cutOffFreq + 0.027300818681318707
    taps[18] = -5.975274725274153e-10*cutOffFreq**2 + 6.733049450549372e-06*cutOffFreq + 0.029187791208791225
    taps[19] = 2.392857142857198e-09*cutOffFreq**2 + 5.533571428571342e-06*cutOffFreq + 0.030995571428571442
    taps[20] = 5.45467032967036e-09*cutOffFreq**2 + 4.076236263736212e-06*cutOffFreq + 0.032673565934065944
    taps[21] = 8.382433742727883e-09*cutOffFreq**2 + 2.5076906916612625e-06*cutOffFreq + 0.03416525274725271
    taps[22] = 1.0910148674854602e-08*cutOffFreq**2 + 1.0860180995474374e-06*cutOffFreq + 0.03539280219780221
    taps[23] = 1.2886958629605689e-08*cutOffFreq**2 + -8.688267614737062e-08*cutOffFreq + 0.036316192307692285
    taps[24] = 1.4127343244990317e-08*cutOffFreq**2 + -8.299321266968571e-07*cutOffFreq + 0.03688068681318682
    taps[25] = 1.4560924369747938e-08*cutOffFreq**2 + -1.1003781512605608e-06*cutOffFreq + 0.03707528571428571
    taps[26] = 1.4127343244990317e-08*cutOffFreq**2 + -8.299321266968571e-07*cutOffFreq + 0.03688068681318682
    taps[27] = 1.2886958629605689e-08*cutOffFreq**2 + -8.688267614737062e-08*cutOffFreq + 0.036316192307692285
    taps[28] = 1.0910148674854602e-08*cutOffFreq**2 + 1.0860180995474374e-06*cutOffFreq + 0.03539280219780221
    taps[29] = 8.382433742727883e-09*cutOffFreq**2 + 2.5076906916612625e-06*cutOffFreq + 0.03416525274725271
    taps[30] = 5.45467032967036e-09*cutOffFreq**2 + 4.076236263736212e-06*cutOffFreq + 0.032673565934065944
    taps[31] = 2.392857142857198e-09*cutOffFreq**2 + 5.533571428571342e-06*cutOffFreq + 0.030995571428571442
    taps[32] = -5.975274725274153e-10*cutOffFreq**2 + 6.733049450549372e-06*cutOffFreq + 0.029187791208791225
    taps[33] = -3.3194085326437917e-09*cutOffFreq**2 + 7.5424353587588235e-06*cutOffFreq + 0.027300818681318707
    taps[34] = -5.589366515837072e-09*cutOffFreq**2 + 7.83728829993531e-06*cutOffFreq + 0.02538917582417582
    taps[35] = -7.282239819004503e-09*cutOffFreq**2 + 7.566245959922407e-06*cutOffFreq + 0.023491010989010973
    taps[36] = -8.31423723335483e-09*cutOffFreq**2 + 6.704555591467284e-06*cutOffFreq + 0.021650423076923088
    taps[37] = -8.704670329670315e-09*cutOffFreq**2 + 5.3666208791208585e-06*cutOffFreq + 0.019864362637362635
    taps[38] = -8.486910148674832e-09*cutOffFreq**2 + 3.6500096961861395e-06*cutOffFreq + 0.01814094505494506
    taps[39] = -7.735374919198432e-09*cutOffFreq**2 + 1.6704605688428931e-06*cutOffFreq + 0.01648817582417584
    taps[40] = -6.601971557853891e-09*cutOffFreq**2 + -3.6930833872012435e-07*cutOffFreq + 0.014891675824175821
    taps[41] = -5.2408694246929445e-09*cutOffFreq**2 + -2.283220749838409e-06*cutOffFreq + 0.013339631868131871
    taps[42] = -3.788380736910136e-09*cutOffFreq**2 + -3.952700387847461e-06*cutOffFreq + 0.011836516483516482
    taps[43] = -2.3846961861667595e-09*cutOffFreq**2 + -5.2671897220426785e-06*cutOffFreq + 0.010393884615384614
    taps[44] = -1.1389786683904227e-09*cutOffFreq**2 + -6.159124111182947e-06*cutOffFreq + 0.009017060439560439
    taps[45] = -1.2605042016805994e-10*cutOffFreq**2 + -6.631680672268912e-06*cutOffFreq + 0.007740142857142854
    taps[46] = 6.481092436974827e-10*cutOffFreq**2 + -6.776239495798323e-06*cutOffFreq + 0.006603999999999999
    taps[47] = 1.2066095669036878e-09*cutOffFreq**2 + -6.7201115061409195e-06*cutOffFreq + 0.0056588461538461515
    taps[48] = 1.6213639301874615e-09*cutOffFreq**2 + -6.649169360051711e-06*cutOffFreq + 0.004963626373626372
    taps[49] = 1.9774563671622507e-09*cutOffFreq**2 + -6.737635746606334e-06*cutOffFreq + 0.004558340659340658
    taps[50] = 2.4114414996767963e-09*cutOffFreq**2 + -7.236308985132517e-06*cutOffFreq + 0.004511274725274724
    return taps
def design_fir_lpf(fpass, fstop, fs, numtaps):
    nyquist = fs / 2

    bands = [0, fpass, fstop, nyquist]
    desired = [1, 0]
    taps = signal.remez(numtaps, bands, desired, fs=fs)
    return taps

def remez_filter_save(orig, cutOffFrequency):
    numtaps = 15
    Fs = 44000
    Fpass = cutOffFrequency
    Fstop = Fpass + 200
    # freqRatio = (cutOffFrequency/Fs)
    # N = int(math.sqrt(0.196196 + freqRatio**2)/freqRatio)
    h = design_fir_lpf(Fpass, Fstop, Fs, numtaps)
    print(f"taps: {h}")
    # from this we see that the lienar interpolation is not great, but it is at least accurate w order of mag?
    filtered_remez = signal.lfilter(h, 1.0, orig)
    filtered_file_path_remez= f'filter/filteredOde_{cutOffFrequency}_remez.wav'
    print(f"saving to {filtered_file_path_remez}")
    sf.write(filtered_file_path_remez, filtered_remez[::2], Fs)
    return filtered_remez, taps

def apply_filter(orig, taps):
    # this function will right shift and roll things to the right since 0th element is furthest left
    # in systemverilog, it will be different since 0th element is furthest right
    orig = np.array(orig)
    taps = np.array(taps)
    shiftreg = np.array([float(0)]*len(taps))
    filtered = np.array([float(0)]*len(orig))
    print(taps)
    # [b0, b1, b2, b3, b4, b5, b6] = taps
    for i in range(len(orig)):
        # print(i)
        # roll new value into shiftreg
        shiftreg = np.roll(shiftreg, 1)
        shiftreg[0] = orig[i]
        # print(shiftreg)
        # compute output
        # only really works after all 7 bits of shiftreg have been loaded
        # but shiftreg is initialized as all 0s anyways so it should be fine
        filtered[i] = np.dot(taps, shiftreg)
        # filtered[i] = b0*shiftreg[0] + b1*shiftreg[1] + b2*shiftreg[2] + b3*shiftreg[3] + b4*shiftreg[4] + b5*shiftreg[5] + b6*shiftreg[6] 
        # print(shiftreg)
        # print(filtered[i])
    return filtered

def spectrum(signal, Fs):
    ## FFT again to check
    n = len(signal) # length of the signal
    k = np.arange(n)
    T = n/Fs
    frq = k/T # two sides frequency range
    frq = frq[:len(frq)//2] # one side frequency range
    signal_spec = np.fft.fft(signal)/n # dft and normalization
    signal_spec = signal_spec[:n//2]
    return signal_spec, frq
# print(type(taps[0]))
# print(sum(taps))

# ### SOME TEST CASES
# # sample = [-0.1841494764562041, -0.2694839801868455, -0.2041507304533199, -0.2869145400965577, -0.2236503856041131, -0.301711706063076, -0.2427738416201642, -0.3133111793842874, -0.2616464982130541, -0.3218383597717725, -0.2793278575459276, -0.3273559470813217, -0.2954417204840429, -0.3296758417455639, -0.3097372876042385, -0.329299642610822, -0.3214621606370305, -0.3265408489560474, -0.3303655401592576, -0.3214621606370305, -0.3362593266035488, -0.314377076932723, -0.3386419211235814, -0.3057871966894476, -0.3375760235751457, -0.2960060191861559, -0.3336259326603549, -0.2849081447112672, -0.3259765502539344, -0.2728070725437331, -0.314377076932723, -0.2601417016740861, -0.2999561101009467, -0.2471001316696971, -0.2829644491817669, -0.2333061633958242, -0.2629004953288607, -0.2191359959872092, -0.2400150479653896, -0.2047777290112232, -0.2149978055050473, -0.189980563044705, -0.187723368236253, -0.1749325976550254, -0.1583798357263778, -0.1598219324095554, -0.1279704056680669, -0.1442096683177628, -0.0972474763308044, -0.1282839049470186] 
# # print(apply_filter(sample, taps))
# taps = list(range(7))
# testin = list(range(35))
# # testin = [1, 1, 1, 0, 0, 0]*20
# print(testin)
# apply_filter(testin, taps)
# # testout = [x.item() for x in apply_filter(testin, taps)]
# # print(testout)
# # plt.figure(1)
# # plt.subplot(2, 1, 1); plt.title("Original Signal"); plt.plot(testin)
# # plt.subplot(2, 1, 2); plt.title("Filtered Signal"); plt.plot(testout, 'g')
# # plt.show()

# # recording, Fs = sf.read("filter/Beethoven - Ode To Joy ｜ EASY Piano Tutorial.wav")
# # print(Fs)


### MAIN FILTERING SCRIPT
cutOffFrequency = 400
samp_freq = 44100
nyquist_freq = samp_freq/2
crit_freq = cutOffFrequency/nyquist_freq
taps = gettaps(cutOffFrequency)
[a, b] = signal.butter(6, crit_freq, btype='low')
print(a)
print(b) 
# taps = [0.24919844, 0.00283417, 0.00262954, 0.00253264, 0.00262954, 0.00283417, 0.24919844]
# taps = [0.00107165, 0.00115588, 0.00129729, 0.00150299, 0.00177938, 0.00213195,
#  0.00256521, 0.00308251, 0.00368605, 0.00437667, 0.00515392, 0.00601595,
#  0.00695948, 0.0079799,  0.00907119, 0.01022607, 0.011436,   0.01269134,
#  0.01398143, 0.01529471, 0.01661895, 0.0179413,  0.01924857, 0.02052735,
#  0.02176423, 0.02294598, 0.02405976, 0.02509326, 0.02603493, 0.02687415,
#  0.02760135, 0.02820819, 0.02868764, 0.02903416, 0.0292437,  0.02931382,
#  0.0292437,  0.02903416, 0.02868764, 0.02820819, 0.02760135, 0.02687415,
#  0.02603493, 0.02509326, 0.02405976, 0.02294598, 0.02176423, 0.02052735,
#  0.01924857, 0.0179413,  0.01661895, 0.01529471, 0.01398143, 0.01269134,
#  0.011436,   0.01022607, 0.00907119, 0.0079799,  0.00695948, 0.00601595,
#  0.00515392, 0.00437667, 0.00368605, 0.00308251, 0.00256521, 0.00213195,
#  0.00177938, 0.00150299, 0.00129729, 0.00115588, 0.00107165]

print(f"taps: {taps}")
filter = 1
read_orig_wav = 1

if (read_orig_wav):
    audio_file_path = "filter/Beethoven - Ode To Joy ｜ EASY Piano Tutorial.wav"
    recording, Fs = sf.read(audio_file_path)
    orig = recording.flatten()
    orig = orig / np.max(np.abs(orig))
    # print(orig)
    # np.savetxt("orig audio.csv", orig, delimiter="," )
    orig_df = pd.DataFrame(orig)
    orig_df.to_csv("orig audio.csv", header=False, index=False)
else:
    Fs = 44100 #hardcoded...
    orig_df = pd.read_csv("orig audio.csv")
    orig = [x[0] for x in orig_df.values.tolist()]
# print(type(orig[0]))

if(filter):
    filtered = apply_filter(orig, taps)
    filtered_df = pd.DataFrame(filtered)
    # np.savetxt("filtered audio.csv", filtered, delimiter="," )
    filtered_df.to_csv("filtered audio.csv", header=False, index=False)
else:
    filtered_df = pd.read_csv("filtered audio.csv")
    filtered = [x[0] for x in filtered_df.values.tolist()]
    # print(filtered)
# filtered_r, taps_r = remez_filter_save(orig, cutOffFrequency)

print(f"length of original data: {len(orig)}")
print(f"length of filtered data: {len(filtered)}")


filtered_file_path_diy = f'filter/filteredOde_{cutOffFrequency}_diy_filter.wav'
print(f"saving to {filtered_file_path_diy}")
sf.write(filtered_file_path_diy, filtered[::2], Fs)
# plt.figure(1)
# plt.subplot(3, 1, 1); plt.title("Original Signal, freq domain"); plt.plot(orig)
# plt.subplot(3, 1, 2); plt.title("My Filtered Signal, freq domain"); plt.plot(filtered, 'g')
# plt.subplot(3, 1, 3); plt.title("Python Library Filtered Signal, freq domain"); plt.plot(filtered_r, 'r')

# plt.show()

## FFT again to check
filtered_spec, frq_spec = spectrum(filtered, Fs)
orig_spec, frq_orig= spectrum(orig, Fs)

plt.figure(2)
w, h = signal.freqz(taps, worN=8000)
plt.plot(np.log((w/np.pi)*(Fs/2)), np.log(abs(h)), linewidth=2)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Gain')
plt.title('Frequency Response for Interpolated Filter')
# plt.ylim(-0.05, 1.05)
plt.grid(True)


# plt.figure(3)
# w_r, h_r = signal.freqz(taps_r, worN=8000)
# plt.plot(np.log((w_r/np.pi)*(Fs/2)), np.log(abs(h_r)), linewidth=2)
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Gain')
# plt.title('Frequency Response for Remez Filter')
# # plt.ylim(-0.05, 1.05)
# plt.grid(True)
# # Upper inset plot.
# ax1 = plt.axes([0.42, 0.6, .45, .25])
# plt.plot((w/np.pi)*(Fs/2), abs(h), linewidth=2)
# # plt.xlim(0,8.0)
# # plt.ylim(0.9985, 1.001)
# plt.grid(True)

# # Lower inset plot
# ax2 = plt.axes([0.42, 0.25, .45, .25])
# plt.plot((w/np.pi)*(Fs/2), abs(h), linewidth=2)
# # plt.xlim(12.0, 20.0)
# # plt.ylim(0.0, 0.0025)
# plt.grid(True)


filtered_py = signal.lfilter(taps, 1.0, orig)
filtered_file_path_diy = f'filter/filteredOde_{cutOffFrequency}_interp.wav'
print(f"saving to {filtered_file_path_diy}")
sf.write(filtered_file_path_diy, filtered_py[::2], Fs)

plt.figure(1)
# magnitude_spectrum = np.abs(np.fft.rfft(signal))
# frequencies = np.fft.rfftfreq(signal.shape[0], 1 / Fs)
# plt.subplot(2, 1, 1); plt.title("Filtered Signal"); plt.plot(frq_spec, -20*np.log(abs(filtered_spec))); plt.xlabel('Freq (Hz)'); plt.ylabel('|filtered| (dB)')
# plt.subplot(2, 1, 2); plt.title("Original Signal"); plt.plot(frq_orig, -20*np.log(abs(orig_spec)), 'g'); plt.xlabel('Freq (Hz)'); plt.ylabel('|original| (dB)')
plt.subplot(3, 1, 1); plt.title("Filtered Signal, DIY"); plt.plot(20*np.log(np.fft.rfftfreq(len(filtered), 1 / Fs)), -20*np.log(np.abs(np.fft.rfft(filtered)))); plt.xlabel('Freq (Hz)'); plt.ylabel('|filtered|')
plt.subplot(3, 1, 2); plt.title("Original Signal"); plt.plot(20*np.log(np.fft.rfftfreq(len(orig), 1 / Fs)), -20*np.log(np.abs(np.fft.rfft(orig))), 'g'); plt.xlabel('Freq (Hz)'); plt.ylabel('|original|')
# plt.subplot(3, 1, 3); plt.title("Filtered Signal, python lib"); plt.plot(20*np.log(np.fft.rfftfreq(len(filtered_py), 1 / Fs)), -20*np.log(np.abs(np.fft.rfft(filtered_r))), 'r'); plt.xlabel('Freq (Hz)'); plt.ylabel('|library filtered|')

plt.show()




