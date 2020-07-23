import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('matplotlibrc')

# typical errors for abundances (from Table 8, Gjoll 2/G31873905)
err = {'Mg/Fe': 0.23, 'Al/Fe': 0.4, 'Si/Fe': 0.31, 'Na/Fe': 0.27, 'Fe/H': 0.27, 'Y/Fe': 0.25, 'Ca/Fe': 0.28}
err['alpha/Fe'] = np.sqrt(err['Mg/Fe']**2 + err['Si/Fe']**2 + err['Ca/Fe']**2) / 3

data = {}
keys = ['C09', 'C09_upper', 'M18', 'M20',
        'Gjoll1', 'Gjoll2', 'Gjoll4', 'Gjoll5', 'gjoll']
files = ['carretta_asp', 'carretta_upper_asp', 'Magurno18', 'N3201_red_asp',
         'Gjoll1', 'Gjoll2', 'Gjoll4', 'Gjoll5', 'gjoll']
skipends = [1, 3, 0, 0, 1, 0, 0, 1, 0]
k = {'sep': '\s+', 'engine': 'python'}
for key, file, foot in zip(keys, files, skipends):
    infile = 'data/abundances/'+file+'.tab'
    col = None if key == 'M20' else 0
    data[key] = pd.read_csv(infile, index_col=col, skipfooter=foot, **k)

upper = data['C09'] == -9.99
C09_upper = data['C09_upper'].where(~(upper * data['C09_upper'] == 0), other=-9.99)

sel = data['gjoll'].index != 'Gjoll1'
fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(8,8))
c = ['lightgrey', 'black', 'blue', 'green', 'orange']
s = 20
k = {'marker': '*', 's': s**2, 'zorder': 100}
up = {'c': 'black', 'fmt': '*', 'uplims': True, 'yerr': 0.3, 'ms': s}
C09up = {'c': c[0], 'fmt': 'o', 'uplims': True, 'yerr': 0.1, 'ms': 0}

# Al/Fe vs Mg/Fe
ax[0,0].plot(data['C09']['Mg'], data['C09']['Al'], 's', c=c[0])
ax[0,0].plot(data['M20']['[Mg/Fe]'], data['M20']['[Al/Fe]'], 'o', c=c[0])
ax[0,0].scatter(data['gjoll']['Mg'][sel], data['gjoll']['Al'][sel], c=c[2:], **k)
ax[0,0].errorbar(data['gjoll']['Mg'][~sel], data['gjoll']['Al'][~sel], **up)
ax[0,0].errorbar(data['C09']['Mg'], C09_upper['Al'], **C09up)
ax[0,0].errorbar(0.533,-0.9, xerr=err['Mg/Fe'], yerr=err['Al/Fe'], c='k')
ax[0,0].set_xlim(-1, 1)
ax[0,0].set_ylim(-1.5, 1.5)
ax[0,0].set_xlabel('[Mg/Fe]')
ax[0,0].set_ylabel('[Al/Fe]')

# Al/Fe vs Si/Fe
ax[0,1].plot(data['C09']['Si'], data['C09']['Al'], 's', c=c[0])
ax[0,1].plot(data['M20']['[Si/Fe]'], data['M20']['[Al/Fe]'], 'o', c=c[0])
ax[0,1].scatter(data['gjoll']['Si'][sel], data['gjoll']['Al'][sel], c=c[2:], **k)
ax[0,1].errorbar(data['gjoll']['Si'][~sel], data['gjoll']['Al'][~sel], **up)
ax[0,1].errorbar(data['C09']['Si'], C09_upper['Al'], **C09up)
ax[0,1].errorbar(0.65,-0.9, xerr=err['Si/Fe'], yerr=err['Al/Fe'], c='k')
ax[0,1].set_xlim(-0.5, 1)
ax[0,1].set_ylim(-1.5, 1.5)
ax[0,1].set_xlabel('[Si/Fe]')
ax[0,1].set_ylabel('[Al/Fe]')

# Mg/Fe vs Si/Fe
ax[1,0].plot(data['C09']['Si'], data['C09']['Mg'], 's', c=c[0])
ax[1,0].plot(data['M20']['[Si/Fe]'], data['M20']['[Mg/Fe]'], 'o', c=c[0])
ax[1,0].scatter(data['gjoll']['Si'], data['gjoll']['Mg'], c=c[1:], **k)
ax[1,0].errorbar(data['C09']['Si'], C09_upper['Mg'], **C09up)
ax[1,0].errorbar(0.65,-0.14, xerr=err['Si/Fe'], yerr=err['Mg/Fe'], c='k')
ax[1,0].set_xlim(-0.5, 1)
ax[1,0].set_ylim(-0.5, 1)
ax[1,0].set_xlabel('[Si/Fe]')
ax[1,0].set_ylabel('[Mg/Fe]')

# Al/Fe vs Na/Fe
ax[1,1].plot(data['C09']['Na'], data['C09']['Al'], 's', c=c[0])
ax[1,1].plot(data['M20']['[Na/Fe]'], data['M20']['[Al/Fe]'], 'o', c=c[0])
ax[1,1].scatter(data['gjoll']['Na'][sel], data['gjoll']['Al'][sel], c=c[2:], **k)
ax[1,1].errorbar(data['gjoll']['Na'][~sel], data['gjoll']['Al'][~sel], **up)
ax[1,1].errorbar(data['C09']['Na'], C09_upper['Al'], **C09up)
ax[1,1].errorbar(0.65,-0.9, xerr=err['Na/Fe'], yerr=err['Al/Fe'], c='k')
ax[1,1].set_xlim(-0.5, 1)
ax[1,1].set_ylim(-1.5, 1)
ax[1,1].set_xlabel('[Na/Fe]')
ax[1,1].set_ylabel('[Al/Fe]')

plt.tight_layout()
plt.savefig('plots/pdfs/na-mg-al-si.pdf', bbox_inches='tight')

# alpha/Fe vs Fe/H
data['C09']['alpha'] = data['C09'][['Mg', 'Si']].mean(axis=1)
data['M20']['alpha'] = data['M20'][['[Mg/Fe]', '[Si/Fe]', '[Ca/Fe]']].mean(axis=1)
data['M18']['alpha'] = data['M18'][['[Mg/Fe]', '[Ca/Fe]']].mean(axis=1)
data['gjoll']['alpha'] = data['gjoll'][['Mg', 'Si', 'Ca']].mean(axis=1)

fig, ax = plt.subplots(figsize=(4,4))
ax.plot(data['C09']['Fe'], data['C09']['alpha'], 's', c=c[0])
ax.plot(data['M20']['[Fe/H]'], data['M20']['alpha'], 'o', c=c[0])
ax.plot(data['M18']['Fe/H'], data['M18']['alpha'], '*', c=c[0], ms=10)
ax.scatter(data['gjoll']['Fe'], data['gjoll']['alpha'], c=c[1:], **k)
ax.errorbar(-0.845,-0.14, xerr=err['Fe/H'], yerr=err['alpha/Fe'], c='k')
ax.set_xlim(-2, -0.5)
ax.set_ylim(-0.5, 1)
ax.set_xlabel('[Fe/H]')
ax.set_ylabel(r'[$\alpha$/Fe]')
plt.tight_layout()
plt.savefig('plots/pdfs/alpha-vs-fe.pdf', bbox_inches='tight')

# Y/Fe vs Fe/H
up = {'c': c[-1], 'fmt': '*', 'uplims': True, 'yerr': 0.2, 'ms': s, 'zorder': 100}
fig, ax = plt.subplots(figsize=(4,4))
ax.plot(data['M18']['Fe/H'], data['M18']['[Y/Fe]'], '*', c=c[0], ms=10)
ax.errorbar(-0.845,-0.14, xerr=err['Fe/H'], yerr=err['Y/Fe'], c='k')
ax.scatter(data['gjoll']['Fe'], data['gjoll']['Y'], c=c[1:], **k)
ax.errorbar(data['gjoll'].loc['Gjoll5']['Fe'], data['gjoll'].loc['Gjoll5']['Y'], **up)
ax.set_xlim(-2, -0.5)
ax.set_ylim(-0.5, 1)
ax.set_xlabel('[Fe/H]')
ax.set_ylabel('[Y/Fe]')
plt.tight_layout()
plt.savefig('plots/pdfs/y-vs-fe.pdf', bbox_inches='tight')
