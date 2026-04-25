# Docker-Lab

Hands-on Lab: Building a Secure Docker ApplicationIntroduction
This lab will guide you through the process of building a Dockerized application, intentionally introducing common security vulnerabilities, and then hardening it using best practices. You will learn to identify and mitigate risks associated with Docker images and runtime configurations.

Learning Objectives:

• Understand common Docker security vulnerabilities.
• Learn to create a Dockerfile with security flaws.
• Utilize security scanning tools (Trivy) to identify vulnerabilities.
• Apply Docker security best practices to harden a Dockerfile.
• Verify the effectiveness of security measures.

Prerequisites:

• Docker Desktop or Docker Engine installed and running.
• Basic familiarity with Docker commands (`docker build`, `docker run`).
• A text editor (e.g., VS Code, Sublime Text).

Part 1: Building a “Vulnerable” Application
In this section, we will create a simple Python Flask application and containerize it using a Dockerfile that incorporates several common security anti-patterns.

Step 1.1: Create the Flask Application
Create a directory named `vulnerable-app` and inside it, create a file named `app.py` with the following content:

```python
# app.pyfrom flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
return "<h1>Hello, Cyber Security Club! This is a VULNERABLE app.</h1>"

@app.route('/secret')
def secret():
# Insecurely exposing an environment variable
return f"<h1>The secret is: {os.environ.get('MY_SECRET', 'No secret found')}</h1>"

if __name__ == '__main__':
# Running on all interfaces, potentially insecure
app.run(host='0.0.0.0', port=5000)
```

Next, create a `requirements.txt` file in the same directory:

```bash
# requirements.txt
Flask==2.3.2
```
￼
Step 1.2: Create the “Bad” Dockerfile
In the `vulnerable-app` directory, create a file named `Dockerfile.bad` with the following content:
```bash 
FROM python:latest

# Running as root user by default

# Copying all application files
COPY . /app

# Setting working directory
WORKDIR /app

# Installing dependencies
RUN pip install -r requirements.txt

# Exposing port 5000
EXPOSE 5000

# Running the application as root
CMD ["python", "app.py"]
```

Step 1.3: Build the Vulnerable Image
Navigate to the `vulnerable-app` directory in your terminal and build the Docker image:
```bash
docker build -t vulnerable-app:bad -f Dockerfile.bad .
```
￼
Step 1.4: Run the Vulnerable Container
Run the container and expose the application on port 8080 of your host machine:

```bash
docker run -d -p 8080:5000 --name bad-app -e MY_SECRET="super_secret_key_123" vulnerable-app:bad
```
￼
Open your browser and navigate to `http://localhost:8080/` and `http://localhost:8080/secret` to confirm the application is running and the secret is exposed.

Part 2: Scanning for Vulnerabilities
Now that we have a vulnerable application, we will use Trivy to scan the Docker image and identify its security flaws.

Step 2.1: Install Trivy
If you don’t have Trivy installed, follow the instructions for your operating system:

Linux (Debian/Ubuntu):
```bash
sudo apt-get install wget apt-transport-https gnupg -ywget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install trivy -y
```

macOS (Homebrew):
```bash
brew install trivy
```
￼
Windows (Scoop):

```bash
scoop install trivy
```

Step 2.2: Scan the Vulnerable Image
Run Trivy against your `vulnerable-app:bad` image:
```bash
trivy image vulnerable-app:bad
```

Analyze the Output:

• Observe the number of critical, high, medium, and low vulnerabilities.
• Pay attention to the specific CVEs, their descriptions, and recommended fixes.
• Note any exposed secrets or misconfigurations reported by Trivy.

Part 3: Hardening the Application
In this part, we will refactor the Dockerfile to address the vulnerabilities identified by Trivy and implement Docker security best practices.

Step 3.1: Create the “Good” Dockerfile
Create a file named `Dockerfile.good` in the `vulnerable-app` directory with the following content:
```bash
FROM python:3.11-alpine AS builder

# Create a non-root user and group
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Set working directory
WORKDIR /app

# Copy only necessary files for dependencies first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY app.py .

# Switch to the non-root user
USER appuser

# Expose port (optional, good for documentation)
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
```

Step 3.2: Build the Hardened Image
Build the new, hardened Docker image:

```bash
docker build -t vulnerable-app:good -f Dockerfile.good .
```
￼
Step 3.3: Run the Hardened Container
Run the hardened container. Notice we are still passing the secret via an environment variable, but the image itself is more secure.

```bash
docker run -d -p 8081:5000 --name good-app -e MY_SECRET="super_secret_key_123" vulnerable-app:good
```
￼
Open your browser and navigate to `http://localhost:8081/` and `http://localhost:8081/secret` to confirm the application is still running correctly.

Part 4: Verifying the Fix
Finally, we will re-scan the hardened image with Trivy to confirm that the vulnerabilities have been mitigated.

Step 4.1: Re-scan the Hardened Image
Run Trivy against your `vulnerable-app:good` image:

```bash
trivy image vulnerable-app:good
```
￼
Compare the Output:

• Observe the significant reduction or elimination of critical and high-severity vulnerabilities.
• Note how using a minimal base image and a non-root user drastically improves the security posture.

Step 4.2: Clean Up
Stop and remove the containers and images to free up resources:
```bash
docker stop bad-app good-appdocker rm bad-app good-app
docker rmi vulnerable-app:bad vulnerable-app:good
```
Conclusion
By following Docker security best practices, such as using minimal base images, pinning versions, running as non-root users, and regularly scanning images, you can significantly reduce the attack surface and improve the overall security of your containerized applications. Remember that security is an ongoing process, and continuous vigilance is key.

References
• [1] Aikido. (n.d.). 9 Common Docker Container Security Vulnerabilities & Fixes. Retrieved from https://www.aikido.dev/blog/docker-container-security-vulnerabilities <br/>
• [2] Aqua Security. (n.d.). Trivy Documentation. Retrieved from https://aquasecurity.github.io/trivy/v0.49/<br/>
• [3] Docker. (n.d.). Docker Security. Retrieved from https://docs.docker.com/engine/security/<br/>
