# 统一topic处理所有消息
resource "google_pubsub_topic" "unified_topic" {
  name = "ns-topic-unified"
}
