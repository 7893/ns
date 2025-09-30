# === Dispatcher Function ===
resource "google_cloudfunctions2_function" "dispatcher_function" {
  name     = "ns-func-dispatcher"
  location = local.region

  build_config {
    runtime     = "python311"
    entry_point = "handle_pubsub"
    source {
      repo_source {
        project_id   = local.project_id
        repo_name    = "github_7893_ns"
        branch_name  = "main"
        dir          = "apps/dispatcher"
      }
    }
  }

  service_config {
    service_account_email = local.runtime_service_account
    available_memory      = "256Mi"
    timeout_seconds       = 60
    max_instance_count    = 1
    min_instance_count    = 0
  }

  event_trigger {
    trigger_region = local.region
    event_type     = "google.cloud.pubsub.topic.v1.messagePublished"
    pubsub_topic   = google_pubsub_topic.scheduler_triggers_topic.id
    retry_policy   = "RETRY_POLICY_RETRY"
  }
}

# === 13 Worker Functions (one per dataset) ===
resource "google_cloudfunctions2_function" "worker_functions" {
  for_each = local.worker_functions

  name     = "ns-func-${each.key}"
  location = local.region

  build_config {
    runtime     = "python311"
    entry_point = "handle_pubsub"
    source {
      repo_source {
        project_id   = local.project_id
        repo_name    = "github_7893_ns"
        branch_name  = "main"
        dir          = "apps/${each.key}"
      }
    }
  }

  service_config {
    service_account_email = local.runtime_service_account
    available_memory      = "256Mi"
    timeout_seconds       = 300
    max_instance_count    = 1
    min_instance_count    = 0
    environment_variables = {
      NASA_API_KEY = var.nasa_api_key
    }
  }

  event_trigger {
    trigger_region = local.region
    event_type     = "google.cloud.pubsub.topic.v1.messagePublished"
    pubsub_topic   = google_pubsub_topic.worker_topics[each.key].id
    retry_policy   = "RETRY_POLICY_RETRY"
  }
}

