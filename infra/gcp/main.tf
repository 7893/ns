# NS - NASA Data System - Unified Infrastructure
terraform {
  required_version = ">= 1.0"
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
  project = "sigma-outcome"
  region  = "us-central1"
}

variable "nasa_api_key" {
  description = "NASA API Key"
  type        = string
  sensitive   = true
}

# === 函数源码 ===
data "archive_file" "function_source" {
  type        = "zip"
  source_dir  = "${path.module}/../../apps/nasa-unified"
  output_path = "/tmp/nasa-unified.zip"
}

resource "google_storage_bucket_object" "function_source" {
  name   = "source/nasa-unified/${data.archive_file.function_source.output_md5}.zip"
  bucket = "ns-2025"
  source = data.archive_file.function_source.output_path
}

# === 函数 ===
resource "google_cloudfunctions2_function" "unified" {
  name     = "ns-func-unified"
  location = "us-central1"

  build_config {
    runtime     = "python311"
    entry_point = "handle_all"
    source {
      storage_source {
        bucket = "ns-2025"
        object = google_storage_bucket_object.function_source.name
      }
    }
  }

  service_config {
    service_account_email = "817261716888-compute@developer.gserviceaccount.com"
    available_memory      = "512Mi"
    timeout_seconds       = 300
    max_instance_count    = 10
    environment_variables = {
      GCP_PROJECT  = "sigma-outcome"
      NASA_API_KEY = var.nasa_api_key
    }
  }

  event_trigger {
    trigger_region = "us-central1"
    event_type     = "google.cloud.pubsub.topic.v1.messagePublished"
    pubsub_topic   = "projects/sigma-outcome/topics/ns-topic-unified"
    retry_policy   = "RETRY_POLICY_RETRY"
  }
}
