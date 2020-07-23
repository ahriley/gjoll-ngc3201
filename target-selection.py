import numpy as np
import astropy.units as u
import astropy.coordinates as coord
import matplotlib.pyplot as plt
import gala.potential as gp
import gala.dynamics as gd
import pandas as pd
from scipy.interpolate import interp1d
import utils

# Galactocentric frame post-Gaia (defaults from astropy v4.0)
coord.galactocentric_frame_defaults.set('v4.0')

# potential default from gala
potential = gp.MilkyWayPotential()

# parameters for orbit integration
timestep = 0.05 * u.Myr
totaltime = 25*u.Myr
nsteps = (totaltime / timestep).to(u.dimensionless_unscaled)

# NGC 3201 coordinates
icrs = coord.SkyCoord(ra=154.403*u.deg,
                      dec=-46.412*u.deg,
                      distance=4.9*u.kpc,
                      pm_ra_cosdec=8.324*u.mas/u.yr,
                      pm_dec=-1.991*u.mas/u.yr,
                      radial_velocity=494.34*u.km/u.s)

# integrate NGC 3201 orbit
galcen = icrs.transform_to(coord.Galactocentric)
w0 = gd.PhaseSpacePosition(galcen.data)
orbit = potential.integrate_orbit(w0, dt=-timestep, n_steps=nsteps)
sc = coord.SkyCoord(x=orbit.x, y=orbit.y, z=orbit.z,
                    v_x=orbit.v_x, v_y=orbit.v_y, v_z=orbit.v_z,
                    frame=coord.Galactocentric)
orbit_gal = sc.transform_to(coord.Galactic)
orbit_icrs = sc.transform_to(coord.ICRS)

# interpolate orbit as a function of l
x = orbit_gal.l.value
y = np.vstack([orbit_icrs.pm_ra_cosdec.value,
               orbit_icrs.pm_dec.value,
               orbit_gal.b.value,
               orbit_gal.distance.value,
               orbit_gal.distance.parallax.value])
f = interp1d(x,y, fill_value=[-99,-99,-99,np.inf,-99], bounds_error=False)

# load Ibata+19 data
df_ibata = pd.read_csv('data/gaia-data/ibata19.csv')
df_ibata['v_hel_ibata'] = [74.41, -10.92, 0.81, -15.18, -33.17, -80.44]
df_ibata['v_hel_error_ibata'] = [1.51, 0.28, 3.18, 4.38, 0.65, 0.26]
df_ibata['good_cand_ibata'] = ['Y', 'Y', 'N', 'Y', 'N', 'N']
ibata = coord.SkyCoord(ra=df_ibata['ra'].values*u.deg,
                    dec=df_ibata['dec'].values*u.deg,
                    pm_ra_cosdec=df_ibata['pmra'].values*u.mas/u.yr,
                    pm_dec=df_ibata['pmdec'].values*u.mas/u.yr,
                    radial_velocity=df_ibata['v_hel_ibata'].values*u.km/u.s)
ibata_gal = ibata.transform_to(coord.Galactic)
utils.extinction_correct_photometry(df_ibata)

# load the (large) query from Gaia
df = pd.read_csv('data/gaia-data/final-input.csv')
df = df[utils.recommended_quality_cut(df)]
sc = coord.SkyCoord(ra=df['ra'].values*u.deg,
                    dec=df['dec'].values*u.deg,
                    pm_ra_cosdec=df['pmra'].values*u.mas/u.yr,
                    pm_dec=df['pmdec'].values*u.mas/u.yr)
sc_gal = sc.transform_to(coord.Galactic)
utils.extinction_correct_photometry(df)

# cuts based on tolerances around orbit
pmra, pmdec, b, distance, parallax = f(sc_gal.l)
sel = np.abs(pmra * u.mas/u.yr - sc.pm_ra_cosdec) < 1.5 * u.mas/u.yr
sel &= np.abs(pmdec * u.mas/u.yr - sc.pm_dec) < 1.5 * u.mas/u.yr
sel &= np.abs(parallax - df['parallax'])/df['parallax_error'] < 4
sel &= np.abs(b * u.deg - sc_gal.b) < 3*u.deg

# flag if candidate falls near CMD (Dotter, Fe/H=-1.241, 11.1 Gyr)
iso = utils.isochrone()
df['M_G'] = df['g0'] - coord.Distance(distance*u.kpc).distmod.value
df_ibata['M_G'] = df_ibata['g0'] - coord.Distance(f(ibata_gal.l)[3]*u.kpc).distmod.value
df['cmdflag'] = np.abs(df['bp_rp0'] - iso(df['M_G'])) < 0.1
df_ibata['cmdflag'] = np.abs(df_ibata['bp_rp0'] - iso(df_ibata['M_G'])) < 0.1

# select stars that are kinematic candidates
cand_kinematic = df[sel].copy()
cand = cand_kinematic[cand_kinematic['g'] < 15]

# merge with Ibata results for convenience
cand = pd.concat([df_ibata, cand], sort=False)

cand.drop_duplicates(subset=['source_id'], inplace=True)
cand['good_cand_ibata'].fillna('NA', inplace=True)

cand.set_index('source_id', inplace=True)
cand_kinematic.set_index('source_id', inplace=True)

# helpful info for Terese
cand['coordstring'] = coord.SkyCoord(cand['ra'], cand['dec'], unit='deg').to_string('hmsdms')
cand['johnson_V'] = cand['g'] - (-0.01760 - 0.006860*cand['bp_rp'] - 0.1732*(cand['bp_rp']**2))

# re-identify already observed objects
cand['other_id'] = ''
cand.loc[3200439105894310272, 'other_id'] = 'ibata_1'
cand.loc[3254112556278356608, 'other_id'] = 'gjoll_1' # ibata_2
cand.loc[3187390548572555136, 'other_id'] = 'gjoll_2' # ibata_3
cand.loc[3229373063616887936, 'other_id'] = 'ibata_4' # gjoll_3, not followed up
cand.loc[3188058536245928576, 'other_id'] = 'ibata_5'
cand.loc[2985543956292701312, 'other_id'] = 'ibata_6'
cand.loc[2990142148280216960, 'other_id'] = 'gjoll_4'
cand.loc[3259158764894232192, 'other_id'] = 'gjoll_5'
cand.loc[3258976074166599680, 'other_id'] = 'gjoll_6'
cand.dropna(subset=['ra'], inplace=True)

# add Terese's radial velocities
cand['v_hel'] = cand['v_hel_ibata']
cand.loc[3254112556278356608, 'v_hel'] = -79.5
cand.loc[3187390548572555136, 'v_hel'] = -10.3
cand.loc[2990142148280216960, 'v_hel'] = 7.2
cand.loc[3259158764894232192, 'v_hel'] = -150.6
cand.loc[3258976074166599680, 'v_hel'] = 112.1

cand['v_hel_error'] = cand['v_hel_error_ibata']
cand.loc[3254112556278356608, 'v_hel_error'] = 0.9
cand.loc[3187390548572555136, 'v_hel_error'] = 0.6
cand.loc[2990142148280216960, 'v_hel_error'] = 0.6
cand.loc[3259158764894232192, 'v_hel_error'] = 3.5
cand.loc[3258976074166599680, 'v_hel_error'] = 3

cand.to_csv('data/gaia-data/gjoll-plus-bright.csv')
cand_kinematic.to_csv('data/gaia-data/all-candidates.csv')
