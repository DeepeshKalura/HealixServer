# For running the basic applications
gunicorn -k uvicorn.workers.UvicornWorker app.main:app

# Run fot the docker if you are using docker
# docker run -d -p 3000:3100 deepeshkalura/fastapi-healix

