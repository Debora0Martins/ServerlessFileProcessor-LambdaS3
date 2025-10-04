# 🚀 ServerlessFileProcessor-LambdaS3

[![Python](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)
[![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-orange)](https://aws.amazon.com/lambda/)
[![S3](https://img.shields.io/badge/AWS-S3-yellow)](https://aws.amazon.com/s3/)
[![DynamoDB](https://img.shields.io/badge/AWS-DynamoDB-brightgreen)](https://aws.amazon.com/dynamodb/)
[![SNS](https://img.shields.io/badge/AWS-SNS-red)](https://aws.amazon.com/sns/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**Processamento serverless de arquivos com AWS Lambda, S3, DynamoDB e SNS.**  

O ServerlessFileProcessor-LambdaS3 é uma solução serverless que automatiza o processamento de dados de usuários armazenados no DynamoDB. Ele gera arquivos em múltiplos formatos (.txt, .csv e .json), armazena-os de forma segura no S3 e envia notificações em tempo real via SNS.

Projetado para ser escalável, eficiente e econômico, o projeto elimina tarefas manuais, integra-se facilmente com outros sistemas e permite acompanhar o processamento em tempo real, garantindo confiabilidade e agilidade no fluxo de dados.

---

## 🌟 Visão Geral do Projeto

O projeto lê dados de usuários de uma tabela DynamoDB, processa e gera arquivos TXT, CSV e JSON, salva-os no S3 e envia notificações via SNS.  

### 💡 Fluxo do Processo
![Fluxo Lambda-S3-DynamoDB](https://user-images.githubusercontent.com/SEU_USUARIO/fluxo_lambda.png)

**Descrição do fluxo:**
1. Lambda é acionada manual ou via evento.
2. Lê dados da tabela DynamoDB `usuarios`.
3. Trata registros (`nome`, `idade`, `codigo`).
4. Gera arquivos `.txt`, `.csv` e `.json`.
5. Salva os arquivos na pasta `processed/` do bucket S3.
6. Envia notificação via SNS confirmando o processamento.

---

## 📂 Estrutura do Projeto

ServerlessFileProcessor-LambdaS3/
│
├─ lambda/ # Código da Lambda
│ └─ lambda_function.py
├─ terraform/ # Infraestrutura como código
│ ├─ main.tf
│ ├─ variables.tf
│ └─ outputs.tf
├─ README.md
└─ LICENSE

yaml
Copiar código

---

## ⚙ Deploy Rápido

### 1. Configurar AWS CLI
```bash
aws configure
2. Criar Bucket S3
bash
Copiar código
aws s3 mb s3://serverless-file-processor-bucket
3. Criar Tabela DynamoDB
bash
Copiar código
aws dynamodb create-table \
    --table-name usuarios \
    --attribute-definitions AttributeName=12345,AttributeType=N \
    --key-schema AttributeName=12345,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST
4. Deploy Lambda
bash
Copiar código
zip lambda_function.zip lambda/lambda_function.py
aws lambda create-function \
    --function-name ProcessUsuarios \
    --runtime python3.11 \
    --role arn:aws:iam::<AWS_ACCOUNT_ID>:role/<LAMBDA_ROLE> \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://lambda_function.zip
🖼 Demonstração do Projeto
GIF mostrando o fluxo completo do Lambda processando os arquivos:

📝 Dependências
Python 3.11

boto3

csv

json

datetime

🔒 Permissões Necessárias
Lambda precisa de permissões para:

DynamoDB (leitura)

S3 (upload e leitura)

SNS (publicação)

📌 Observações
Para arquivos grandes, utilize Git LFS no GitHub.

É recomendável monitorar S3, DynamoDB e Lambda via CloudWatch para logs e métricas.

🏷 Licença
MIT License © 2025 Débora Martins



