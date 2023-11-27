import grpc
from concurrent import futures
import threading
import ChaveValor_pb2
import ChaveValor_pb2_grpc
import sys
import socket

class ChaveValorServicer(ChaveValor_pb2_grpc.ChaveValorServicer):
    def __init__(self,stop_event):
        self.data = {}
        self._stop_event = stop_event

    def Insercao(self, pedido,contexto):
        chave = pedido.chave
        valor = pedido.valor
        if chave not in self.data:
            self.data[chave] = valor
            return ChaveValor_pb2.RespostaInsercao(status=0)
        else:
            return ChaveValor_pb2.RespostaInsercao(status=-1)

    def Consulta(self, pedido, contexto):
        chave = pedido.chave
        if chave in self.data:
            return ChaveValor_pb2.RespostaConsulta(valor=self.data[chave])
        else:
            return ChaveValor_pb2.RespostaConsulta(valor="")

    def Ativacao(self, pedido,contexto):
        if(len(sys.argv)>2):
            id_servico_central = pedido.id_servico
            channel =  grpc.insecure_channel(id_servico_central)
            stub = ChaveValor_pb2_grpc.ServidorCentralStub(channel)

            id_servico_atual = socket.getfqdn() + ":" + sys.argv[1]
            ListaChaves = self.data.keys()

            pedido = ChaveValor_pb2.PedidoRegistro(id_servico=id_servico_atual, ListaChaves=ListaChaves)
            resposta = stub.Registro(pedido)

            return ChaveValor_pb2.RespostaAtivacao(status= resposta.numeroChaves)
        else:
            return ChaveValor_pb2.RespostaAtivacao(status=0)

    def Termino(self, pedido,contexto):
        self._stop_event.set()
        return ChaveValor_pb2.RespostaTermino(status=0)

def serve():
    stop_event = threading.Event()
    port = sys.argv[1]
    id_servico = "0.0.0.0:" + port
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ChaveValor_pb2_grpc.add_ChaveValorServicer_to_server(ChaveValorServicer(stop_event), server)
    server.add_insecure_port(id_servico)
    server.start()
    stop_event.wait()
    server.stop(1)

if __name__ == '__main__':
    serve()