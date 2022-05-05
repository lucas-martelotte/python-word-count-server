import socket
import pickle
import os


#=================================================================#
#=========================== FUNÇÕES =============================#
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

#=================================================================#
#=========================== SERVIDOR ============================#
#=================================================================#

HOST = 'localhost'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(6)

print(f'Server started. Listening to connections on port {PORT}.')

connection, address = server.accept()
while True:
  filename = pickle.loads(connection.recv(1024))

  # Se a mensagem for none, vamos encerrar a conexão
  if filename is None:
      break

  # Se a mensagem não for uma string, vamos retornar uma lista vazia
  if type(filename) != str:
      connection.sendall(pickle.dumps([]))
      continue

  # Se o diretório do arquivo não existir, também vamos retornar uma lista vazia
  if not os.path.exists(filename + '.txt'):
      connection.sendall(pickle.dumps([]))
      continue

  # Caso nada tenha dado errado, vamos retonar as 5 palavras mais frequentes
  connection.sendall(pickle.dumps(get_top_five_words(filename)))

connection.close()

