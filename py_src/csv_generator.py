import sys
import csv
import numpy as np
import matplotlib.pyplot as plt


def get_sin(f, dur, fs, mag):
    return mag * np.sin(2*np.pi*np.arange(fs*dur)*f/fs, dtype=np.float32)


def get_cos(f, dur, fs, mag):
    return mag * np.cos(2*np.pi*np.arange(fs*dur)*f/fs, dtype=np.float32)


def get_noisy_peak(dur, fs):
    peak = np.zeros(dur*fs)
    peak[int(0.490*dur*fs):int(0.510*dur*fs)] = 500
    return get_sin(8, dur, fs, 5) + get_sin(11, dur, fs, 10) + peak


def get_irregular(dur, fs):
    peak = np.zeros(dur*fs)
    peak[int(0.400*dur*fs):int(0.490*dur*fs)] = 30
    return get_sin(1, dur, fs, 10) + peak


def make_csv(filename, sig_1, sig_2):
    if sig_1.shape != sig_2.shape:
        print('ERROR: signal shapes were not the same')
        sys.exit()

    time = range(sig_1.shape[0])
    data = np.concatenate((np.matrix(time), np.matrix(sig_1), np.matrix(sig_2)), axis=0)
    np.savetxt(filename, data.T, fmt='%d', delimiter=',')
    return data


if __name__ == '__main__':
    s1 = get_noisy_peak(5, 60)
    s2 = get_irregular(5, 60)
    data = make_csv('test.csv', s1, s2)
    plt.plot(data.T[:,1:])
    plt.show()
