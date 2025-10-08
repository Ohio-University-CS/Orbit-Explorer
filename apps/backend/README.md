docker build -t backend ./apps/backend
docker run -p 8000:8000 backend
http://localhost:8000
docker stop <container_id>