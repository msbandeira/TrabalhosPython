import requests
from bs4 import BeautifulSoup
import time
from plyer import notification

# URLs dos sites que você quer monitorar
urls = [
    "https://exemplo.com.br",
    "https://exemplo2.com.br"
]

# Função para obter o conteúdo do site
def get_site_content(url):
    response = requests.get(url)
    return response.text

# Função para extrair títulos de artigos ou conteúdos específicos
def extract_content(html, site_id):
    soup = BeautifulSoup(html, 'html.parser')
    if site_id in [0, 1]:
        titles = [article.text.strip() for article in soup.find_all('h1', class_='panel-title')]
    return titles

# Função para enviar notificações
def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name='Site Monitor',
        timeout=10  # Duração da notificação em segundos
    )

# Função principal para monitorar os sites
def monitor_sites(urls, check_interval=60):
    last_titles_list = [set() for _ in urls]

    while True:
        for i, url in enumerate(urls):
            html = get_site_content(url)
            current_titles = set(extract_content(html, i))

            if not last_titles_list[i]:
                print(f"Títulos atuais para {url}:")
                for title in current_titles:
                    print(title)
            else:
                new_titles = current_titles - last_titles_list[i]
                if new_titles:
                    print(f"Novos conteúdos publicados em {url}:")
                    for title in new_titles:
                        print(title)
                        send_notification(f"Novo conteúdo em {url}", title)
                else:
                    print(f"Nenhum novo conteúdo encontrado em {url}.")

            last_titles_list[i] = current_titles

        time.sleep(check_interval)

# Inicia a monitorização dos sites
monitor_sites(urls, check_interval=300)  # Verifica a cada 300 segundos (5 minutos)
