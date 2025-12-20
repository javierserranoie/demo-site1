FROM python:3.13-slim

LABEL org.opencontainers.image.description="Zettelkasten static site"

RUN set -eux; \
    addgroup --system sitegroup && \
    adduser --system --ingroup sitegroup --home /app siteuser

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    pip install markdown && \
    rm -rf /var/lib/apt/lists/*

COPY --chown=siteuser:sitegroup index.html style.css build.py app.js /app/

RUN mkdir /app/site && chown siteuser:sitegroup /app/site

USER siteuser

EXPOSE 8000

CMD ["sh", "-c", "python build.py && cd site && python -m http.server 8000 --bind 0.0.0.0"]

