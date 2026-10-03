ls

# first start UVICORN, then start nginx. 
server/docker-pythonAPI/.venv/bin/uvicorn server:app --host 0.0.0.0 --port 8000

#start nginx

