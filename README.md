# Pokédex ASCII via Telnet

Projeto final da disciplina de **Automação e Programabilidade em Redes**, que integra redes, scraping web e terminal interativo com temática Pokémon.

---

## O que o projeto faz?

- Conecta usuários via Telnet.
- Exibe um menu interativo com múltiplas funções temáticas do universo Pokémon.
- Permite consultar dados reais de Pokémon extraídos da internet.
- Oferece jogos e quizzes interativos.

---

## Funcionalidades do Menu

1. Dizer Olá
2. Hora atual no servidor
3. Busca na Pokédex (com arte ASCII, tipo, espécie, entrada, evoluções)
4. Curiosidade aleatória sobre Pokémon
5. Jogo: adivinhe o Pokémon pelo tipo/especie/número/entrada/imagem
6. Gere um time aleatório de até 6 Pokémon
7. Mostre as fraquezas de um Pokémon informado
8.  Quem é esse Pokémon? (minigame estilo anime com imagem ASCII)
9.  Quiz: qual é o tipo do Pokémon? (4 alternativas)
10. Gerador de números para loteria
11. Batalha de Pokémon (comparação de tipos)
12. Sair

---

## 🗂️ Estrutura do Projeto

```
/Trabalho final automação em redes
├── servidor_telnet.py # Código principal (servidor TCP com menu interativo)
├── pokedex.py # Funções de scraping, conversão de imagem e manipulação de dados
├── curiosidades.py # Lista de curiosidades Pokémon
├── requirements.txt # Dependências do projeto
└── README.md # Este arquivo
```


---

## ⚙️ Como rodar o projeto

### 1. Clonar ou baixar o repositório

```
cd Trabalho-final-APR

python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
```


## 📦 Dependências
O projeto usa as seguintes bibliotecas principais:

- `selenium`: automação e scraping de sites.

- `pillow`: manipulação de imagens (ASCII art).

- `requests`: download de imagens.

- `translate`: tradução de texto (descrição e espécie).

## 🧪 Uso do Telnet
Execute o servidor com:

```
python servidor_telnet.py
```
Em outro terminal:

```
telnet localhost 8025
```