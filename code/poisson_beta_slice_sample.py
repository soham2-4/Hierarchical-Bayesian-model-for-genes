import numpy as np

def slice_sample_beta(logdist, xx, widths, max_step_size=1000):
    log_px = logdist(xx)
    log_uprime = np.log(np.random.rand()) + log_px

    rr = np.random.rand()
    x_l = xx - rr * widths
    x_r = xx + (1 - rr) * widths

    j = np.floor(np.random.rand() * max_step_size)
    k = max_step_size - 1 - j

    while logdist(x_l) > log_uprime and x_l - widths >= 0 and j > 0:
        x_l -= widths
        j -= 1

    while logdist(x_r) > log_uprime and x_r + widths <= 1 and k > 0:
        x_r += widths
        k -= 1

    x_l = max(x_l, 0)
    x_r = min(x_r, 1)

    while True:
        xprime = np.random.rand() * (x_r - x_l) + x_l
        log_px = logdist(xprime)
        if log_px > log_uprime:
            return xprime
        else:
            if xprime > xx:
                x_r = xprime
            elif xprime < xx:
                x_l = xprime
            else:
                raise ValueError("Shrunk to current position and still not acceptable.")

def slice_sample_gamma(logdist, xx, widths, max_step_size=1000):
    log_px = logdist(xx)
    log_uprime = np.log(np.random.rand()) + log_px

    rr = np.random.rand()
    x_l = xx - rr * widths
    x_r = xx + (1 - rr) * widths

    j = np.floor(np.random.rand() * max_step_size)
    k = max_step_size - 1 - j

    while logdist(x_l) > log_uprime and x_l - widths >= 0 and j > 0:
        x_l -= widths
        j -= 1

    while logdist(x_r) > log_uprime and k > 0:
        x_r += widths
        k -= 1

    while True:
        xprime = np.random.rand() * (x_r - x_l) + x_l
        log_px = logdist(xprime)
        if log_px > log_uprime:
            return xprime
        else:
            if xprime > xx:
                x_r = xprime
            elif xprime < xx:
                x_l = xprime
            else:
                raise ValueError("Shrunk to current position and still not acceptable.")