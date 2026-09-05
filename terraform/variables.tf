# ============================================================================
# Variables: Agentic AI Governance on GCP
# ============================================================================

variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "us-central1"
}

variable "notification_email" {
  description = "Email address for alerts and notifications"
  type        = string
}

variable "agent_registry_project" {
  description = "Project ID for Agent Registry"
  type        = string
  default     = ""
}

variable "enable_model_armor" {
  description = "Enable Model Armor for prompt protection"
  type        = bool
  default     = true
}

variable "enable_semantic_governance" {
  description = "Enable Semantic Governance Policy"
  type        = bool
  default     = true
}

variable "retention_days" {
  description = "Log retention in days (minimum 365 for compliance)"
  type        = number
  default     = 3650
}
