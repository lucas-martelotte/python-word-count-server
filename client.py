import socket
import pickle

HOST = "localhost"
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

while True:
    print('Digite o nome do arquivo (não digite nada para sair):')
    filename = str(input())
    if filename == '':
        exit()
    else:
        client.sendall(pickle.dumps(filename))
        data = pickle.loads(client.recv(1024))
        if data == []:
            print('Entrada invalida. Tente Novamente.')
        else:
            print(f'As palavras mais frequentes do arquivo \"{filename}.txt\" são {data}')