'''
'''
import numpy as np 
import astropy.units as u
from astropy.io import fits
from astropy.table import Table



def nihao(filters, dust=False): 
    '''
    '''
    # read galaxies
    gals = Table.read('/scratch/gpfs/chhahn/dusty/nihao-integrated-seds.fits', hdu=1)

    # read SEDS
    wave = fits.open('/scratch/gpfs/chhahn/dusty/nihao-integrated-seds.fits')[3].data
    
    if dust: 
        seds = fits.open('/scratch/gpfs/chhahn/dusty/nihao-integrated-seds.fits')[4].data
    else: 
        seds = fits.open('/scratch/gpfs/chhahn/dusty/nihao-integrated-seds.fits')[5].data

    zred = 0.022229
    # observed frame z
    wavez = wave * (1+zred)

    fl = seds / (3.34e4) / wavez**2 # ergs/s/cm^2/A

    maggies = np.array([np.array(list(arr))
                        for arr in filters.get_ab_maggies(fl, wavelength=wave).as_array()]) * 1e9
    return gals, maggies 
