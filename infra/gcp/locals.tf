locals {
  project_id = "sigma-outcome"
  region     = "us-central1"
  
  runtime_service_account = "817261716888-compute@developer.gserviceaccount.com"
  
  # 终极简化：只需1个函数
  functions = {
    nasa-unified = "nasa-unified"
  }
}
