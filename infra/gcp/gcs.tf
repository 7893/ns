# 代码源桶（美国中部区域，永久保存数据）
resource "google_storage_bucket" "function_source_code" {
  name          = "ns-2025"
  location      = "US-CENTRAL1"  # 美国中部区域
  force_destroy = true
  
  # 永久保存数据 - 移除生命周期删除规则
  # 不设置lifecycle_rule以确保数据永久保存
}

# 数据存储桶（用于NASA数据持久化）
resource "google_storage_bucket" "nasa_data_storage" {
  name          = "ns-2025-data"
  location      = "US-CENTRAL1"  # 美国中部区域
  force_destroy = false  # 防止意外删除
  
  # 启用版本控制
  versioning {
    enabled = true
  }
  
  # 永久保存数据
  # 不设置lifecycle_rule以确保数据永久保存
}

# 将 apps/<func> 目录打成 zip（14 个：13 worker + dispatcher）
data "archive_file" "source_zips" {
  for_each    = local.all_functions
  type        = "zip"
  source_dir  = "${path.module}/../../apps/${each.value}"
  output_path = "/tmp/source-${each.key}.zip"
}

# 上传 zip 到 GCS（路径：source/<func>/<md5>.zip）
resource "google_storage_bucket_object" "source_objects" {
  for_each = local.all_functions
  name     = "source/${each.key}/${data.archive_file.source_zips[each.key].output_md5}.zip"
  bucket   = google_storage_bucket.function_source_code.name
  source   = data.archive_file.source_zips[each.key].output_path
}
