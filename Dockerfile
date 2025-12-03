# File: Dockerfile
FROM python:3.11-slim

LABEL org.opencontainers.image.authors="you@example.com"
LABEL org.opencontainers.image.description="Minimal static site served by python -m http.server (no healthcheck)"

# create non-root user
RUN set -eux; \
    addgroup --system sitegroup && \
    adduser --system --ingroup sitegroup --home /app --shell /bin/sh siteuser

WORKDIR /app

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends curl; \
    rm -rf /var/lib/apt/lists/*

# copy site; ensure correct ownership
COPY --chown=siteuser:sitegroup index.html /app/index.html

# switch to non-root user
USER siteuser

EXPOSE 8000

# run simple static server bound to 0.0.0.0 on port 8000
CMD ["python", "-m", "http.server", "8000", "--bind", "0.0.0.0"]

