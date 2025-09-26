from Bibliotecas_e_caminhos import EmailMessage, smtplib, date, BeautifulSoup

def novidades(df_email, para_quem_vou_enviar,html_table2, df_email_dividendos):   
      # Setando corpo e demais infos do e-mail
      date_time = date.today().strftime("%d/%m/%Y")
      print(date_time)
      df_email.reset_index(drop=True)
      print(df_email)
      html_table_email = []
      html_table_email_envio = []
      count= 0
      while count < len(df_email):
          print(count)
          ticker = f'<tr><h3 style="color:rgb(28,71,101)">{df_email["Ticker"][count]}</h3></tr>'
          Categoria = f'<tr><td style="padding-left: 20px;"><b>Categoria:</b></td><td>{df_email["Categoria"][count]}</td></tr>'
          Tipo = f'<tr><td style="padding-left: 20px;"><b>Tipo:</b></td><td>{df_email["Tipo"][count]}</td></tr>'
          #noticias = f'<tr><td style="padding-left: 20px;"><b>Notícia:</b></td><td>{df_email["noticia"][count]}</td></tr>'
          Visualizar = f'<tr><td style="padding-left: 20px;"><b>Visualizar:</b></td><td><a href="{df_email["Visualizar"][count]}">Acesse a Notícia</a></td></tr>'
          corpo = f'<table>{ticker}{Categoria}{Tipo}{Visualizar}</table>'

          html_table_email_envio.append(corpo)
          count = count + 1
      print(html_table_email_envio)
      html_table_email_envio = '<hr>'.join(html_table_email_envio)
      corpo_email_Ndiv = f"""
    
        <html>
        <img src="https://bancariosjundiai.com.br/wp-content/uploads/2022/01/funcef.png" width="400" height="150"/>
        <head>
        <h1 style="color:rgb(24,150,179)">ATUALIZAÇÃO DE DADOS BMF BOVESPA | {date_time} </h1>
        <h2 style="color:rgb(28,71,101)">ACOMPANHAMENTO DE FUNDOS - COFII</h2>
        <hr>
        <hr>
        </head>
    
    
    
              <h3 style="color:rgb(24,150,179)">Prezados,</h3>
              <h3 style="color:rgb(24,150,179)">Seguem os dados mais recentes, filtrados do site
                <a href="https://fnet.bmfbovespa.com.br/fnet/publico/abrirGerenciadorDocumentosCVM"> fnet.bmfbovespa.com:</a>
    
              </h3>
    
    
        <hr>
    
        {html_table_email_envio}
    
    
    
        <hr>
    
    
    
        <h4 style="color:rgb(28,71,101)">Atenciosamente, </h4>
        <h4 style="color:rgb(28,71,101)">Robo FNET
        </h4>
        </body>
        </html>
        """
    
      login = 'automatizacaofnetcofii@gmail.com'
      msg = EmailMessage()
      msg['Subject'] = f"Dados fnet.bmfbovespa - {date_time}"
      msg['From'] = f'Análise.COFII <{login}> '
      msg['To'] = ", ".join(para_quem_vou_enviar)
      password = 'pcmx lxbo yzsu mjpd'
      msg.add_header('Content-Type', 'text/html')
    
      # Verifica se a primeira linha da coluna 'Ticker' de df_email_dividendos está vazia
      if len(df_email_dividendos)<1:corpo = corpo_email_Ndiv
      else:
            # Construa o corpo do email quando df_email_dividendos não está vazio
            corpo_email = f"""
        <html>
        <img src="https://bancariosjundiai.com.br/wp-content/uploads/2022/01/funcef.png" width="400" height="150"/>
        <head>
        <h1 style="color:rgb(24,150,179)">ATUALIZAÇÃO DE DADOS BMF BOVESPA | {date_time} </h1>
        <h2 style="color:rgb(28,71,101)">ACOMPANHAMENTO DE FUNDOS - COFII</h2>
        <hr>
        <hr>
              <h3 style="color:rgb(24,150,179)">Tabela de recebimento de proventos:</h3>
        {html_table2}
        <hr>
        <hr>
    
    
    
        </head>
    
    
    
              <h3 style="color:rgb(24,150,179)">Prezados,</h3>
              <h3 style="color:rgb(24,150,179)">Seguem os dados mais recentes, filtrados do site
                <a href="https://fnet.bmfbovespa.com.br/fnet/publico/abrirGerenciadorDocumentosCVM"> fnet.bmfbovespa.com:</a>
              </h3>
    
    
        <hr>
    
        {html_table_email_envio}
    
    
        <hr>
    
    
    
        <h4 style="color:rgb(28,71,101)">Atenciosamente, </h4>
        <h4 style="color:rgb(28,71,101)">Robo FNET
        </h4>
        </body>
        </html>
        """
    
            corpo = corpo_email
    
      msg.set_payload(corpo)
    
      #Conexao e envio do e-mail
      s = smtplib.SMTP('smtp.gmail.com: 587')
      s.starttls()
    
      # Atribuindo credenciais para envio do e-mail
      s.login(login, password)
      s.sendmail(login, [msg['To']], msg.as_string().encode('iso-8859-1'))
      #s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
      print('Email enviado')
      

      #################################
      # Salvando txt com a data atual #
      #################################
      # Converter a data para string, caso necessário
      date_time_str = str(date_time)
      # Abrir o arquivo em modo de escrita
      with open('data.txt', 'w') as file:
          # Escrever o conteúdo da variável no arquivo
          file.write(date_time_str)
    

