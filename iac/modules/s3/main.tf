# modules/s3/main.tf
resource "aws_s3_bucket" "this" {
  bucket        = "kb-example-bucket"
  force_destroy = true
}

