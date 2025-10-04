provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "file_bucket" {
  bucket = "serverless-file-processor-bucket"
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda-s3-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_lambda_function" "file_processor" {
  function_name = "ServerlessFileProcessor"
  runtime       = "python3.11"
  role          = aws_iam_role.lambda_role.arn
  handler       = "handler.lambda_handler"
  filename      = "../lambda/lambda.zip"
}

resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.file_processor.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.file_bucket.arn
}

# Delay para garantir que a função Lambda esteja pronta
resource "null_resource" "wait_lambda" {
  depends_on = [aws_lambda_function.file_processor]

  provisioner "local-exec" {
    command = "sleep 10"
  }
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.file_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.file_processor.arn
    events              = ["s3:ObjectCreated:*"]
  }

  depends_on = [
    aws_lambda_permission.allow_s3,
    null_resource.wait_lambda
  ]
}

