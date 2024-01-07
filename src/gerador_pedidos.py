import argparse
import random
import json
import boto3
import sys
import time
import uuid
from datetime import datetime, timedelta
from faker import Faker

fake = Faker(locale='pt_BR')

class PedidoDeCompra:
    def __init__(self, produto, valor_unitario, quantidade, data_criacao, uf, id_cliente):
        self.id_pedido = str(uuid.uuid4()) 
        self.produto = produto
        self.valor_unitario = valor_unitario
        self.quantidade = quantidade
        self.data_criacao = data_criacao.isoformat()
        self.uf = uf
        self.id_cliente = id_cliente

    def to_dict(self):
        return self.__dict__

produtos = {
    "TV": 2500,
    "GELADEIRA": 2000,
    "HOMETHEATER": 500,
    "COMPUTADOR": 700,
    "MONITOR": 600,
    "TABLET": 1100,
    "SOUNDBAR": 900,
    "CELULAR": 1000,
    "NOTEBOOK": 1500
}

def gerar_pedido_aleatorio(data=None):
    if data is None:
        data = datetime.datetime.now()
    produto, valor_unitario = random.choice(list(produtos.items()))
    quantidade = random.randint(1, 3)
    data_criacao = data.replace(hour=random.randint(0, 23), minute=random.randint(0, 59), second=random.randint(0, 59))
    uf = fake.state_abbr()
    id_cliente = random.randint(1, 14000)
    return PedidoDeCompra(produto, valor_unitario, quantidade, data_criacao, uf, id_cliente)

def gerar_pedidos_por_dia(inicio, fim, quantidade_por_dia):
    data_inicio = datetime.strptime(inicio, "%d/%m/%Y")
    data_fim = datetime.strptime(fim, "%d/%m/%Y")

    data_atual = data_inicio
    while data_atual <= data_fim:
        data_atual_str = data_atual.strftime("%Y-%m-%d")
        arquivo = open("pedidos-" + data_atual_str + ".txt", "w")  
        for _ in range(quantidade_por_dia):
            pedido = gerar_pedido_aleatorio(data_atual)
            arquivo.write(json.dumps(pedido.to_dict()) + "\n")  
        arquivo.close()  # fecha o arquivo

        data_atual += timedelta(days=1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--destino", default="arquivo", help="Destino dos pedidos gerados")
    parser.add_argument("--quantidade", default=200, help="Quantidade de pedidos gerados")
    parser.add_argument("--inicio", default="01/01/2024", help="Data de início dos pedidos gerados")
    parser.add_argument("--fim", default="31/01/2024", help="Data de fim dos pedidos gerados")
    args = parser.parse_args()

    print("Destino dos dados:", args.destino)
    print("Quantidade de pedidos:", args.quantidade)
    print("Data de início:", args.inicio)
    print("Data de fim:", args.fim)

    destino = args.destino.lower()
    quantidade = int(args.quantidade)
    data_inicio = args.inicio
    data_fim = args.fim

    if destino == "arquivo":
        gerar_pedidos_por_dia(data_inicio, data_fim, quantidade)
    elif destino == "kinesis":
        kinesis = boto3.client('kinesis')  
        stream_name = 'pedidos'  

        for _ in range(quantidade): 
            pedido = gerar_pedido_aleatorio()
            kinesis.put_record(
                StreamName=stream_name,
                Data=json.dumps(pedido.to_dict()),
                PartitionKey=str(pedido.id_pedido)
            )
            time.sleep(0.1)  # pausa por 1 segundo
    else:
        print("Destino inválido")
        sys.exit(1)

if __name__ == '__main__':
    main()