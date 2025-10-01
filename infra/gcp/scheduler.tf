# 统一调度器 - 每日任务
resource "google_cloud_scheduler_job" "daily_job" {
  name             = "ns-unified-daily"
  description      = "Daily NASA data collection"
  schedule         = "0 8 * * *"  # 每天8点
  time_zone        = "America/Chicago"
  region           = local.region
  attempt_deadline = "300s"

  pubsub_target {
    topic_name = google_pubsub_topic.unified_topic.id
    data       = base64encode(jsonencode({"schedule_type": "daily"}))
  }
}

# 统一调度器 - 每小时任务  
resource "google_cloud_scheduler_job" "hourly_job" {
  name             = "ns-unified-hourly"
  description      = "Hourly NASA data collection"
  schedule         = "0 * * * *"  # 每小时
  time_zone        = "America/Chicago"
  region           = local.region
  attempt_deadline = "300s"

  pubsub_target {
    topic_name = google_pubsub_topic.unified_topic.id
    data       = base64encode(jsonencode({"schedule_type": "hourly"}))
  }
}

# 统一调度器 - 每周任务
resource "google_cloud_scheduler_job" "weekly_job" {
  name             = "ns-unified-weekly"
  description      = "Weekly NASA data collection"
  schedule         = "0 9 * * 1"  # 每周一9点
  time_zone        = "America/Chicago"
  region           = local.region
  attempt_deadline = "300s"

  pubsub_target {
    topic_name = google_pubsub_topic.unified_topic.id
    data       = base64encode(jsonencode({"schedule_type": "weekly"}))
  }
}
