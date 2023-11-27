import grpc
import ChaveValor_pb2
import ChaveValor_pb2_grpc
import socket
import sys

def run():
    id_servico = sys.argv[1]
    channel = grpc.insecure_channel(id_servico)
    stub = ChaveValor_pb2_grpc.ChaveValorStub(channel)

    while True:
        try:
            comando = input("").split(',')
        except EOFError:
            break

        if comando[0] == 'I':
            chave = int(comando[1])
            valor = ','.join(comando[2:])
            pedido = ChaveValor_pb2.Pedido(chave=chave, valor=valor)
            resposta = stub.Insercao(pedido)
            print(f"{resposta.status}")

        elif comando[0] == 'C':
            chave = int(comando[1])
            pedido = ChaveValor_pb2.Pedido(chave=chave)
            resposta = stub.Consulta(pedido)
            print(f"{resposta.valor}")

        elif comando[0] == 'A':
            id_servico = str(comando[1])
            pedido = ChaveValor_pb2.Pedido(id_servico=id_servico)
            resposta = stub.Ativacao(pedido)
            print(f"{resposta.status}")
            pass

        elif comando[0] == 'T':
            pedido = ChaveValor_pb2.Pedido()
            resposta = stub.Termino(pedido)
            print(f"{resposta.status}")
            break


if __name__ == '__main__':
    run()

