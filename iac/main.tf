provider "aws" {
  region = "us-east-1"
}

#Deploy network infrastructure
module "network" {
  source = "./modules/network"
}

#Creating autoscaling group using network resources
module "autoscaling" {
  source             = "./modules/autoscaling"
  public_subnet_ids  = module.network.public_subnet_ids
  private_subnet_ids = module.network.private_subnet_ids
  public_sg_id       = module.network.public_sg_id
  private_sg_id      = module.network.private_sg_id
}

# Create and configure load balancer
module "loadbalancer" {
  source         = "./modules/loadbalancer"
  public_subnets = module.network.public_subnet_ids
  vpc_id         = module.network.vpc_id
  public_sg_id   = module.network.public_sg_id
}

#Provision S3 bucket
module "s3" {
  source = "./modules/s3"
}
