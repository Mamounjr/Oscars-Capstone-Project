resource "aws_launch_template" "public" {
  name_prefix   = "public-lt"
  image_id      = "ami-0c94855ba95c71c99"
  instance_type = "t2.micro"
  vpc_security_group_ids = [var.public_sg_id]
}

resource "aws_autoscaling_group" "public" {
  desired_capacity    = 1
  max_size            = 2
  min_size            = 1
  vpc_zone_identifier = var.public_subnet_ids
  launch_template {
    id      = aws_launch_template.public.id
    version = "$Latest"
  }
}

resource "aws_launch_template" "private" {
  name_prefix   = "private-lt"
  image_id      = "ami-0c94855ba95c71c99"
  instance_type = "t2.micro"
  vpc_security_group_ids = [var.private_sg_id]
}

resource "aws_autoscaling_group" "private" {
  desired_capacity    = 1
  max_size            = 2
  min_size            = 1
  vpc_zone_identifier = var.private_subnet_ids
  launch_template {
    id      = aws_launch_template.private.id
    version = "$Latest"
  }
}