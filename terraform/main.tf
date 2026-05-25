terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# ── Security Group ────────────────────────────────────────────────────────────
resource "aws_security_group" "wedding_sg" {
  name        = "wedding-invite-sg"
  description = "Allow HTTP, HTTPS and SSH"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Grafana"
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "wedding-invite-sg" }
}

# ── EC2 Instance ──────────────────────────────────────────────────────────────
resource "aws_instance" "wedding_server" {
  ami                    = var.ami_id          # Amazon Linux 2023
  instance_type          = "t2.micro"          # Free tier
  key_name               = var.key_pair_name
  vpc_security_group_ids = [aws_security_group.wedding_sg.id]

  user_data = <<-EOF
    #!/bin/bash
    set -e

    # Update system
    yum update -y

    # Install Docker
    yum install -y docker git
    systemctl enable docker
    systemctl start docker

    # Install Docker Compose
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
      -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose

    # Add ec2-user to docker group
    usermod -aG docker ec2-user

    # Clone the project
    cd /home/ec2-user
    git clone https://github.com/${var.github_repo} wedding-invite-manager
    cd wedding-invite-manager

    # Create .env file from environment
    cat > .env <<ENVEOF
    SECRET_KEY=${var.secret_key}
    TWILIO_ACCOUNT_SID=${var.twilio_sid}
    TWILIO_AUTH_TOKEN=${var.twilio_token}
    TWILIO_WHATSAPP_FROM=${var.twilio_from}
    GOOGLE_AI_API_KEY=${var.google_ai_key}
    ENVEOF

    # Start the application
    docker-compose up -d

    echo "Wedding Invite Manager started!" > /home/ec2-user/startup.log
  EOF

  tags = { Name = "wedding-invite-server" }
}
