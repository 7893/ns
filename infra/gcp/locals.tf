locals {
  # —— 项目与区域（与设计文档一致）——
  project_id = "sigma-outcome"
  region     = "us-central1"

  # —— 运行时服务账号（你已确认权限就绪）——
  runtime_service_account = "817261716888-compute@developer.gserviceaccount.com"

  # —— 12 个 Worker 名称（与 ns 约定完全一致，影响函数名/Topic 名/代码包名）——
  worker_functions = {
    apod              = "apod"
    asteroids-neows   = "asteroids-neows"
    donki             = "donki"
    earth             = "earth"
    eonet             = "eonet"
    epic              = "epic"
    exoplanet         = "exoplanet"
    genelab           = "genelab"
    mars-rover-photos = "mars-rover-photos"
    nasa-ivl          = "nasa-ivl"
    techport          = "techport"
    techtransfer      = "techtransfer"
  }

  # —— 13 个函数总表（包含 dispatcher）——
  all_functions = merge(local.worker_functions, { dispatcher = "dispatcher" })
}

