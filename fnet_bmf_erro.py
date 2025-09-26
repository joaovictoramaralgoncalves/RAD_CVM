#manipulação de dados
from Bibliotecas_e_caminhos import pd as pd
from Bibliotecas_e_caminhos import re, json
from e_mail_html_table_dividendos import Nav_dividendo
from docs import consulta, get_names, Nav_dividendo, tentativa_insistente
from docs_resumoAI import resumo_da_noticia
import email_sem_novas_informacoes, email_novidades


#tempo
from Bibliotecas_e_caminhos import time, date, datetime

def codigo_todo():
        #####################
        ## CAMINHOS USADOS ##
        #####################
        camin_FNET = 'C:/Users/joaovictor/Desktop/FNETv3'
        camin_excel = f'{camin_FNET}/CNPJ_.txt'

        #############################
        ## para quem enviar e-mail ##
        #############################
        #para_quem_vou_enviar = 'joaovictor@funcef.com.br, joaovictoramaralgoncalves@gmail.com'
        para_quem_vou_enviar = 'GFUNCEF_automatizacofii@funcef.com.br'

        ## DF 
        #########

        excel = pd.read_csv(camin_excel , sep=",")   #caminho para o TXT
        del excel[excel.columns[0]]

        df_email = pd.DataFrame(columns=['id', 'Ticker', 'Categoria', 'Tipo', 'Visualizar'])
        df_email_dividendos = pd.DataFrame(columns=['Data_pagamento', 'Ticker', 'Dividendo', 'Quantidade', 'Valor'])
        linhas_selecionadas_all = pd.DataFrame(columns=['id', 'categoriaDocumento', 'tipo', 'descricaoFundo','Visualizar','Ticker'])

        date_time = date.today()

        valor=0
        i=0

        while (i<len(excel['Doc'])):
                last_id = excel.loc[i,'Doc']
                cnpj = str(excel.loc[i,'CNPJ'])
                ticker = excel.loc[i,'Fundo']
                Quant = excel.loc[i,'QTD']
                print('^'*100)
                print(f'analisando {ticker}')
                try:
                        response = consulta(cnpj)
                except:
                        try:
                                response = consulta(cnpj)
                        except:
                                try:
                                        response = consulta(cnpj)
                                except:
                                        response = consulta(cnpj)

                response_dict = json.loads(response.text)

                ##########################
                ## Criando df principal ##
                ##########################
                df = response_dict['data']
                df = pd.DataFrame(df)

                df["descricaoFundo"] = df["descricaoFundo"].apply(lambda x: get_names(x))
                df["categoriaDocumento"] = df["categoriaDocumento"].apply(lambda x: get_names(x))
                df["tipoDocumento"] = df["tipoDocumento"].apply(lambda x: get_names(x))
                df["especieDocumento"] = df["especieDocumento"].apply(lambda x: get_names(x))
                df["formatoDataReferencia"] = pd.to_numeric(df["formatoDataReferencia"])
                df["dataEntrega"] = df["dataEntrega"].apply(lambda x: get_names(x)) #.apply(lambda x: get_names(x)) #.apply(lambda x: get_dates(date=x, from_format="%d/%m/%Y %H:%M"))
                df["dataReferencia"] = df["dataReferencia"].apply(lambda x: get_names(x)) #.apply(lambda x: get_dates(date=x, from_format="%d/%m/%Y %H:%M"))
                df["situacaoDocumento"] = df["situacaoDocumento"].apply(lambda x: get_names(x))
                df["versao"] = pd.to_numeric(df["formatoDataReferencia"])
                df["tipo"] = df["tipoDocumento"].apply(lambda x: get_names(x))
                df = df[['id', 'tipo', 'descricaoFundo', 'nomePregao', 'categoriaDocumento', 'tipoDocumento', 'especieDocumento', 'dataReferencia', 'dataEntrega', 'situacaoDocumento', 'formatoDataReferencia', 'versao']]

                #######################
                ## Criando df e-mail ##
                #######################
                exibir_doc = 'https://fnet.bmfbovespa.com.br/fnet/publico/exibirDocumento?id='
                exibir_doc_fim = '&cvm=true'

                # Função para concatenar as colunas
                def concatena_url(row):
                        return f"{exibir_doc}{row['id']}{exibir_doc_fim}"

                dfe = df[['id', 'categoriaDocumento', 'tipo', 'descricaoFundo']]
                dfe['Visualizar'] = dfe.apply(concatena_url, axis=1)
                dfe['Ticker'] = ticker
                linhas_selecionadas = dfe[dfe['id'] > last_id]


                #################################
                ## Verificando se tem novidade ##
                #################################
                if len(linhas_selecionadas) > 0:
                        print('tem novidade')
                        info = pd.DataFrame({
                        'id' : list(linhas_selecionadas['id']) ,
                        'Ticker': list(linhas_selecionadas['Ticker']) ,
                        'Categoria' : list(linhas_selecionadas['categoriaDocumento']) ,
                        'Tipo' :  list(linhas_selecionadas['tipo']),
                        'Visualizar' : list(linhas_selecionadas['Visualizar']),
                        })

                        frames = [df_email, info]
                        df_email = pd.concat(frames)
                #########################
                ## DataFrame Dividendo ##
                #########################
                linhas_selecionadas_div = linhas_selecionadas[linhas_selecionadas['categoriaDocumento'].str.contains('Aviso', case=False, na=False)]
                if len(linhas_selecionadas_div) > 0:
                        info_div = linhas_selecionadas_div
                        frames_div = [info_div, linhas_selecionadas_all]
                        linhas_selecionadas_all = pd.concat(frames_div)
                i+=1
        linhas_selecionadas_all = linhas_selecionadas_all.reset_index(drop=True)
        print(linhas_selecionadas_all)
        tickers = list(linhas_selecionadas_all['Ticker'])
        print("-"*84)
        for ticker in tickers:
                index_div = 0
                while index_div < len(linhas_selecionadas_all):
                        print(f'index_div é {index_div}')
                        try:
                                id = linhas_selecionadas_all['id'][index_div]
                                Fundo = linhas_selecionadas_all['Ticker'][index_div]
                                linha = excel.loc[excel['Fundo'] == Fundo]
                                Quant = linha['QTD'].values[0] if not linha.empty else None
                                df_transposed, dividendo, data_pagamento = Nav_dividendo(id)
                                Valor = float(dividendo)*int(Quant)
                                Valor = f"R$ {Valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                                info_div = [str(data_pagamento), str(Fundo), str(dividendo), str(Quant), str(Valor)]
                                df_email_dividendos.loc[len(df_email_dividendos)] = info_div
                        except:
                                pass
                        index_div += 1
        


        print('TABELA DE DIVIDENDOS')
        print('-'*84)
        df_email_dividendos = df_email_dividendos.drop_duplicates()
        df_email_dividendos = df_email_dividendos.reset_index(drop=True)
        print(df_email_dividendos)
        print('-'*84)
        print('-'*100)
        print('TABELA ENVIO DE E-MAIL')
        print('-'*100)
        df_email = df_email.reset_index(drop=True)
        df_email["noticia"] = df_email["id"].apply(lambda x: tentativa_insistente(resumo_da_noticia(x)))
        print(df_email)
        print('-'*100)
        



               
        html_table2 = df_email_dividendos.to_html(index=False)
        df = df_email.reset_index(drop=True)
        numero_de_linhas = df.shape[0]

        if numero_de_linhas < 1:
                print('Não houve nenhum documento novo postado desde a última vez que busquei.')
                email_sem_novas_informacoes.email(date_time.strftime("%d/%m/%Y"), para_quem_vou_enviar)
        else:
                print('Houve documento novo postado desde a última vez que busquei.')
                html_table2 = df_email_dividendos.to_html(index=False)
                print('Preparando e-mail')
                email_novidades.novidades(df_email, para_quem_vou_enviar,html_table2, df_email_dividendos)
                print(datetime.datetime.now())

                df_email["id"] = pd.to_numeric(df_email["id"], errors='coerce')

                # Função lambda para atualizar ou manter o valor
                def update_or_keep(fundo, current_doc):
                        # Filtrando valores válidos e convertendo para numérico
                        valid_ids = pd.to_numeric(df_email.loc[df_email["Ticker"] == fundo, "id"], errors='coerce').dropna()
                        if valid_ids.empty:
                                return current_doc
                        else:
                                max_name = valid_ids.max()
                                if pd.isna(max_name) or max_name <= current_doc:
                                  return current_doc
                                else:
                                   return max_name

                # Aplicando a função lambda para atualizar a coluna "Doc"
                excel["Doc"] = excel.apply(lambda row: update_or_keep(row["Fundo"], row["Doc"]), axis=1)
                
                # Salva a versao atualizada do arquivo CNPJ_.txt
                excel.to_csv(f'{camin_FNET}/CNPJ_.txt')
        

