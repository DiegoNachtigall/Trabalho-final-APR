import random
import socket
import time
from pokedex import *
from curiosidades import curiosidades
def input(cliente):
    buffer = b''
    while True:
        byte = cliente.recv(1)
        if not byte or byte == b'\n':
            break
        buffer += byte
    return buffer.decode('UTF-8').strip()

# Passo 1: Criar Socket
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Passo 2: Fazer o Bind, definir endereço e porta de comunicaçao
servidor.bind(('0.0.0.0', 8025))

servidor.listen(1)

cliente, endereco = servidor.accept()

menu = (
    "====================MENU====================\r\n"
    "1. Dizer Olá\r\n"
    "2. Hora atual no servidor\r\n"
    "3. Busca na pokedex\r\n"
    "4. Curiosidade aleatoria sobre pokemon\r\n"
    "5. Numeros para jogar na loteria\r\n"
    "6. Teste de latencia\r\n"
    "7. Jogo de adivinhar pokemon\r\n"
    "8. Time aleatório\r\n"
    "9. Fraquezas do pokemon\r\n"
    "10. Ideia nova 7\r\n"
    "11. Ideia nova 8\r\n\r\n"
    "12. Sair\r\n"
    "Escolha uma opcao: \r\n"
)

while True:
    cliente.sendall(menu.encode('UTF-8'))
    opcao = input(cliente)
    
    # Opcao de olá
    if opcao == '1':
        cliente.sendall("\r\n==================================\r\n".encode('UTF-8'))
        cliente.sendall("\r\nOlá\r\n".encode('UTF-8'))
        cliente.sendall("\r\n==================================\r\n".encode('UTF-8'))
        cliente.sendall("\r\nAperte ENTER para voltar ao menu\r\n".encode('UTF-8'))
        input(cliente)

    # Opcao de hora
    elif opcao == '2':
        cliente.sendall("\r\n==================================\r\n".encode('UTF-8'))
        cliente.sendall(time.strftime("\r\n%H:%M:%S\r\n").encode('UTF-8'))
        cliente.sendall("\r\n==================================\r\n".encode('UTF-8'))
        cliente.sendall("\r\nAperte ENTER para voltar ao menu\r\n".encode('UTF-8'))
        input(cliente)

    # Opcao de buscar na pokedex
    elif opcao == '3':
        cliente.sendall("\r\n==================================\r\n".encode('UTF-8'))
        cliente.sendall("Digite o nome do Pokemon: \r\n".encode('UTF-8'))
        nome_pokemon = input(cliente)
        cliente.sendall("\r\nAguarde um momento, procurando pokemon...\r\n".encode('UTF-8'))
        dados = obter_dados_pokemon(nome_pokemon)
        if dados:
            resposta = (
                f"{dados['imagem']}\r\n"
                f"Nome: {dados['nome']}\r\n"
                f"Numero: {dados['numero']}\r\n"
                f"Tipo: {dados['tipo']}\r\n"
                f"Especie: {dados['especie']}\r\n"
                f"Entrada: {dados['entrada']}\r\n"
                f"Evolucoes: {dados['evolucoes']}\r\n"
            )
        else:
            resposta = "Pokemon não encontrado.\r\n"
        cliente.sendall(resposta.encode('UTF-8'))
        cliente.sendall("\r\n==================================\r\n".encode('UTF-8'))
        cliente.sendall("\r\nAperte ENTER para voltar ao menu\r\n".encode('UTF-8'))
        input(cliente)

    # Opcao de curiosidades
    elif opcao == '4':
        curiosidade = random.choice(curiosidades)
        cliente.sendall("\r\n==================================\r\n".encode('UTF-8'))
        cliente.sendall(f"\r\n{curiosidade}\r\n".encode('UTF-8'))
        cliente.sendall("\r\n==================================\r\n".encode('UTF-8'))
        cliente.sendall("\r\nAperte ENTER para voltar ao menu\r\n".encode('UTF-8'))
        input(cliente)
        
    # Opcao de numeros da loteria
    elif opcao == '5':
        numeros = []
        cliente.sendall("\r\n==================================\r\n".encode('UTF-8'))
        cliente.sendall("\r\nGerando números para jogar na loteria...\r\n".encode('UTF-8'))
        while len(numeros) < 6:
            numero_aleatorio = str(random.randint(1, 60))
            if numero_aleatorio not in numeros:
                numeros.append(numero_aleatorio)
        numeros.sort()
        numeros_sorteados = ', '.join(numeros[:6])
        cliente.sendall(f"\r\nNúmeros sorteados: {numeros_sorteados}\r\n".encode('UTF-8'))
        cliente.sendall("\r\n==================================\r\n".encode('UTF-8'))
        cliente.sendall("\r\nAperte ENTER para voltar ao menu\r\n".encode('UTF-8'))
        input(cliente)

    # Opcao de teste de latencia
    elif opcao == '6':
        cliente.sendall("\r\n==================================\r\n".encode('UTF-8'))
        cliente.sendall("\r\nDigite o número de pacotes a serem enviados: \r\n".encode('UTF-8'))
        num_pacotes = int(input(cliente))
        tempo_inicial = time.time()
        for i in range(num_pacotes):
            cliente.sendall(f"Pacote {i + 1} enviado\r\n".encode('UTF-8'))
            time.sleep(0.1)
        tempo_final = time.time()
        latencia = (tempo_final - tempo_inicial) / num_pacotes
        cliente.sendall(f"Latência média: {latencia:.4f} segundos\r\n".encode('UTF-8'))
        cliente.sendall("\r\n==================================\r\n".encode('UTF-8'))
        cliente.sendall("\r\nAperte ENTER para voltar ao menu\r\n".encode('UTF-8'))
        input(cliente)
        
    # Opcao de jogo de adivinhar pokemon
    elif opcao == '7':
        cliente.sendall("\r\n==================================\r\n".encode('UTF-8'))
        cliente.sendall("\r\nVamos jogar! Eu vou te dar os tipos do pokemon e você deve tentar adivinhar o nome.\r\n".encode('UTF-8'))
        cliente.sendall("\r\nTente adivinhar em 5 tentativas.\r\n".encode('UTF-8'))
        cliente.sendall("\r\nAguarde um momento, procurando pokemon...\r\n".encode('UTF-8'))
        nome_pokemon = pokemon_aleatorio()
        cliente.sendall("\r\n==================================\r\n".encode('UTF-8'))
        cliente.sendall("\r\nVamos jogar!\r\n".encode('UTF-8'))
        tentativas = 5
        while tentativas > 0:
            if tentativas == 5:
                cliente.sendall(f"\r\nO Pokémon é do tipo: {nome_pokemon['tipo']}\r\n".encode('UTF-8'))
            elif tentativas == 4:
                cliente.sendall(f"\r\nO Pokémon é da espécie: {nome_pokemon['especie']}\r\n".encode('UTF-8'))
            elif tentativas == 3:
                cliente.sendall(f"\r\nO Pokémon tem o número: {nome_pokemon['numero']}\r\n".encode('UTF-8'))
            elif tentativas == 2:
                cliente.sendall(f"\r\nO Pokémon tem a seguinte entrada: {nome_pokemon['entrada']}\r\n".encode('UTF-8'))
            elif tentativas == 1:
                cliente.sendall(f"\r\n{nome_pokemon['imagem']}\r\n".encode('UTF-8'))
            cliente.sendall("Digite o nome do Pokémon: \r\n".encode('UTF-8'))
            palpite = input(cliente)
            if palpite.lower() == nome_pokemon['nome'].lower():
                cliente.sendall("\r\nVocê acertou!\r\n".encode('UTF-8'))
                break
            tentativas -= 1
            if tentativas > 0:
                cliente.sendall(f"\r\nTentativas restantes: {tentativas}\r\n".encode('UTF-8'))
            else:
                cliente.sendall(f"\r\nVocê perdeu! O Pokémon era: {nome_pokemon['nome']}\r\n".encode('UTF-8'))

        if tentativas == 0:
            cliente.sendall(f"\r\nVocê perdeu! O Pokemon era: {nome_pokemon['nome']}\r\n".encode('UTF-8'))
        cliente.sendall("\r\n==================================\r\n".encode('UTF-8'))
        cliente.sendall("\r\nAperte ENTER para voltar ao menu\r\n".encode('UTF-8'))
        input(cliente)

    # Opção de time aleatorio
    elif opcao == '8':        
        cliente.sendall("\r\n==================================\r\n".encode('UTF-8'))
        cliente.sendall("\r\nGerando um time aleatório de Pokémon...\r\n".encode('UTF-8'))
        qtd = random.randint(1, 6)
        cliente.sendall(f"\r\nO time terá {qtd} Pokémon(s).\r\n".encode('UTF-8'))
        for _ in range(qtd):
            pokemon = pokemon_aleatorio()
            cliente.sendall(f"\r\n{pokemon['nome']} ({pokemon['tipo']})\r\n".encode('UTF-8'))
        cliente.sendall("\r\n==================================\r\n".encode('UTF-8'))
        cliente.sendall("\r\nAperte ENTER para voltar ao menu\r\n".encode('UTF-8'))
        input(cliente)

    # Opcao de fraquezas do pokemon
    elif opcao == '9':
        cliente.sendall("\r\n==================================\r\n".encode('UTF-8'))
        cliente.sendall("\r\nOs tipos de fraquezas do Pokémon\r\n".encode('UTF-8'))
        cliente.sendall("\r\nDigite o nome do Pokémon: \r\n".encode('UTF-8'))
        pesquisa = input(cliente)
        cliente.sendall("\r\nAguarde um momento, procurando fraquezas...\r\n".encode('UTF-8'))
        nome_pokemon = obter_dados_pokemon(pesquisa)
        if nome_pokemon:
            tipos = nome_pokemon['tipo'].split(', ')
            fraquezas = []
            fraquezas_tipos = {
                'FIRE': ['Water', 'Rock', 'Ground'],
                'WATER': ['Electric', 'Grass'],
                'GRASS': ['Fire', 'Flying', 'Bug', 'Poison', 'Ice'],
                'ELECTRIC': ['Ground'],
                'ROCK': ['Water', 'Grass', 'Fighting', 'Ground', 'Steel'],
                'FIGHTING': ['Psychic', 'Fairy', 'Flying'],
                'PSYCHIC': ['Bug', 'Ghost', 'Dark'],
                'BUG': ['Fire', 'Flying', 'Rock'],
                'GHOST': ['Ghost', 'Dark'],
                'DARK': ['Fairy', 'Fighting'],
                'FAIRY': ['Poison', 'Steel'],
                'POISON': ['Ground', 'Psychic'],
                'GROUND': ['Water', 'Grass', 'Ice'],
                'FLYING': ['Electric', 'Ice', 'Rock'],
                'ICE': ['Fire', 'Fighting', 'Rock', 'Steel'],
                'STEEL': ['Fire', 'Fighting', 'Ground'],
                'DRAGON': ['Ice', 'Dragon', 'Fairy'],
                'NORMAL': ['Fighting']
            }

            fraquezas_tipo = []
            for tipo in tipos:
                tipo_upper = tipo.upper()
                if tipo_upper in fraquezas_tipos:
                    fraquezas_tipo.extend(fraquezas_tipos[tipo_upper])

            fraquezas.extend(
                [f'{fraqueza} (x{fraquezas_tipo.count(fraqueza)})' if fraquezas_tipo.count(fraqueza) > 1 else fraqueza for fraqueza in set(fraquezas_tipo)]
            )
            cliente.sendall("\r\n==================================\r\n".encode('UTF-8'))
            cliente.sendall(f"\r\nFraquezas do Pokémon {nome_pokemon['nome']} ({nome_pokemon['tipo']}): {', '.join(fraquezas)}\r\n".encode('UTF-8'))
        else:
            cliente.sendall("\r\nPokemon não encontrado.\r\n".encode('UTF-8'))
        cliente.sendall("\r\n==================================\r\n".encode('UTF-8'))
        cliente.sendall("\r\nAperte ENTER para voltar ao menu\r\n".encode('UTF-8'))
        input(cliente)

    # Opcao de curiosidades
    elif opcao == '10':
        cliente.sendall("\r\n==================================\r\n".encode('UTF-8'))
        curiosidade = random.choice(curiosidades)

    # Opcao de sair
    elif opcao == '12':
        cliente.sendall("\r\nEncerrando conexao\r\n".encode('UTF-8'))
        break
# Encerrar conexões
cliente.close()
servidor.close()