Criado por: Prof. Marcelo Barbosa
Criado em: Janeiro/2024
Github: https://github.com/infobarbosa
Linkedin: https://www.linkedin.com/in/infobarbosa/

### Pré-requisitos
- Os comandos a seguir presumem um ambiente e terminal ativos do AWS Cloud9.
- Python e pip instalados.

# 01. Criando a stream `pedidos`
```
aws kinesis create-stream --stream-name pedidos --shard-count 1
```

# 02. Clonando o projeto

1. No console, faça o clone do projeto com o comando a seguir:
```
git clone https://github.com/infobarbosa/gerador-pedidos.git
```

2. Navegue para o diretório `gerador-pedidos`:
```
cd gerador-pedidos/ 
```

# 03. Empacotando e instalando a função lambda na AWS

Este guia irá orientá-lo sobre como empacotar sua função Lambda com suas dependências e como implantá-la na AWS.

### Empacotando a Função Lambda
1. Navegue até a raiz do projeto no terminal.

2. Instale todas as dependências do projeto em um diretório chamado `package`:
```
pip install -r requirements.txt -t ./package
```

3. Copie o código da função Lambda para o diretório package:
```
cp src/lambda_function.py ./package/
```

4. Empacote o código e as dependências em um arquivo ZIP:
```
cd package
zip -r ../function.zip .
cd ..
```

### Instalando a Função Lambda na AWS
1. Crie uma nova função Lambda com o comando `aws lambda create-function`. Substitua `my-function`, `main.lambda_handler`, `python3.8`, e `arn:aws:iam::123456789012:role/my-role` pelos valores apropriados para o seu caso:
```
aws lambda create-function --function-name gerador-pedidos --zip-file fileb://function.zip --handler lambda_function.lambda_handler --runtime python3.8 --role arn:aws:iam::123456789012:role/LabRole
```
2. Se você já tem uma função Lambda e quer atualizá-la com um novo código, use o comando aws lambda update-function-code:
```
aws lambda update-function-code --function-name my-function --zip-file fileb://function.zip
```

Agora, sua função Lambda está pronta para ser usada na AWS.

# 04. Lendo os dados da stream `pedidos`

1. No console instale os pacotes `boto3` e `faker`
```
pip install boto3 faker
```

2. 