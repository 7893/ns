# NS - NASA Data System - Complete Infrastructure as Code
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

  backend "gcs" {
    bucket = "ns-data-2025"
    prefix = "terraform/state"
  }
}

provider "google" {
  project = "sigma-outcome"
  region  = "us-central1"
}

variable "project_id" {
  description = "GCP Project ID"
  type        = string
  default     = "sigma-outcome"
}

variable "nasa_api_key" {
  description = "NASA API Key"
  type        = string
  sensitive   = true
}

# === 数据存储桶 ===
resource "google_storage_bucket" "nasa_data" {
  name          = "ns-data-2025"
  location      = "US-CENTRAL1"
  force_destroy = false

  versioning {
    enabled = true
  }
}

# === Artifact Registry ===
resource "google_artifact_registry_repository" "functions" {
  location      = "us-central1"
  repository_id = "ns-functions"
  description   = "NS Functions Docker Repository"
  format        = "DOCKER"
}

# === Pub/Sub Topic ===
resource "google_pubsub_topic" "unified" {
  name = "ns-topic-unified"
}

# === 函数源码 ===
data "archive_file" "function_source" {
  type        = "zip"
  source_dir  = "${path.module}/../../apps/nasa-unified"
  output_path = "/tmp/nasa-unified.zip"
}

resource "google_storage_bucket_object" "function_source" {
  name   = "functions/nasa-unified/${data.archive_file.function_source.output_md5}.zip"
  bucket = google_storage_bucket.nasa_data.name
  source = data.archive_file.function_source.output_path
}

# === Cloud Function ===
resource "google_cloudfunctions2_function" "unified" {
  name     = "ns-func-unified"
  location = "us-central1"

  build_config {
    runtime           = "python311"
    entry_point       = "handle_all"
    docker_repository = "projects/${var.project_id}/locations/us-central1/repositories/ns-functions"
    source {
      storage_source {
        bucket = google_storage_bucket.nasa_data.name
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
    pubsub_topic   = google_pubsub_topic.unified.id
    retry_policy   = "RETRY_POLICY_RETRY"
  }
}

# === Cloud Scheduler Jobs ===
resource "google_cloud_scheduler_job" "daily" {
  name      = "ns-unified-daily"
  schedule  = "0 8 * * *"
  time_zone = "Asia/Hong_Kong"
  region    = "us-central1"

  pubsub_target {
    topic_name = google_pubsub_topic.unified.id
    data       = base64encode(jsonencode({ "schedule_type" : "daily" }))
  }
}

resource "google_cloud_scheduler_job" "hourly" {
  name      = "ns-unified-hourly"
  schedule  = "0 * * * *"
  time_zone = "Asia/Hong_Kong"
  region    = "us-central1"

  pubsub_target {
    topic_name = google_pubsub_topic.unified.id
    data       = base64encode(jsonencode({ "schedule_type" : "hourly" }))
  }
}

resource "google_cloud_scheduler_job" "weekly" {
  name      = "ns-unified-weekly"
  schedule  = "0 9 * * 1"
  time_zone = "Asia/Hong_Kong"
  region    = "us-central1"

  pubsub_target {
    topic_name = google_pubsub_topic.unified.id
    data       = base64encode(jsonencode({ "schedule_type" : "weekly" }))
  }
}
