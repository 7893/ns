locals {
  project_id              = "sigma-outcome"
  region                  = "us-central1"
  runtime_service_account = "817261716888-compute@developer.gserviceaccount.com"
  worker_functions = {
    "apod"              = "apod", "asteroids-neows" = "asteroids-neows", "donki" = "donki",
    "earth"             = "earth", "eonet" = "eonet", "epic" = "epic",
    "exoplanet"         = "exoplanet", "genelab" = "genelab", "insight" = "insight",
    "mars-rover-photos" = "mars-rover-photos", "nasa-ivl" = "nasa-ivl", "techport" = "techport",
    "techtransfer"      = "techtransfer"
  }
  all_functions = merge(local.worker_functions, { "dispatcher" = "dispatcher" })
}