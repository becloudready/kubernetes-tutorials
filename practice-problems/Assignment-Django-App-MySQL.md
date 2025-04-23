# Kubernetes & Docker Assignment: Django & MySQL Deployment


## Overview

In this assignment, you are required to build a containerized application that consists of a Django web application and a MySQL database. The two components will be deployed on a public cloud Kubernetes cluster with proper configuration management. You’ll work with Docker, ConfigMaps, Secrets, Services, and Deployments — and use a MySQL backend in a production-style environment.

## 📦 What’s Provided

- A basic Django project with a single app.
- Default `settings.py` (Use the Database values from here).
- Example models and views for testing.

Your task is to containerize the Django application, build and push its Docker image to Docker Hub, and deploy both the Flask app and MySQL database on Kubernetes following the guidelines described below.

## Assignment Requirements
1. **Containerization & Docker:**
   - Write a `Dockerfile` to containerize the Django application.
   - The image should:
   - Install dependencies from `requirements.txt`.
   - Run migrations automatically.
   - Start the Django development server on port 8000.

2. **Kubernetes Manifests:**
   - **ConfigMaps:**
     - Create a ConfigMap with data containing MYSQL_HOST, MYSQL_PORT and MYSQL_DATABASE.
     - hint (refer to values in django_project/settings.py file)  
   - **Secrets:**
     - Create a Secret for the database credentials. (The correct values are: `MYSQL_USER: django`, `MYSQL_PASSWORD: securepassword`.)
   - **MySQL Deployment:**
     - Deploy a Mysql pod use image mysql:8, use the env variables created via ConfigMap and Secret in the above steps.
   - **Django Deployment:**
     - Deploy the Django application using a Deployment use containerport 8000.
     - Configure the Deployment to load environment variables from the ConfigMap and Secret.
   - **Services:**
     -  Expose both MySQL (ClusterIP) and Django (LoadBalancer) services.
     - Create a ClusterIP Service for MySQL (Port 3306) Loadbalancer service port 80 and target port 8000.
    
3. **Validation & Testing:**
   - Ensure that the Django application can connect to the MySQL database using the provided credentials.
   - Use kubectl get svc to get the EXTERNAL-IP of your LoadBalancer.
     Then open: http://<EXTERNAL-IP>/admin.
