from dotenv import load_dotenv
import bs4 as bs
import os
import re
import sys
import requests
import urllib.request
import wget


def check_diff(url, file_name):
    '''
    Verifica se o arquivo no servidor existe no disco e se ele tem o mesmo
    tamanho no servidor.
    '''
    if not os.path.isfile(file_name):
        return True # ainda nao foi baixado

    response = requests.head(url)
    new_size = int(response.headers.get('content-length', 0))
    old_size = os.path.getsize(file_name)
    if new_size != old_size:
        os.remove(file_name)
        return True # tamanho diferentes

    return False # arquivos sao iguais


#%%
def makedirs(path):
    '''
    cria path caso seja necessario
    '''
    if not os.path.exists(path):
        os.makedirs(path)

#%%
def to_sql(dataframe, **kwargs):
    '''
    Quebra em pedacos a tarefa de inserir registros no banco
    '''
    size = 4096
    total = len(dataframe)
    name = kwargs.get('name')

    def chunker(df):
        return (df[i:i + size] for i in range(0, len(df), size))

    for i, df in enumerate(chunker(dataframe)):
        df.to_sql(**kwargs)
        index = i * size
        percent = (index * 100) / total
        progress = f'{name} {percent:.2f}% {index:0{len(str(total))}}/{total}'
        sys.stdout.write(f'\r{progress}')

#%%
# Ler arquivo de configuração de ambiente # https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1
def getEnv(env):
    return os.getenv(env)

print('Especifique o local do seu arquivo de configuração ".env". Por exemplo: C:\...\Receita_Federal_do_Brasil_-_Dados_Publicos_CNPJ\code')
# C:\Aphonso_C\Git\Receita_Federal_do_Brasil_-_Dados_Publicos_CNPJ\code
local_env = 'env'
dotenv_path = os.path.join(local_env, '.env')
load_dotenv(dotenv_path=dotenv_path)

dados_rf = 'http://200.152.38.155/CNPJ/'

#%%
# Read details from ".env" file:
output_files = None
extracted_files = None
try:
    output_files = '/Users/eugeniopozzobon/Documents/GitHub/Receita_Federal_do_Brasil_-_Dados_Publicos_CNPJ/code'
    makedirs(output_files)

    extracted_files = getEnv('EXTRACTED_FILES_PATH')
    makedirs(extracted_files)

    print('Diretórios definidos: \n' +
          'output_files: ' + str(output_files)  + '\n' +
          'extracted_files: ' + str(extracted_files))
except:
    pass
    print('Erro na definição dos diretórios, verifique o arquivo ".env" ou o local informado do seu arquivo de configuração.')

#%%
raw_html = urllib.request.urlopen(dados_rf)
raw_html = raw_html.read()

# Formatar página e converter em string
page_items = bs.BeautifulSoup(raw_html, 'lxml')
html_str = str(page_items)

# Obter arquivos
Files = []
text = '.zip'
for m in re.finditer(text, html_str):
    i_start = m.start()-40
    i_end = m.end()
    i_loc = html_str[i_start:i_end].find('href=')+6
    Files.append(html_str[i_start+i_loc:i_end])

# Correcao do nome dos arquivos devido a mudanca na estrutura do HTML da pagina - 31/07/22 - Aphonso Rafael
Files_clean = []
for i in range(len(Files)):
    if not Files[i].find('.zip">') > -1:
        Files_clean.append(Files[i])

try:
    del Files
except:
    pass

Files = Files_clean

print('Arquivos que serão baixados:')
i_f = 0
for f in Files:
    i_f += 1
    print(str(i_f) + ' - ' + f)

#%%
########################################################################################################################
## DOWNLOAD ############################################################################################################
########################################################################################################################
# Create this bar_progress method which is invoked automatically from wget:
def bar_progress(current, total, width=80):
  progress_message = "Downloading: %d%% [%d / %d] bytes - " % (current / total * 100, current, total)
  # Don't use print() as it will print in new line every time.
  sys.stdout.write("\r" + progress_message)
  sys.stdout.flush()

#%%
# Download arquivos ################################################################################################################################
i_l = 0
for l in Files:
    # Download dos arquivos
    i_l += 1
    print('Baixando arquivo:')
    print(str(i_l) + ' - ' + l)
    url = dados_rf+l
    file_name = os.path.join(output_files, l)
    if check_diff(url, file_name):
        wget.download(url, out=output_files, bar=bar_progress)

#%%
# Download layout:
Layout = 'https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/cadastros/consultas/arquivos/NOVOLAYOUTDOSDADOSABERTOSDOCNPJ.pdf'
print('Baixando layout:')
wget.download(Layout, out=output_files, bar=bar_progress)

####################################################################################################################################################


