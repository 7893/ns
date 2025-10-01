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

# === 存储桶 ===
resource "google_storage_bucket" "nasa_data" {
  name          = "ns-2025-data"
  location      = "US-CENTRAL1"
  force_destroy = false
  
  versioning {
    enabled = true
  }
}

resource "google_storage_bucket" "function_source" {
  name          = "ns-2025"
  location      = "US-CENTRAL1"
  force_destroy = true
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
  name   = "source/nasa-unified/${data.archive_file.function_source.output_md5}.zip"
  bucket = google_storage_bucket.function_source.name
  source = data.archive_file.function_source.output_path
}

# === Cloud Function ===
resource "google_cloudfunctions2_function" "unified" {
  name     = "ns-func-unified"
  location = "us-central1"

  build_config {
    runtime     = "python311"
    entry_point = "handle_all"
    source {
      storage_source {
        bucket = google_storage_bucket.function_source.name
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
  time_zone = "America/Chicago"
  region    = "us-central1"

  pubsub_target {
    topic_name = google_pubsub_topic.unified.id
    data       = base64encode(jsonencode({ "schedule_type" : "daily" }))
  }
}

resource "google_cloud_scheduler_job" "hourly" {
  name      = "ns-unified-hourly"
  schedule  = "0 * * * *"
  time_zone = "America/Chicago"
  region    = "us-central1"

  pubsub_target {
    topic_name = google_pubsub_topic.unified.id
    data       = base64encode(jsonencode({ "schedule_type" : "hourly" }))
  }
}

resource "google_cloud_scheduler_job" "weekly" {
  name      = "ns-unified-weekly"
  schedule  = "0 9 * * 1"
  time_zone = "America/Chicago"
  region    = "us-central1"

  pubsub_target {
    topic_name = google_pubsub_topic.unified.id
    data       = base64encode(jsonencode({ "schedule_type" : "weekly" }))
  }
}
