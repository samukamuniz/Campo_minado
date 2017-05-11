import sys
from rpc_server import server
from rpc_cliente import main_menu

print("Você quer executar:")
print("1 para servidor")
print("2 para cliente")
opcao = input("Opção:")

try:
    if int(opcao) == 1:
        print("Servidor ativado:\n")
        server()
    elif int(opcao) == 2:
        print("Cliente ativado:\n")
        main_menu()

except : # pega todas possíveis
    for val in sys.exc_info():
        print(val)

input()
