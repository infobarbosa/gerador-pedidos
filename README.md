# Empacotando e Instalando a Função Lambda na AWS

Este guia irá orientá-lo sobre como empacotar sua função Lambda com suas dependências e como implantá-la na AWS.

### Pré-requisitos
- AWS CLI instalada e configurada com suas credenciais da AWS.
- Python e pip instalados.
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
aws lambda create-function --function-name gerador-pedidos-lambda --zip-file fileb://function.zip --handler lambda_function.lambda_handler --runtime python3.8 --role arn:aws:iam::123456789012:role/LabRole
```
2. Se você já tem uma função Lambda e quer atualizá-la com um novo código, use o comando aws lambda update-function-code:
```
aws lambda update-function-code --function-name my-function --zip-file fileb://function.zip
```

Agora, sua função Lambda está pronta para ser usada na AWS.