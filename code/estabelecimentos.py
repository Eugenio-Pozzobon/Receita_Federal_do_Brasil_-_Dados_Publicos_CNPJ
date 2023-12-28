import os
import pandas as pd
arquivos_estabelecimento = os.listdir('./')
arquivos_estabelecimento = [arq for arq in arquivos_estabelecimento if arq.find('estabelecimento') > -1]
arquivos_estabelecimento = [arq for arq in arquivos_estabelecimento if arq.endswith('csv')]
todos_estabelecimentos = pd.DataFrame()
print(arquivos_estabelecimento)
dfs = []
for index, arquivo in enumerate(arquivos_estabelecimento):
    df = pd.read_csv(arquivo,sep=';',decimal=',', low_memory=False)
    dfs.append(df)

print('Open Empresas')
todos_estabelecimentos = pd.concat(dfs, ignore_index=True)
todos_estabelecimentos = todos_estabelecimentos.drop_duplicates()

dfs = []
chunksize = 10 ** 6
for chunk in pd.read_csv('empresas.csv', sep=';',decimal=',', low_memory=False, chunksize=chunksize):
    chunk = chunk[chunk['cnpj_basico'].isin(todos_estabelecimentos['cnpj_basico'])]
    dfs.append(chunk)

# filter empresas by cnpj_basico in total
print('Merging')
empresas = pd.concat(dfs, ignore_index=True)
total = pd.merge(todos_estabelecimentos, empresas, on='cnpj_basico', how='inner')

total = total[total['situacao_cadastral'] == 2]

# drop motivo_situacao_cadastral	nome_cidade_exterior data_situacao_cadastral, situacao_especial
# data_situacao_especial, qualificacao_responsavel, ente_federativo_responsavel
total = total.drop(columns=['motivo_situacao_cadastral', 'nome_cidade_exterior', 'data_situacao_cadastral',
                      'situacao_especial', 'data_situacao_especial', 'qualificacao_responsavel',
                      'ente_federativo_responsavel'])


total.to_csv('estabelecimentos.csv', sep=';',decimal=',')

exit()
arquivos_estabelecimento = os.listdir('./')
arquivos_estabelecimento = [arq for arq in arquivos_estabelecimento if arq.find('ESTABELE') > -1]

arquivos_estabelecimento.sort()

for index, file in enumerate(arquivos_estabelecimento):
    print('Trabalhando no arquivo: ' + file + ' [...]')

    estabelecimento = pd.read_csv(filepath_or_buffer=file,
                                  sep=';',
                                  skiprows=0,
                                  header=None,
                                  dtype='object',
                                  encoding='latin-1',
                                  low_memory=False,
                                  )

    # Tratamento do arquivo antes de inserir na base:
    estabelecimento = estabelecimento.reset_index()
    del estabelecimento['index']

    # Renomear colunas
    estabelecimento.columns = ['cnpj_basico',
                               'cnpj_ordem',
                               'cnpj_dv',
                               'identificador_matriz_filial',
                               'nome_fantasia',
                               'situacao_cadastral',
                               'data_situacao_cadastral',
                               'motivo_situacao_cadastral',
                               'nome_cidade_exterior',
                               'pais',
                               'data_inicio_atividade',
                               'cnae_fiscal_principal',
                               'cnae_fiscal_secundaria',
                               'tipo_logradouro',
                               'logradouro',
                               'numero',
                               'complemento',
                               'bairro',
                               'cep',
                               'uf',
                               'municipio',
                               'ddd_1',
                               'telefone_1',
                               'ddd_2',
                               'telefone_2',
                               'ddd_fax',
                               'fax',
                               'correio_eletronico',
                               'situacao_especial',
                               'data_situacao_especial']

    # filter where email or telefone is not null
    estabelecimento = estabelecimento[
        estabelecimento['correio_eletronico'].notnull() | estabelecimento['telefone_1'].notnull() | estabelecimento[
            'telefone_2'].notnull()]

    # filter estabelecimento by cnae fiscal, o primeário e a lista de secundarios deve conter:
    # '0111303', 0115600, 0111302, 0111301

    estabelecimento['cnaes'] = estabelecimento['cnae_fiscal_principal'].str.cat(
        estabelecimento['cnae_fiscal_secundaria'], sep=',')
    estabelecimento['cnaes'] = estabelecimento['cnaes'].str.split(',')
    estabelecimento = estabelecimento.explode('cnaes')
    estabelecimento['cnaes'] = estabelecimento['cnaes'].str.strip()
    estabelecimento = estabelecimento[estabelecimento['cnaes'].isin(['0111303', '0115600', '0111302', '0111301'])]
    estabelecimento = estabelecimento.reset_index(drop=True)
    del estabelecimento['cnaes']

    print(f'Quantidade de estabelecimentos: {len(estabelecimento)}')
    estabelecimento.to_csv(f'estabelecimento{index}.csv', index=False, sep=';', decimal=',')

# save only the columns that we need to use: cnpj_basico, cnpj_ordem, cnpj_dv, nome_fantasia, situacao_cadastral,
# pais, data_inicio_atividade, cnae_fiscal_principal, cnae_fiscal_secundaria, tipo_logradouro, logradouro, numero, complemento, bairro, cep, uf, municipio, ddd_1, telefone_1, ddd_2, telefone_2, ddd_fax, fax, correio_eletronico
