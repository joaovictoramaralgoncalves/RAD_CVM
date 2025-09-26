from Bibliotecas_e_caminhos import BeautifulSoup, time, pd 
from docs import consulta_dividendos
def Nav_dividendo(id):
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





