import boto3
import json

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Ignorar arquivos já processados
    if key.startswith("processed_"):
        print(f"Ignorando arquivo {key} porque já foi processado")
        return {
            'statusCode': 200,
            'body': json.dumps(f"Ignorado: {key}")
        }

    print(f"Processando arquivo {key} do bucket {bucket}")

    # Verifica se o arquivo existe
    try:
        s3.head_object(Bucket=bucket, Key=key)
    except s3.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            print(f"Arquivo {key} não encontrado. Abortando.")
            return {
                'statusCode': 404,
                'body': json.dumps(f"Arquivo {key} não encontrado")
            }
        else:
            raise

    copy_source = {'Bucket': bucket, 'Key': key}
    new_key = f"processed/{key}"
    print(f"CopySource: {copy_source}, NewKey: {new_key}")

    s3.copy_object(CopySource=copy_source, Bucket=bucket, Key=new_key)

    return {
        'statusCode': 200,
        'body': json.dumps(f"Arquivo processado: {new_key}")
    }

