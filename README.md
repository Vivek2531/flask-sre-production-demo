# 🚀 Flask SRE Production Demo

## 📌 Overview
This repository demonstrates how a simple **Flask application** can be deployed into a **production-ready environment on AWS** with scalability, high availability, monitoring, and security.  

The project was built as part of an **SRE skills challenge** to showcase AWS fluency, deployment, observability, and cost optimization.  

---

## ✅ Current Deployment

### 🔹 Application Hosting
- Application containerized using **multi-stage Docker build** with a **distroless image** → resulting in a **lightweight, secure, and fast** container.  
- Port changed from **5000 → 8080** for compatibility with App Runner.  
- Image stored in **Amazon ECR**.  
- Deployed via **AWS App Runner** for:
  - Built-in **HTTPS** endpoint  
  - **Autoscaling** based on traffic  
  - **High availability** with no infrastructure management  

### 🔹 Security
- **AWS WAF** created using a **CloudFormation template**.  
- **AWS WAF** integrated with App Runner to protect against common web exploits (SQLi, XSS, bots)  
-  App Runner has  **TLS/HTTPS by default** so, we can have application with best security as it covers TLS as well.

### 🔹 Monitoring & Observability
**AWS X-Ray SDK** integrated into the Flask app to trace incoming requests and measure latency.  
- **Amazon CloudWatch Dashboard** created with metrics:
  - CPU utilization
  - Memory utilization
  - requests count
  - latnecy requests
  - 4xx errors
  - 5xx errors (added intentionally since application initially produced 5xx errors → metric/alarms now track them for early detection)  
- **CloudWatch Alarms** set up to trigger notifications for abnormal CPU, memory, and error spikes.  

---

### 🔹 Cost Controls
- **AWS Budget** configured at **$300/month**
- **AWS Budget Report** will be delivered every week on the Monday to make sure we are under budget.
- **SNS notifications** when spend reaches **80% of budget**  
- Deployment optimized to stay under the challenge limit of **$20/day**  

---

---

## 💰 Cost Considerations
For this Flask application, **AWS App Runner** is the most cost-effective option:
- It charges only for the **vCPU and memory used per second**, with no idle charges.  
- **EC2** would bill for full instance uptime, even when traffic is low.  
- **ECS on EC2** still requires paying for underlying instances.  
- **EKS** introduces extra **control plane costs** in addition to worker nodes.  

👉 By choosing App Runner, this application stays well under the **$20/day budget requirement**, while still meeting goals of **High availability, **scalability, security, cost optimization, and monitoring**.  

---

## 🛠️ Why App Runner?
- **Built-in HTTPS, high availability, and autoscaling** with no cluster management  
- **Fully managed** → no servers, patching, or orchestration overhead  
- **Cost-efficient** for small apps with variable traffic  
- **Faster deployment** → where we can focus on monitoring, security, caching the application, automating further deployments using ci/cd. 
- **Best fit** for this lightweight Flask application compared to ECS, EKS, or EC2  


## 🌐 Public URL
👉 [App Runner Service URL](https://gd7rq432nc.us-east-1.awsapprunner.com/) 

---

## 📂 Repository Contents
- `app.py` – Flask application code (with AWS X-Ray SDK integration)  
- `Dockerfile` – Multi-stage build using a distroless base image  
- `cloudformation/waf.yml` – CloudFormation template for AWS WAF setup  
- `.github/workflows/deploy.yml` – GitHub Actions workflow (future step)  
- `terraform/` – Infrastructure as Code skeleton (future step)  
- `README.md` – Project documentation  

---

## 🚦 Next Steps / Future Improvements
If working with an SRE team, the following would be added to improve the system further:  

### Infrastructure as Code (IaC)
- Use **Terraform** to manage:
  - App Runner Service & ECR  
  - AWS WAF rules (including optional rate limiting)  
  - CloudWatch dashboards & alarms  
  - Budgets & IAM roles
  - creating dbs, moving the application to EKS if the appliaction size increases
  - configuring the applicaton atmost security with vpc, WAF, KMS, IAM
  - creating prod and non prod environments to isolate the environements and easy for developers for pushing and testing the code

### CI/CD Pipeline
- performing automate deployments using terraform in infrastructure level for **DEV** and **QA** approval deploment to **UAT** and with release planning and after client approval for **PROD** 
-  for **Application** deployments also using Jenkins, Github Actions and ArgoCD. Integrating with testings, performing code scanning, testing and vunerability scanning code and for containers.
-  using scripting in automation for updates, cronjobs, script automations.

### Secrets & Config Management
- Store sensitive values (DB credentials, API keys) in **AWS Secrets Manager** or **SSM Parameter Store**  or **Hashicorp Vault** 

### Caching
- Integrating **Route 53 + Cloudfront** for caching with less latency for the application. If production level increases more then going higher content delivery networks as **Akamai**, **Cloudfare**. 
- 
### Advanced Monitoring
- Extend monitoring with **CloudWatch Logs Insights** or external tools like **Datadog / ELK**
- Setting up proper monitoring tools like Prometheus, Grafana, cloudwatch, Datadog, Dynatrace.
- Define **SLOs/SLIs** and track error budgets  

### Scaling & Performance
- Fine-tune App Runner scaling policies  
- Add **RDS** for persistent storage  
- Add **ElastiCache (Redis)** for faster performance  

---

## 📌 Assumptions
- Application is lightweight, Flask-based with low-to-moderate traffic  
- Required: secure (HTTPS + WAF), monitored, scalable, and within cost cap  
- Focus was on **deploying quickly and securely** while optimizing for **cost efficiency**  

---

## 📊 References
- [AWS App Runner](https://docs.aws.amazon.com/apprunner/)  
- [AWS WAF](https://docs.aws.amazon.com/waf/)  
- [AWS X-Ray](https://docs.aws.amazon.com/xray/)  
- [AWS Budgets](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html)  
- [CloudWatch Dashboards](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Dashboards.html)  
