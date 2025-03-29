

### **Kubernetes Practical Interview Test**  
📌 **Duration:** 90 minutes  
📌 **Environment:** Candidate should have access to a Kubernetes cluster (Minikube, Kind, or a cloud-based cluster like GKE/EKS/AKS).  

---

## **Section 1: Basic Deployment (20 mins)**  
✅ **Task 1: Create a Deployment**  
- Create a **Deployment** named `web-app` using the `nginx:latest` image.  
- Ensure that the Deployment has **3 replicas**.  
- The containers should expose port **80**.  
- The Deployment should have a label: `app=web-app`.  
- The pods should have an environment variable `ENV=production`.  

**Expected Output:**  
- `kubectl get deployments` should show `web-app` with 3 replicas.  
- `kubectl get pods -l app=web-app` should return 3 pods.  

---

## **Section 2: Networking & Services (15 mins)**  
✅ **Task 2: Create a Service**  
- Expose the `web-app` Deployment using a **ClusterIP** Service named `web-service`.  
- The Service should be accessible on port **80** and route traffic to the correct pod port.  

**Expected Output:**  
- `kubectl get svc web-service` should return a ClusterIP service.  
- `kubectl describe svc web-service` should show endpoints mapped to the pods.  

---

## **Section 3: Configurations using ConfigMaps & Secrets (20 mins)**  
✅ **Task 3: Create a ConfigMap & Secret**  
1. Create a **ConfigMap** named `app-config` with:  
   ```
   APP_NAME=MyK8sApp
   APP_VERSION=1.0
   ```  
2. Create a **Secret** named `db-credentials` with:  
   ```
   DB_USER=admin
   DB_PASSWORD=supersecret
   ```  
3. Modify the `web-app` Deployment to:  
   - Inject ConfigMap values as environment variables.  
   - Mount the Secret as an environment variable.  

**Expected Output:**  
- `kubectl get configmap app-config` should show the ConfigMap.  
- `kubectl get secret db-credentials` should show a Secret.  
- `kubectl exec -it <web-app-pod> -- printenv | grep APP_` should display ConfigMap values.  
- `kubectl exec -it <web-app-pod> -- printenv | grep DB_` should display Secret values.  

---

## **Section 4: Troubleshooting & Debugging (15 mins)**  
✅ **Task 4: Debug a Broken Pod**  
- A Pod named `faulty-app` is failing. Run:  
  ```
  kubectl get pods
  kubectl describe pod faulty-app
  kubectl logs faulty-app
  ```  
- Identify and fix the issue (e.g., incorrect image, missing env variable, or port conflict).  

**Expected Output:**  
- The candidate should identify the issue and deploy a working Pod.  

---

## **Section 5: Stateful Workload (20 mins)**  
✅ **Task 5: Deploy a StatefulSet with Persistent Storage**  
1. Create a **StatefulSet** named `db` using the `mysql:5.7` image.  
2. Use a **PersistentVolumeClaim (PVC)** for storage.  
3. Set an environment variable `MYSQL_ROOT_PASSWORD=mysecret` from a Secret.  
4. Ensure the StatefulSet has 2 replicas.  

**Expected Output:**  
- `kubectl get statefulset` should show `db` with 2 replicas.  
- `kubectl get pvc` should show a dynamically provisioned volume.  
- The database should retain data after pod restarts.  

