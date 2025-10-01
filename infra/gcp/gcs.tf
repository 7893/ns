# 数据存储桶（用于NASA数据持久化）
resource "google_storage_bucket" "nasa_data_storage" {
  name          = "ns-2025-data"
  location      = upper(local.region) # 使用统一的区域配置
  force_destroy = false               # 防止意外删除

  # 启用版本控制
  versioning {
    enabled = true
  }

  # 永久保存数据
  # 不设置lifecycle_rule以确保数据永久保存
}

# 函数源代码存储桶
resource "google_storage_bucket" "function_source_code" {
  name          = "ns-2025"
  location      = upper(local.region)
  force_destroy = true
}

# 创建源代码压缩包
data "archive_file" "source_archives" {
  for_each = local.all_functions

  type        = "zip"
  source_dir  = "${path.module}/../../apps/${each.key}"
  output_path = "/tmp/source-${each.key}.zip"
}

# 上传源代码到GCS
resource "google_storage_bucket_object" "source_objects" {
  for_each = local.all_functions

  name   = "source/${each.key}/${data.archive_file.source_archives[each.key].output_md5}.zip"
  bucket = google_storage_bucket.function_source_code.name
  source = data.archive_file.source_archives[each.key].output_path
}
