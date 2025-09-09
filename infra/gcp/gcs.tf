resource "google_storage_bucket" "function_source_code" {
  name          = "ns-2025" # Using the new bucket name
  location      = "US"
  force_destroy = true
}

# Archive all 14 function sources
data "archive_file" "source_zips" {
  for_each    = local.all_functions
  type        = "zip"
  source_dir  = "${path.module}/../../apps/${each.value}"
  output_path = "/tmp/source-${each.key}.zip"
}

# Upload all 14 function sources
resource "google_storage_bucket_object" "source_objects" {
  for_each = local.all_functions
  name     = "source/${each.key}/${data.archive_file.source_zips[each.key].output_md5}.zip"
  bucket   = google_storage_bucket.function_source_code.name
  source   = data.archive_file.source_zips[each.key].output_path
}