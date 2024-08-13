'''
'''
from speclite import filters as specFilter

def lsst(): 
    # lsst filters
    return specFilter.load_filters('lsst2023-*')


def ugrizJ(): 
    # set up photometric filters u, g, r, i, z, J
    sdss_u = specFilter.load_filter('sdss2010-u')
    sdss_g = specFilter.load_filter('sdss2010-g')
    sdss_r = specFilter.load_filter('sdss2010-r')
    sdss_i = specFilter.load_filter('sdss2010-i')
    sdss_z = specFilter.load_filter('sdss2010-z')
    hsc_y = specFilter.load_filter('hsc2017-y')

    return specFilter.FilterSequence([sdss_u, sdss_g, sdss_r, sdss_i, sdss_z, hsc_y])
