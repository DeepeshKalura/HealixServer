# For running the basic applications
# gunicorn -k uvicorn.workers.UvicornWorker app.main:app
# gunicorn --config gunicorn.py app.main:app
# uvicorn app.main:app --host
uvicorn app.main:app --host 0.0.0.0 --port 8000
# Run fot the docker if you are using docker
# docker run -d -p 3000:3100 deepeshkalura/fastapi-healix

