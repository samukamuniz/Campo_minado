from jsonrpclib import Server
import sys, os
import random
from ast import literal_eval
import pickle
'''
def client():
    proxy = Server('http://localhost:7002')
    print(proxy.printName("André", "Bessa"))
'''

def mostrarMatriz(matriz,l):
    print("")
    for i in range(l):
        print(matriz[i])

####################################################################
def layout():
    print("==================================================")
    print("                   CAMPO MINADO")
    print("==================================================\n")
    print("Seja bem vindo(a) ao jogo Campo minado!!!")
    print("Escolha um opção e divirta-se \n")
    print("1. Iniciar um novo jogo")
    print("0. Sair")

def gameOver():
    print("\n\n. . @ . . . . . . . . . . . . . . . . . . @ . .")
    print(". . . . @ . . . . . . . . . . . . . . @ . . . .")
    print(". . . . . . @ BOOM!!! Você perdeu @ . . . . . .")
    print(". . . . @ . . . . . . . . . . . . . . @ . . . .")
    print(". . @ . . . . . . . . . . . . . . . . . . @ . .\n\n")

def win():
    print("\n\nPARABÉNS!!! Você ganhou o desafio.")
    print("Congratulations!!! You won the challenge\n\n")

def restart():
    os.system("cls")
    print("==================================================")
    print("                   CAMPO MINADO")
    print("==================================================\n")
    print("Seja bem vindo(a) ao jogo Campo minado!!!")
    print("\nVocê possui um jogo em andamento!!!Deseja continuar?\n1: Para Sim\n2: Para Não\n")

########################################################################

# ============================
#       MENUS FUNCTIONS
# ============================
# Main menu

proxy = Server('http://localhost:7002')

def main_menu():
    print("Passei")
    if os.path.exists("log_game.txt") == True:
        dict = literal_eval(str(proxy.verifyFile()))
        #dict = waiter[0]
        print("Passei")
        if (dict.get('without') == "-1"):
            layout()
            choice = input(" >> ")
            exec_menu(choice)
            return
        else:
            #restartGame()
            print("Restart Game")
    else:
        layout()
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

#New Game
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
    matriz = proxy.gerarMatriz(linhasMatriz, colunasMatriz)
    mostrarMatriz(matriz, linhasMatriz)
    posBombas = proxy.sortearBombas(quantidadeBombas, linhasMatriz, colunasMatriz)
    qtdJogadas = ((linhasMatriz * colunasMatriz) - len(posBombas))

#Restart Game



#######################################################
# Back to main menu
def back():
    menu_actions['main_menu']()

# Exit program
def exit():
    print("\nMuito Obrigado!!!\nVolte sempre! ")
    os.system("pause")
    sys.exit()

menu_actions = {
    'main_menu': main_menu,
    '1': newGame,
    #'2': restartGame,
    '9': back,
    '0': exit,
}

# Main program
if __name__ == "__main__":
    # Launch main menu
    main_menu()