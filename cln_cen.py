import grpc
import ChaveValor_pb2
import ChaveValor_pb2_grpc
import sys

def run():
    id_servico = sys.argv[1]
    channel = grpc.insecure_channel(id_servico)
    stub = ChaveValor_pb2_grpc.ServidorCentralStub(channel)

    while True:
        try:
            comando = input("").split(',')
        except EOFError:
            break
        
        if comando[0] == 'C':
           chave = int(comando[1])
           pedido = ChaveValor_pb2.Pedido(chave=chave)
           resposta = stub.Mapeamento(pedido)
           print(f"{resposta.id_servico}")
        
        elif comando[0] == 'T':
            pedido = ChaveValor_pb2.Pedido()
            resposta = stub.Termino(pedido)
            print(f"{resposta.status}")
            break

if __name__ == '__main__':
    run()