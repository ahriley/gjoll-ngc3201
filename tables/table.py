import pandas as pd

def row_to_tex(row):
    if 'good_cand_ibata' in row.index:
        flag = '' if pd.isnull(row['good_cand_ibata']) else row['good_cand_ibata']
    else:
        flag = ''

    string = str(row['source_id']) + ' & '
    string += "${0:.3f}$ & ".format(row['ra'])
    string += "${0:.3f}$ & ".format(row['dec'])
    string += "{0:.3f} & ".format(row['g0'])
    string += "{0:.3f} & ".format(row['bp_rp0'])
    string += "${0:.2f} \pm {1:.2f}$ & ".format(row['parallax'], row['parallax_error'])
    string += "${0:.2f} \pm {1:.2f}$ & ".format(row['pmra'], row['pmra_error'])
    string += "${0:.2f} \pm {1:.2f}$ & ".format(row['pmdec'], row['pmdec_error'])
    if 'v_hel' in row.index:
        if pd.isnull(row['v_hel']):
            string += ''
        else:
            string += "${0:.2f} \pm {1:.2f}$".format(row['v_hel'], row['v_hel_error'])
        if ~pd.isnull(row['other_id']) & ('ibata' in row['other_id']):
            string += '*'
    else:
        string += ''
    string += ' & ' + flag
    string += ' \\\\\n'

    return string

df = pd.read_csv('data/gaia-data/gjoll-plus-bright.csv')
filename = 'tables/candidates.tex'
df.sort_values('ra', inplace=True)

all = pd.read_csv('data/gaia-data/all-candidates.csv')
all = all[all['cmdflag'] == True]
all.sort_values('ra', inplace=True)

with open(filename, 'w') as f:
    for name, row in df.iterrows():
        string = row_to_tex(row)
        f.write(string)
    f.write('\\hline \n')

    for name, row in all.iloc[:5].iterrows():
        string = row_to_tex(row)
        f.write(string)
    string = '\\vdots & ' * 10
    f.write(string[:-2] + "\\\\\n")

cols = ['source_id', 'ra', 'dec', 'g0', 'bp_rp0', 'parallax', 'parallax_error',
        'pmra', 'pmra_error', 'pmdec', 'pmdec_error', 'v_hel', 'v_hel_error',
        'good_cand_ibata']
table1 = pd.concat([df, all], ignore_index=True)[cols]
table1.drop_duplicates(subset=['source_id'], inplace=True)
table1.to_csv('tables/table1-long.csv', index=False)
