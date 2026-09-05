# ============================================================================
# Terraform Configuration: Agentic AI Governance on GCP
# ============================================================================

terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# ============================================================================
# Enable Required APIs
# ============================================================================

resource "google_project_service" "services" {
  for_each = toset([
    "cloudfunctions.googleapis.com",
    "cloudmonitoring.googleapis.com",
    "logging.googleapis.com",
    "iam.googleapis.com",
    "iamcredentials.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "serviceusage.googleapis.com",
    "cloudkms.googleapis.com",
    "cloudscheduler.googleapis.com",
    "pubsub.googleapis.com",
    "aiplatform.googleapis.com",
    "dlp.googleapis.com",
    "lookerstudio.googleapis.com"
  ])
  service = each.key
}

# ============================================================================
# Storage & Logging
# ============================================================================

resource "google_storage_bucket" "agent_logs" {
  name     = "${var.project_id}-agent-logs"
  location = var.region
  force_destroy = true
  
  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 3650  # 10-year retention
    }
  }
}

resource "google_storage_bucket" "agent_artifacts" {
  name     = "${var.project_id}-agent-artifacts"
  location = var.region
  force_destroy = true
}

# ============================================================================
# Cloud KMS (for agent credentials)
# ============================================================================

resource "google_kms_key_ring" "agent_key_ring" {
  name     = "agent-key-ring"
  location = var.region
}

resource "google_kms_crypto_key" "agent_key" {
  name     = "agent-key"
  key_ring = google_kms_key_ring.agent_key_ring.id
  rotation_period = "86400s"  # 24 hours
}

# ============================================================================
# Cloud Functions (PDP - Policy Decision Point)
# ============================================================================

resource "google_storage_bucket" "function_bucket" {
  name = "${var.project_id}-function-source"
  location = var.region
  force_destroy = true
}

resource "google_storage_bucket_object" "policy_engine_zip" {
  name   = "policy-engine-${data.archive_file.policy_engine.output_md5}.zip"
  bucket = google_storage_bucket.function_bucket.name
  source = data.archive_file.policy_engine.output_path
}

data "archive_file" "policy_engine" {
  type        = "zip"
  source_dir  = "../src/policy-engine"
  output_path = "/tmp/policy-engine.zip"
}

resource "google_cloudfunctions_function" "policy_engine" {
  name                  = "agent-policy-engine"
  description           = "Policy Decision Point for agentic AI governance"
  runtime               = "python311"
  available_memory_mb   = 256
  source_archive_bucket = google_storage_bucket.function_bucket.name
  source_archive_object = google_storage_bucket_object.policy_engine_zip.name
  trigger_http          = true
  entry_point           = "evaluate_policy"
  
  environment_variables = {
    PROJECT_ID            = var.project_id
    AGENT_REGISTRY_PROJECT = var.project_id
    KMS_KEY_ID            = google_kms_crypto_key.agent_key.id
    LOG_BUCKET            = google_storage_bucket.agent_logs.name
  }
  
  iam_policy {
    members = ["allUsers"]
    role    = "roles/cloudfunctions.invoker"
  }
}

# ============================================================================
# Cloud Scheduler (for periodic compliance scans)
# ============================================================================

resource "google_cloud_scheduler_job" "compliance_scan" {
  name        = "agent-compliance-scan"
  description = "Periodic compliance scan for AI agents"
  schedule    = "0 */6 * * *"
  time_zone   = "UTC"
  
  http_target {
    uri         = google_cloudfunctions_function.policy_engine.https_trigger_url
    http_method = "POST"
    body        = base64encode(jsonencode({
      action = "compliance_scan"
    }))
  }
}

# ============================================================================
# Pub/Sub Topics
# ============================================================================

resource "google_pubsub_topic" "agent_events" {
  name = "agent-events"
}

resource "google_pubsub_topic" "agent_alerts" {
  name = "agent-alerts"
}

# ============================================================================
# Cloud Monitoring
# ============================================================================

resource "google_monitoring_alert_policy" "agent_anomaly" {
  display_name = "Agent Anomaly Detection"
  combiner     = "OR"
  
  conditions {
    display_name = "Policy Violation Rate"
    condition_threshold {
      filter = "metric.type=\"logging.googleapis.com/user/agent_policy_violations\""
      duration = "60s"
      comparison = "COMPARISON_GT"
      threshold_value = 5
    }
  }
  
  notification_channels = [
    google_monitoring_notification_channel.email.id
  ]
}

resource "google_monitoring_notification_channel" "email" {
  display_name = "Email Notifications"
  type         = "email"
  labels = {
    email_address = var.notification_email
  }
}

# ============================================================================
# Outputs
# ============================================================================

output "policy_engine_url" {
  value = google_cloudfunctions_function.policy_engine.https_trigger_url
}

output "agent_logs_bucket" {
  value = google_storage_bucket.agent_logs.name
}

output "agent_key_ring" {
  value = google_kms_key_ring.agent_key_ring.name
}

output "pubsub_events_topic" {
  value = google_pubsub_topic.agent_events.name
}
