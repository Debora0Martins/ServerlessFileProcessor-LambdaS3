import json
import csv
import boto3
from datetime import datetime

# Configurações
TABLE_NAME = 'usuarios'
BUCKET_NAME = 'serverless-file-processor-bucket'
TOPIC_ARN = 'arn:aws:sns:REGIAO:ID_DO_BANCO:TopicoNotificacao'

# Inicializa serviços AWS
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
sns = boto3.client('sns')

# Função para tratar dados
def tratar_dados(items):
    dados_tratados = []
    for item in items:
        nome = item.get('nome') or "N/A"
        idade = item.get('idade') or "N/A"
        codigo = item.get('12345') or "N/A"
        dados_tratados.append({
            "codigo": codigo,
            "nome": nome,
            "idade": idade
        })
    return dados_tratados

# Função para gerar arquivos no S3
def gerar_arquivos(dados):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # TXT
    txt_output = "\n".join([f"{d['codigo']} - {d['nome']} - {d['idade']}" for d in dados])
    s3.put_object(Bucket=BUCKET_NAME, Key=f"processed/processed_{timestamp}.txt", Body=txt_output.encode("utf-8"))

    # CSV
    csv_file = "/tmp/arquivo_tratado.csv"
    with open(csv_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["codigo", "nome", "idade"])
        writer.writeheader()
        writer.writerows(dados)
    with open(csv_file, "rb") as f:
        s3.put_object(Bucket=BUCKET_NAME, Key=f"pro

