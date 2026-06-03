output "server_ip" {
  value       = hcloud_server.wedding_server.ipv4_address
  description = "Hetzner server public IP — open this in the browser"
}

output "app_url" {
  value = "http://${hcloud_server.wedding_server.ipv4_address}"
}

output "grafana_url" {
  value = "http://${hcloud_server.wedding_server.ipv4_address}:3000"
}
