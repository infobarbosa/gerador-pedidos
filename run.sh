# Criado por: Prof. Marcelo Barbosa
# Criado em: Janeiro/2024
# Github: https://github.com/infobarbosa
# Linkedin: https://www.linkedin.com/in/infobarbosa/

echo "Instalando pacotes"
sudo apt install -y python3-pip
pip3 install boto3 faker

echo "01. Criando a stream pedidos"
aws kinesis create-stream --stream-name pedidos --shard-count 1


echo "02. Empacotando a Função Lambda"
rm -rf package
mkdir -p package
pip install -r requirements.txt -t ./package

echo "03. Copiando o código da função Lambda para o diretório package"
cp src/lambda_function.py ./package/

echo "04. Empacotando o código e as dependências em um arquivo ZIP"
zip -r ./function.zip ./package/*	

echo "05. Obtendo o ARN da role"
export LAB_ROLE=$(aws iam get-role --role-name LabRole | jq '.Role.Arn' -r)
echo "ARN da role: " $LAB_ROLE

echo "06. Instalando a Função Lambda na AWS"
aws lambda create-function \
    --function-name gerador-pedidos \
    --zip-file fileb://function.zip \
    --handler lambda_function.lambda_handler \
    --runtime python3.12 \
    --role $LAB_ROLE \
    --timeout 900

echo "07. Invocando a função Lambda"
aws lambda invoke --function-name gerador-pedidos out.json

echo "Lambda invocada com sucesso!"