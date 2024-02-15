# Criado por: Prof. Marcelo Barbosa
# Criado em: Janeiro/2024
# Github: https://github.com/infobarbosa
# Linkedin: https://www.linkedin.com/in/infobarbosa/

echo "01. Instalando pacotes"
sudo apt install -y python3-pip
pip3 install boto3 faker

echo "02. Organizando as dependências da Função Lambda"
rm -rf package
mkdir -p package
pip install -r requirements.txt -t ./package

echo "03. Copiando o código da função Lambda para o diretório package"
cp src/lambda_function.py ./package/

echo "04. Empacotando o código e as dependências em um arquivo ZIP"
zip -r ./function.zip ./package/*	

echo "Lambda empacotada com sucesso!"