# TJD-546 DEV fixture: smallest runnable Cloud Run image for the rv-demo bytes4ai-site project (TJD-536 AC3).
# Static server (python http.server, stdlib only) on $PORT (default 8080), non-root user 10001. No secrets, no env beyond PORT.
#   GET /         -> 200 index.html
#   GET /healthz  -> 200 "ok"
FROM python:3.12-slim
RUN useradd --uid 10001 --no-create-home --shell /usr/sbin/nologin web \
 && mkdir -p /srv/site \
 && printf '<!doctype html>\n<html><head><meta charset="utf-8"><title>Bytes4AI website</title></head>\n<body><h1>Bytes4AI website - DEV fixture (TJD-546)</h1></body></html>\n' > /srv/site/index.html \
 && printf 'ok\n' > /srv/site/healthz \
 && chown -R 10001:10001 /srv/site
USER 10001:10001
ENV PORT=8080 PYTHONUNBUFFERED=1
EXPOSE 8080
CMD ["sh", "-c", "exec python3 -m http.server \"${PORT:-8080}\" --bind 0.0.0.0 --directory /srv/site"]
