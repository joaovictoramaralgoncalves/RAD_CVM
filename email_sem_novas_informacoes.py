from Bibliotecas_e_caminhos import EmailMessage, smtplib


def email(date_time, para_quem_vou_enviar):
    corpo = f"""
    <html>
    <img src="https://bancariosjundiai.com.br/wp-content/uploads/2022/01/funcef.png" width="400" height="150"/>
    <head>
    <h1 style="color:rgb(24,150,179)">ATUALIZAÇÃO DE DADOS BMF BOVESPA | {date_time} </h1>
    <h2 style="color:rgb(28,71,101)">ACOMPANHAMENTO DE FUNDOS - COFII</h2>
    <hr>
    <hr>
    </head>

    <table>
    <tr>
        <th>
            <h3 style="color:rgb(24,150,179)">Não há documentos novos postados desde a última busca.</h3>
            <h3 style="color:rgb(242,148,0)">Não há documentos novos postados desde a última busca.</h3>
            <h3 style="color:rgb(28,71,101)">Não há documentos novos postados desde a última busca.</h3>

        </th>
    </tr>
    </table>


    <hr>
    <hr>

    <h4 style="color:rgb(28,71,101)">Fonte de Dados: <a href="https://fnet.bmfbovespa.com.br/fnet/publico/abrirGerenciadorDocumentosCVM"> FNET.BMFBOVESPA</a>
    </h4>
    <h4 style="color:rgb(28,71,101)">Atenciosamente, </h4>
    <h4 style="color:rgb(28,71,101)">Robo FNET
    </h4>
    </body>
    </html>
    """


    msg = EmailMessage()
    msg['Subject'] = f"Dados fnet.bmfbovespa - {date_time}"
    msg['From'] = 'automatizacaofnetcofii@gmail.com'
    msg['To'] = para_quem_vou_enviar
    msg.set_content(corpo, subtype='html')
    password = 'pcmx lxbo yzsu mjpd'

    # Conexão e envio do e-mail
    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()

    # Atribuindo credenciais para envio do e-mail
    s.login(msg['From'], password)
    s.send_message(msg)
    s.quit()

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
