# Arquivos de empresa:
import os
import pandas as pd
cnpjs = pd.DataFrame()

arquivos_empresa = os.listdir('./')
arquivos_empresa = [arq for arq in arquivos_empresa if arq.find('EMPRE') > -1]

for file in arquivos_empresa:
    print('Trabalhando no arquivo: '+file+' [...]')

    empresa = pd.DataFrame(columns=[0, 1, 2, 3, 4, 5, 6])
    empresa_dtypes = {0: 'object', 1: 'object', 2: 'object', 3: 'object', 4: 'object', 5: 'object', 6: 'object'}

    empresa = pd.read_csv(filepath_or_buffer=file,
                          sep=';',
                          skiprows=0,
                          header=None,
                          dtype=empresa_dtypes,
                          encoding='latin-1',
                          decimal=',',
    )

    # Tratamento do arquivo antes de inserir na base:
    empresa = empresa.reset_index()
    del empresa['index']

    # Renomear colunas
    empresa.columns = ['cnpj_basico', 'razao_social', 'natureza_juridica', 'qualificacao_responsavel', 'capital_social', 'porte_empresa', 'ente_federativo_responsavel']
    cnpjs = cnpjs._append(empresa)

print(f'Quantidade de CNPJs: {len(cnpjs)}')
cnpjs.to_csv('empresas.csv', index=False, sep=';', decimal=',')

