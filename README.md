# CCZG583-Bookmarks-App

## Building:
#### Set environment to minikube's docker -
```
 $ eval $(minikube docker-env)
```

### Build the services -
```
 $ docker build -t bookmark-service:v1 .
 $ docker build -t search-service:v1 .
 $ docker build -t trending-service:v1 .
```

# Deployment:
#### Starting Minikube with dashboard -
```
 $ minikube start --driver=docker
 $ minikube dashboard
```

#### Deploying the services -
```
 $ kubectl apply -f postgres-deployment.yaml
 $ kubectl apply -f bookmark-deployment.yaml
 $ kubectl apply -f search-deployment.yaml
 $ kubectl apply -f trending-deployment.yaml
 $ kubectl get pods
 $ kubectl get svc
```

### Checking DB events - 
Attach to the postgres service and query the db:
```
 $ kubectl exec -it postgres-deployment-7cccbc5978-lgrrl -- psql -U bookmark_user -d bookmark_db 
```

# API testing via Curl -

Create a new bookmark -
```
#curl -X POST http://192.168.49.2:31654/bookmarks \
  -H "Content-Type: application/json" \
  -d '{"title": "My Blog", "url": "https://myblog.com", "description": "Personal blog", "user_id": 1}'
```

Delete a specific bookmark by id -
```
#curl -X DELETE http://<Minikube-IP>:<NodePort>/bookmarks/<bookmark_id>
```

Get all bookmarks of a user -
```
#curl http://<Minikube-IP>:<NodePort>/bookmarks/user/<user_id>
```

Search (by title & url) -
```
#curl "http://<Minikube-IP>:<NodePort>/search?query=<string>"
```

Find trending bookmark -
```
#curl "http://<Minikube-IP>:<NodePort>/trending"
```

