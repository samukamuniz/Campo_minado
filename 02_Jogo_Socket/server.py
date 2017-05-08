import socket, pickle
import sys, os, os.path
import threading, random
from ast import literal_eval

HOST = ''
PORT = 5000
ENCODE = "UTF-8"
MAX_BYTES = 65535

def thread_object():
    source = (HOST, PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(source)
    while True:
        #Recebimento de dados
        data, address = sock.recvfrom(MAX_BYTES)

        #Criando Thread com orientação a objeto
        tratador = ThreadTratador(sock, data, address)
        tratador.start()

def thread_procedure():
    source = (HOST, PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(source)
    while True:
        #Recebimento de dados
        data, address = sock.recvfrom(MAX_BYTES)
        t = threading.Thread(target=connection, args=tuple([sock, data, address]))
        t.start()

def connection(sock, data, address):
    text = pickle.loads(data)
    cod, *dados = text

    if cod == "GM":
        gerarMatriz(sock, dados, address)
    elif cod == "SB":
        sortearBombas(sock, dados, address)
    elif cod == "BR":
        bombasAoRedor(sock, dados, address)
    elif cod == "SV":
        save(dados,address)
    elif cod == "JS":
        openGame(sock, address)
    elif cod == "VF":
        verifyFile(sock, address)
    elif cod == "EX":
        exit(sock, address)
    elif cod == "GO":
        gameOver(sock, address)
    elif cod == "WI":
        win(sock, address)

def gerarMatriz(sock, dados, address):
    linhasMatriz, colunasMatriz, _ = dados
    matriz = [["*" for x in range(linhasMatriz)] for y in range(colunasMatriz)]
    print("Cliente: ", address, "Gerou a matriz do jogo")
    data = pickle.dumps(matriz)
    sock.sendto(data, address)

def sortearBombas(sock, dados, address):#n, l, c
    linhasMatriz, colunasMatriz, quantidadeBombas, matriz = dados
    vetor = []
    for i in range(quantidadeBombas):  # número de bombas
        i = random.randint(0, linhasMatriz - 1)  # y -1
        n = random.randint(0, colunasMatriz - 1)  # x -1
        while ([i, n] in vetor):
            i = random.randint(0, linhasMatriz - 1)  # y -1
            n = random.randint(0, colunasMatriz - 1)  # x -1
        vetor.append([i, n])
    print("Cliente: ", address, "Realizou o sorteio das bombas")
    data = pickle.dumps(vetor)
    sock.sendto(data, address)

def bombasAoRedor(sock, dados, address):
    linha, coluna, posBombas = dados
    count = 0
    if ([linha + 1, coluna] in posBombas):
        count += 1
    if ([linha - 1, coluna] in posBombas):
        count += 1
    if ([linha, coluna - 1] in posBombas):
        count += 1
    if ([linha - 1, coluna - 1] in posBombas):
        count += 1
    if ([linha + 1, coluna - 1] in posBombas):
        count += 1
    if ([linha - 1, coluna + 1] in posBombas):
        count += 1
    if ([linha + 1, coluna + 1] in posBombas):
        count += 1
    if ([linha, coluna + 1] in posBombas):
        count += 1
    print("Cliente: ", address, "Realizou uma jogada")
    print("Cliente: ", address, "Realizou a verificação das bombas aos redores")
    data = pickle.dumps(count)
    sock.sendto(data, address)

def save(dados,address):
    historico = dados
    hist = open('log_game.txt', 'w')
    hist.write(str(historico))
    print("Cliente: ", address, "Salvou o jogo")
    hist.close()

def openGame(sock, address):
    arquivo = open("log_game.txt", 'r')
    dados = literal_eval(arquivo.read())
    dict = dados[0]
    arquivo.close()
    data = pickle.dumps(dict)
    sock.sendto(data, address)
    print("Cliente: ", address, "Reiniciou um jogo em andamento")

def gameOver(sock, address):
    print("Cliente: ", address, "Acertou uma mina! Game Over! ")

def win(sock, address):
    print("Cliente: ", address, "Ganhou o jogo")

def exit(sock, address):
    print("Cliente: ", address, "Encerrou o jogo")


def verifyFile(sock, address):
    arquivo = open("log_game.txt", 'r')
    dados = literal_eval(arquivo.read())
    dict = dados[0]
    arquivo.close()
    data = pickle.dumps(dict)
    sock.sendto(data, address)
    print("Cliente: ", address, "Verificou se há algum jogo salvo")

class ThreadTratador(threading.Thread):
    def __init__(self, a, b, c):
        threading.Thread.__init__(self)
        self.sock = a
        self.data = b
        self.address = c

    def run(self):
        tratar_conexao(self.sock, self.data, self.address)

if __name__ == "__main__":
    thread_procedure()