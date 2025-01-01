resource "aws_autoscaling_group" "basic_asg" {
  availability_zones = [var.aws_az]
  desired_capacity   = 1
  max_size           = 1
  min_size           = 1

  launch_template {
    id      = aws_launch_template.basic.id
    version = "$Latest"
  }
}
