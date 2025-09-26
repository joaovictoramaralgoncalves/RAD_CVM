import os
import requests
from Bibliotecas_e_caminhos import time, date
from fnet_bmf import codigo_todo


# Obter a data atual
data_atual = str(date.today().strftime("%d/%m/%Y"))

# Abrir o arquivo em modo de leitura
with open('data.txt', 'r') as file:
    # Ler o conteúdo do arquivo
    data_arquivo = file.read().strip()


# Verificar se a data no arquivo é igual à data atual
if data_atual == data_arquivo:
    print("A data no arquivo é igual à data atual.")
else:
    print("A data no arquivo é diferente da data atual.")
    
    try:
        codigo_todo()
    except:
        time.sleep(15)
        print(f"Erro ao acessar o site")
        try:
            time.sleep(15)
            codigo_todo()
        except:
            print(f"Erro ao acessar o site")
            time.sleep(15)
            codigo_todo()
            try:
                time.sleep(15)
                codigo_todo()
            except:
                print(f"Erro ao acessar o site")
                time.sleep(15)
                codigo_todo()        
                try:
                    time.sleep(15)
                    codigo_todo()
                except:
                    print(f"Erro ao acessar o site")
                    time.sleep(15)
                    codigo_todo()
