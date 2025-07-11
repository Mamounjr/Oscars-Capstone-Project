# modules/loadbalancer/variables.tf
variable "public_subnets" {
  type = list(string)
}

variable "vpc_id" {
  type = string
}

variable "public_sg_id" {
  type = string
}