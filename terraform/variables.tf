variable "hcloud_token"          { sensitive = true; description = "Hetzner Cloud API token (from Hetzner Console)" }
variable "ssh_public_key"        { description = "SSH public key content (e.g. contents of ~/.ssh/id_rsa.pub)" }
variable "github_repo"           { description = "GitHub user/repo-name  e.g. myuser/wedding-invite-manager" }
variable "secret_key"            { sensitive = true }
variable "green_api_instance_id" { sensitive = true; description = "Green API instance ID" }
variable "green_api_token"       { sensitive = true; description = "Green API token" }
variable "google_ai_key"         { sensitive = true }
variable "location"              { default = "nbg1"; description = "Hetzner datacenter: nbg1 (Nuremberg), hel1 (Helsinki), ash (Ashburn)" }
variable "server_type"           { default = "cx22"; description = "Hetzner server type: cx22 = 2 vCPU / 4 GB RAM" }
