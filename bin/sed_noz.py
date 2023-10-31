'''

script to run SED modeling on NIHAO sims 


'''
import os, sys
import numpy as np
import scipy.optimize as op


import zeus

from provabgs import util as UT
from provabgs import infer as Infer
from provabgs import models as Models

from dusty import util as U
from dusty import data as D

##################################################################
igal = int(sys.argv[1])
iang = int(sys.argv[2])
nmcmc = int(sys.argv[3])
keep = (sys.argv[4] == 'True') 

ised = 10*igal + iang
##################################################################
if os.path.isdir('/scratch/gpfs/chhahn/dusty/'): 
    dat_dir = '/scratch/gpfs/chhahn/dusty/'
elif os.path.isdir('/scratch/network/chhahn/dusty/'): 
    dat_dir = '/scratch/network/chhahn/dusty/'
else: 
    dat_dir = '/Users/chahah/data/dusty/'
print(dat_dir)

# set up photometric filters u, g, r, i, z, J
filters = U.ugrizJ()

# get data 
nihao, maggies = D.nihao(filters, dust=True) 

# declare SPS model
m_nmf = Models.NMF(burst=True, emulator=True)

# prior
prior = Infer.load_priors([
    Infer.UniformPrior(7., 12.5, label='sed'),
    Infer.FlatDirichletPrior(4, label='sed'),   # flat dirichilet priors
    Infer.UniformPrior(0., 1., label='sed'), # burst fraction
    Infer.UniformPrior(1e-2, 13.27, label='sed'), # tburst
    Infer.LogUniformPrior(4.5e-5, 1.5e-2, label='sed'), # log uniform priors on ZH coeff
    Infer.LogUniformPrior(4.5e-5, 1.5e-2, label='sed'), # log uniform priors on ZH coeff
    Infer.UniformPrior(0., 3., label='sed'),        # uniform priors on dust1
    Infer.UniformPrior(0., 3., label='sed'),        # uniform priors on dust2
    Infer.UniformPrior(-2., 1., label='sed'),   # uniform priors on dust_index
    Infer.UniformPrior(0.01, 0.2, label='sed')   # uniform priors on photoz 
])


def log_prior(theta): 
    ''' prior
    '''
    lp = prior.lnPrior(theta)
    if not np.isfinite(lp): 
        return -np.inf
    return lp 


def log_like(tt, photo_obs, photo_ivar_obs, filters=None):
    ''' calculated the log likelihood. 
    '''
    # calculate SED model(theta) 
    _sed = m_nmf.sed(tt[:-1], tt[-1], filters=filters)
    _, _flux, photo = _sed

    # data - model(theta) for photometry  
    dphoto = (photo - photo_obs) 
    # calculate chi-squared for photometry 
    return -0.5 * np.sum(dphoto**2 * photo_ivar_obs) 

        
def log_post(theta, *args, **kwargs): 
    ''' posterior
    '''
    lp = log_prior(theta) # log prior
    if not np.isfinite(lp): 
        return -np.inf

    # transformed theta. Some priors require transforming the parameter
    # space for sampling (e.g. Dirichlet). For most priors, this
    # transformation will return the same value  
    ttheta = prior.transform(theta) 

    # calculate likelihood 
    lnlike = log_like(ttheta, *args, **kwargs)

    return lp  + lnlike 


# initialize walkers 
nwalkers = 30 
ndim = 12

if not keep: 
    _lnpost = lambda tt: -2. * log_post(tt, maggies[ised], np.ones(maggies.shape[1]), filters=filters) 

    x0 = prior.sample()
    std0 = 0.1*np.std([prior.sample() for i in range(10)], axis=0)

    min_result = op.minimize(
            _lnpost, 
            x0, 
            method='Nelder-Mead', 
            options={'maxiter': 1000}) 
    tt0 = min_result['x'] 
    logp0 = -0.5*min_result['fun']

    p0 = [tt0 + 1e-3 * std0 * np.random.randn(ndim) for i in range(nwalkers)]
    # chekc that they're within the prior
    for i in range(nwalkers): 
        while not np.isfinite(log_prior(p0[i])): 
            p0[i] = tt0 + 1e-3 * std0 * np.random.randn(ndim)
else: 
    p0 = np.load(os.path.join(dat_dir, 'mcmc/mcmc.noz.%i.%i.npy' % (igal, iang)))[-1,:,:]

zeus_sampler = zeus.EnsembleSampler(
        len(p0),
        len(p0[0]), 
        log_post, 
        args=(maggies[ised], np.ones(maggies.shape[1])), 
        kwargs={'filters': filters})

zeus_sampler.run_mcmc(p0, nmcmc, progress=True)

np.save(os.path.join(dat_dir, 'mcmc/mcmc.noz.%i.%i.npy' % (igal, iang)), 
        zeus_sampler.get_chain())
