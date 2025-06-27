# pokedex.py
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from translate import Translator
import time
from PIL import Image
import requests
from io import BytesIO

# Mapeamento de tons para caracteres
ASCII_CHARS = "@%#*+=-:. "

def redimensionar(imagem, nova_largura=50):
    largura, altura = imagem.size
    proporcao = altura / largura
    nova_altura = int(nova_largura * proporcao * 0.55)  # ajusta altura para terminal
    return imagem.resize((nova_largura, nova_altura))

def cinza(imagem):
    return imagem.convert("L")

def pixel_para_ascii(imagem):
    pixels = imagem.getdata()
    escala = len(ASCII_CHARS) - 1
    ascii_str = "".join(ASCII_CHARS[pixel * escala // 255] for pixel in pixels)
    return ascii_str

def imagem_para_ascii(url_imagem, largura=50):
    resposta = requests.get(url_imagem)
    imagem = Image.open(BytesIO(resposta.content))
    
    imagem = redimensionar(imagem, largura)
    imagem = cinza(imagem)
    
    ascii_str = pixel_para_ascii(imagem)
    
    largura = imagem.width
    ascii_img = "\n".join(ascii_str[i:i+largura] for i in range(0, len(ascii_str), largura))
    return ascii_img


def iniciar_navegador():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    navegador = webdriver.Chrome(options=options)
    return navegador

def buscar_pokemon(navegador, nome):
    navegador.get('https://pokemondb.net/pokedex/all')
    time.sleep(2)
    pesquisa = navegador.find_element(By.ID, 'filter-pkmn-name')
    pesquisa.send_keys(nome)
    time.sleep(2)
    linhas = navegador.find_elements(By.CSS_SELECTOR, 'table#pokedex tbody tr')
    for linha in linhas:
        if linha.is_displayed():
            link = linha.find_element(By.CSS_SELECTOR, 'a.ent-name')
            link.click()
            return WebDriverWait(navegador, 10)
    return None

def extrair_dados(navegador, wait):
    img = navegador.find_element(By.CSS_SELECTOR, "div.grid-col.span-md-6.span-lg-4.text-center img").get_attribute("src")
    nome = navegador.find_element(By.TAG_NAME, "h1").text
    numero = navegador.find_element(By.TAG_NAME, "strong").text
    especie, tipos = '', []
    for linha in navegador.find_elements(By.CLASS_NAME, "vitals-table")[0].find_elements(By.TAG_NAME, 'tr'):
        th = linha.find_element(By.TAG_NAME, 'th')
        td = linha.find_element(By.TAG_NAME, 'td')
        if th.text == 'Type':
            tipos = [a.text for a in td.find_elements(By.TAG_NAME, 'a')]
        if th.text == 'Species':
            especie = td.text
    entrada = navegador.find_element(By.XPATH, "//h2[contains(text(), 'Pokédex entries')]/following-sibling::div[@class='resp-scroll']/table").find_elements(By.TAG_NAME, 'tr')[-1].find_element(By.TAG_NAME, 'td').text
    try:
        nomes_evolucoes = [e.find_element(By.CSS_SELECTOR, 'a.ent-name').text for e in navegador.find_elements(By.CSS_SELECTOR, 'div.infocard-list-evo div.infocard')]
    except:
        nomes_evolucoes = ['Nenhuma evolução']
    tradutor = Translator(to_lang="pt")
    return {
        'imagem': imagem_para_ascii(img, largura=50).replace('\n', '\r\n'),
        'nome': nome,
        'numero': numero,
        'tipo': ', '.join(tipos),
        'especie': tradutor.translate(especie),
        'entrada': tradutor.translate(entrada),
        'evolucoes': ', '.join(nomes_evolucoes),
    }

def obter_dados_pokemon(nome):
    navegador = iniciar_navegador()
    wait = buscar_pokemon(navegador, nome)
    if not wait:
        navegador.quit()
        return None
    dados = extrair_dados(navegador, wait)
    navegador.quit()
    return dados

def pokemon_aleatorio():
    import random
    
    navegador = iniciar_navegador()
    numero_pokemon = random.randint(1, 1025)
    
    navegador.get(f'https://pokemondb.net/pokedex/{numero_pokemon}')
    time.sleep(2)
    wait = WebDriverWait(navegador, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.grid-col.span-md-6.span-lg-4.text-center img')))
    dados = extrair_dados(navegador, wait)
    navegador.quit()
    return dados
