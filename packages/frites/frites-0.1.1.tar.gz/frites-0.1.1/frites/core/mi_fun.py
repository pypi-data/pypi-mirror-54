"""MI functions for ffx / rfx inferences."""
import numpy as np

from frites.config import CONFIG
from frites.core import mi_nd_gg, mi_model_nd_gd, gccmi_nd_ccnd


###############################################################################
#                        I(CONTINUOUS; CONTINUOUS)
###############################################################################


def mi_gg(x, y, z, suj, inference):
    """I(C; C) for rfx.

    The returned mi array has a shape of (n_subjects, n_times) if inference is
    "rfx", (1, n_times) if "ffx".
    """
    # proper shape of the regressor
    n_times, _, n_trials = x.shape
    y_t = np.tile(y.T[np.newaxis, ...], (n_times, 1, 1))
    # compute mi across (ffx) or per subject (rfx)
    if inference == 'ffx':
        mi = mi_nd_gg(x, y_t, **CONFIG["KW_GCMI"])[np.newaxis, :]
    elif inference == 'rfx':
        # get subject informations
        suj_u = np.unique(suj)
        n_subjects = len(suj_u)
        # compute mi per subject
        mi = np.zeros((n_subjects, n_times), dtype=float)
        for n_s, s in enumerate(suj_u):
            is_suj = suj == s
            mi[n_s, :] = mi_nd_gg(x[..., is_suj], y_t[..., is_suj],
                                  **CONFIG["KW_GCMI"])

    return mi


###############################################################################
#                        I(CONTINUOUS; DISCRET)
###############################################################################


def mi_gd(x, y, z, suj, inference):
    """I(C; D) for ffx.

    The returned mi array has a shape of (n_subjects, n_times) if inference is
    "rfx", (1, n_times) if "ffx".
    """
    n_times, _, _ = x.shape
    _y = y.squeeze().astype(int)
    # compute mi across (ffx) or per subject (rfx)
    if inference == 'ffx':
        mi = mi_model_nd_gd(x, _y, **CONFIG["KW_GCMI"])[np.newaxis, :]
    elif inference == 'rfx':
        # get subject informations
        suj_u = np.unique(suj)
        n_subjects = len(suj_u)
        # compute mi per subject
        mi = np.zeros((n_subjects, n_times), dtype=float)
        for n_s, s in enumerate(suj_u):
            is_suj = suj == s
            mi[n_s, :] = mi_model_nd_gd(x[..., is_suj], _y[is_suj],
                                        **CONFIG["KW_GCMI"])

    return mi


###############################################################################
#                        I(CONTINUOUS; CONTINUOUS | DISCRET)
###############################################################################


def mi_ggd(x, y, z, suj, inference):
    """I(C; C | D) for ffx.

    The returned mi array has a shape of (n_subjects, n_times) if inference is
    "rfx", (1, n_times) if "ffx".
    """
    # discard gcrn
    kw = CONFIG["KW_GCMI"].copy()
    kw['gcrn'] = False
    # proper shape of the regressor
    n_times, _, n_trials = x.shape
    y_t = np.tile(y.T[np.newaxis, ...], (n_times, 1, 1))
    # compute mi across (ffx) or per subject (rfx)
    if inference == 'ffx':
        _z = tuple([z[:, n] for n in range(z.shape[1])])
        mi = gccmi_nd_ccnd(x, y_t, *_z, **kw)[np.newaxis, :]
    elif inference == 'rfx':
        # get subject informations
        suj_u = np.unique(suj)
        n_subjects = len(suj_u)
        # compute mi per subject
        mi = np.zeros((n_subjects, n_times), dtype=float)
        for n_s, s in enumerate(suj_u):
            is_suj = suj == s
            _z = tuple([z[is_suj, n] for n in range(z.shape[1])])
            mi[n_s, :] = gccmi_nd_ccnd(x[..., is_suj], y_t[..., is_suj], *_z,
                                       **kw)

    return mi


###############################################################################
#                              PERMUTATION VECTOR
###############################################################################


def permute_mi_vector(y, suj, mi_type='cc', inference='rfx', n_perm=1000):
    """Permute regressor variable for performing non-parameteric statistics.

    Parameters
    ----------
    y : array_like
        Array of shape (n_epochs,) to be permuted
    suj : array_like
        Array of shape (n_epochs,) used for permuting per subject
    mi_type : {'cc', 'cd', 'ccd'}
        Mutual information type
    inference : {'ffx', 'rfx'}
        Inference type (fixed or random effect)
    n_perm : int | 1000
        Number of permutations to return

    Returns
    -------
    y_p : list
        List of length (n_perm,) of random permutation of the regressor
    """
    y_p = []
    for p in range(n_perm):
        if inference == 'ffx':    # FFX (FIXED EFFECT)
            y_p += [np.random.permutation(y)]
        elif inference == 'rfx':  # RFX (RANDOM EFFECT)
            _y = y.copy()
            for s in np.unique(suj):
                # find everywhere the subject is present
                is_suj = suj == s
                # randomize per subject
                _y[is_suj] = np.random.permutation(y[is_suj])
            y_p += [_y]
    assert len(y_p) == n_perm

    return y_p
