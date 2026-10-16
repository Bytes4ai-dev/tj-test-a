# TJD-641: build the static Astro site, then serve dist/ as non-root on $PORT (default 8080).
#   GET /         -> 200 Home
#   GET /healthz  -> 200 "ok"   (TJD-546 contract kept; cloudbuild.yaml unchanged)
FROM node:22-alpine AS build
RUN apk add --no-cache bash grep
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY . .
# TJD-645: TJ_SITE_ENV=production makes the build fail on any fixture entry. Defaults keep the TJD-641 build.
ARG TJ_SITE_ENV=
ENV TJ_SITE_ENV=$TJ_SITE_ENV
# FIXTURES-HOOK-BEGIN (DEV-only [TEST] archive: --build-arg TJ_SITE_FIXTURES=1; removed by scripts/remove-fixtures.sh)
ARG TJ_SITE_FIXTURES=0
ENV TJ_SITE_FIXTURES=$TJ_SITE_FIXTURES PRELAUNCH_ALLOW_FIXTURES=$TJ_SITE_FIXTURES
# FIXTURES-HOOK-END
RUN npm run build && bash scripts/prelaunch-check.sh dist

FROM nginxinc/nginx-unprivileged:stable-alpine
ENV PORT=8080
COPY docker/default.conf.template /etc/nginx/templates/default.conf.template
COPY --from=build /app/dist /usr/share/nginx/html
USER 101
EXPOSE 8080
