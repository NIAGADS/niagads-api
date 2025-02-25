# syntax=docker/dockerfile:1

FROM python:3.12.9-slim-bookworm AS builder

ARG BUILD

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install git to be able to fetch niagads-pylib from git
RUN apt-get update && apt-get install --no-install-recommends -y \
    git \
    # remove cache
    && apt autoremove --purge -y \
    && rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/*.list

RUN python -m venv /opt/venv

# ensure venv is used; see https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
# to understand how this "activates" the venv
ENV PATH="/opt/venv/bin:$PATH"

# Install application
WORKDIR /init

COPY ./requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt 

FROM python:3.12.9-slim-bookworm AS python-runner

ARG BUILD

COPY --from=builder /opt/venv /opt/venv

WORKDIR /init

COPY ./start.sh init.sh
RUN chmod +x init.sh 

# need to redefine in this stage
ENV PATH="/opt/venv/bin:$PATH"
ENV BUILD_ENV=${BUILD}

EXPOSE 8000
# CMD ["fastapi", "run", "api/main.py", "--port", "8000"]
CMD ["./init.sh"]

# # FROM nginx:bookworm-slim
# # COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
# # COPY --from=builder  /usr/share/nginx/html

# CMD ["tail", "-f", "/dev/null"]



# CMD tail -f /dev/nullx