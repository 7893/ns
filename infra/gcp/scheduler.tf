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