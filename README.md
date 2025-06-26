# Pokédex ASCII via Telnet

Este é um projeto da disciplina de automação e programabilidade em redes que integra:

-  Um **servidor Telnet em Python**, com menu interativo;
-  Uma **Pokédex automatizada com Selenium**, que busca informações de Pokémon em tempo real;
-  Exibição da imagem do Pokémon em **ASCII art** diretamente no terminal Telnet!

---

##  Funcionalidades

-  Menu com múltiplas opções interativas;
-  Busca por Pokémon por nome (ex: `bulbasaur`, `pikachu`);
-  Retorno de dados: nome, número, tipo, espécie, entrada da Pokédex, linha evolutiva;
-  Conversão da imagem do Pokémon em **ASCII art** visível no terminal;
-  Funções adicionais como hora atual, testes de latência e curiosidades aleatórias.

---


##  Estrutura do Projeto

```bash
/Trabalho final automação em redes
├── servidor_telnet.py      # Servidor que aceita conexões Telnet e interage com o usuário
├── pokedex.py              # Módulo responsável por extrair e exibir os dados do Pokémon
├── README.md               # Este arquivo
├── requirements.txt        # Dependências do projeto
├── curiosidades.py        # Curiosidades aleatórias sobre Pokémon
```

##  Como executar
Para garantir que o projeto funcione corretamente e com dependências isoladas, é recomendado o uso de um ambiente virtual:

```bash
# 1. Clone ou baixe este repositório
cd Trabalho-final-APR

# 2. Crie o ambiente virtual
python -m venv venv

# 3. Ative o ambiente virtual
# No Windows:
venv\Scripts\activate

# No Linux/macOS:
source venv/bin/activate

# 4. Instale as dependências do projeto
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
