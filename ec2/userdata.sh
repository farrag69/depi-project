#!/bin/bash
set -ex

# ----------------------------
# Update system
# ----------------------------
yum update -y

# ----------------------------
# Install Docker
# ----------------------------
yum install -y docker
systemctl enable docker
systemctl start docker
usermod -aG docker ec2-user

# ----------------------------
# Install Java (required for Jenkins)
# ----------------------------
amazon-linux-extras install java-openjdk17 -y || yum install -y java-17-amazon-corretto

# ----------------------------
# Install Jenkins repo
# ----------------------------
wget -O /etc/yum.repos.d/jenkins.repo \
    https://pkg.jenkins.io/redhat-stable/jenkins.repo
rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key

# ----------------------------
# Install Jenkins
# ----------------------------
yum install jenkins -y
systemctl enable jenkins
systemctl start jenkins

# ----------------------------
# Install Docker Compose (optional)
# ----------------------------
curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" \
    -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
