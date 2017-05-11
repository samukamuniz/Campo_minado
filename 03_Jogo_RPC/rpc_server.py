from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
import sys, os
import random
from ast import literal_eval

def gerarMatriz(l,c):
    matriz = [["*" for x in range(l)] for y in range(c)] # l -> linhas ; c -> colunas
    return matriz

def sortearBombas(n,l,c):
    vetor = []
    for i in range(n): #número de bombas
        i = random.randint(0,l-1) # y -1
        n = random.randint(0,c-1) # x -1
        while ([i,n] in vetor):
            i = random.randint(0,l-1) # y -1
            n = random.randint(0,c-1) # x -1
        vetor.append([i,n])
    return vetor

def bombasAoRedor(l,c,posBombas):
    count = 0
    if ([l+1,c] in posBombas):
        count += 1
    if ([l-1,c] in posBombas):
        count += 1
    if ([l,c-1] in posBombas):
        count += 1
    if ([l-1,c-1] in posBombas):
        count += 1
    if ([l+1,c-1] in posBombas):
        count += 1
    if ([l-1,c+1] in posBombas):
        count += 1
    if ([l+1,c+1] in posBombas):
        count += 1
    if ([l,c+1] in posBombas):
        count += 1
    return count;

def save(historico):
    hist = open('log_game.txt', 'w')
    hist.write(str(historico))
    hist.close()

def verifyFile():
    arquivo = open('log_game.txt', 'r')
    waiter = str(arquivo.read())
    dados = literal_eval(waiter)
    arquivo.close()
    return dados

def server():
    serverRPC = SimpleJSONRPCServer(('localhost', 7002))
    print("Servidor Conectado")
    serverRPC.register_function(gerarMatriz)
    serverRPC.register_function(verifyFile)
    serverRPC.register_function(sortearBombas)
    serverRPC.register_function(bombasAoRedor)
    serverRPC.register_function(save)
    serverRPC.serve_forever()

server()