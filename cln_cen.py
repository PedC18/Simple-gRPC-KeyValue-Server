import grpc
import Servicos_pb2
import Servicos_pb2_grpc
import sys

def run():
    id_servico = sys.argv[1]
    channel = grpc.insecure_channel(id_servico)
    stub = Servicos_pb2_grpc.ServidorCentralStub(channel)

    while True:
        try:
            comando = input("").split(',')
        except EOFError:
            break
        
        if comando[0] == 'C':
            chave = int(comando[1])
            pedido = Servicos_pb2.Pedido(chave=chave)
            respostaCen = stub.Mapeamento(pedido)
            if respostaCen.id_servico == "":
                pass
            else:
                channel = grpc.insecure_channel(respostaCen.id_servico)
                stubPar = Servicos_pb2_grpc.ChaveValorStub(channel)

                novo_pedido = Servicos_pb2.Pedido(chave=chave)
                respostaPar = stubPar.Consulta(novo_pedido)
                print(f"{respostaCen.id_servico}:{respostaPar.valor}")
        
        elif comando[0] == 'T':
            pedido = Servicos_pb2.Pedido()
            resposta = stub.Termino(pedido)
            print(f"{resposta.status}")
            break

if __name__ == '__main__':
    run()