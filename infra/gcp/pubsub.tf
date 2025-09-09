# Topic for the 3 schedulers to trigger the dispatcher
resource "google_pubsub_topic" "scheduler_triggers_topic" {
  name = "ns-topic-scheduler-triggers"
}

# Create 13 Topics, one for each worker
resource "google_pubsub_topic" "worker_topics" {
  for_each = local.worker_functions
  name     = "ns-topic-${each.key}"
}