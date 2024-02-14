- Criado por: Prof. Marcelo Barbosa
- Criado em: Janeiro/2024
- Github: https://github.com/infobarbosa
- Linkedin: https://www.linkedin.com/in/infobarbosa/

### Pré-requisitos
- Os comandos a seguir presumem um ambiente e terminal ativos do AWS Cloud9 com Python 3.8+ e pip instalados.

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
1. Obtendo o ARN da role:
> Atenção! Substitua `LabRole` pelo nome da role que você tem disponível na sua conta.
```
export LAB_ROLE=$(aws iam get-role --role-name LabRole | jq '.Role.Arn' -r)
```

```
echo $LAB_ROLE
```

2. Crie uma nova função Lambda com o comando `aws lambda create-function`:
```
aws lambda create-function \
    --function-name gerador-pedidos \
    --zip-file fileb://function.zip \
    --handler lambda_function.lambda_handler \
    --runtime python3.12 \
    --role $LAB_ROLE \
    --timeout 900
```

3. Se você já tem uma função Lambda e quer atualizá-la com um novo código, use o comando aws lambda update-function-code:
```
aws lambda update-function-code --function-name gerador-pedidos --zip-file fileb://function.zip
```

Agora, sua função Lambda está pronta para ser usada na AWS.

### Invocando a função lambda
```
aws lambda invoke --function-name gerador-pedidos out.json
```
