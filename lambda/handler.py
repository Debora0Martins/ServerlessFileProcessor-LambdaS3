import boto3
import os

s3 = boto3.client('s3')

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        print(f"Processando arquivo {key} do bucket {bucket}")

        # Novo caminho
        new_key = f"processed/{key}"

        # Copiar arquivo para processed/
        s3.copy_object(Bucket=bucket, CopySource={'Bucket': bucket, 'Key': key}, Key=new_key)

        # Opcional: deletar arquivo original
        s3.delete_object(Bucket=bucket, Key=key)

        print(f"Arquivo movido para {new_key}")

