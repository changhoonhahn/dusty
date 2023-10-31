'''
'''
import os
import numpy as np 
import astropy.units as u
from astropy.io import fits
from astropy.table import Table


if os.path.isdir('/scratch/gpfs/chhahn/dusty/'): 
    dat_dir = '/scratch/gpfs/chhahn/dusty/'
elif os.path.isdir('/scratch/network/chhahn/dusty/'): 
    dat_dir = '/scratch/network/chhahn/dusty/'
else: 
    dat_dir = '/Users/chahah/data/dusty/'


def nihao(filters, dust=False): 
    '''
    '''
    # read galaxies
    gals = Table.read(os.path.join(dat_dir, 'nihao-integrated-seds.fits'), hdu=1)

    # read SEDS
    f = fits.open(os.path.join(dat_dir, 'nihao-integrated-seds.fits'))

    wave = f[3].data
    
    if dust: seds = f[4].data
    else: seds = f[5].data

    zred = 0.022229
    # observed frame z
    wavez = wave * (1+zred)

    fl = seds / (3.34e4) / wavez**2 # ergs/s/cm^2/A

    maggies = np.array([np.array(list(arr))
        for arr in filters.get_ab_maggies(fl, wavelength=wave).as_array()]) * 1e9
    return gals, maggies 
