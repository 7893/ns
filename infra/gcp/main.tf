# Force redeploy - updated timestamp
terraform {
  required_version = "~> 1.13.3"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }

    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.0"
    }
  }
}

provider "google" {
  project = local.project_id
  region  = local.region
}


