terraform {
  required_providers {
    hcloud = {
      source  = "hetznercloud/hcloud"
      version = "~> 1.45"
    }
  }
}

provider "hcloud" {
  token = var.hcloud_token
}

# ── SSH Key ───────────────────────────────────────────────────────────────────
resource "hcloud_ssh_key" "wedding_key" {
  name       = "wedding-invite-key"
  public_key = var.ssh_public_key
}

# ── Firewall ──────────────────────────────────────────────────────────────────
resource "hcloud_firewall" "wedding_fw" {
  name = "wedding-invite-fw"

  rule {
    direction  = "in"
    protocol   = "tcp"
    port       = "22"
    source_ips = ["0.0.0.0/0", "::/0"]
  }

  rule {
    direction  = "in"
    protocol   = "tcp"
    port       = "80"
    source_ips = ["0.0.0.0/0", "::/0"]
  }

  rule {
    direction  = "in"
    protocol   = "tcp"
    port       = "3000"
    source_ips = ["0.0.0.0/0", "::/0"]
  }
}

# ── Server ────────────────────────────────────────────────────────────────────
resource "hcloud_server" "wedding_server" {
  name         = "wedding-invite-server"
  image        = "ubuntu-22.04"
  server_type  = var.server_type
  location     = var.location
  ssh_keys     = [hcloud_ssh_key.wedding_key.id]
  firewall_ids = [hcloud_firewall.wedding_fw.id]

  user_data = <<-EOF
    #!/bin/bash
    set -e

    apt-get update -y
    apt-get install -y docker.io docker-compose git

    systemctl enable docker
    systemctl start docker

    # Clone the project
    cd /root
    git clone https://github.com/${var.github_repo} wedding-invite-manager
    cd wedding-invite-manager

    # Create .env file
    cat > .env <<ENVEOF
SECRET_KEY=${var.secret_key}
GREEN_API_INSTANCE_ID=${var.green_api_instance_id}
GREEN_API_TOKEN=${var.green_api_token}
GOOGLE_AI_API_KEY=${var.google_ai_key}
NGINX_PORT=80
ENVEOF

    docker-compose up -d

    echo "Wedding Invite Manager started on Hetzner!" > /root/startup.log
  EOF
}
