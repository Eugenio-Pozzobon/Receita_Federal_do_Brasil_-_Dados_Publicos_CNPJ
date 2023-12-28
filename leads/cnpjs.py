import pandas as pd

cnpj = pd.read_csv('../code/empresas.csv', sep=';', decimal=',', low_memory=False)

cnpj = cnpj[cnpj['cnpj_basico'] == '43748374']
print(cnpj.to_string())