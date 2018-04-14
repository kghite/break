import sys
import csv
import numpy as np
import matplotlib.pyplot as plt


def get_sin(f, dur, fs):
    return 100 * np.sin(2*np.pi*np.arange(fs*dur)*f/fs, dtype=np.float32)


def get_cos(f, dur, fs):
    return 100 * np.cos(2*np.pi*np.arange(fs*dur)*f/fs, dtype=np.float32)


def make_csv(filename, sig_1, sig_2):
    if sig_1.shape != sig_2.shape:
        print('ERROR: signal shapes were not the same')
        sys.exit()

    time = range(sig_1.shape[0])
    data = np.concatenate((np.matrix(time), np.matrix(sig_1), np.matrix(sig_2)), axis=0)
    np.savetxt(filename, data.T, fmt='%d', delimiter=',')
    return data


if __name__ == '__main__':
    s1 = get_sin(2, 5, 60)
    s2 = get_sin(4, 5, 60)
    data = make_csv('test.csv', s1, s2)
    plt.plot(data.T[:,1:])
    plt.show()
