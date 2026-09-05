# 🤖 Agentic AI Governance on Google Cloud Platform (GCP)

## Zero-Trust Governance for Autonomous AI Agents on Gemini Enterprise Agent Platform

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-brightgreen.svg)]()
[![GCP](https://img.shields.io/badge/GCP-Certified-blue.svg)]()
[![Gemini Enterprise](https://img.shields.io/badge/Gemini%20Enterprise-Ready-blue.svg)]()
[![OWASP Agentic](https://img.shields.io/badge/OWASP%20Agentic-Aligned-green.svg)]()
[![CSA ATF](https://img.shields.io/badge/CSA%20ATF-Compatible-purple.svg)]()

---

## 📋 Table of Contents

- [About This Project](#-about-this-project)
- [Why This Matters](#-why-this-matters)
- [Google Cloud Agentic AI Stack](#-google-cloud-agentic-ai-stack)
- [Architecture](#-architecture)
- [GCP Services Used](#-gcp-services-used)
- [Framework Alignment](#-framework-alignment)
- [Quick Start](#-quick-start)
- [What's Inside](#-whats-inside)
- [Key Artifacts](#-key-artifacts)
- [Compliance Dashboard](#-compliance-dashboard)
- [Deployment](#-deployment)
- [References](#-references)
- [License](#-license)

---

## 🎯 About This Project

This project implements a **complete governance and security framework** for AI agents built on **Google Cloud's Gemini Enterprise Agent Platform**[reference:6] — Google's enterprise platform for building, deploying, and operating autonomous AI agents with built-in governance.

**What it does:**

| Capability | Description |
|------------|-------------|
| 🔐 **Zero-Trust Identity** | Agent Identity with cryptographic, SPIFFE-based credentials per agent[reference:7] |
| 📋 **Policy-as-Code** | Semantic Governance Policy (SGP) for fine-grained authorization[reference:8] |
| 🛡️ **Runtime Guardrails** | Model Armor for prompt injection protection and DLP[reference:9] |
| 🌐 **Network Security** | VPC Service Controls with agent identities in ingress/egress rules[reference:10] |
| 📊 **Continuous Monitoring** | Cloud Monitoring + Cloud Logging for telemetry and observability |
| 🚨 **Incident Response** | Agentic-specific incident runbook with kill-switch capabilities |
| 📁 **Audit Evidence** | Agent Registry for centralized agent inventory and governance[reference:11] |

**Organization:** NovaTech Financial Group *(hypothetical)*  
**Effective Date:** September 2026  
**Version:** 1.0

---

## 🚨 Why This Matters

### The Agentic AI Governance Gap

Agentic AI represents a fundamental shift in risk profile. Unlike traditional AI that generates outputs, agentic AI:

| Traditional AI | Agentic AI |
|----------------|------------|
| Generates recommendations | Takes autonomous actions |
| Requires human approval | Executes independently |
| Single-turn interactions | Multi-step planning and execution |
| Limited tool access | Full tool and API integration |
| Predictable outputs | Emergent, adaptive behavior |

> *"Google Cloud introduced Gemini Enterprise Agent Platform and two services that remove the complex engineering workarounds organizations have been forced to cobble together for AI governance."*[reference:12]

### Google Cloud's Agentic Governance Services

At **Google Cloud Next 2026**, Google introduced a comprehensive enterprise control plane[reference:13]:

| Service | Purpose |
|---------|---------|
| **Agent Identity** | Unique, cryptographic ID per agent; enforces true least-privilege access[reference:14] |
| **Agent Registry** | Centralized catalog for agent governance and inventory[reference:15] |
| **Agent Gateway** | Centralized control plane to enforce enterprise guardrails[reference:16] |
| **Semantic Governance Policy (SGP)** | Intelligent security and compliance layer for tool calls[reference:17] |
| **Model Armor** | Protection against prompt injection and sensitive data leakage[reference:18] |
| **VPC Service Controls** | Network-level controls with agent identities[reference:19] |

---

## 🏗️ Google Cloud Agentic AI Stack
┌─────────────────────────────────────────────────────────────────────────────┐
│ GOOGLE CLOUD AGENTIC AI STACK │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ IDENTITY & ACCESS LAYER │ │
│ │ │ │
│ │ ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────┐ │ │
│ │ │ Agent │ │ Cloud IAM │ │ Context-Aware Access │ │ │
│ │ │ Identity │ │ Policies │ │ (CAA) │ │ │
│ │ └──────────────┘ └──────────────┘ └──────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ GOVERNANCE LAYER │ │
│ │ │ │
│ │ ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────┐ │ │
│ │ │ Agent │ │ Semantic │ │ Agent Gateway │ │ │
│ │ │ Registry │ │ Governance │ │ (Centralized Control) │ │ │
│ │ │ (Inventory) │ │ Policy │ │ │ │ │
│ │ └──────────────┘ └──────────────┘ └──────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ SECURITY LAYER │ │
│ │ │ │
│ │ ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────┐ │ │
│ │ │ Model Armor │ │ VPC Service │ │ Cloud DLP │ │ │
│ │ │ (Prompt │ │ Controls │ │ (Data Loss Prevention) │ │ │
│ │ │ Shield) │ │ (Network) │ │ │ │ │
│ │ └──────────────┘ └──────────────┘ └──────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ OBSERVABILITY LAYER │ │
│ │ │ │
│ │ ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────┐ │ │
│ │ │ Cloud │ │ Cloud │ │ Looker Studio │ │ │
│ │ │ Monitoring │ │ Logging │ │ (Dashboard) │ │ │
│ │ └──────────────┘ └──────────────┘ └──────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ EXECUTION LAYER │ │
│ │ │ │
│ │ ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────┐ │ │
│ │ │ Cloud │ │ Gemini │ │ Vertex AI Agent │ │ │
│ │ │ Functions │ │ Enterprise │ │ Builder │ │ │
│ │ │ (PDP) │ │ Agent │ │ │ │ │
│ │ │ │ │ Runtime │ │ │ │ │
│ │ └──────────────┘ └──────────────┘ └──────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘



### Key Architecture Components

| Component | Purpose | Documentation |
|-----------|---------|---------------|
| **Agent Identity** | Unique, cryptographic ID per agent; enforces true least-privilege access[reference:20] | Cloud IAM |
| **Agent Registry** | Centralized catalog for agent governance and inventory[reference:21] | Gemini Enterprise |
| **Agent Gateway** | Centralized control plane to enforce enterprise guardrails[reference:22] | Gemini Enterprise |
| **Semantic Governance Policy (SGP)** | Intelligent security and compliance layer for tool calls[reference:23] | Gemini Enterprise |
| **Model Armor** | Protection against prompt injection and sensitive data leakage[reference:24] | Vertex AI |
| **VPC Service Controls** | Network-level controls with agent identities[reference:25] | VPC |
| **Cloud Functions (PDP)** | Policy Decision Point for authorization decisions | Cloud Functions |
| **Cloud Monitoring** | Telemetry and alerting for agent behavior | Cloud Monitoring |
| **Cloud Logging** | Audit logging for all agent actions | Cloud Logging |

---

## 🔧 GCP Services Used

| Service | Purpose | Key Feature |
|---------|---------|-------------|
| **Gemini Enterprise Agent Platform** | Agent runtime and governance[reference:26] | Agent Identity, Registry, Gateway |
| **Agent Identity** | Cryptographic per-agent identity[reference:27] | SPIFFE-based, least-privilege |
| **Agent Registry** | Centralized agent inventory[reference:28] | Governance and discovery |
| **Agent Gateway** | Centralized control plane[reference:29] | Guardrails, access policies |
| **Semantic Governance Policy (SGP)** | Intelligent policy enforcement[reference:30] | Tool call validation |
| **Model Armor** | Prompt injection protection[reference:31] | Input sanitization, DLP |
| **VPC Service Controls** | Network-level security[reference:32] | Agent identities in rules |
| **Cloud IAM** | Identity and access management | Agent-specific policies |
| **Cloud Functions** | Serverless PDP | Policy evaluation |
| **Cloud Monitoring** | Telemetry and alerting | Agent behavior monitoring |
| **Cloud Logging** | Audit logging | 10-year retention |
| **Cloud DLP** | Data loss prevention | Sensitive data detection |
| **Looker Studio** | Executive dashboards | Compliance visualization |

---

## 📋 Framework Alignment

| Framework | Alignment | Artifact |
|-----------|-----------|----------|
| **OWASP Agentic Top 10 2026** | ✅ Full Mapping | `audit-framework/agentic-ai-governance-framework.json` |
| **CSA Agentic Trust Framework** | ✅ Full Mapping | `audit-framework/agentic-ai-governance-framework.json` |
| **NIST AI RMF** | ✅ Full Mapping | All controls |
| **ISO/IEC 42001** | ✅ Full Mapping | All controls |

### CSA Agentic Trust Framework (ATF) Alignment

The Cloud Security Alliance's Agentic Trust Framework applies established Zero Trust principles to autonomous AI agents:

| ATF Element | How This Project Addresses It |
|-------------|-------------------------------|
| **Identity** | Agent Identity with cryptographic, SPIFFE-based credentials[reference:33] |
| **Authorization** | Semantic Governance Policy + IAM policies[reference:34] |
| **Runtime** | Agent Gateway with Model Armor guardrails[reference:35] |
| **Observability** | Cloud Monitoring + Cloud Logging |
| **Data Boundaries** | VPC Service Controls with agent identities[reference:36] |

---

## 🚀 Quick Start

| Step | Action | Command |
|------|--------|---------|
| **1** | Clone the repository | `git clone https://github.com/yourusername/agentic-ai-governance-gcp.git` |
| **2** | Navigate to the project | `cd agentic-ai-governance-gcp` |
| **3** | Configure Terraform | `cp terraform/terraform.tfvars.example terraform/terraform.tfvars` |
| **4** | Deploy infrastructure | `./scripts/deploy.sh` |
| **5** | Test governance | `python scripts/test-governance.py` |

---

## 📂 What's Inside

| Folder | Description |
|--------|-------------|
| **terraform/** | Terraform infrastructure-as-code for all GCP resources |
| **src/policy-engine/** | Cloud Function PDP for policy evaluation |
| **src/agent-gateway-middleware/** | Agent Gateway integration |
| **src/agent-monitor/** | Monitoring and telemetry |
| **src/remediator/** | Kill-switch and remediation |
| **policies/iam/** | Cloud IAM policies for agents |
| **policies/semantic-governance/** | Semantic Governance Policy (SGP) configuration |
| **policies/model-armor/** | Model Armor configuration |
| **audit-framework/** | CSA ATF and OWASP Agentic Top 10 mapping |
| **dashboard/** | Looker Studio dashboard template |
| **scripts/** | Deployment and testing scripts |

---

## 🏆 Key Artifacts

### 1. [Agent Identity Configuration](policies/iam/agent-iam-policies.yaml)

Zero-trust identity for AI agents:

- **Agent Identity** — Unique, cryptographic ID per agent[reference:37]
- **Least-Privilege** — IAM policies applied directly to agent identities
- **Context-Aware Access** — CAA policies for token theft protection[reference:38]

### 2. [Semantic Governance Policy](policies/semantic-governance/semantic-governance-policy.yaml)

Intelligent policy enforcement:

- **Tool Call Validation** — Validate tool calls against user intent[reference:39]
- **Intent Alignment** — Ensure agent actions match organizational rules[reference:40]
- **Dynamic Enforcement** — Real-time policy evaluation

### 3. [Model Armor Configuration](policies/model-armor/model-armor-config.yaml)

Runtime security:

- **Prompt Injection Protection** — Block malicious inputs[reference:41]
- **Data Leakage Prevention** — Screen tool calls and agent responses[reference:42]
- **Content Safety** — Enforce content policies[reference:43]

### 4. [VPC Service Controls](terraform/modules/networking/main.tf)

Network-level security:

- **Agent Identities in Rules** — First-class identities in ingress/egress rules[reference:44]
- **Conditional Access** — Based on Model Context Protocol attributes[reference:45]
- **Least-Privilege Network Access** — Enforce at network layer

---

## 📊 Compliance Dashboard

The Looker Studio dashboard provides real-time visibility into:

| Dashboard Section | Metrics |
|-------------------|---------|
| **Agent Inventory** | Agent Registry count, status, types |
| **Identity Compliance** | Agent Identity coverage, IAM policy status |
| **Policy Compliance** | Semantic Governance Policy violations |
| **Security Health** | Model Armor blocks, prompt injection attempts |
| **Network Security** | VPC Service Controls violations |
| **Cost Monitoring** | Agent resource consumption |

---

## 🚀 Deployment

### Prerequisites

- Google Cloud SDK installed and configured
- Terraform installed
- Python 3.11+ installed
- Gemini Enterprise Agent Platform enabled in your GCP project

### One-Click Deployment

```bash
# Clone the repository
git clone https://github.com/yourusername/agentic-ai-governance-gcp.git
cd agentic-ai-governance-gcp

# Make the deployment script executable
chmod +x scripts/deploy.sh

# Run the deployment
./scripts/deploy.sh

##Manual Deployment
```bash
# Initialize Terraform
cd terraform
terraform init

# Plan and apply
terraform plan
terraform apply

# Deploy Cloud Functions
gcloud functions deploy agent-policy-engine \
  --runtime python311 \
  --trigger-http \
  --entry-point evaluate_policy \
  --source ../src/policy-engine

# Configure Agent Registry
gcloud alpha gemini enterprise agents register \
  --agent-id=my-agent \
  --display-name="My Agent"

# Configure Semantic Governance Policy
# (via Gemini Enterprise Agent Platform console)

# Configure Model Armor
# (via Vertex AI Agent Builder console)
🔗 References
Resource	Link
Gemini Enterprise Agent Platform	Google Cloud Documentation
Agent Identity	Cloud IAM Documentation
Agent Registry	Gemini Enterprise Documentation
Agent Gateway	Gemini Enterprise Documentation
Semantic Governance Policy	Gemini Enterprise Documentation
Model Armor	Vertex AI Documentation
VPC Service Controls for Agents	Cloud Blog
📝 License
This project is licensed under the MIT License.

⭐ Star This Repository
If you find this project helpful, please star this repository and share it with your network!
