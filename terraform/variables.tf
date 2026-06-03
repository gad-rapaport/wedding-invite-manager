variable "aws_region"             { default = "us-east-1" }
variable "ami_id"                 { default = "ami-0c02fb55956c7d316" } # Amazon Linux 2023 us-east-1
variable "key_pair_name"          { description = "EC2 Key Pair name" }
variable "github_repo"            { description = "GitHub user/repo-name" }
variable "secret_key"             { sensitive = true }
variable "green_api_instance_id"  { sensitive = true; description = "Green API instance ID" }
variable "green_api_token"        { sensitive = true; description = "Green API token" }
variable "google_ai_key"          { sensitive = true }
