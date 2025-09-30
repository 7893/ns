# 供三类调度消息触发 dispatcher 的 Topic
resource "google_pubsub_topic" "scheduler_triggers_topic" {
  name = "ns-topic-scheduler-triggers"
}

# 13 个 Worker 专属 Topic（与 locals.worker_functions 的 key 一一对应）
resource "google_pubsub_topic" "worker_topics" {
  for_each = local.worker_functions
  name     = "ns-topic-${each.key}"
}

