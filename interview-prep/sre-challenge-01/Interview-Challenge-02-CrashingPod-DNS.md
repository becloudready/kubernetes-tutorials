
### **Kubernetes Pod Crashing Issue - Interview Problem**  

#### **Problem Statement**  
You are a Site Reliability Engineer (SRE) managing an EKS cluster. 
A simple Python application deployed as a pod repeatedly fails due to DNS resolution issues. The application performs periodic cURL requests to `google.com`, and if DNS resolution fails, the application exits.  

A developer reports that the pod crashes with an error indicating a failure in DNS resolution.  

Pods are crashing

```bash
kubectl get po 

prod-ns   pod-crashing-dns-xxxxxxx                      1/1     CrashLoopBackOff   1661 (2m ago)   54m
```


#### **Questions**  
1. What are the possible reasons for CrashLoopBackOff failures in the failing pod?  
2. What steps would you take to diagnose the issue further?  
3. How does changing `dnsPolicy` and `dnsConfig` help in debugging?  

