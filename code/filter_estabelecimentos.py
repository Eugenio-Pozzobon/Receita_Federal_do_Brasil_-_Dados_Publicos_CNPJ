import pandas as pd

# cnpj = pd.read_csv('estabelecimentos.csv', sep=';', decimal=',', low_memory=False)
#
#
# # filter where telefone 1 or 2 has the first digits greater then 6
# # fill nan with nan
# cnpj['telefone_1'] = cnpj['telefone_1'].fillna('0')
# cnpj['telefone_2'] = cnpj['telefone_2'].fillna('0')
# cnpj = cnpj[(cnpj['telefone_1'].str[0].astype(int) > 6) | (cnpj['telefone_2'].str[0].astype(int) > 6)]
#
# # filter where capital social is LESS then 30M
# # replace nan with 0
# cnpj['capital_social'] = cnpj['capital_social'].fillna(0)
# cnpj = cnpj[cnpj['capital_social'].astype(float) < 30000000]
#
# # filter unique cnpj_basico
#
# # save
# cnpj.to_csv('estabelecimentos_filtered.csv', sep=';', decimal=',', index=False)
# print('estabelecimentos_filtered.csv saved')

cnpj = pd.read_csv('estabelecimentos_filtered.csv', sep=';', decimal=',', low_memory=False)
cnpj = cnpj.drop_duplicates(subset=['cnpj_basico'])
# filter only where uf = rs
# cnpj = cnpj[cnpj['uf'] == 'RS']
# drop if there is fax number
cnpj = cnpj[cnpj['fax'].isnull()]
cnpj = cnpj.reset_index(drop=True)
print('estabelecimentos_filtered.csv filtered step 1')

cnpj['telefone_1'] = cnpj['telefone_1'].astype(str)
cnpj['telefone_2'] = cnpj['telefone_2'].astype(str)
cnpj['ddd_1'] = cnpj['ddd_1'].astype(str)
cnpj['ddd_2'] = cnpj['ddd_2'].astype(str)
cnpj['telefone_1'] = cnpj['telefone_1'].str.replace('.0', '')
cnpj['telefone_2'] = cnpj['telefone_2'].str.replace('.0', '')
cnpj['ddd_1'] = cnpj['ddd_1'].str.replace('.0', '')
cnpj['ddd_2'] = cnpj['ddd_2'].str.replace('.0', '')

cnpj['ddd_1'] = cnpj['ddd_1'].str[0:2]
cnpj['ddd_2'] = cnpj['ddd_2'].str[0:2]

# replace any telefone with  a number higher or equal to 6 to nan
cnpj.loc[cnpj['telefone_1'].str[0].astype(int) <= 6, 'telefone_1'] = 'nan'
cnpj.loc[cnpj['telefone_2'].str[0].astype(int) <= 6, 'telefone_2'] = 'nan'
# if telefones has 8 digits, add 9 in the beginning
cnpj.loc[cnpj['telefone_1'].str.len() == 8, 'telefone_1'] = '9' + cnpj['telefone_1']
cnpj.loc[cnpj['telefone_2'].str.len() == 8, 'telefone_2'] = '9' + cnpj['telefone_2']
# create a column named telefone, this column will merge ddd and telefone 1 and 2, but only the telefones that starts
# with a number higher or equal to 6

cnpj.loc[cnpj['telefone_1'] != 'nan', 'telefone'] = cnpj['ddd_1'] + cnpj['telefone_1']
cnpj.loc[(cnpj['telefone_2'] != 'nan') & cnpj['telefone'].isnull(), 'telefone'] = cnpj['ddd_2'] + cnpj['telefone_2']

# reset index
cnpj = cnpj.reset_index(drop=True)
print('estabelecimentos_filtered.csv filtered step 2')
# keep razao social, telefone, capital social Cidade - UF

municipios = pd.read_csv('F.K03200$Z.D31209.MUNICCSV', sep=';',
                         header=None, names=['id', 'nome'],
                         decimal=',', low_memory=False).astype(str)
print('municipios.csv loaded')
# merge
cnpj['municipio'] = cnpj['municipio'].astype(str)
cnpj = pd.merge(cnpj, municipios, left_on='municipio', right_on='id')
# with lambda
cnpj['Cidade - UF'] = cnpj['nome'] + ' - ' + cnpj['uf']
# save

# filter if telefone is na0 and email is empty
cnpj['correio_eletronico'] = cnpj['correio_eletronico'].astype(str)
cnpj = cnpj[(cnpj['telefone'] != 'na0') & (cnpj['correio_eletronico'] != 'nan')]
cnpj = cnpj.reset_index(drop=True)

# filter any email that contains 'esc' or 'contabil'
# convert to str and lowercase
cnpj['correio_eletronico'] = cnpj['correio_eletronico'].str.lower()
cnpj = cnpj[~cnpj['correio_eletronico'].str.contains('esc')]
cnpj = cnpj[~cnpj['correio_eletronico'].str.contains('contab')]
cnpj = cnpj[~cnpj['correio_eletronico'].str.contains('adv')]

# drop all coluns where the email and the phone repeat, without keeping the first one
cnpj = cnpj.drop_duplicates(subset=['correio_eletronico', 'telefone'], keep=False)

print('loading socios')

cnpj_basico = cnpj['cnpj_basico'].tolist()
print('len cnpj_basico: ' + str(len(cnpj_basico)))
chunks = []
for chunk in pd.read_csv('socios.csv', sep=';',
                            decimal=',', low_memory=False, chunksize=1000000):
    chunk = chunk[chunk['cnpj_basico'].isin(cnpj_basico)]
    chunk = chunk.reset_index(drop=True)
    chunks.append(chunk)
    print('chunk loaded')

socios = pd.concat(chunks, ignore_index=True)

# filter socios by cnpj_basico
# there is many columns for each socio in the same cnpj, join all the name of the socio, in a new column of cnpj
socios['nome_socio_razao_social'] = socios['nome_socio_razao_social'].astype(str)
socios = socios[['cnpj_basico', 'nome_socio_razao_social']]
socios = socios.groupby('cnpj_basico')['nome_socio_razao_social'].apply(lambda x: ', '.join(x)).reset_index()
# merge

cnpj = pd.merge(cnpj, socios, on='cnpj_basico', how='left')
cnpj = cnpj[['razao_social', 'nome_fantasia', 'nome_socio_razao_social', 'telefone', 'capital_social', 'Cidade - UF',
             'correio_eletronico']]

cnpj.to_csv('estabelecimentos_filtered_telefone_global.csv', sep=';', decimal=',', index=False)
