# Scheduler triggers topic
resource "google_pubsub_topic" "scheduler_triggers_topic" {
  name = "ns-topic-scheduler-triggers"
}

# Main collector topic
resource "google_pubsub_topic" "collector_topic" {
  name = "ns-topic-collector"
}
