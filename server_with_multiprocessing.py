import socket
import select
import sys
import multiprocessing
import pickle
import os

HOST        = 'localhost'
PORT        = 5000
inputs      = [] # List of I/O
connections = {} # A dictionary {socket : address} to hold connection information
client_threads = [] # List to hold all the created threads

#=================================================================#
#========================== FUNCTIONS ============================#
#=================================================================#

def get_top_five_words(filename):

    # Criando um dicionario {palavra : quantidade}
    # Onde a chave é uma palavra do texto e o valor é a quantidade
    # de vezes que ela aparece no texto
    word_to_count = {}

    with open(filename + '.txt', encoding='utf8') as f:
        for line in f.readlines():
            for word in line.split(' '):
                if word in word_to_count:
                    word_to_count[word] += 1
                else:
                    word_to_count[word] = 1

    # Pegando as 5 palavras mais frequentes
    top_five_words = []

    for i in range(min(5, len(word_to_count))):
        top_word = None
        top_count = 0

        for word, count in word_to_count.items():
            if count > top_count:
                top_count = count
                top_word = word

        top_five_words.append(top_word)
        del word_to_count[top_word]

    return top_five_words

#======================================#
#========== THREADED CLIENT ===========#
#======================================#

def listen_to_client(client, address):
    '''
    Receives data from the client and returns the corresponding outputs
    Entrada: the client's socket and address
    Saida:
    '''

    while True:
        filename = pickle.loads(client.recv(1024))

        # Se a mensagem for none, vamos encerrar a conexão
        if filename is None:
            break

        # Se a mensagem não for uma string, vamos retornar uma lista vazia
        if type(filename) != str:
            client.sendall(pickle.dumps([]))
            continue

        # Se o diretório do arquivo não existir, também vamos retornar uma lista vazia
        if not os.path.exists(filename + '.txt'):
            client.sendall(pickle.dumps([]))
            continue

        # Caso nada tenha dado errado, vamos retonar as 5 palavras mais frequentes
        client.sendall(pickle.dumps(get_top_five_words(filename)))


#======================================#
#============ SERVER LOOP =============#
#======================================#

if __name__=='__main__':

    # Starting the server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(6)
    server.setblocking(False) # Non-blocking mode
    inputs.append(server) # Adding the server to the I/O list
    print(f'Server started. Listening to connections on port {PORT}.')

    while True:
        # espera por qualquer entrada de interesse
        reading, writing, exception = select.select(inputs, [], [])

        for ready in reading:
            # In this case, it is a new connection to the server
            if ready == server:

                client, address = server.accept()
                connections[client] = address
                print (f'Connected to client {client} with address {address}.')

                # Creating a new thread to handle requests from that client
                client_thread = multiprocessing.Process(target=listen_to_client, args=(client,address))
                client_thread.start()
                client_threads.append(client_thread)