"""Core functions of information theoretical measures.

This submodule contains all of the functions to compute mutual-information,
entropy etc..

For further details about the Gaussian-Copula Mutual information see
:cite:`ince2017statistical`
"""
from .copnorm import (copnorm_1d, copnorm_cat_1d, copnorm_nd, copnorm_cat_nd)  # noqa
from .gcmi_1d import (ent_1d_g, mi_1d_gg, gcmi_1d_cc, mi_model_1d_gd,  # noqa
                      gcmi_model_1d_cd, mi_mixture_1d_gd, gcmi_mixture_1d_cd,
                      cmi_1d_ggg, gccmi_1d_ccc, gccmi_1d_ccd)
from .gcmi_nd import (mi_nd_gg, mi_model_nd_gd, cmi_nd_ggg, gcmi_nd_cc,  # noqa
                      gcmi_model_nd_cd, gccmi_nd_ccnd, gccmi_model_nd_cdnd,
                      gccmi_nd_ccc, transfer_entropy)
from .mi_fun import (mi_gg, mi_gd, mi_ggd, permute_mi_vector) # noqa

MI_FUN = dict(
    cc=mi_gg,
    cd=mi_gd,
    ccd=mi_ggd
)
