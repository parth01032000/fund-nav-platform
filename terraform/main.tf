terraform {
  required_providers {
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.4"
    }
  }
}

resource "random_id" "suffix" {
  byte_length = 4
}

resource "local_file" "ecr_config_note" {
  filename = "${path.module}/ecr-repo-name-${random_id.suffix.hex}.txt"
  content  = "Planned ECR repository: fund-nav-platform-${random_id.suffix.hex} (image_scanning_configuration: scan_on_push = true)"
}

output "config_file" {
  value = local_file.ecr_config_note.filename
}
