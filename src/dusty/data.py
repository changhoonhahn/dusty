'''
'''
import os
import numpy as np 
import astropy.units as u
from astropy.io import fits
from astropy.table import Table


from . import util as U


if os.path.isdir('/scratch/gpfs/chhahn/dusty/'): 
    dat_dir = '/scratch/gpfs/chhahn/dusty/'
elif os.path.isdir('/scratch/network/chhahn/dusty/'): 
    dat_dir = '/scratch/network/chhahn/dusty/'
else: 
    dat_dir = '/Users/chahah/data/dusty/'



class Nihao(object): 
    ''' class object for dealing with the NIHAO simulations 
    '''
    def __init__(self): 
        # read properties of the 65 Niaho galaxies
        gal_prop = Table.read(os.path.join(dat_dir, 'nihao-integrated-seds.fits'), hdu=1)
    
        # read properties of the 650 forward models (10 per galaxy) 
        self.prop = Table.read(os.path.join(dat_dir, 'nihao-integrated-seds.fits'), hdu=2)
        for col in ['sfh', 'ceh', 'ages', 'metals']: 
            val = np.empty((len(self.prop),) + gal_prop[col].shape[1:])
            for i in range(len(gal_prop)): 
                val[i*10:(i+1)*10] = gal_prop[col][i]

            self.prop.add_column(val, name=col)

        # read SEDS
        f = fits.open(os.path.join(dat_dir, 'nihao-integrated-seds.fits'))
    
        # wavelength 
        self.wave = f[3].data 
    
        # dusty SED 
        self.seds = f[4].data 
        
        # unattenuated SED 
        self.seds_unatten = f[5].data 

    def maggies(self, zred, filters=None, dust=False): 
        ''' calculate magnitudes in maggies given the redshifts and photometric
        bandpass filters. 


        Parameters
        ----------
        zred : float or array_like
            redshift
        
        filters : object
            Photometric bandpass filter to generate photometry.
            `speclite.FilterResponse` object. default filter is u,g,r,i,z,J
    
        dust : bool
            Attenuated or unattenuated magnitudes


        Returns
        -------
        maggies : array_like 
            magnitudes in specified filters in units of maggies
        '''
        if filters is None: filters = U.ugrizJ()

        if dust: 
            _seds = self.seds
            print('blah') 
        else: 
            _seds = self.seds_unatten

        if isinstance(zred, float): 
            # redshift the wavelength 
            wavez = self.wave * (1+zred)

            fl = _seds / (3.34e4) / wavez**2 # ergs/s/cm^2/A

            maggies = np.array([np.array(list(arr)) 
                                for arr in filters.get_ab_maggies(fl, wavelength=wavez).as_array()]) * 1e9
        else: 
            assert zred.shape[0] == (_seds).shape[0], 'provide the same number of redshifts as galaxies'
        
            maggies = np.empty((zred.shape[0], len(filters.effective_wavelengths)))
            for i, zz in enumerate(zred): 
                # redshift the wavelength 
                wavez = self.wave * (1+zz)

                fl = _seds[i] / (3.34e4) / wavez**2 # ergs/s/cm^2/A

                maggies[i,:] = np.array([np.array(list(arr)) 
                                    for arr in filters.get_ab_maggies(fl, wavelength=wavez).as_array()]) * 1e9

        return maggies 


'''
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
'''
