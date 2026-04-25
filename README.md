# 🐳 Docker Security Lab: From Vulnerable to Verifiable

[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![Security: Trivy](https://img.shields.io/badge/Security-Trivy-blueviolet?style=for-the-badge)](https://aquasecurity.github.io/trivy/)

## 📖 Overview
This hands-on lab demonstrates the "Shift Left" security philosophy. You will build a Python Flask application, intentionally introduce common Docker misconfigurations, and then systematically harden the container using industry best practices.

### 🎯 Learning Objectives
* **Identify** common Dockerfile anti-patterns (Root execution, bloated base images, etc.).
* **Analyze** image layers and vulnerabilities using **Trivy**.
* **Implement** security mitigations including Multi-stage builds and Non-root users.
* **Validate** security posture improvements through automated scanning.

---

## 🏗️ Lab Architecture
The lab is divided into three distinct phases:
1.  **Phase 1: The Vulnerable Build** – Focuses on functionality over security.
2.  **Phase 2: Vulnerability Analysis** – Using static analysis to find "hidden" risks.
3.  **Phase 3: The Hardened Build** – Applying the principle of least privilege.

---

## 🚀 Getting Started

### Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) or Engine installed.
* [Trivy](https://aquasecurity.github.io/trivy/v0.49/getting-started/installation/) installed on your local machine.

### Installation
```bash
git clone https://github.com/cperry183/Docker-Lab.git
cd Docker-Lab
```

---

## 🧪 Lab Exercises

### Part 1: Building the "Bad" Image
The initial image uses `python:latest`, runs as `root`, and includes unnecessary build tools.
```bash
# Build the vulnerable image
docker build -t docker-lab:vulnerable -f docker/Dockerfile.bad .

# Run the container
docker run -d -p 8080:5000 --name bad-app -e MY_SECRET="super_secret_123" docker-lab:vulnerable
```
*Explore the app at `http://localhost:8080`.*

### Part 2: Security Scanning
Use Trivy to see why `python:latest` is a risky choice.
```bash
trivy image docker-lab:vulnerable
```

### Part 3: Hardening the Container
We refactor the build using **Alpine Linux**, **Multi-stage builds**, and a **Non-privileged user**.
```bash
# Build the hardened image
docker build -t docker-lab:secure -f docker/Dockerfile.good .

# Compare the size and security results
trivy image docker-lab:secure
```

---

## 🛡️ Security Best Practices Applied
| Feature | Vulnerable Version | Hardened Version |
| :--- | :--- | :--- |
| **Base Image** | `python:latest` (Debian-based) | `python:3.11-alpine` (Minimal) |
| **User Privileges** | `root` (Default) | `appuser` (Non-root) |
| **Layer Optimization** | Bulky, includes build tools | Multi-stage (Production only) |
| **Secret Handling** | Exposed in ENV | *Note: Use Docker Secrets/Vault in Prod* |

---

## 🧹 Cleanup
To remove all lab artifacts:
```bash
docker stop bad-app secure-app
docker rm bad-app secure-app
docker rmi docker-lab:vulnerable docker-lab:secure
```

---

## 📚 References
* [Docker Security Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
* [Aqua Security Trivy Docs](https://aquasecurity.github.io/trivy/)
* [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker)
