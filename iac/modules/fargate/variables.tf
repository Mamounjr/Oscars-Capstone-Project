variable "aws_region" {
  default = "us-east-1"
}

variable "docker_image_url" {
  description = "Docker image URI (ECR)"
}

variable "subnet_ids" {
  type = list(string)
}

variable "security_group_id" {
  type = string
}
