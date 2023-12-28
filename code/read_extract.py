#%%
########################################################################################################################
## LER E INSERIR DADOS #################################################################################################
########################################################################################################################
# Files:
#%%
# Extracting files:
import os
import zipfile

output_files = '/Users/eugeniopozzobon/Documents/GitHub/Receita_Federal_do_Brasil_-_Dados_Publicos_CNPJ/code'
extracted_files = './'
i_l = 0
Files = [name for name in os.listdir(output_files) if name.endswith('.zip')]

# filter files that does not start with estebalecimento
Files = [f for f in Files if not f.startswith('Estabelecimento')]

for l in Files:
    try:
        i_l += 1
        print('Descompactando arquivo:')
        print(str(i_l) + ' - ' + l)
        full_path = os.path.join(output_files, l)
        with zipfile.ZipFile(full_path, 'r') as zip_ref:
            zip_ref.extractall(extracted_files)
    except:
        pass

Items = [name for name in os.listdir(extracted_files) if name.endswith('')]

# Separar arquivos:
arquivos_empresa = []
arquivos_estabelecimento = []
arquivos_socios = []
arquivos_simples = []
arquivos_cnae = []
arquivos_moti = []
arquivos_munic = []
arquivos_natju = []
arquivos_pais = []
arquivos_quals = []
for i in range(len(Items)):
    if Items[i].find('EMPRE') > -1:
        arquivos_empresa.append(Items[i])
    elif Items[i].find('ESTABELE') > -1:
        arquivos_estabelecimento.append(Items[i])
    elif Items[i].find('SOCIO') > -1:
        arquivos_socios.append(Items[i])
    elif Items[i].find('SIMPLES') > -1:
        arquivos_simples.append(Items[i])
    elif Items[i].find('CNAE') > -1:
        arquivos_cnae.append(Items[i])
    elif Items[i].find('MOTI') > -1:
        arquivos_moti.append(Items[i])
    elif Items[i].find('MUNIC') > -1:
        arquivos_munic.append(Items[i])
    elif Items[i].find('NATJU') > -1:
        arquivos_natju.append(Items[i])
    elif Items[i].find('PAIS') > -1:
        arquivos_pais.append(Items[i])
    elif Items[i].find('QUALS') > -1:
        arquivos_quals.append(Items[i])
    else:
        pass
