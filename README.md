# 159-Unauthorized-Cloud-Resource-Provisioning-Detection
# Unauthorized Cloud Resource Provisioning Detection

An advanced cloud security analytics and monitoring framework designed to detect, flag, and mitigate unauthorized or shadow-it resource provisioning across multi-cloud environments (AWS, Azure, GCP).

---

## 📖 Overview
In modern cloud infrastructures, unauthorized resource provisioning (such as rogue VMs, unapproved storage buckets, or unauthorized crypto-mining clusters spun up via compromised credentials) poses severe financial and security risks. Traditional perimeter defenses often fail to catch these internal anomalies. 

The **Unauthorized Cloud Resource Provisioning Detection** project provides a continuous monitoring framework. By analyzing audit logs, API telemetry (e.g., AWS CloudTrail, Azure Activity Logs), and resource creation velocity, this system empowers cloud security teams and DevOps engineers to instantly spot policy violations, rogue deployments, and potential privilege escalation attempts.

---

## 🔑 Key Features & Objectives
* **Real-Time Audit Log Analysis:** Ingests and parses cloud provider activity logs to monitor resource creation events (`RunInstances`, `CreateBucket`, etc.).
* **Anomaly & Policy Detection:** Flags out-of-policy provisioning, unusual geographic locations, and unexpected volume spikes.
* **Risk Scoring & Alerting:** Evaluates provisioning requests against baseline organizational profiles and IAM permission matrices.
* **Automated Remediation Support:** Generates actionable security alerts and incident logs to streamline containment workflows.

---

## 🛠️ Core Architecture & Pipeline

1. **Log Ingestion & Normalization:** 
   * Collects raw activity logs and event streams from cloud environment audit trails.
2. **Feature Extraction & Behavioral Modeling:** 
   * Computes user-specific behavioral baselines, frequency of resource creation, and API call characteristics.
3. **Detection & Classification Engine:** 
   * Applies heuristic rules and machine learning anomaly detection models to flag unauthorized infrastructure changes.
4. **Reporting & Dashboards:** 
   * Outputs structured incident logs and visualization metrics tracking unauthorized provisioning attempts.

---

## 🛠️ Tech Stack
* **Language:** Python
* **Data Processing & Analysis:** Pandas, NumPy
* **Cloud Parsing & SDKs:** Boto3 (for AWS analysis) / Python cloud logging utilities
* **Visualization:** Matplotlib, Seaborn

---

## ⚙️ Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Delightech25/159-Unauthorized-Cloud-Resource-Provisioning-Detection.git](https://github.com/Delightech25/159-Unauthorized-Cloud-Resource-Provisioning-Detection.git)
   cd 159-Unauthorized-Cloud-Resource-Provisioning-Detection
