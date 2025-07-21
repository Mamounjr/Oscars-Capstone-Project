output "ecs_cluster_name" {
  value = aws_ecs_cluster.capstone_cluster.name
}

output "ecr_repo_url" {
  value = aws_ecr_repository.app_repo.repository_url
}
