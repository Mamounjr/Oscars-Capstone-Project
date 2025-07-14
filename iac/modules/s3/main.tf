# modules/s3/main.tf
resource "aws_s3_bucket" "this" {
  bucket        = "oscar-project-bucket"
  force_destroy = true
}
