# For Linux wheels on Python 3.12
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System headers if your deps build native code. Add more as needed.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl git && \
    rm -rf /var/lib/apt/lists/*

# Preinstall pip/uv if you like; pip is fine:
RUN python -m pip install --upgrade pip

# Install Python deps early to leverage docker layer caching
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Add source
COPY . /app

EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0", "--server.port=8501"]