# === Dispatcher Function ===
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
    service_account_email = local.runtime_service_account
    available_memory      = "256Mi"
    timeout_seconds       = 60
    max_instance_count    = 1
    environment_variables = {
      GCP_PROJECT = local.project_id
    }
  }

  event_trigger {
    trigger_region = local.region
    event_type     = "google.cloud.pubsub.topic.v1.messagePublished"
    pubsub_topic   = google_pubsub_topic.scheduler_triggers_topic.id
    retry_policy   = "RETRY_POLICY_RETRY"
  }
}

# === NASA Collector Function ===
resource "google_cloudfunctions2_function" "collector_function" {
  name     = "ns-func-collector"
  location = local.region

  build_config {
    runtime     = "python311"
    entry_point = "handle_pubsub"
    source {
      storage_source {
        bucket = google_storage_bucket.function_source_code.name
        object = google_storage_bucket_object.source_objects["nasa-collector"].name
      }
    }
  }

  service_config {
    service_account_email = local.runtime_service_account
    available_memory      = "512Mi"
    timeout_seconds       = 300
    max_instance_count    = 10
    environment_variables = {
      NASA_API_KEY = var.nasa_api_key
    }
  }

  event_trigger {
    trigger_region = local.region
    event_type     = "google.cloud.pubsub.topic.v1.messagePublished"
    pubsub_topic   = google_pubsub_topic.collector_topic.id
    retry_policy   = "RETRY_POLICY_RETRY"
  }
}
