# Dockerfile
# -----------
# Bouwt een image die de scraper draait en daarna het dashboard start.
# Builds an image that runs the scraper and then starts the dashboard.

FROM python:3.12-slim

WORKDIR /app

# Systeemdependencies voor lxml/pandas bouwen (indien geen wheels beschikbaar)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Zorg dat de data map bestaat (voor de SQLite database)
RUN mkdir -p data

EXPOSE 8501

# Health check zodat Docker weet of de container gezond is
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Bij opstarten: eerst scrapen (eerste keer data verzamelen), dan dashboard starten
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

ENTRYPOINT ["/app/docker-entrypoint.sh"]
