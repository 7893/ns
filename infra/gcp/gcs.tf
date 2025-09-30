# 代码源桶（优化为单区域降低成本）
resource "google_storage_bucket" "function_source_code" {
  name          = "ns-2025"
  location      = local.region  # 使用单区域而非多区域
  force_destroy = true
  
  # 启用生命周期管理降低成本
  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete"
    }
  }
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

