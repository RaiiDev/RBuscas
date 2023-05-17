import requests
import numpy as np
from bs4 import BeautifulSoup
import json
import re
import time
import random
# Defina a URL base da busca
url_base_facebook = "https://www.facebook.com/search/people/?q={termo}"
url_base_instagram = "https://www.instagram.com/web/search/topsearch/?query={termo}"
url_base_google_compl = "https://suggestqueries.google.com/complete/search?q={termo}&client=firefox&ds=yt"
# Solicite que o usuário digite o termo de busca

print("""
================BY RDEV=========================================================
//...............................................................................
//.RRRRRRRRRR...BBBBBBBBBB...UUUU...UUUU...SSSSSSS......CCCCCCC.......AAAAA......
//.RRRRRRRRRRR..BBBBBBBBBBB..UUUU...UUUU..SSSSSSSSS....CCCCCCCCC......AAAAA......
//.RRRRRRRRRRR..BBBBBBBBBBB..UUUU...UUUU..SSSSSSSSSS..SCCCCCCCCCC....AAAAAA......
//.RRRR...RRRRR.BBBB...BBBB..UUUU...UUUU.USSSS..SSSS..SCCC...CCCCC...AAAAAAA.....
//.RRRR...RRRRR.BBBB...BBBB..UUUU...UUUU.USSSS.......SSCC.....CCC...AAAAAAAA.....
//.RRRRRRRRRRR..BBBBBBBBBBB..UUUU...UUUU..SSSSSSS....SSCC...........AAAAAAAA.....
//.RRRRRRRRRRR..BBBBBBBBBB...UUUU...UUUU...SSSSSSSSS.SSCC...........AAAA.AAAA....
//.RRRRRRRR.....BBBBBBBBBBB..UUUU...UUUU.....SSSSSSS.SSCC..........CAAAAAAAAA....
//.RRRR.RRRR....BBBB....BBBB.UUUU...UUUU........SSSSSSSCC.....CCC..CAAAAAAAAAA...
//.RRRR..RRRR...BBBB....BBBB.UUUU...UUUU.USSS....SSSS.SCCC...CCCCC.CAAAAAAAAAA...
//.RRRR..RRRRR..BBBBBBBBBBBB.UUUUUUUUUUU.USSSSSSSSSSS.SCCCCCCCCCC.CCAA....AAAA...
//.RRRR...RRRRR.BBBBBBBBBBB...UUUUUUUUU...SSSSSSSSSS...CCCCCCCCCC.CCAA.....AAAA..
//.RRRR....RRRR.BBBBBBBBBB.....UUUUUUU.....SSSSSSSS.....CCCCCCC..CCCAA.....AAAA..
//...............................................................................

Utilize como busca CPF, NOME etc...

================BY RDEV==========================================================
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
print("[6] Buscar por CPF, TELEFONE e EMAIL (OPÇÃO 2 LENTO)")
plataforma = input("Digite o número da plataforma: ")
print("""

    """)
if plataforma == "1":
    print("Desenvolvido por RDEV")
    print("Ver: 1.5")

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


    print("[1] Básico (Recomendado) ")
    print("[2] Avançado")
    print("[3] Super Avançado")
    print("")

    escolha = input("Escolha uma opção: ")

    if escolha == "1":
        max_resultados = 150
    elif escolha == "2":
        max_resultados = 350
    elif escolha == "3":
        max_resultados = 2500
    else:
        print("Opção inválida.")
        exit()

    url_base_google_compl = "https://www.google.com/search?q={termo}&start={start}&num=10"
    start = 0
    espera = 1  # Tempo inicial de espera (1 segundo)

    resultados = []
    while len(resultados) < max_resultados:
        url_busca = url_base_google_compl.format(termo=termo_formatado, start=start)
        try:
            headers = {
                "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{random.randint(500, 600)}.{random.randint(0, 99)} (KHTML, like Gecko) Chrome/{random.randint(80, 89)}.0.{random.randint(4000, 5000)}.{random.randint(100, 999)} Safari/537.36",
            }
            resposta = requests.get(url_busca, headers=headers)
            if resposta.status_code == 429:
                print("Muitas solicitações! Tente novamente mais tarde.")
                time.sleep(espera)
                espera *= 2  # Dobra o tempo de espera a cada solicitação
                continue
            resposta.raise_for_status()  # Verifica se ocorreu algum outro erro na requisição
        except requests.exceptions.RequestException as e:
            print(f"Ocorreu um erro ao fazer a requisição: {e}")
            exit()

        soup = BeautifulSoup(resposta.text, "html.parser")
        sugestoes = soup.find_all("div", class_="BNeawe s3v9rd AP7Wnd")
        for sugestao in sugestoes:
            nome = sugestao.text.strip()
            if nome not in resultados:
                resultados.append(nome)
        if len(sugestoes) == 0:
            break
        start += 10
        espera = 1  # Reseta o tempo de espera para 1 segundo após uma solicitação bem-sucedida

    cpfs = []
    telefones = []
    emails = []

    for resultado in resultados:
        try:
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
        except Exception as e:
            print(f"Ocorreu um erro ao processar o resultado: {e}")

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
    print("Este metodo é mais lento que a opção 1")
    print("")
    print("[1] Básico (Recomendado) ")
    print("[2] Avançado")
    print("[3] Super Avançado")
    print("")

    escolha = input("Escolha uma opção: ")

    if escolha == "1":
        max_resultados = 20
    elif escolha == "2":
        max_resultados = 50
    elif escolha == "3":
        max_resultados = 500
    else:
        print("Opção inválida.")
        exit()

    url_base_search_engine = "https://search.yahoo.com/search?p={termo}&b={start}"  # Defina a URL base do mecanismo de busca
    start = 0

    resultados = []
    while len(resultados) < max_resultados:
        url_busca = url_base_search_engine.format(termo=termo_formatado, start=start)
        try:
            resposta = requests.get(url_busca)
            resposta.raise_for_status()
            if resposta.status_code == 200:
                soup = BeautifulSoup(resposta.text, "html.parser")
                links = soup.select("h3 > a")
                for link in links:
                    titulo = link.text
                    url = link["href"]
                    resultados.append((titulo, url))
            else:
                print("Não foi possível conectar ao mecanismo de busca.")
                break
        except requests.exceptions.RequestException as e:
            print(f"Ocorreu um erro ao fazer a requisição: {e}")
            break

        start += 10


    cpfs = []
    telefones = []
    emails = []

    for resultado in resultados:
        titulo = resultado[0]
        url = resultado[1]
        try:
            resposta = requests.get(url)
            resposta.raise_for_status()
            conteudo = resposta.text

            # Busca CPF
            cpf_match = re.findall(r"\d{3}\.\d{3}\.\d{3}-\d{2}", conteudo)
            for cpf in cpf_match:
                if cpf not in cpfs:
                    cpfs.append(cpf)

            # Busca telefone
            telefone_match = re.findall(r"\(\d{2}\)\s\d{4,5}-\d{4}", conteudo)
            for telefone in telefone_match:
                if telefone not in telefones:
                    telefones.append(telefone)

            # Busca e-mail
            email_match = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", conteudo)
            for email in email_match:
                if email not in emails:
                    emails.append(email)

        except requests.exceptions.RequestException as e:
            print(f"Ocorreu um erro ao obter o conteúdo da página: {e}")
            continue

    print("CPFs encontrados:")
    for cpf in cpfs:
        print("- " + cpf)

    print("Telefones encontrados:")
    for telefone in telefones:
        print("- " + telefone)

    print("E-mails encontrados:")
    for email in emails:
        print("- " + email)
