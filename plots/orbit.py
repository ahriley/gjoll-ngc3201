import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import astropy.coordinates as coord
import astropy.units as u
import gala.potential as gp
import gala.dynamics as gd
import utils

plt.style.use('matplotlibrc')

# assumed Galactocentric properties
coord.galactocentric_frame_defaults.set('v4.0')

# parameters for orbit integration
potential = gp.MilkyWayPotential()
totaltime = 21 * u.Myr
timestep = -0.05 * u.Myr

# load candidate stream members
df = pd.read_csv('data/gaia-data/gjoll-plus-bright.csv')

cand = coord.SkyCoord(ra=df['ra'].values*u.deg,
                      dec=df['dec'].values*u.deg,
                      pm_ra_cosdec=df['pmra'].values*u.mas/u.yr,
                      pm_dec=df['pmdec'].values*u.mas/u.yr)
cand_gal = cand.transform_to(coord.Galactic)
df['l'] = cand_gal.l
df['b'] = cand_gal.b

# present-day coordinates of NGC 3201 (Vasiliev2019)
glob = coord.SkyCoord(ra=154.403*u.deg,
                      dec=-46.412*u.deg,
                      distance=4.9*u.kpc,
                      pm_ra_cosdec=8.324*u.mas/u.yr,
                      pm_dec=-1.991*u.mas/u.yr,
                      radial_velocity=494.34*u.km/u.s)
monte = np.random.normal(loc=[4.9, 8.324, -1.991, 494.34],
                         scale=[0.225, 0.044, 0.044, 0.14],
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

# load other datasets
all = pd.read_csv('data/gaia-data/all-candidates.csv')
sc = coord.SkyCoord(ra=all['ra'], dec=all['dec'], unit='deg')
sc = sc.transform_to(coord.Galactic)
all['l'] = sc.l.deg
all['b'] = sc.b.deg
all = all[all['l'] < 260]
n3201 = pd.read_csv('data/gaia-data/NGC3201.csv', index_col=0)
utils.extinction_correct_photometry(n3201)
n3201['M_G'] = n3201['g0'] - glob.distance.distmod.value

ebar = {'fmt': 'none'}

labels = ['b [deg]', r'$\mu_\alpha$ [mas yr$^{-1}$]',
          r'$\mu_\delta$ [mas yr$^{-1}$]', r'$\delta\pi$ [mas]',
          r'v$_\mathrm{helio}$ [km s$^{-1}$]', r'$M_G$ [mag]']
limits = [(-40, 15), (15, 25), (-25, -15), (0, 0.7), (-200, 150), (6.1,-3)]
s = 20
k = {'marker': '*', 's': s**2, 'zorder': 100}

sel = df['M_G'] > 2
ibata = df[sel]
df = df[~sel]

# orbit/cluster, all candidates, special
# c = ['C0', 'C1', 'orange', 'red', 'green', 'blue', 'black']
c = ['C0', 'C1', 'blue', 'black', 'orange', 'red', 'green']
i19c = 'black'

fig = plt.figure(constrained_layout=True, figsize=(15,9))
gs = fig.add_gridspec(3, 3)
spaces = [gs[0, :], gs[1, 0], gs[1, 1], gs[2, 0], gs[2, 1], gs[1:, 2]]
pars = ['b', 'pmra', 'pmdec', 'parallax', 'v_hel', 'M_G']
for space, par, label, lim in zip(spaces, pars, labels, limits):
    ax = fig.add_subplot(space)
    ax.set_ylabel(label)
    ax.set_ylim(lim[0], lim[1])
    if par == 'M_G':
        ax.plot(n3201['bp_rp0'], n3201['M_G'], '.', c=c[0], alpha=0.1, rasterized=True)
        ax.plot(all['bp_rp0'], all['M_G'], '.', c=c[1])
        ax.scatter(df['bp_rp0'], df['M_G'], c=c[2:], **k)
        ax.plot(ibata['bp_rp0'], ibata['M_G'], 'o', c=i19c)
        ax.set_xlim(0,2)
        ax.set_xlabel(r'$(G_{BP} - G_{RP})_0$')
        continue
    if par == 'parallax':
        ax.plot(all['parallax'], all['parallax_error'], '.', c=c[1])
        ax.plot(ibata['parallax'], ibata['parallax_error'], 'o', c=i19c)
        ax.scatter(df['parallax'], df['parallax_error'], c=c[2:], **k)
        ax.set_xlim(-0.5,1.5)
        ax.set_xlabel(r'$\pi$ [mas]')
        continue
    ax.plot(orbit['l'], orbit[par], c=c[0], alpha=0.05)
    ax.plot(orbit0['l'], orbit0[par], '--', c=c[0])
    ax.set_xlabel('l [deg]')
    if par == 'b':
        ax.scatter(orbit['l'][0,0], orbit['b'][0,0], facecolors='none', edgecolors=c[0], **k)
        ax.plot(all['l'], all['b'], '.', c=c[1])
        ax.plot(ibata['l'], ibata['b'], 'o', c=i19c)
        ax.scatter(df['l'], df['b'], c=c[2:], **k)
        ax.set_xlim(180, 280)
        continue
    if par != 'v_hel':
        ax.errorbar(all['l'], all[par], yerr=all[par+'_error'], ecolor=c[1], **ebar)
        ax.plot(all['l'], all[par], '.', c=c[1])
    ax.errorbar(df['l'], df[par], yerr=df[par+'_error'], ecolor=c[2:], **ebar)
    ax.scatter(df['l'], df[par], c=c[2:], **k)
    ax.errorbar(ibata['l'], ibata[par], yerr=ibata[par+'_error'], ecolor=i19c, **ebar)
    ax.scatter(ibata['l'], ibata[par], c=i19c, zorder=100)
    ax.set_xlim(185, 220)

plt.savefig('plots/pdfs/orbit.pdf', bbox_inches='tight')
