import pandas as pd

cnpj = pd.read_csv('estabelecimentos.csv', sep=';', decimal=',', low_memory=False)

# filter where telefone 1 or 2 has the first digits greater then 6
# fill nan with nan
cnpj['telefone_1'] = cnpj['telefone_1'].fillna('0')
cnpj['telefone_2'] = cnpj['telefone_2'].fillna('0')
cnpj = cnpj[(cnpj['telefone_1'].str[0].astype(int) > 6) | (cnpj['telefone_2'].str[0].astype(int) > 6)]

# filter where capital social is LESS then 30M
# replace nan with 0
cnpj['capital_social'] = cnpj['capital_social'].fillna(0)
cnpj = cnpj[cnpj['capital_social'].astype(float) < 30000000]

# save
cnpj.to_csv('estabelecimentos_filtered.csv', sep=';', decimal=',', index=False)

# txt with only telefone 1 and 2
telefones = cnpj[['ddd_1', 'telefone_1']].copy()
telefones.columns = ['ddd', 'telefone']
# append telefone 2
cnpj['ddd'] = cnpj['ddd_2']
cnpj['telefone'] = cnpj['telefone_2']
telefones = telefones._append(cnpj[['ddd', 'telefone']])


telefones = telefones.drop_duplicates()
# fill nan with 0
telefones = telefones.dropna()
telefones = telefones.fillna('nan')
telefones = telefones[telefones != '0']
telefones = telefones[telefones != 'nan']
telefones = telefones[telefones != '']
telefones['telefone'] = telefones['telefone'].astype(str)
telefones['ddd'] = telefones['ddd'].astype(str)
telefones['telefone'] = telefones['telefone'].str.replace('.0', '')
telefones['ddd'] = telefones['ddd'].str.replace('.0', '')
telefones = telefones[(telefones['telefone'].str[0].astype(int) > 6)]


telefones = telefones.reset_index(drop=True)
print(telefones.shape)

# convert ddd to 2 digits and str
telefones = telefones.astype(str)
telefones['ddd'] = telefones['ddd'].str[0:2]

# add ddi
telefones['ddi'] = '55'

# complete number ddi + ddd + telefone
telefones['telefone_completo'] = telefones['ddi'] + telefones['ddd'] + telefones['telefone']

# save
telefones.to_csv('telefones.csv', sep=';', decimal=',', index=False)