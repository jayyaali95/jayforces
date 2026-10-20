FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

# numpy and CPU-only torch are for the questions; the server itself is stdlib only.
RUN pip install --no-cache-dir numpy==2.1.3 \
 && pip install --no-cache-dir torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu

WORKDIR /pitstop
COPY app app
COPY questions questions

EXPOSE 8000
CMD ["python", "app/server.py"]
