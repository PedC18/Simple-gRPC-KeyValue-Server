import grpc
from concurrent import futures
import threading
import ChaveValor_pb2
import ChaveValor_pb2_grpc
import sys
import socket

class ServidorCentralServicer(ChaveValor_pb2_grpc.ServidorCentralServicer):
    def __init__(self,stop_event):
        self.data = {}
        self._stop_event = stop_event
    
    def Registro(self,pedido,contexto):
        id_servico = pedido.id_servico
        ListaChaves = pedido.ListaChaves
        for ch in ListaChaves:
            self.data[ch] = id_servico
        return ChaveValor_pb2.RespostaRegistro(numeroChaves = len(ListaChaves))
    
    def Mapeamento(self,pedido,contexto):
        chave = pedido.chave
        if chave in self.data:
            id_servico = self.data[chave]
            return ChaveValor_pb2.RespostaMap(id_servico=id_servico)
        else:
            return ChaveValor_pb2.RespostaMap(id_servico="")
            
        
    def Termino(self, pedido,contexto):
        self._stop_event.set()
        return ChaveValor_pb2.RespostaTermino(status=len(self.data))


def serve():
    stop_event = threading.Event()
    port = sys.argv[1]
    id_servico = "0.0.0.0:" + port
    serverCentral = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ChaveValor_pb2_grpc.add_ServidorCentralServicer_to_server(ServidorCentralServicer(stop_event), serverCentral)
    serverCentral.add_insecure_port(id_servico)
    serverCentral.start()
    stop_event.wait()
    serverCentral.stop(1)


if __name__ == '__main__':
    serve()