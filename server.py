import socket
import threading

# Configurações do servidor
host = ''
port = 80

# Dicionário para rastrear conexões de clientes
clientes = {}

# Função para lidar com as mensagens de um cliente
def handle_cliente(cliente, nome):
    while True:
        try:
            mensagem = cliente.recv(1024).decode()
            if not mensagem:
                break
            #print(f"({nome}): {mensagem}")
            
            # Encaminha a mensagem para todos os outros clientes
            for cliente_destino, conexao in clientes.items():
                if cliente_destino != nome:
                    conexao.send(f"({nome}): {mensagem}".encode())
        except:
            # Lidar com erros de conexão
            break

# Configuração do servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

print("Servidor está esperando conexões...")

# Loop para aceitar clientes
while True:
    cliente, endereco = server.accept()
    nome_cliente = cliente.recv(1024).decode()
    print(f"Cliente conectado: {nome_cliente} ({endereco})")
    clientes[nome_cliente] = cliente

    # Inicia uma thread para lidar com as mensagens do cliente
    cliente_thread = threading.Thread(target=handle_cliente, args=(cliente, nome_cliente))
    cliente_thread.start()
