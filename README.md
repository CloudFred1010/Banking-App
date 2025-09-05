# Banking Demo with DevSecOps on AWS

## 1. Project Overview
This project demonstrates how to implement a **DevSecOps pipeline in AWS** that aligns with the responsibilities of an AWS Cloud Engineer in a fintech environment.

It uses a **banking demo application** (FastAPI + PostgreSQL) as the workload to showcase how security is embedded from **code → pipeline → cloud infrastructure → monitoring & governance**.

The design ensures compliance with **ISO 27001, PCI DSS, GDPR, and NIST CSF**, while embedding strategic principles of **security by design, automation, and continuous improvement**.

---

## 2. Architecture at a Glance

### Application
- Banking Demo App (FastAPI + Postgres) with APIs for:
  - Account creation
  - Loan issue
  - Card issue
  - Transaction history
  - Loan repayment (batch workflow)

Runs in two modes:
1. **Local**: Docker Compose for development and testing.
2. **Production**: AWS ECS Fargate with Aurora PostgreSQL backend.

### Infrastructure (IaC)
Provisioned with Terraform:
- VPC with private/public subnets and NAT Gateway.
- ECS Fargate cluster for app containers.
- Aurora PostgreSQL (encrypted, Multi-AZ).
- S3 + KMS for document storage.
- API Gateway + Cognito for secure API access.
- CloudFront + WAF + Shield for DDoS and OWASP protection.
- CloudTrail + Config + Security Hub for compliance.
- EventBridge + Step Functions for nightly loan repayment jobs.

### CI/CD (GitHub Actions)
- Code → Build → Test → Deploy fully automated.
- Security gates block insecure builds.
- Terraform plans require approval before apply.
- Canary/blue-green deployments for safer releases.

### Security & Governance
- **Zero Trust** enforced: Cognito MFA for customers, Entra ID/OIDC for staff.
- Secrets Manager stores all DB/API credentials.
- GuardDuty + Inspector + Macie for threat detection and sensitive data protection.
- KMS encryption everywhere (S3, RDS, Secrets, logs).
- WAF rules aligned to OWASP Top 10.
- Audit evidence mapped to ISO 27001, PCI DSS, and NIST CSF.

---

## 3. Key Security Domains

### 3.1 Application Security & SSDLC
- Secure SDLC integrated into CI/CD.
- Automated testing for OWASP Top 10 vulnerabilities.
- SAST, SCA, IaC scanning on every commit.
- DAST (ZAP/Playwright) post-deployment.

### 3.2 Secrets Management
- AWS Secrets Manager for DB credentials, API keys, TLS certs.
- Automated rotation policies.
- GitHub secret scanning + pre-commit hooks to prevent leaks.

### 3.3 Logging & Observability
- Centralised logs in CloudWatch Logs + CloudTrail.
- Tracing with AWS X-Ray across services.
- Immutable S3 logging for audit evidence.
- Alerts to Slack/Teams via SNS.

### 3.4 Zero Trust Security
- Cognito MFA + JWT for customers.
- OIDC with Entra ID for internal staff.
- Micro-segmentation at VPC/security group level.
- IAM least privilege with no wildcards.

### 3.5 Supply Chain Security
- Dependency scanning (Snyk).
- SBOM generation (Syft/Grype).
- Container image scanning (Trivy) on build.
- IaC scanning (Checkov/TerraScan).

### 3.6 Testing Strategy
- Unit tests → PyTest.
- API/UI tests → Playwright.
- SAST → Bandit / CodeQL.
- DAST → ZAP scans.
- IaC tests → Checkov policy enforcement.
- Quality gates prevent insecure builds.

### 3.7 Governance & Reporting
- Compliance mapped to ISO 27001, PCI DSS, GDPR, NIST CSF.
- Security posture dashboards in Security Hub + GuardDuty.
- Audit dashboards in QuickSight for leadership.

---

## 4. Threat Modelling (STRIDE)
- **Spoofing** → Cognito auth, OIDC validation, MFA.
- **Tampering** → Signed Docker images, Terraform in Git with approvals.
- **Repudiation** → CloudTrail immutable logging.
- **Information Disclosure** → TLS 1.2+, KMS encryption, Secrets Manager.
- **Denial of Service** → WAF + Shield Advanced + autoscaling.
- **Elevation of Privilege** → IAM least privilege + JIT role assumption.

---

## 5. CI/CD Pipeline Workflow

### Commit Stage
- Pre-commit hooks: lint, secrets check (Gitleaks), dependency checks.
- Developer pushes code → GitHub Actions triggers.

### Security Stage
- **SAST**: Bandit / CodeQL scan.
- **SCA**: Snyk dependency check.
- **IaC**: Checkov Terraform scan.
- **Container**: Trivy CVE scan.
- **SBOM**: Syft/Grype generation.

### Build & Deploy Stage
- Multi-stage Docker build (non-root user, minimal base).
- Push image to AWS ECR.
- Terraform plan → approval → apply.
- ECS deployment with blue-green/canary strategy.

### Post-Deploy Stage
- DAST: OWASP ZAP scan against live app.
- Playwright API/UI tests.
- CloudWatch alarms checked.
- Compliance checks via AWS Config + Security Hub.

---

## 6. Network & Compute Security

### ECS Security
- Tasks run with IAM roles (no instance creds).
- Containers run as non-root, read-only filesystem.
- ECR image scanning enabled.

### VPC & Network Security
- Private subnets for RDS.
- ALB in public subnets, ECS tasks in private subnets.
- WAF rules against OWASP Top 10.
- Security groups: least privilege, deny by default.

---

## 7. Incident Management
- GuardDuty detects threats (e.g. unusual API calls).
- Automated Lambda playbooks isolate ECS tasks or rotate creds.
- Incident workflow: triage → contain → eradicate → recover.
- Post-incident reviews logged in Confluence/Jira backlog.

---

## 8. Cost Management
- CloudWatch + Trusted Advisor cost dashboards.
- S3 lifecycle → archive logs to Glacier.
- Aurora auto-scaling and storage rightsizing.
- Monthly FinOps review with Finance/Tech.

---

## 9. Tools & Services Summary

### Security Tools
- **SAST**: Bandit, CodeQL
- **DAST**: OWASP ZAP
- **SCA**: Snyk
- **Container**: Trivy
- **IaC**: Checkov / TerraScan
- **SBOM**: Syft / Grype
- **Secrets**: Gitleaks

### AWS Native
- Security Hub, GuardDuty, Inspector, Macie
- Cognito (MFA, JWT auth)
- Secrets Manager
- CloudWatch + X-Ray
- WAF + Shield
- Config (compliance)

### Governance
- Compliance mapped to ISO 27001, PCI DSS, GDPR, NIST CSF
- Risk dashboards in Security Hub + QuickSight
- Incident tracking in Jira/Confluence

---
