import random
import socket
import time
from pokedex import *
from dados import *
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
    "5. Jogo de adivinhar pokemon\r\n"
    "6. Time aleatório\r\n"
    "7. Fraquezas do pokemon\r\n"
    "8. Quem é esse pokemon?\r\n"
    "9. Quiz: qual é o tipo do Pokémon?\r\n"
    "10. Batalha de Pokémon\r\n"
    "11. Numeros para jogar na loteria\r\n\r\n"
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

    # Opcao de jogo de adivinhar pokemon
    elif opcao == '5':
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
    elif opcao == '6':        
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
    elif opcao == '7':
        cliente.sendall("\r\n==================================\r\n".encode('UTF-8'))
        cliente.sendall("\r\nOs tipos de fraquezas do Pokémon\r\n".encode('UTF-8'))
        cliente.sendall("\r\nDigite o nome do Pokémon: \r\n".encode('UTF-8'))
        pesquisa = input(cliente)
        cliente.sendall("\r\nAguarde um momento, procurando fraquezas...\r\n".encode('UTF-8'))
        nome_pokemon = obter_dados_pokemon(pesquisa)
        if nome_pokemon:
            tipos = nome_pokemon['tipo'].split(', ')
            fraquezas = []
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

    # Opcao de adivinhar pokemon (Quem é esse Pokémon?)
    elif opcao == '8':
        cliente.sendall("\r\n==================================\r\n".encode('UTF-8'))
        cliente.sendall("Quem é esse Pokémon?\r\n".encode('UTF-8'))
        cliente.sendall("Você verá a imagem ascii de um Pokémon e terá 3 tentativas para adivinhar!\r\n".encode('UTF-8'))
        cliente.sendall("\r\nAguarde um momento, procurando Pokémon...\r\n".encode('UTF-8'))

        pokemon = pokemon_aleatorio()
        cliente.sendall("\r\nAqui está a silhueta:\r\n\r\n".encode('UTF-8'))
        cliente.sendall(pokemon['imagem'].replace('\n', '\r\n').encode('cp1252'))

        tentativas = 3
        while tentativas > 0:
            cliente.sendall(f"\r\nTentativas restantes: {tentativas}\r\n".encode('UTF-8'))
            cliente.sendall("Quem é esse Pokémon? ".encode('UTF-8'))
            palpite = input(cliente)
            if palpite.strip().lower() == pokemon['nome'].lower():
                cliente.sendall("\r\nVocê acertou!\r\n".encode('UTF-8'))
                break
            tentativas -= 1

        if tentativas == 0:
            cliente.sendall(f"\r\nNão foi dessa vez! O Pokémon era: {pokemon['nome']}\r\n".encode('UTF-8'))
        cliente.sendall("\r\n==================================\r\n".encode('UTF-8'))
        cliente.sendall("\r\nAperte ENTER para voltar ao menu\r\n".encode('UTF-8'))
        input(cliente)

    # Opcao de quiz: qual é o tipo do Pokémon?
    elif opcao == '9':
        cliente.sendall("\r\n==================================\r\n".encode('UTF-8'))
        cliente.sendall("Quiz: Qual é o tipo do Pokémon?\r\n".encode('UTF-8'))
        cliente.sendall("Você verá um Pokémon e deverá escolher o tipo correto entre 4 opções!\r\n".encode('UTF-8'))
        cliente.sendall("\r\nAguarde um momento, procurando Pokémon...\r\n".encode('UTF-8'))

        pokemon = pokemon_aleatorio()
        tipo_correto = pokemon['tipo'].split(', ')[0]  # pega o primeiro tipo, se for duplo

        # Lista de tipos existentes
        todos_os_tipos = [
            'FIRE', 'WATER', 'GRASS', 'ELECTRIC', 'ROCK', 'GROUND',
            'BUG', 'FLYING', 'FIGHTING', 'POISON', 'PSYCHIC', 'DARK',
            'GHOST', 'STEEL', 'ICE', 'DRAGON', 'FAIRY', 'NORMAL'
        ]

        # Gera alternativas falsas, sem repetir o tipo correto
        alternativas = [tipo_correto]
        while len(alternativas) < 4:
            falso = random.choice(todos_os_tipos)
            if falso not in alternativas:
                alternativas.append(falso)
        random.shuffle(alternativas)

        # Exibe a pergunta
        cliente.sendall(f"\r\nQual é o tipo de {pokemon['nome']}?\r\n".encode('UTF-8'))
        for i, tipo in enumerate(alternativas):
            cliente.sendall(f"{i + 1}. {tipo}\r\n".encode('UTF-8'))

        cliente.sendall("\r\nEscolha (1-4): ".encode('UTF-8'))
        resposta = input(cliente)

        try:
            indice = int(resposta.strip()) - 1
            if alternativas[indice] == tipo_correto:
                cliente.sendall("\r\nResposta correta!\r\n".encode('UTF-8'))
            else:
                cliente.sendall(f"\r\nResposta errada! O tipo correto era: {tipo_correto}\r\n".encode('UTF-8'))
        except:
            cliente.sendall("\r\nEntrada inválida. Tente novamente na próxima vez!\r\n".encode('UTF-8'))

        cliente.sendall("\r\n==================================\r\n".encode('UTF-8'))
        cliente.sendall("\r\nAperte ENTER para voltar ao menu\r\n".encode('UTF-8'))
        input(cliente)

    # Opcao de duelos aleatorios
    elif opcao == '10':
        cliente.sendall("\r\n==================================\r\n".encode('UTF-8'))
        cliente.sendall("Duelos Aleatórios!\r\n".encode('UTF-8'))
        cliente.sendall("Escolha qual Pokémon venceria em uma batalha!\r\n".encode('UTF-8'))
        cliente.sendall("\r\nAguarde um momento, procurando Pokémons...\r\n".encode('UTF-8'))

        p1 = pokemon_aleatorio()
        p2 = pokemon_aleatorio()

        while p2['nome'] == p1['nome']:
            p2 = pokemon_aleatorio()  # Garante que não sejam iguais
            
        cliente.sendall("\r\n==================================\r\n".encode('UTF-8'))
        cliente.sendall(f"\r\n1. {p1['nome']}\r\n".encode('UTF-8'))
        cliente.sendall("VS\r\n".encode('UTF-8'))
        cliente.sendall(f"2. {p2['nome']}\r\n".encode('UTF-8'))
        cliente.sendall("\r\n==================================\r\n".encode('UTF-8'))
        cliente.sendall("\r\nQuem venceria? Digite 1 ou 2: ".encode('UTF-8'))
        escolha = input(cliente)

        # Fraquezas simples para decisão
        def tipo_vantajoso(tipos, fraq):
            for t in tipos:
                for f in fraq:
                    if f in fraquezas_tipos.get(t, []):
                        print(f"{t} -> {f}")
                        return True
            return False

        tipos_p1 = [t.strip().upper() for t in p1['tipo'].split(',')]
        tipos_p2 = [t.strip().upper() for t in p2['tipo'].split(',')]

        # Verifica se p1 tem vantagem sobre p2
        p1_loss = tipo_vantajoso(tipos_p1, tipos_p2)
        p2_loss = tipo_vantajoso(tipos_p2, tipos_p1)

        vencedor = None
        if p1_loss and not p2_loss:
            vencedor = '2'
        elif p2_loss and not p1_loss:
            vencedor = '1'
        print(f"Vencedor: {vencedor}")
        if vencedor:
            if escolha == vencedor:
                cliente.sendall(f"\r\nVocê acertou!!\r\n".encode('UTF-8'))
            else:
                cliente.sendall(f"\r\nVocê errou!!\r\n".encode('UTF-8'))
        else:
            cliente.sendall(f"\r\nEmpate técnico! Nenhum tem vantagem clara de tipo. {p1['tipo']} vs {p2['tipo']}\r\n".encode('UTF-8'))

        cliente.sendall("\r\n==================================\r\n".encode('UTF-8'))
        cliente.sendall("\r\nAperte ENTER para voltar ao menu\r\n".encode('UTF-8'))
        input(cliente)

    # Opcao de numeros da loteria
    elif opcao == '11':
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

    # Opcao de sair
    elif opcao == '12':
        cliente.sendall("\r\nEncerrando conexao\r\n".encode('UTF-8'))
        break
# Encerrar conexões
cliente.close()
servidor.close()