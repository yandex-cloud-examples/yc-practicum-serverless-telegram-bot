terraform {
  required_providers {
    yandex = {
      source = "terraform-providers/yandex"
    }
  }
}

provider "yandex" {
  token     = "<OAuth>"
  cloud_id  = "<CLOUD_ID>"
  folder_id = "<FOLDER_ID>"
  // zone      = "ru-central1-a"
}

resource "yandex_storage_bucket" "bucket" {
  access_key = "<ACCESS_KEY>"
  secret_key = "<SECRET_KEY>"
  bucket = "<BUCKET-ID>"
}