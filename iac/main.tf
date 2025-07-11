provider "aws" {
  region = "us-east-1"
}

module "network" {
  source = "./iac/modules/network"
}

module "autoscaling" {
  source             = "./iac/modules/autoscaling"
  public_subnet_ids  = module.network.public_subnet_ids
  private_subnet_ids = module.network.private_subnet_ids
  public_sg_id       = module.network.public_sg_id
  private_sg_id      = module.network.private_sg_id
  ec2_profile_name   = module.iam.ec2_profile_name
}

module "loadbalancer" {
  source         = "./iac/modules/loadbalancer"
  public_subnets = module.network.public_subnet_ids
  vpc_id         = module.network.vpc_id
  public_sg_id   = module.network.public_sg_id
}

module "s3" {
  source = "./iac/modules/s3"
}