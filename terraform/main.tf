terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.34.0"
    }
  }
}

provider "google" {
  credentials = file(var.creds)
  project     = var.project_id
  region      = var.region
}

resource "google_storage_bucket" "raw_bucket" {
  name          = var.google_storage_bucket_name
  location      = var.location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 14
    }
    action {
      type = "Delete"
    }
  }
}

# resource "google_bigquery_dataset" "bq_prod" {
#   dataset_id                 = var.bq_prod
#   location                   = var.location
#   delete_contents_on_destroy = true
# }