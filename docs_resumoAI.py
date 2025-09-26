#################
## BIBLIOTECAS ##
#################
from docs import consulta_dividendos
import google.generativeai as genai #Perguntas_para_AI
import PyPDF2 #resumo_pdf
import tempfile #resumo_pdf
from bs4 import BeautifulSoup #remove_html_tags_bs
from requests.exceptions import ConnectionError
import os
import markdown
import re

def remove_html_tags_bs(text):
    soup = BeautifulSoup(text, "html.parser")

    pdf_text = soup.get_text()

    if len(pdf_text) > 9714:
        texto_info = pdf_text[:9714]
    else:
        texto_info = pdf_text

    return pdf_text


def resumo_pdf(pdf_content):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(pdf_content)
        temp_pdf_path = temp_pdf.name

    # Ler o PDF com PyPDF2
    with open(temp_pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        num_pages = len(reader.pages)

        # Extrair o texto de cada página
        pdf_text = ""
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            pdf_text += page.extract_text()

    if len(pdf_text) > 9714:
        texto_info = pdf_text[:9714]
    else:
        texto_info = pdf_text

    return texto_info



def Perguntas_para_AI(Pergunta_para_AI):
    genai.configure(api_key='AIzaSyCFDQedXxmPEdm_TY12cblNlDCBi45zUYA') ##Tolken da API

    ''' Caso queira saber quais são os modelos disponíveis basta tirar do comentário as seguintes linhas:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
    '''
            
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(f"{Pergunta_para_AI}")
    return response.text


def resumo_da_noticia(id):
    print('_'*84)
    print(id)
    texto_info = ""
    try:
        response = consulta_dividendos(id)
    except ConnectionError as e:
        try:
            response = consulta_dividendos(id)
        except ConnectionError as e:
            response = consulta_dividendos(id)
            
    response_content  = response.content

    if 'htm' in str(response_content[:10]).lower(): # Tentando ler arquivo em formato HTML
        texto_info = remove_html_tags_bs(response_content) 
    elif 'pdf' in str(response_content[:10]).lower():
        texto_info = resumo_pdf(response_content) # Tentando ler arquivo em formato PDF
    else:
        pass

    try:
        texto_info = texto_info.replace('\n', ' ')
    except:
        pass
    resposta = ""
    try:
        pergunta_para_AI = f"Sua resposta deve ter menos que 101 caracteres, se limite as principais informações. Resuma o texto a seguir com as principais informações Quantitativas, para colocar em uma lista de notícias (se tiver um comentário do gestor ou gestão é importante sintetizar na resposta):'{texto_info}'"
        resposta = Perguntas_para_AI(pergunta_para_AI)
        print(f"resumo é: {resposta}")
    except:
        pass

    # Converte a string Markdown para HTML
    html = markdown.markdown(resposta, extensions=['nl2br', 'extra'])

    # Substitui \n por <br> no HTML resultante
    compact_html = re.sub(r'\s+', ' ', html).strip()
    resposta = compact_html.replace('<br>', '')

    print(f"Resposta final: {resposta}")


    return resposta
