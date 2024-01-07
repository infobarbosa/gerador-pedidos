import random
import datetime
import json
import boto3
import time
import uuid
from faker import Faker

fake = Faker()

class PedidoDeCompra:
    def __init__(self, produto, valor_unitario, quantidade, data_criacao, pais, id_cliente):
        self.id_pedido = str(uuid.uuid4())  # adiciona um identificador único a cada pedido
        self.produto = produto
        self.valor_unitario = valor_unitario
        self.quantidade = quantidade
        self.data_criacao = data_criacao.isoformat()
        self.pais = pais
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

paises = ["BR", "US", "AR"]

def gerar_pedido_aleatorio():
    produto, valor_unitario = random.choice(list(produtos.items()))
    quantidade = random.randint(1, 3)
    data_criacao = datetime.datetime.now().replace(hour=random.randint(0, 23), minute=random.randint(0, 59), second=random.randint(0, 59))
    pais = random.choice(paises)
    id_cliente = fake.unique.random_number(digits=5)
    return PedidoDeCompra(produto, valor_unitario, quantidade, data_criacao, pais, id_cliente)

def main():
    kinesis = boto3.client('kinesis')  
    stream_name = 'pedidos'  

    while True:  # loop infinito
        pedidos = [gerar_pedido_aleatorio() for _ in range(50)]  # gera 50 pedidos
        for pedido in pedidos:
            kinesis.put_record(
                StreamName=stream_name,
                Data=json.dumps(pedido.to_dict()),
                PartitionKey=str(pedido.id_pedido)
            )
        time.sleep(1)  # pausa por 1 segundo

if __name__ == '__main__':
    main()  # chamada da função principal
        