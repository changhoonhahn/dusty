'''

script to run SED modeling on NIHAO sims 


'''
import os, sys
import numpy as np
from scipy.stats import uniform

import pocomc as pc

from provabgs import infer as Infer
from provabgs import models as Models

from dusty import util as U
from dusty import data as D

##################################################################
igal = int(sys.argv[1])
##################################################################
filters = U.lsst()

# get data 
maggies     = np.load('/scratch/gpfs/chhahn/dusty/nihao_lsst.v3.z0p4.maggies_nodust.npy')
sig_maggies = np.load('/scratch/gpfs/chhahn/dusty/nihao_lsst.v3.z0p4.sig_maggies_nodust.npy')

# declare SPS model
m_nmf = Models.NMF(burst=True, emulator=True)

prior = pc.Prior([uniform(loc=7, scale=6),
                  uniform(loc=0., scale=1.),
                  uniform(loc=0., scale=1.),
                  uniform(loc=0., scale=1.),
                  uniform(loc=0., scale=1.),
                  uniform(loc=1e-2, scale=13.26),
                  uniform(loc=np.log10(4.5e-5), scale=np.log10(1.5e-2) - np.log10(4.5e-5)),
                  uniform(loc=np.log10(4.5e-5), scale=np.log10(1.5e-2) - np.log10(4.5e-5)), 
                  uniform(loc=0.01, scale=0.6)])
# prior
provabgs_prior = Infer.load_priors([
    Infer.UniformPrior(7., 13, label='sed'),
    Infer.FlatDirichletPrior(4, label='sed'),   # flat dirichilet priors
    Infer.UniformPrior(0., 1., label='sed'), # burst fraction
    Infer.UniformPrior(1e-2, 13.27, label='sed'), # tburst
    Infer.LogUniformPrior(4.5e-5, 1.5e-2, label='sed'), # log uniform priors on ZH coeff
    Infer.LogUniformPrior(4.5e-5, 1.5e-2, label='sed') # log uniform priors on ZH coeff
])

for iang in range(10): 
    ised = 10*igal + iang

    dat_dir = '/scratch/gpfs/chhahn/dusty/'
    fsamp = os.path.join(dat_dir, 'mcmc/pocomc.lsst.z0p4.noz.nodust.%i.%i.samples.npy' % (igal, iang))
    fweig = os.path.join(dat_dir, 'mcmc/pocomc.lsst.z0p4.noz.nodust.%i.%i.weights.npy' % (igal, iang))
    flogl = os.path.join(dat_dir, 'mcmc/pocomc.lsst.z0p4.noz.nodust.%i.%i.logl.npy' % (igal, iang))
    flogp = os.path.join(dat_dir, 'mcmc/pocomc.lsst.z0p4.noz.nodust.%i.%i.logp.npy' % (igal, iang))

    if os.path.isfile(fsamp) and os.path.isfile(fweig) and os.path.isfile(flogl) and os.path.isfile(flogp): 
        continue 

    def log_likelihood(tt):
        _theta = tt.copy()[:,:-1]
        _theta[:,6] = 10**_theta[:,6]
        _theta[:,7] = 10**_theta[:,7]    

        __theta = provabgs_prior.transform(_theta)
        theta = np.concatenate([__theta, np.tile(np.array([0., 0., -0.7]), (tt.shape[0],1))], axis=1)
        
        # calculate SED model(theta)
        photos = []
        for _tt, _z in zip(theta, tt[:,-1]): 
            _, _, photo = m_nmf.sed(_tt, _z, filters=filters)
            photos.append(photo)
        
        photos = np.array(photos)
        # data - model(theta) for photometry
        dphoto = (photos - maggies[ised])
        
        # calculate chi-squared for photometry
        chi2 = (-0.5 * np.sum(dphoto**2 / sig_maggies[ised]**2, axis=1))
        return chi2


    # Initialise sampler
    sampler = pc.Sampler(
        prior=prior,
        likelihood=log_likelihood,
        vectorize=True,
        random_state=0, 
        pool=10
    )

    # Start sampling
    sampler.run(progress=False)

    # Get the results
    samples, weights, logl, logp = sampler.posterior()

    # save to file 
    np.save(fsamp, samples)
    np.save(fweig, weights)
    np.save(flogl, logl)
    np.save(flogp, logp)
