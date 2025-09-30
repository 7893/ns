# 数据存储桶（用于NASA数据持久化）
resource "google_storage_bucket" "nasa_data_storage" {
  name          = "ns-2025-data"
  location      = upper(local.region)  # 使用统一的区域配置
  force_destroy = false  # 防止意外删除
  
  # 启用版本控制
  versioning {
    enabled = true
  }
  
  # 永久保存数据
  # 不设置lifecycle_rule以确保数据永久保存
}
