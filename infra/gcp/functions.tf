# Create the 13 Worker Functions, each with its own topic trigger
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
    pubsub_topic   = google_pubsub_topic.worker_topics[each.key].id
    retry_policy   = "RETRY_POLICY_RETRY"
  }
}

# Create the Dispatcher Function
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