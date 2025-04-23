# 📘 Kubernetes & Docker Assignment: Django & MySQL Deployment

## 🚀 Overview

In this assignment, you will build and deploy a containerized Django web application backed by a MySQL database. The two components will be hosted on a public cloud Kubernetes cluster, following production-style best practices.

You’ll work with **Docker**, **Kubernetes ConfigMaps**, **Secrets**, **Deployments**, and **Services**, leveraging **MySQL** as the backend. This simulates a real-world DevOps workflow using infrastructure-as-code principles.

---

## 📂 What’s Provided

- A basic Django project with one app.
- A default `settings.py` file (use database values from here).
- Example models and views for testing.

---

## ✅ Assignment Requirements

### 1. 🐳 Containerization with Docker

- Create a `Dockerfile` to containerize the Django application.
- Your Docker image must:
  - Install dependencies from `requirements.txt`
  - Automatically run database migrations
  - Start the Django development server on port **8000**

---

### 2. Architectural Diagram 
![Architecture Diagram](django_app.io)

### 3. ⚙️ Kubernetes Manifests

#### a. 🧾 ConfigMap

- Create a ConfigMap with the following keys:
  - `MYSQL_HOST`
  - `MYSQL_PORT`
  - `MYSQL_DATABASE`
- 💡 *Hint:* Use the environment variable names referenced in `django_project/settings.py`.

#### b. 🔐 Secret

- Create a Secret containing database credentials:
  - `MYSQL_USER: django`
  - `MYSQL_PASSWORD: securepassword`

#### c. 🐘 MySQL Deployment

- Deploy MySQL using the `mysql:8` image.
- Use environment variables from the ConfigMap and Secret.

#### d. 🌐 Django Deployment

- Deploy the Django application using your custom Docker image.
- Expose container port **8000**
- Load environment variables from both the ConfigMap and Secret.

#### e. 🌉 Kubernetes Services

- Create a **ClusterIP** service for MySQL on port **3306**
- Create a **LoadBalancer** service for Django:
  - Service port: **80**
  - Target port: **8000**

---

## 🔍 Validation & Testing

- Ensure the Django app connects to the MySQL database using the provided credentials.
- Use the following command to retrieve the external IP of your LoadBalancer:

  ```bash
  kubectl get svc
Access the Django Admin Panel at:
http://EXTERNAP-IP/admin
