# modules/loadbalancer/main.tf
resource "aws_lb" "alb" {
  name               = "main-alb"
  load_balancer_type = "application"
  subnets            = var.public_subnets
  security_groups    = [var.public_sg_id]
}

resource "aws_lb_target_group" "tg" {
  name     = "main-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id
}

resource "aws_lb_listener" "listener" {
  load_balancer_arn = aws_lb.alb.arn
  port              = 80
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.tg.arn
  }
}
