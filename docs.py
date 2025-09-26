import requests
import os
from Bibliotecas_e_caminhos import BeautifulSoup, time, pd, requests

def get_names(name: str = ''):
    if name == '':
        return None
    else:
        try:
            return ' '.join(name.split())
        except:
            return None
def consulta(cnpj):
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
    }
    params = {
        'd': '1',
        's': '0',
        'l': '30',
        'o[0][dataEntrega]': 'desc',
        'cnpjFundo': cnpj,
        'idCategoriaDocumento': '0',
        'idTipoDocumento': '0',
        'idEspecieDocumento': '0',
        '_': '1719250395169',
    }
    try:
        response = requests.get(
            'https://fnet.bmfbovespa.com.br/fnet/publico/pesquisarGerenciadorDocumentosDados',
            params=params,
            headers=headers,
            verify=os.environ.get("REQUESTS_CA_BUNDLE"),
        )
    except:
        try:
            response = requests.get(
                'https://fnet.bmfbovespa.com.br/fnet/publico/pesquisarGerenciadorDocumentosDados',
                params=params,
                headers=headers,
                verify=os.environ.get("REQUESTS_CA_BUNDLE"),
            )
        except:
            response = requests.get(
                'https://fnet.bmfbovespa.com.br/fnet/publico/pesquisarGerenciadorDocumentosDados',
                params=params,
                headers=headers,
                verify=os.environ.get("REQUESTS_CA_BUNDLE"),
            )
    return response
def consulta_dividendos(id):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    }

    params = {
        'id': id,
        'cvm': 'true',
    }

    try:
        response = requests.get(
            'https://fnet.bmfbovespa.com.br/fnet/publico/exibirDocumento',
            params=params,
            headers=headers,
            verify=os.environ.get("REQUESTS_CA_BUNDLE"),
        )
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:", errh)
        response
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:", errc)
        response
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:", errt)
        response
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else", err)
        response


    return response
def Nav_dividendo(id):
    try:
        response = consulta_dividendos(id)
    except:
        try:
            response = consulta_dividendos(id)
        except:
            response = consulta_dividendos(id)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extraia os valores das células da tabela
    data = []
    for row in soup.find_all('tr'):
        row_data = []
        for cell in row.find_all('td'):
            # Se houver um span com a classe 'dado-valores', pegue seu texto, caso contrário, pegue o texto da célula
            span = cell.find('span', class_='dado-valores')
            if span:
                row_data.append(span.text.strip())
            else:
                row_data.append(cell.text.strip())
        data.append(row_data)
        row_data

    # Crie um DataFrame do Pandas com os dados
    df = pd.DataFrame(data)

    df_transposed = df.transpose()
    print(len(df_transposed))
    # Atualize o cabeçalho do DataFrame transposto
    try:
        new_header = df_transposed.iloc[0]  # Pegue a primeira linha para usar como cabeçalho
        df_transposed = df_transposed[1:]  # Descarte a primeira linha
        df_transposed.columns = new_header  # Defina a primeira linha como cabeçalho


        dividendo = df_transposed['Valor do provento (R$/unidade)'][1].replace(',', '.')
        dividendo = dividendo.replace(',', '.')
        data_pagamento = df_transposed['Data do pagamento'][1]
        
        return df_transposed, dividendo, data_pagamento
    except:
        print(f"Sem tabela. Len da df_transposed: {len(df_transposed)}")


def tentativa_insistente(var_tentar, max_retries=10, delays=[15, 15, 15, 15, 15, 15, 15, 15, 15, 15]):
    for delay in delays:
        try:
            time.sleep(delay)
            return var_tentar
        except Exception as e:
            last_exception = e
    raise last_exception
        
