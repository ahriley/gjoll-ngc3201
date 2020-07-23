import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import sfdmap
import astropy.units as u
import gala.potential as gp
import gala.dynamics as gd
import astropy.coordinates as coord

# sfdmap for calculating extinction using Schlafly & Finkbeiner (2011)
# corrections to the Schlegel+98 dust maps
m_g = sfdmap.SFDMap('$HOME/sfddata/', scaling=0.85926)
m_bp = sfdmap.SFDMap('$HOME/sfddata/', scaling=1.06794)
m_rp = sfdmap.SFDMap('$HOME/sfddata/', scaling=0.65199)

def extinction_correct_photometry(df):
    ra, dec = df[['ra', 'dec']].values.T
    df['g0'] = df['g'] - 3.1*m_g.ebv(ra, dec, unit='degree')
    df['bp_rp0'] = df['bp_rp']
    df['bp_rp0'] -= 3.1*m_bp.ebv(ra, dec, unit='degree')
    df['bp_rp0'] += 3.1*m_rp.ebv(ra, dec, unit='degree')

def integrate_orbit(init, total, tstep):
    potential = gp.MilkyWayPotential()
    coord.galactocentric_frame_defaults.set('v4.0')

    nsteps = np.abs((total / tstep).to(u.dimensionless_unscaled))
    galcen = init.transform_to(coord.Galactocentric)
    w0 = gd.PhaseSpacePosition(galcen.data)
    orbit = potential.integrate_orbit(w0, dt=tstep, n_steps=nsteps)
    sc = coord.SkyCoord(x=orbit.x, y=orbit.y, z=orbit.z,
                        v_x=orbit.v_x, v_y=orbit.v_y, v_z=orbit.v_z,
                        frame=coord.Galactocentric)
    sc = sc.transform_to(coord.ICRS)
    result = {'ra': sc.ra, 'dec': sc.dec, 'parallax': sc.distance.parallax,
              'dist': sc.distance, 'pmra': sc.pm_ra_cosdec,
              'pmdec': sc.pm_dec, 'v_hel': sc.radial_velocity,
              'l': sc.galactic.l, 'b': sc.galactic.b}
    return result

def isochrone(file=None):
    if file is None:
        file = 'data/isochrones/dotter08-1p241-11p1.dat'

    assert 'dotter' in file, 'Only trust interpolating Dotter isochrones'
    iso = pd.read_csv(file, header=8, sep='\s+')
    color = iso['Gaia_BP'] - iso['Gaia_RP']
    return interp1d(iso['Gaia_G'], color, fill_value=-99, bounds_error=False)

def recommended_quality_cut(df):
    u = df['astrometric_chi2_al'] / (df['astrometric_n_good_obs_al'] - 5)
    u = np.sqrt(u)
    limit = np.exp(-0.2*(df['g'] - 19.5))
    limit[limit < 1] = 1

    sel = df['astrometric_excess_noise'] < 1
    sel &= u < 1.2 * limit
    sel &= df['phot_bp_rp_excess_factor'] < 1.3 + 0.06 * df['bp_rp']**2
    sel &= df['phot_bp_rp_excess_factor'] > 1 + 0.015 * df['bp_rp']**2

    return sel
