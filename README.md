# 🚀 Flask SRE Production Demo

## 📌 Overview
This repository demonstrates how a simple **Flask application** can be deployed into a **production-ready environment on AWS** with scalability, high availability, monitoring, and security.  

The project was built as part of an **SRE skills challenge** to showcase AWS fluency, deployment, observability, and cost optimization.  

---

## ✅ Current Deployment

### 🔹 Application Hosting
- Application containerized using **multi-stage Docker build** with a **distroless image** which results in a **lightweight, secure, and fast** container.  
- Port changed from **5000 → 8080** for compatibility with App Runner.  
- Image stored in **Amazon ECR**.  
- Deployed via **AWS App Runner** for:
  - Built-in **HTTPS** endpoint  
  - **Autoscaling** based on traffic  
  - **High availability** with no infrastructure management  

### 🔹 Security
- Created **AWS WAF** using a **CloudFormation template**.  
- **AWS WAF** integrated with App Runner to protect against common web exploits (SQLi, XSS, bots)  
-  App Runner has  **TLS/HTTPS by default** so, we can have application with best security as it covers TLS as well.

### 🔹 Monitoring & Observability
**AWS X-Ray SDK** integrated into the Flask app to trace incoming requests and measure latency.  
- **Amazon CloudWatch Dashboard** created with metrics:
  - CPU utilization
  - Memory utilization
  - requests count
  - latency requests
  - 4xx errors
  - 5xx errors - Intially when the app runner is ready. There are no 5xx related erros. so I myself created reated a crash route (/crash) to generate 500 errors, so that CloudWatch allows     me to create the metric and  alarms. 
- **CloudWatch Alarms** set up to trigger notifications for abnormal CPU, memory, and error spikes.  

---

### 🔹 Cost Controls
- **AWS Budget** configured at **$300/month**
- **AWS Budget Report** will be delivered every week on the Monday to make sure we are under budget.
- **SNS notifications** when spend reaches **80% of budget**  
- Deployment optimized to stay under the challenge limit of **$20/day**  

---

## 💰 Cost Considerations
For this Flask application, **AWS App Runner** is the most cost-effective option:
- As it charges only for the **vCPU and memory used per second**, with no idle charges.
- **EC2** would bill for full instance uptime, even when traffic is low.  
- **ECS on EC2** still requires paying for underlying instances.  
- **EKS** introduces extra **control plane costs** in addition to worker nodes.  

👉 By choosing App Runner, this application stays well under the **$20/day budget requirement**, while still meeting goals of **High availability, **scalability, security, cost optimization, and monitoring**.  

---

## 🛠️ Why App Runner?
- **Built-in HTTPS, high availability, and autoscaling** with no cluster management  
- **Fully managed** → no servers, patching, or orchestration overhead  
- **Cost-efficient** for small apps with variable traffic  
- **Faster deployment** → where we can focus on monitoring, security, focusing on caching and performance., automating further deployments using CI/CD. 
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
If I'm working with an SRE team, the following would be added to improve the system further:  

## Performing Infrastructure/Application level deployments with complete automation.

### Infrastructure as Code (IaC)
- Use **Terraform** to manage:
  - Creating entire Infrastructure using **Terraform**.
  - Using modules, workspaces to create secure infrstructure with prod and non prod environments.
  - Creating Statefile in S3 with dynamoDB as backend and Hashicorp Vault for using storing the passwords, securing the API keys and IAM keys and etc.
  - If required we can also use **Ansible** to maanage the virtual machines.

### CI/CD Pipelines
- performing automate deployments using terraform in infrastructure level for **DEV** and **QA** approval deployment to **UAT** and with release planning and after client approval for **PROD** 
-  for **Application** deployments also using Jenkins, Github Actions and ArgoCD. Integrating with testings, performing code scanning, testing and vulnerability scanning code and for containers.
-  using scripting in automation for updates, cronjobs, script automations.

**Deployment Strategies**
- Implement Blue/Green deployments to reduce downtime and risk by running two environments in parallel and switching traffic only after the new version is validated.
- Use Canary deployments to roll out changes gradually to a small percentage of users first, monitor performance, then scale up to all users if stable.
- Introduce Automated Rollbacks so that if errors or latency increase after a release, traffic automatically reverts to the previous stable version.
   
### Advanced Monitoring
- Extend monitoring with **CloudWatch Logs Insights** or external tools like **Datadog / ELK**
- Setting up proper monitoring tools like Prometheus, Grafana, cloudwatch, Datadog, Dynatrace.
- Define **SLOs/SLIs** and track error budgets.

### Security & Encryption
- Managing sensitive data such as database credentials and API keys using AWS Secrets Manager or SSM Parameter Store, instead of hardcoding values or storing them in plain text.
- Enable AWS KMS encryption for all data at rest (logs, backups, S3 objects, RDS databases) to meet compliance and protect sensitive information.
- Ensure TLS/HTTPS is enforced for all traffic in and out of the application.
- Use IAM roles with least privilege and rotate access keys regularly to minimize security risks.
- Extend AWS WAF with advanced rules such as rate limiting, geo-blocking, and custom signatures to provide stronger protection against DDoS and targeted attacks.
   
### Scaling & Performance
- Using Auto Scaling with best algorithem which routers the traffic as per the traffic
- Using RDS Database with multi region for high availability
- Add **ElastiCache (Redis)** for RDS to get faster performance
- Use Route 53 + CloudFront for caching and reducing application latency. For larger-scale production workloads, consider integrating advanced CDNs such as Akamai or Cloudflare to further improve global performance and reliability. 

### Cost Optimization
- Implementing serverless functions (AWS Lambda) which figure outs the resources which are not is use and eliminating them for cost optimization
- Configure auto-scaling policies so resources scale down during low traffic periods.
- If needed using Savings Plans or Reserved Instances for predictable workloads to lower long-term costs.

### Incident Management
- Creating an incident management process with runbooks, escalation paths, and on-call rotations so issues can be identified, communicated, and resolved quickly with minimal downtime.

### Documentation & Knowledge Sharing
- Creating a clear documentation about release plans, deployment processes, and architecture diagrams so new joiners can get up to speed quickly and the team follows a consistent approach.
  
### Disaster Recovery
- Setting up automated backups and snapshots for critical resources like databases and application state, so the system can be quickly restored in case of failures.
- Implementing multi-region deployment or failover strategies to keep the application available even if an AWS region goes down.

## 📊 References
- [AWS App Runner](https://docs.aws.amazon.com/apprunner/)  
- [AWS WAF](https://docs.aws.amazon.com/waf/)  
- [AWS X-Ray](https://docs.aws.amazon.com/xray/)  
- [AWS Budgets](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html)  
- [CloudWatch Dashboards](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Dashboards.html)  
