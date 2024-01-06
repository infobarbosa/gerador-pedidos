import unittest
from unittest.mock import patch
from src.main import PedidoDeCompra, gerar_pedido_aleatorio

class TestPedidoDeCompra(unittest.TestCase):
    def test_init(self):
        pedido = PedidoDeCompra("TV", 2500, 1, "2022-01-01T00:00:00", "BR", 12345)
        self.assertEqual(pedido.produto, "TV")
        self.assertEqual(pedido.valor_unitario, 2500)
        self.assertEqual(pedido.quantidade, 1)
        self.assertEqual(pedido.data_criacao, "2022-01-01T00:00:00")
        self.assertEqual(pedido.pais, "BR")
        self.assertEqual(pedido.id_cliente, 12345)

    def test_to_dict(self):
        pedido = PedidoDeCompra("TV", 2500, 1, "2022-01-01T00:00:00", "BR", 12345)
        self.assertEqual(pedido.to_dict(), {
            "produto": "TV",
            "valor_unitario": 2500,
            "quantidade": 1,
            "data_criacao": "2022-01-01T00:00:00",
            "pais": "BR",
            "id_cliente": 12345
        })

class TestGerarPedidoAleatorio(unittest.TestCase):
    @patch('src.main.random.choice')
    @patch('src.main.random.randint')
    @patch('src.main.Faker')
    def test_gerar_pedido_aleatorio(self, mock_faker, mock_randint, mock_choice):
        mock_choice.side_effect = [("TV", 2500), "BR"]
        mock_randint.return_value = 1
        mock_faker.unique.random_number.return_value = 12345
        pedido = gerar_pedido_aleatorio()
        self.assertIsInstance(pedido, PedidoDeCompra)

class TestLambdaHandler(unittest.TestCase):
    @patch('src.main.boto3.client')
    @patch('src.main.gerar_pedido_aleatorio')
    @patch('src.main.time.sleep')
    def test_lambda_handler(self, mock_sleep, mock_gerar_pedido_aleatorio, mock_boto3_client):
        # Cria um mock para o objeto Kinesis
        mock_kinesis = mock_boto3_client.return_value

        # Configura gerar_pedido_aleatorio para retornar um pedido específico
        mock_pedido = PedidoDeCompra("TV", 2500, 1, "2022-01-01T00:00:00", "BR", 12345, "1")
        mock_gerar_pedido_aleatorio.return_value = mock_pedido

        # Chama a função lambda_handler
        lambda_handler(None, None)

        # Verifica se boto3.client foi chamado com os parâmetros corretos
        mock_boto3_client.assert_called_once_with('kinesis', region_name='us-east-1')

        # Verifica se kinesis.put_record foi chamado com os parâmetros corretos
        mock_kinesis.put_record.assert_called_with(
            StreamName='your-stream-name',
            Data=json.dumps(mock_pedido.to_dict()),
            PartitionKey=str(mock_pedido.id_pedido)
        )

        # Verifica se time.sleep foi chamado com o parâmetro correto
        mock_sleep.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()