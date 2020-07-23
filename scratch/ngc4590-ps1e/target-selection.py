import numpy as np
import astropy.units as u
import astropy.coordinates as coord
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import interp1d
import utils

# Galactocentric frame post-Gaia (defaults from astropy v4.0)
coord.galactocentric_frame_defaults.set('v4.0')

# parameters for orbit integration
timestep = -1 * u.Myr
totaltime = 500*u.Myr

# cluster coordinates
glob = coord.SkyCoord(ra=189.867*u.deg,
                      dec=-26.744*u.deg,
                      distance=10.3*u.kpc,
                      pm_ra_cosdec=-2.752*u.mas/u.yr,
                      pm_dec=1.762*u.mas/u.yr,
                      radial_velocity=-92.99*u.km/u.s)
monte = np.random.normal(loc=[10.3, -2.752, 1.762, -92.99],
                         scale=[0.4738, 0.044, 0.044, 0.22],
                         size=(100, 4)).T
MCglob = coord.SkyCoord(ra=glob.ra,
                        dec=glob.dec,
                        distance=monte[0]*u.kpc,
                        pm_ra_cosdec=monte[1]*u.mas/u.yr,
                        pm_dec=monte[2]*u.mas/u.yr,
                        radial_velocity=monte[3]*u.km/u.s)

# integrate orbits
orbit = utils.integrate_orbit(init=MCglob, total=totaltime, tstep=timestep)
orbit0 = utils.integrate_orbit(init=glob, total=totaltime, tstep=timestep)
orbit_gal = coord.SkyCoord(l=orbit0['l'], b=orbit0['b'], frame=coord.Galactic)
orbit_icrs = coord.SkyCoord(ra=orbit0['ra'],
                            dec=orbit0['dec'],
                            distance=orbit0['dist'],
                            pm_ra_cosdec=orbit0['pmra'],
                            pm_dec=orbit0['pmdec'], frame=coord.ICRS)

# interpolate orbit as a function of l
x = orbit_gal.l.value
y = np.vstack([orbit_icrs.pm_ra_cosdec.value,
               orbit_icrs.pm_dec.value,
               orbit_gal.b.value,
               orbit_icrs.distance.value,
               orbit_icrs.distance.parallax.value])
f = interp1d(x,y, fill_value=[-99,-99,-99,np.inf,-99], bounds_error=False)

# load the (large) query from Gaia
df = pd.read_csv('scratch/ngc4590-ps1e/query-stream-20mag.csv')
df = df[utils.recommended_quality_cut(df)]
sc = coord.SkyCoord(ra=df['ra'].values*u.deg,
                    dec=df['dec'].values*u.deg,
                    pm_ra_cosdec=df['pmra'].values*u.mas/u.yr,
                    pm_dec=df['pmdec'].values*u.mas/u.yr)
sc_gal = sc.transform_to(coord.Galactic)
utils.extinction_correct_photometry(df)

# load the Helmi+18 stars in NGC 3201 (for making CMD)
helmi = pd.read_csv('scratch/ngc4590-ps1e/NGC4590.csv')
utils.extinction_correct_photometry(helmi)
helmi['M_G'] = helmi['g0'] - glob.distance.distmod.value

# cuts based on tolerances around orbit
pmra, pmdec, b, distance, parallax = f(sc_gal.l)
sel = (np.abs(pmra * u.mas/u.yr - sc.pm_ra_cosdec).value / df['pmra_error']) < 2
sel &= (np.abs(pmdec * u.mas/u.yr - sc.pm_dec).value / df['pmdec_error']) < 2
sel &= np.abs(parallax - df['parallax'])/df['parallax_error'] < 3
sel &= np.abs(b * u.deg - sc_gal.b) < 1*u.deg

a = 480
xvar, yvar = ['ra', 'pmdec']
plt.plot(orbit[xvar][a:], orbit[yvar][a:], 'C0', alpha=0.2)
plt.plot(df[xvar][sel], df[yvar][sel], 'C1.')
plt.xlim(160,195);

plt.plot(helmi['bp_rp0'], helmi['M_G'], '.')
plt.plot(df['bp_rp0'][sel], df['M_G'][sel], '.')
plt.xlim(0,2)
plt.ylim(5,-4);

# flag if candidate falls near CMD (Dotter, Fe/H=-1.241, 11.1 Gyr)
iso = utils.isochrone()
df['M_G'] = df['g0'] - coord.Distance(distance*u.kpc).distmod.value
df['cmdflag'] = np.abs(df['bp_rp0'] - iso(df['M_G'])) < 0.1

# select stars that are kinematic candidates
cand_kinematic = df[sel].copy()
cand = cand_kinematic[cand_kinematic['g'] < 15]

cand.set_index('source_id', inplace=True)
cand_kinematic.set_index('source_id', inplace=True)

# helpful info for Terese
cand['coordstring'] = coord.SkyCoord(cand['ra'], cand['dec'], unit='deg').to_string('hmsdms')
cand['johnson_V'] = cand['g'] - (-0.01760 - 0.006860*cand['bp_rp'] - 0.1732*(cand['bp_rp']**2))

# cand.to_csv('data/gjoll-candidates/gjoll-plus-bright.csv')
# cand_kinematic.to_csv('data/gjoll-candidates/all-candidates.csv')
