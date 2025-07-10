provider "aws" {
  region = "us-east-1"  # or any region you want
}


module "network" {
  source = "./modules/network"
}

module "iam" {
  source = "./modules/iam"
}

module "autoscaling" {
  source = "./modules/autoscaling"
  public_subnet_ids  = module.network.public_subnet_ids
  private_subnet_ids = module.network.private_subnet_ids
  public_sg_id       = module.network.public_sg_id
  private_sg_id      = module.network.private_sg_id
  ec2_profile_name   = module.iam.ec2_profile_name
}

module "loadbalancer" {
  source         = "./modules/loadbalancer"
  public_subnets = module.network.public_subnet_ids
  vpc_id         = module.network.vpc_id
  public_sg_id   = module.network.public_sg_id
}

module "s3" {
  source = "./modules/s3"
}

output "vpc_id" {
  value = module.network.vpc_id
}

output "public_subnet_ids" {
  value = module.network.public_subnet_ids
}

output "private_subnet_ids" {
  value = module.network.private_subnet_ids
}

output "s3_bucket_name" {
  value = module.s3.bucket_name
}

output "alb_dns_name" {
  value = module.loadbalancer.alb_dns_name
}
