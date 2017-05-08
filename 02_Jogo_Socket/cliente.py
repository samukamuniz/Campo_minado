import socket, pickle
import sys, os
import random
from ast import literal_eval

HOST = '127.0.0.1'
PORT = 5000
ENCODE = "UTF-8"
MAX_BYTES = 65535

#Main definition - constants
menu_actions = {}

def mostrarMatriz(matriz, l):
    print("")
    for i in range(l):
        print(matriz[i])

def sortearBombas(matriz, linhasMatriz, colunasMatriz, quantidadeBombas):
    waiter = ["SB", linhasMatriz, colunasMatriz, quantidadeBombas, matriz]
    data = pickle.dumps(waiter)
    #Send to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    destiny = (HOST, PORT)
    sock.sendto(data, destiny)
    # Receive to server
    data, address = sock.recvfrom(MAX_BYTES)
    waiter = pickle.loads(data)
    return waiter

def bombasAoRedor(linha,coluna,posBombas):
    waiter = ["BR", linha, coluna, posBombas]
    data = pickle.dumps(waiter)
    # Send to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    destiny = (HOST, PORT)
    sock.sendto(data, destiny)
    # Receive to server
    data, address = sock.recvfrom(MAX_BYTES)
    waiter = pickle.loads(data)
    return waiter

def save(historico):
    waiter = ["SV", historico]
    data = pickle.dumps(waiter)
    # Send to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    destiny = (HOST, PORT)
    sock.sendto(data, destiny)

def main_menu():

    if (os.path.exists('log_game.txt') == True):
        waiter = ["VF",'log_game.txt']
        data = pickle.dumps(waiter)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        destiny = (HOST, PORT)
        sock.sendto(data, destiny)
        data, address = sock.recvfrom(MAX_BYTES)
        waiter = literal_eval(str(pickle.loads(data)))
        dict = waiter

        if (dict.get('without') == "-1"):
            print("==================================================")
            print("                   CAMPO MINADO")
            print("==================================================\n")
            print("Seja bem vindo(a) ao jogo Campo minado!!!")
            print("Escolha um opção e divirta-se \n")
            print("1. Iniciar um novo jogo")
            print("0. Sair")
            choice = input(" >> ")
            exec_menu(choice)
            return
        else:
            restartGame()
    else:
        print("==================================================")
        print("                   CAMPO MINADO")
        print("==================================================\n")
        print("Seja bem vindo(a) ao jogo Campo minado!!!")
        print("Escolha um opção e divirta-se \n")
        print("1. Iniciar um novo jogo")
        print("0. Sair")
        choice = input(" >> ")
        exec_menu(choice)
        return

def exec_menu(choice):
    os.system("cls")
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print("Seleção inválida, por favor tentar novamente. \n")
            os.system("pause")
            menu_actions['main_menu']()
    return

def newGame():
    os.system("cls")
    print("==================================================")
    print("                   CAMPO MINADO")
    print("==================================================\n")
    perdeu = False
    jogadas = 0
    linhasMatriz = int(input("Digite quantas linhas deseja >> "))
    colunasMatriz = int(input("Digite quantas colunas deseja >> "))
    quantidadeBombas = int(input("Digite a quantidade de bombas >> "))
    waiter = ["GM", linhasMatriz, colunasMatriz, quantidadeBombas]
    data = pickle.dumps(waiter)
    #Send to Server
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    destiny = (HOST,PORT)
    sock.sendto(data, destiny)
    #Receive to server
    print("Requisitando dados ao servidor",sock.getsockname())
    data, address = sock.recvfrom(MAX_BYTES)
    waiter = pickle.loads(data)
    matriz = waiter
    mostrarMatriz(matriz,linhasMatriz)
    posBombas = sortearBombas(waiter, int(linhasMatriz), int(colunasMatriz), int(quantidadeBombas))
    qtdJogadas = ((linhasMatriz * colunasMatriz)-len(posBombas))
    while (perdeu==False):
        print("\nJogadas: %d | Jogadas restantes: %d" %(jogadas,qtdJogadas ))
        linha = int(input("\nDigite a linha >> "))-1
        coluna = int(input("Digite a coluna >> "))-1
        os.system("cls")
        if ([linha,coluna] in posBombas):
            print("\n\n. . @ . . . . . . . . . . . . . . . . . . @ . .")
            print(". . . . @ . . . . . . . . . . . . . . @ . . . .")
            print(". . . . . . @ BOOM!!! Você perdeu @ . . . . . .")
            print(". . . . @ . . . . . . . . . . . . . . @ . . . .")
            print(". . @ . . . . . . . . . . . . . . . . . . @ . .\n\n")
            historico = {"matriz": 0, "posBombas": 0, "jogadas": 0,"qtdJogadas":0, "linhasMatriz": 0, "colunasMatriz": 0, "without": "-1"}
            save(historico)
            waiter = ["GO"]
            data = pickle.dumps(waiter)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            destiny = (HOST, PORT)
            sock.sendto(data, destiny)
            os.system("pause")
            os.system("cls")
            menu_actions['main_menu']()
        else:
            matriz[linha][coluna] = str(bombasAoRedor(linha,coluna,posBombas))
            mostrarMatriz(matriz,linhasMatriz)
            jogadas += 1
            qtdJogadas -= 1
            historico = {"matriz": matriz, "posBombas":posBombas, "jogadas": jogadas,"qtdJogadas":qtdJogadas,"linhasMatriz": linhasMatriz, "colunasMatriz": colunasMatriz, "without": 0}
            if (((linhasMatriz*colunasMatriz)-jogadas)==len(posBombas)):
                print("\n\nPARABÉNS!!! Você ganhou o desafio.")
                print("Congratulations!!! You won the challenge\n\n")
                historico = {"matriz": 0, "posBombas": 0, "jogadas": 0,"qtdJogadas":0, "linhasMatriz": 0, "colunasMatriz": 0,
                             "without": "-1"}
                save(historico)
                waiter = ["WI"]
                data = pickle.dumps(waiter)
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                destiny = (HOST, PORT)
                sock.sendto(data, destiny)
                os.system("pause")
                os.system("cls")
                menu_actions['main_menu']()
            save(historico)
    return


def restartGame():
    os.system("cls")
    print("==================================================")
    print("                   CAMPO MINADO")
    print("==================================================\n")
    print("Seja bem vindo(a) ao jogo Campo minado!!!")
    print("\nVocê possui um jogo em andamento!!!Deseja continuar?\n1: Para Sim\n2: Para Não\n")
    choice = int(input(" >> "))
    if(choice == 2):
        os.system("cls")
        historico = {"matriz": 0, "posBombas": 0, "jogadas": 0,"qtdJogadas":0, "linhasMatriz": 0, "colunasMatriz": 0, "without": "-1"}
        save(historico)
        newGame()
    else:
        waiter = ["JS", 'log_game.txt']
        data = pickle.dumps(waiter)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        destiny = (HOST, PORT)
        sock.sendto(data, destiny)

        data, address = sock.recvfrom(MAX_BYTES)
        waiter = literal_eval(str(pickle.loads(data)))
        dict = waiter
        if (dict.get('without') == "-1"):
            print("\nNão existe nenhum jogo salvo em sistema!!!\n\nVocê deseja iniciar um novo jogo?\n1: para Sim \n2: para não")
            answer = int(input("\n >> "))
            if (answer == 1):
                os.system("cls")
                newGame()
            else:
                print("\nMuito Obrigado!!!\nVolte sempre! ")
                os.system("pause")
                menu_actions['main_menu']()
        else:
            matriz = dict.get('matriz')
            posBombas = dict.get('posBombas')
            jogadas = dict.get('jogadas')
            linhasMatriz = dict.get('linhasMatriz')
            colunasMatriz = dict.get('colunasMatriz')
            qtdJogadas = dict.get('qtdJogadas')
            perdeu = False
            mostrarMatriz(matriz, linhasMatriz)
            while (perdeu == False):
                print("\nJogadas: %d | Jogadas restantes: %d" % (jogadas, qtdJogadas))
                linha = int(input("\nDigite a linha >> ")) - 1
                coluna = int(input("Digite a coluna >> ")) - 1
                os.system("cls")
                if ([linha, coluna] in posBombas):
                    print("\n\n. . @ . . . . . . . . . . . . . . . . . . @ . .")
                    print(". . . . @ . . . . . . . . . . . . . . @ . . . .")
                    print(". . . . . . @ BOOM!!! Você perdeu @ . . . . . .")
                    print(". . . . @ . . . . . . . . . . . . . . @ . . . .")
                    print(". . @ . . . . . . . . . . . . . . . . . . @ . .\n\n")
                    historico = {"matriz": 0, "posBombas": 0, "jogadas": 0,"qtdJogadas":0, "linhasMatriz": 0, "colunasMatriz": 0,"without": "-1"}
                    save(historico)
                    waiter = ["GO"]
                    data = pickle.dumps(waiter)
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    destiny = (HOST, PORT)
                    sock.sendto(data, destiny)
                    os.system("pause")
                    os.system("cls")
                    menu_actions['main_menu']()
                else:
                    matriz[linha][coluna] = str(bombasAoRedor(linha, coluna, posBombas))
                    mostrarMatriz(matriz, linhasMatriz)
                    jogadas += 1
                    qtdJogadas -= 1
                    historico = {"matriz": matriz, "posBombas": posBombas, "jogadas": jogadas,"qtdJogadas":qtdJogadas, "linhasMatriz": linhasMatriz}
                    if (((linhasMatriz * colunasMatriz) - jogadas) == len(posBombas)):
                        print("\n\nPARABÉNS!!! Você ganhou o desafio.")
                        print("Congratulations!!! You won the challenge\n\n")
                        historico = {"matriz": 0, "posBombas": 0, "jogadas": 0, "linhasMatriz": 0, "colunasMatriz": 0,
                                     "without": "-1"}
                        save(historico)
                        waiter = ["WI"]
                        data = pickle.dumps(waiter)
                        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        destiny = (HOST, PORT)
                        sock.sendto(data, destiny)
                        os.system("cls")
                        os.system("pause")
                        menu_actions['main_menu']()
                    save(historico)
            return

# Back to main menu
def back():
    menu_actions['main_menu']()

# Exit program
def exit():
    os.system("cls")
    print("==================================================")
    print("                   CAMPO MINADO")
    print("==================================================\n")
    print("Obrigado pela sua presença!!\nVolte Sempre :)")

    waiter = ["EX"]
    data = pickle.dumps(waiter)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    destiny = (HOST, PORT)
    sock.sendto(data, destiny)

    sys.exit()

menu_actions = {
    'main_menu': main_menu,
    '1': newGame,
    '2': restartGame,
    '9': back,
    '0': exit,
}

#Menu_Principal
if __name__ == "__main__":
    main_menu()