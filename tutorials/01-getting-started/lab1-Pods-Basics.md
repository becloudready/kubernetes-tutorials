### **Lab: Hands-On with Kubernetes Pods**

This lab is designed to help students experiment with Kubernetes Pods, understand their behavior, and learn how to manage them.

---

### **Objective**
By the end of this lab, students will:
1. Create and manage Kubernetes Pods.
2. Understand Pod specifications.
3. Experiment with multi-container Pods.
4. Observe and debug Pod behavior using Kubernetes commands.

---

### **Prerequisites**
1. A Kubernetes cluster (e.g., Minikube, Kind, or a cloud-based cluster).
2. `kubectl` command-line tool installed and configured.
3. Basic YAML knowledge.

---

### Setup kubectl command

Download Latest Kubeconfig

URL = https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/

Setup your environment variable

Linux/MacOS

```
export KUBECONFIG=<PATH TO KUBECONFIG FILE>
```

In Powershell

```
$env:KUBECONFIG="<Path to your folder>\quick-labs-0-kubeconfig.yaml"
```

Ensure it is working

```
 kubectl.exe get no
NAME                 STATUS   ROLES    AGE   VERSION
quick-labs-0-aa0mx   Ready    <none>   21m   v1.32.1
quick-labs-0-aaalz   Ready    <none>   11h   v1.32.1
quick-labs-0-aaapc   Ready    <none>   11h   v1.32.1
```

### **Step 1: Create a Simple Pod**

#### 1. Write a Pod YAML Manifest
Create a file named `simple-pod.yaml`:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-first-pod
  labels:
    app: demo
spec:
  containers:
  - name: nginx
    image: nginx:latest
    ports:
    - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: my-first-service
spec:
  selector:
    app: demo
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: LoadBalancer

```
This YAML file defines two Kubernetes resources:

1. **Pod** (`my-first-pod`):
2. **Service** (`my-first-service`):

---

### **Explaination - Pod Definition**
The first part of the YAML defines a **Pod**, which is the smallest deployable unit in Kubernetes.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-first-pod
  labels:
    app: demo
```
- **`apiVersion: v1`** – Specifies the API version used.
- **`kind: Pod`** – Defines this resource as a Kubernetes Pod.
- **`metadata`**:
  - **`name: my-first-pod`** – Assigns a name to the Pod.
  - **`labels`**:
    - **`app: demo`** – Labels help with organizing and selecting resources.

```yaml
spec:
  containers:
  - name: nginx
    image: nginx:latest
    ports:
    - containerPort: 80
```
- **`spec`** – Describes the desired behavior of the Pod.
- **`containers`** – Defines the list of containers within the Pod.
  - **`name: nginx`** – Container is named `nginx`.
  - **`image: nginx:latest`** – Uses the latest Nginx container image from Docker Hub.
  - **`ports`**:
    - **`containerPort: 80`** – Exposes port 80 inside the container.

---

### **Explaination - Service Definition**
The second part of the YAML defines a **Service**, which provides networking and load balancing.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-first-service
```
- **`apiVersion: v1`** – Specifies the API version used.
- **`kind: Service`** – Defines this resource as a Service.
- **`metadata`**:
  - **`name: my-first-service`** – Assigns a name to the Service.

```yaml
spec:
  selector:
    app: demo
```
- **`spec`** – Describes the desired behavior of the Service.
- **`selector`**:
  - **`app: demo`** – Matches any Pod with the label `app: demo`, which in this case selects `my-first-pod`.

```yaml
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
```
- **`ports`**:
  - **`protocol: TCP`** – Uses TCP for communication.
  - **`port: 80`** – Exposes port 80 on the Service.
  - **`targetPort: 80`** – Forwards traffic to port 80 inside the matching Pods.

```yaml
  type: LoadBalancer
```
- **`type: LoadBalancer`** – Exposes the Service externally with a cloud provider-managed load balancer.

---

#### 2. Apply the Manifest
```bash
kubectl apply -f simple-pod.yaml
```

Output running from Windows Terminal
```
kubectl.exe apply -f .\simple-pod.yaml
pod/my-first-pod created
service/my-first-service created
```

#### 3. Verify the Pod
```
kubectl get pods
```
Example 
```
kubectl.exe get pods
NAME           READY   STATUS    RESTARTS   AGE
my-first-pod   1/1     Running   0          60s
```

#### 4. Check Logs
```bash
kubectl logs my-first-pod
```
Output
```
kubectl.exe logs my-first-pod
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
/docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
2025/02/13 17:28:13 [notice] 1#1: using the "epoll" event method
2025/02/13 17:28:13 [notice] 1#1: nginx/1.27.4
2025/02/13 17:28:13 [notice] 1#1: built by gcc 12.2.0 (Debian 12.2.0-14)
2025/02/13 17:28:13 [notice] 1#1: OS: Linux 6.1.0-29-amd64
2025/02/13 17:28:13 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1048576:1048576
2025/02/13 17:28:13 [notice] 1#1: start worker processes
2025/02/13 17:28:13 [notice] 1#1: start worker process 29
```

#### 5. Access the Pod
```bash
# kubectl get svc
NAME               TYPE           CLUSTER-IP    EXTERNAL-IP      PORT(S)        AGE
kubernetes         ClusterIP      10.109.0.1    <none>           443/TCP        143m
my-first-service   LoadBalancer   10.109.2.95   <External IP>   80:30507/TCP   3m11s
```
Visit `http://<External IP>` in your browser.

---

### **Step 2: Create a Multi-Container Pod**

#### 1. Write a Multi-Container Pod YAML
Create a file named `multi-container-pod.yaml`:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: multi-container-pod
  labels:
    app: demo
spec:
  containers:
  - name: nginx
    image: nginx:latest
    ports:
    - containerPort: 80
  - name: sidecar
    image: busybox:latest
    command: ["sh", "-c", "while true; do echo Hello from Sidecar; sleep 5; done"]
```

#### 2. Apply the Manifest
```bash
kubectl apply -f multi-container-pod.yaml
```

#### 3. Observe Logs from Both Containers
```bash
kubectl logs multi-container-pod -c nginx
kubectl logs multi-container-pod -c sidecar
```

---

### **Step 3: Explore Pod Networking**

#### 1. Create a Networking Pod
Write a manifest `networking-pod.yaml`:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: network-pod
  labels:
    app: demo
spec:
  containers:
  - name: busybox
    image: busybox:latest
    command: ["sh", "-c", "sleep 3600"]
```

#### 2. Apply the Manifest
```bash
kubectl apply -f networking-pod.yaml
```

#### 3. Exec into the Pod
```bash
kubectl exec -it network-pod -- sh
```

#### 4. Test DNS Resolution
Inside the Pod:
```bash
nslookup quick-labs.io
```

#### 5. Exit the Pod
```bash
exit
```

---

### **Step 4: Debug Pod Issues**

#### 1. Create a Failing Pod
Write a manifest `failing-pod.yaml`:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: failing-pod
spec:
  containers:
  - name: failing-container
    image: busybox:latest
    command: ["sh", "-c", "exit 1"]
```

#### 2. Apply the Manifest
```bash
kubectl apply -f failing-pod.yaml
```

#### 3. Check the Pod Status
```bash
kubectl get pods
```

#### 4. Describe the Pod
```bash
kubectl describe pod failing-pod
```

#### 5. Delete the Pod
```bash
kubectl delete pod failing-pod
```

---

### **Step 5: Clean Up**
Delete all resources created during the lab:
```bash
kubectl delete pod my-first-pod multi-container-pod network-pod
```

---

### **What Students Will Learn**
1. How to create and manage Pods using YAML manifests.
2. How to inspect and debug Pods.
3. How Pods handle networking and multiple containers.
4. How to troubleshoot common Pod issues.

