"""pitchdetect.py

This file is meant to be imported as a module and contains the following function:
    * fund

The function fund estimates the fundamental frequency of a signal via a short-time cepstrum.
"""

import numpy as np

def fund(x, f_s):
    """
    Estimate the fundamental frequency of a signal via a short-time cepstrum.

    Args:
        x (array): signal to estimate the fundamental frequency of
        f_s (int): sample rate of x

    Returns:
        int: estimated fundamental frequency of x
    """
    MAX_LENGTH = 20*f_s # max of 20 seconds
    if len(x) > MAX_LENGTH:
        x = x[:MAX_LENGTH]

    short_time = short_time_cepstrum(x, 2048, 1024, f_s)

    MIN_FREQUENCY = 85
    MAX_FREQUENCY = 255
    min_quefrency = int(np.ceil(f_s / MAX_FREQUENCY))
    max_quefrency = int(np.floor(f_s / MIN_FREQUENCY))

    fund_frequencies = []
    for i, cepstrum_i in enumerate(short_time[:-1]):
        if np.isfinite(cepstrum_i).all():
            quefrency = np.argmax(cepstrum_i[min_quefrency:len(cepstrum_i)//2]) + min_quefrency
            if quefrency <= max_quefrency:
                fund_freq = f_s/quefrency
                fund_frequencies.append(fund_freq)
    return int(np.round(np.median(fund_frequencies)))

##########
# helpers
##########
def cepstrum(x):
    """
    Returns the cepstrum of a signal x.

    Args:
        x (array): signal to take cepstrum of

    Returns:
        array: cepstrum of signal x

    References:
        "From frequency to quefrency: a history of the cepstrum"
        by Alan V. Oppenheim and Ronald W. Schafer
    """
    powerspectrum = np.abs(np.fft.rfft(x))
    cepstrum = np.abs(np.fft.irfft(np.log(powerspectrum)))
    return cepstrum

def short_time_cepstrum(x, window_size, step_size, f_s):
    """
    Returns the short-time cepstrum of a signal x,
    using the specified window size and step size.

    Args:
        x (array): signal to take short-time cepstrum of
        window_size (int): window size of short-time cepstrum
        step_size (int): step size of short-time cepstrum
        f_s (int): sample rate of x

    Returns:
        list: short-time cepstrum as a list of arrays, where each array
        represents the cepstrum of one window. Thus output[n] is the cepstrum
        from the nth window.
    """

    # find len_result
    len_result = -1
    numel_stft = 0
    while numel_stft <= len(x):
        len_result += 1
        numel_stft = window_size + len_result*step_size

    result = [0]*len_result
    for m in range(len_result):
        samples_m = x[m*step_size : m*step_size+window_size]
        result[m] = cepstrum(samples_m)
    return result

