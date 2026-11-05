FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

# libgomp is needed by lightgbm and xgboost
RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 \
 && rm -rf /var/lib/apt/lists/*

# numpy, pandas, scikit-learn, lightgbm, CPU-only torch and JupyterLab are for the questions;
# the server itself is stdlib only.
RUN pip install --no-cache-dir numpy==2.1.3 pandas==2.2.3 scikit-learn==1.5.2 lightgbm==4.5.0 xgboost==2.1.3 \
      scipy==1.14.1 matplotlib==3.9.2 seaborn==0.13.2 ipykernel==6.29.5 "jupyterlab>=4.2,<4.4" \
 && pip install --no-cache-dir torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu

WORKDIR /jayforces
COPY app app
COPY questions questions

EXPOSE 8000 8888
CMD ["python", "app/server.py"]
