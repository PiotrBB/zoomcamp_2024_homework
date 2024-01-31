variable "location" {
  description = "My GCP Location"
  default     = "EU"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "demo_dataset_zoomcamp2024"
}

variable "gcs_bucket_name" {
  description = "My GCS Bucket Name"
  default     = "demo_bucket_zoomcamp2024"
}

variable "gcs_storage_class" {
  description = "My GCS Storage Class"
  default     = "STANDARD"
}