# modules/s3/variables.tf
# No input variables needed for this module

# modules/s3/outputs.tf
output "bucket_name" {
  value = aws_s3_bucket.this.bucket
}
