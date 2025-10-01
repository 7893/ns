locals {
  project_id = "sigma-outcome"
  region     = "us-central1"
  
  runtime_service_account = "817261716888-compute@developer.gserviceaccount.com"
  
  # 简化为2个函数
  functions = {
    dispatcher     = "dispatcher"
    nasa-collector = "nasa-collector"
  }
}
