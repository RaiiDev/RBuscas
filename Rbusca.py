import requests
import numpy as np
from bs4 import BeautifulSoup
import json
import re

# Defina a URL base da busca
url_base_facebook = "https://www.facebook.com/search/people/?q={termo}"
url_base_instagram = "https://www.instagram.com/web/search/topsearch/?query={termo}"
url_base_google_compl = "https://suggestqueries.google.com/complete/search?q={termo}&client=firefox&ds=yt"
# Solicite que o usuário digite o termo de busca

print("""
================BY RDEV================
Utilize como busca CPF, NOME etc...
=======================================
    """)
termo = input("Digite o termo de busca:")

# Substitua os espaços por sinal de mais (+)
termo_formatado = termo.replace(" ", "+")

# Solicite que o usuário escolha a plataforma
print("Escolha a plataforma para pesquisar:")
print("[1] Info")
print("[2] Facebook")
print("[3] Instagram")
print("[4] Buscar por termos")
print("[5] Buscar por CPF, TELEFONE e EMAIL")
print("[6] Todos")
plataforma = input("Digite o número da plataforma: ")
print("""

    """)
if plataforma == "1":
    print("Desenvolvido por RDEV")
    print("Ver: 1.0")

elif plataforma == "2":
    url_busca = url_base_facebook.format(termo=termo_formatado)
    resposta = requests.get(url_busca)
    if resposta.status_code == 200:
        soup = BeautifulSoup(resposta.text, "html.parser")
        resultados = soup.select('div[data-testid="browse-result-content"]')
        for resultado in resultados:
            nome_resultado = resultado.select_one('div[data-testid="browse-result-name"]').text
            perfil_url = resultado.select_one('a[data-testid="browse-result-link"]')['href']
            print(f"Nome: {nome_resultado} | Perfil: {perfil_url}")
    else:
        print("Não foi possível conectar ao Facebook.")

elif plataforma == "3":
    # Substitua o termo na URL base do Instagram
    url_busca = url_base_instagram.format(termo=termo_formatado)

    # Faça a requisição HTTP para a página de busca
    resposta = requests.get(url_busca)
    if resposta.status_code == 200:
        resultados = json.loads(resposta.text)['users']
        for resultado in resultados:
            nome_resultado = resultado['user']['full_name']
            perfil_url = f"https://www.instagram.com/{resultado['user']['username']}"
            print(f"Nome: {nome_resultado} | Perfil: {perfil_url}")
    else:
        print("Não foi possível conectar ao Instagram.")

elif plataforma == "4":
    url_base_google_compl = "https://www.google.com/search?q={termo}&start={start}&num=10"
    start = 0
    max_resultados = 100

    resultados = []
    while len(resultados) < max_resultados:
        url_busca = url_base_google_compl.format(termo=termo_formatado, start=start)
        resposta = requests.get(url_busca)
        soup = BeautifulSoup(resposta.text, "html.parser")
        sugestoes = soup.find_all("div", class_="BNeawe s3v9rd AP7Wnd")
        for sugestao in sugestoes:
            nome = sugestao.text.strip()
            if nome not in resultados:
                resultados.append(nome)
        if len(sugestoes) == 0:
            break
        start += 10

    cpfs = []
    nomes = []
    telefones = []
    emails = []

    for resultado in resultados:
        # Busca CPF
        cpf_match = re.search(r"\d{3}\.\d{3}\.\d{3}-\d{2}", resultado)
        if cpf_match:
            cpf = cpf_match.group(0)
            if cpf not in cpfs:
                cpfs.append(cpf)
                print(f"CPF encontrado: {cpf} - {resultado}")
        
        # Busca nome completo
        nome_match = re.search(r"\b([A-Z][a-z]*\s)+[A-Z][a-z]*\b", resultado)
        if nome_match:
            nome = nome_match.group(0)
            if nome not in nomes:
                nomes.append(nome)
                print(f"Nome encontrado: {nome} - {resultado}")
        
        # Busca telefone
        telefone_match = re.search(r"\(\d{2}\)\s\d{4,5}-\d{4}", resultado)
        if telefone_match:
            telefone = telefone_match.group(0)
            if telefone not in telefones:
                telefones.append(telefone)
                print(f"Telefone encontrado: {telefone} - {resultado}")
        
        # Busca email
        email_match = re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", resultado)
        if email_match:
            email = email_match.group(0)
            if email not in emails:
                emails.append(email)
                print(f"E-mail encontrado: {email} - {resultado}")


elif plataforma == "5":
    url_base_google_compl = "https://www.google.com/search?q={termo}&start={start}&num=10"
    start = 0
    max_resultados = 100

    resultados = []
    while len(resultados) < max_resultados:
        url_busca = url_base_google_compl.format(termo=termo_formatado, start=start)
        resposta = requests.get(url_busca)
        soup = BeautifulSoup(resposta.text, "html.parser")
        sugestoes = soup.find_all("div", class_="BNeawe s3v9rd AP7Wnd")
        for sugestao in sugestoes:
            nome = sugestao.text.strip()
            if nome not in resultados:
                resultados.append(nome)
        if len(sugestoes) == 0:
            break
        start += 10

    cpfs = []
    telefones = []
    emails = []

    for resultado in resultados:
        # Busca CPF
        cpf_match = re.search(r"\d{3}\.\d{3}\.\d{3}-\d{2}", resultado)
        if cpf_match:
            cpf = cpf_match.group(0)
            if cpf not in cpfs:
                cpfs.append(cpf)
        
        # Busca telefone
        telefone_match = re.search(r"\(\d{2}\)\s\d{4,5}-\d{4}", resultado)
        if telefone_match:
            telefone = telefone_match.group(0)
            if telefone not in telefones:
                telefones.append(telefone)
        
        # Busca email
        email_match = re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", resultado)
        if email_match:
            email = email_match.group(0)
            if email not in emails:
                emails.append(email)

    print("CPFs encontrados:")
    for cpf in cpfs:
        print("- " + cpf)

    print("Telefones encontrados:")
    for telefone in telefones:
        print("- " + telefone)

    print("Emails encontrados:")
    for email in emails:
        print("- " + email)

elif plataforma == "6":
    # busca em todas as plataformas

    # Google Imagens
    url_busca = url_base_google_compl.format(termo=termo_formatado)
    resposta = requests.get(url_busca)
    if resposta.status_code == 200:
        soup = BeautifulSoup(resposta.text, "html.parser")
        imagens = soup.select('img[src^="http"]')
        for imagem in imagens:
            imagem_url = imagem["src"]
            resposta_imagem = requests.get(imagem_url, stream=True)
            imagem_array = np.asarray(bytearray(resposta_imagem.content), dtype=np.uint8)
            imagem_opencv = cv2.imdecode(imagem_array, -1)
            classificador = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            faces = classificador.detectMultiScale(imagem_opencv, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            if len(faces) > 0:
                print("Imagem relacionadas: " + imagem_url)
    else:
        print("A busca no Google Imagens não foi bem-sucedida. Status code:", resposta.status_code)

    print("""

    """)

    # Facebook
    url_busca = url_base_facebook.format(termo=termo_formatado)
    resposta = requests.get(url_busca)
    if resposta.status_code == 200:
        soup = BeautifulSoup(resposta.text, "html.parser")
        resultados = soup.select('div[data-testid="browse-result-content"]')
        for resultado in resultados:
            nome_resultado = resultado.select_one('div[data-testid="browse-result-name"]').text
            perfil_url = resultado.select_one('a[data-testid="browse-result-link"]')['href']
            print(f"Nome: {nome_resultado} | Perfil: {perfil_url}")
    else:
        print("Não foi possível conectar ao Facebook.")

    print("""

        """)

    # Instagram
    url_busca = url_base_instagram.format(termo=termo_formatado)
    resposta = requests.get(url_busca)
    if resposta.status_code == 200:
        resultados = json.loads(resposta.text)['users']
        for resultado in resultados:
            nome_resultado = resultado['user']['full_name']
            perfil_url = f"https://www.instagram.com/{resultado['user']['username']}"
            print(f"Nome: {nome_resultado} | Perfil: {perfil_url}")
    else:
        print("Não foi possível conectar ao Instagram.")

    print("""

        """)

    #Busca por EMAIL, CPF, EMAIL
    url_base_google_compl = "https://www.google.com/search?q={termo}&start={start}&num=10"
    start = 0
    max_resultados = 100

    resultados = []
    while len(resultados) < max_resultados:
        url_busca = url_base_google_compl.format(termo=termo_formatado, start=start)
        resposta = requests.get(url_busca)
        soup = BeautifulSoup(resposta.text, "html.parser")
        sugestoes = soup.find_all("div", class_="BNeawe s3v9rd AP7Wnd")
        for sugestao in sugestoes:
            nome = sugestao.text.strip()
            if nome not in resultados:
                resultados.append(nome)
        if len(sugestoes) == 0:
            break
        start += 10

    cpfs = []
    telefones = []
    emails = []

    for resultado in resultados:
        # Busca CPF
        cpf_match = re.search(r"\d{3}\.\d{3}\.\d{3}-\d{2}", resultado)
        if cpf_match:
            cpf = cpf_match.group(0)
            if cpf not in cpfs:
                cpfs.append(cpf)
        
        # Busca telefone
        telefone_match = re.search(r"\(\d{2}\)\s\d{4,5}-\d{4}", resultado)
        if telefone_match:
            telefone = telefone_match.group(0)
            if telefone not in telefones:
                telefones.append(telefone)
        
        # Busca email
        email_match = re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", resultado)
        if email_match:
            email = email_match.group(0)
            if email not in emails:
                emails.append(email)

    print("CPFs encontrados:")
    for cpf in cpfs:
        print("- " + cpf)

    print("Telefones encontrados:")
    for telefone in telefones:
        print("- " + telefone)

    print("Emails encontrados:")
    for email in emails:
        print("- " + email)

    print("""

        """)
    #Busca por Termo
    url_base_google_compl = "https://www.google.com/search?q={termo}&start={start}&num=10"
    start = 0
    max_resultados = 100

    resultados = []
    while len(resultados) < max_resultados:
        url_busca = url_base_google_compl.format(termo=termo_formatado, start=start)
        resposta = requests.get(url_busca)
        soup = BeautifulSoup(resposta.text, "html.parser")
        sugestoes = soup.find_all("div", class_="BNeawe s3v9rd AP7Wnd")
        for sugestao in sugestoes:
            nome = sugestao.text.strip()
            if nome not in resultados:
                resultados.append(nome)
        if len(sugestoes) == 0:
            break
        start += 10

    cpfs = []
    nomes = []
    telefones = []
    emails = []

    for resultado in resultados:
        # Busca CPF
        cpf_match = re.search(r"\d{3}\.\d{3}\.\d{3}-\d{2}", resultado)
        if cpf_match:
            cpf = cpf_match.group(0)
            if cpf not in cpfs:
                cpfs.append(cpf)
                print(f"CPF encontrado: {cpf} - {resultado}")
        
        # Busca nome completo
        nome_match = re.search(r"\b([A-Z][a-z]*\s)+[A-Z][a-z]*\b", resultado)
        if nome_match:
            nome = nome_match.group(0)
            if nome not in nomes:
                nomes.append(nome)
                print(f"Nome encontrado: {nome} - {resultado}")
        
        # Busca telefone
        telefone_match = re.search(r"\(\d{2}\)\s\d{4,5}-\d{4}", resultado)
        if telefone_match:
            telefone = telefone_match.group(0)
            if telefone not in telefones:
                telefones.append(telefone)
                print(f"Telefone encontrado: {telefone} - {resultado}")
        
        # Busca email
        email_match = re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", resultado)
        if email_match:
            email = email_match.group(0)
            if email not in emails:
                emails.append(email)
                print(f"E-mail encontrado: {email} - {resultado}")

else:
    print("Opção inválida.")
