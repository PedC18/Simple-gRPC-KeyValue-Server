import grpc
from concurrent import futures
import threading
import Servicos_pb2
import Servicos_pb2_grpc
import sys

class ServidorCentralServicer(Servicos_pb2_grpc.ServidorCentralServicer):
    def __init__(self,stop_event):
        self.data = {}
        self._stop_event = stop_event
    
    def Registro(self,pedido,contexto):
        id_servico = pedido.id_servico
        ListaChaves = pedido.ListaChaves
        for ch in ListaChaves:
            self.data[ch] = id_servico
        return Servicos_pb2.RespostaRegistro(numeroChaves = len(ListaChaves))
    
    def Mapeamento(self,pedido,contexto):
        chave = pedido.chave
        if chave in self.data:
            id_servico = self.data[chave]
            return Servicos_pb2.RespostaMap(id_servico=id_servico)
        else:
            return Servicos_pb2.RespostaMap(id_servico="")
            
        
    def Termino(self, pedido,contexto):
        self._stop_event.set()
        return Servicos_pb2.RespostaTermino(status=len(self.data))


def serve():
    stop_event = threading.Event()
    port = sys.argv[1]
    id_servico = "0.0.0.0:" + port
    serverCentral = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Servicos_pb2_grpc.add_ServidorCentralServicer_to_server(ServidorCentralServicer(stop_event), serverCentral)
    serverCentral.add_insecure_port(id_servico)
    serverCentral.start()
    stop_event.wait()
    serverCentral.stop(1)


if __name__ == '__main__':
    serve()