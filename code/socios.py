# Arquivos de socios:
import os

import pandas as pd

files = os.listdir('./')
files = [arq for arq in files if arq.find('SOCIO') > -1]

todos_socios = pd.DataFrame()
for file in files:
    print('Trabalhando no arquivo: '+file+' [...]')

    socios = pd.DataFrame(columns=[1,2,3,4,5,6,7,8,9,10,11])
    socios = pd.read_csv(filepath_or_buffer=file,
                          sep=';',
                          #nrows=100,
                          skiprows=0,
                          header=None,
                          dtype='object',
                          encoding='latin-1',
    )

    # Tratamento do arquivo antes de inserir na base:
    socios = socios.reset_index()
    del socios['index']

    # Renomear colunas
    socios.columns = ['cnpj_basico',
                      'identificador_socio',
                      'nome_socio_razao_social',
                      'cpf_cnpj_socio',
                      'qualificacao_socio',
                      'data_entrada_sociedade',
                      'pais',
                      'representante_legal',
                      'nome_do_representante',
                      'qualificacao_representante_legal',
                      'faixa_etaria']
    todos_socios = todos_socios._append(socios)

print(f'Quantidade de sócios: {len(todos_socios)}')
todos_socios.to_csv('socios.csv', index=False, sep=';', decimal=',')
print('Arquivos de socios finalizados!')
