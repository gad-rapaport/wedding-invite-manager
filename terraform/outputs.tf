output "server_ip" {
  value       = aws_instance.wedding_server.public_ip
  description = "EC2 public IP — open this in the browser"
}

output "app_url" {
  value = "http://${aws_instance.wedding_server.public_ip}"
}

output "grafana_url" {
  value = "http://${aws_instance.wedding_server.public_ip}:3000"
}
