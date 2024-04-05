# syntax=docker/dockerfile:1

FROM python:slim-bookworm AS builder

ARG BUILD

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    # python3 python3-pip 
    git \
    # && ln -sf python3 /usr/bin/python \
    && apt autoremove --purge -y \
    && rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/*.list

# Install application
WORKDIR /src

COPY ./requirements.txt .

# ENV BUILD_ENV=${BUILD}
# ENV LOG_LEVEL=${PYTHON_LOG_LEVEL}

# --break-system-packages let you install non-debian packaged libraries
# bypass `externally-managed-environment` error
RUN pip3 install -r requirements.txt --break-system-packages
    # && apt remove -y python3-pip git --> [prod only]


# # FROM nginx:bookworm-slim
# # COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
# # COPY --from=builder  /usr/share/nginx/html

# COPY ./start.sh .
# RUN chmod +x start.sh 

# # CMD ls /app && gunicorn -w 4 --reload --bind 0.0.0.0:8000 'app:create_app(None)'

# # CMD ["./start.sh"]
# CMD tail -f /dev/null