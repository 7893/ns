terraform {
  required_version = "~> 1.13"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = local.project_id
  region  = local.region
}

locals {
  project_id              = "sigma-outcome"
  region                  = "us-central1"
  runtime_service_account = "817261716888-compute@developer.gserviceaccount.com"
  worker_functions = {
    "apod"              = "apod", "asteroids-neows" = "asteroids-neows", "donki" = "donki",
    "earth"             = "earth", "eonet" = "eonet", "epic" = "epic",
    "exoplanet"         = "exoplanet", "genelab" = "genelab", "insight" = "insight",
    "mars-rover-photos" = "mars-rover-photos", "nasa-ivl" = "nasa-ivl", "techport" = "techport",
    "techtransfer"      = "techtransfer"
  }
  all_functions = merge(local.worker_functions, { "dispatcher" = "dispatcher" })
}

# --- Core Resources ---
resource "google_pubsub_topic" "scheduler_triggers_topic" {
  name = "ns-topic-scheduler-triggers"
}

resource "google_storage_bucket" "function_source_code" {
  name          = "ns-functions-source-${local.project_id}"
  location      = "US"
  force_destroy = true
}

# --- Create 13 Topics, one for each worker ---
resource "google_pubsub_topic" "worker_topics" {
  for_each = local.worker_functions
  name     = "ns-topic-${each.key}"
}

# --- Archive and Upload all 14 function sources ---
data "archive_file" "source_zips" {
  for_each    = local.all_functions
  type        = "zip"
  source_dir  = "${path.module}/../../apps/${each.value}"
  output_path = "/tmp/source-${each.key}.zip"
}

resource "google_storage_bucket_object" "source_objects" {
  for_each = local.all_functions
  name     = "source/${each.key}/${data.archive_file.source_zips[each.key].output_md5}.zip"
  bucket   = google_storage_bucket.function_source_code.name
  source   = data.archive_file.source_zips[each.key].output_path
}

# --- Create the 13 Worker Functions, each with its own topic trigger ---
resource "google_cloudfunctions2_function" "worker_functions" {
  for_each = local.worker_functions
  name     = "ns-func-${each.key}"
  location = local.region

  build_config {
    runtime     = "python311"
    entry_point = "handle_pubsub"
    source {
      storage_source {
        bucket = google_storage_bucket.function_source_code.name
        object = google_storage_bucket_object.source_objects[each.key].name
      }
    }
  }

  service_config {
    max_instance_count    = 1
    min_instance_count    = 0
    available_memory      = "256Mi"
    timeout_seconds       = 300
    service_account_email = local.runtime_service_account
  }

  event_trigger {
    trigger_region = local.region
    event_type     = "google.cloud.pubsub.topic.v1.messagePublished"
    # Triggered by its own dedicated topic, NO FILTERS NEEDED
    pubsub_topic   = google_pubsub_topic.worker_topics[each.key].id
    retry_policy   = "RETRY_POLICY_RETRY"
  }
}

# --- Create the Dispatcher Function ---
resource "google_cloudfunctions2_function" "dispatcher_function" {
  name     = "ns-func-dispatcher"
  location = local.region

  build_config {
    runtime     = "python311"
    entry_point = "handle_pubsub"
    source {
      storage_source {
        bucket = google_storage_bucket.function_source_code.name
        object = google_storage_bucket_object.source_objects["dispatcher"].name
      }
    }
  }

  service_config {
    max_instance_count    = 1
    min_instance_count    = 0
    available_memory      = "256Mi"
    timeout_seconds       = 60
    service_account_email = local.runtime_service_account
  }

  event_trigger {
    trigger_region = local.region
    event_type     = "google.cloud.pubsub.topic.v1.messagePublished"
    pubsub_topic   = google_pubsub_topic.scheduler_triggers_topic.id
    retry_policy   = "RETRY_POLICY_RETRY"
  }
}

# --- Create the 3 Schedulers ---
resource "google_cloud_scheduler_job" "daily_scheduler" {
  name      = "ns-scheduler-main-daily"
  schedule  = "0 8 * * *"
  time_zone = "Etc/UTC"
  pubsub_target {
    topic_name = google_pubsub_topic.scheduler_triggers_topic.id
    data       = base64encode("{\"schedule_type\":\"daily\"}")
  }
}

resource "google_cloud_scheduler_job" "hourly_scheduler" {
  name      = "ns-scheduler-fast-hourly"
  schedule  = "0 * * * *"
  time_zone = "Etc/UTC"
  pubsub_target {
    topic_name = google_pubsub_topic.scheduler_triggers_topic.id
    data       = base64encode("{\"schedule_type\":\"hourly\"}")
  }
}

resource "google_cloud_scheduler_job" "weekly_scheduler" {
  name      = "ns-scheduler-slow-weekly"
  schedule  = "0 0 * * 1"
  time_zone = "Etc/UTC"
  pubsub_target {
    topic_name = google_pubsub_topic.scheduler_triggers_topic.id
    data       = base64encode("{\"schedule_type\":\"weekly\"}")
  }
}