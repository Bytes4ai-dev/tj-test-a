# TJD-641: build the static Astro site, then serve dist/ as non-root on $PORT (default 8080).
#   GET /         -> 200 Home
#   GET /healthz  -> 200 "ok"   (TJD-546 contract kept; cloudbuild.yaml unchanged)
FROM node:22-alpine AS build
RUN apk add --no-cache bash grep
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY . .
RUN npm run build && bash scripts/prelaunch-check.sh dist

FROM nginxinc/nginx-unprivileged:stable-alpine
ENV PORT=8080
COPY docker/default.conf.template /etc/nginx/templates/default.conf.template
COPY --from=build /app/dist /usr/share/nginx/html
USER 101
EXPOSE 8080
