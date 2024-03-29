# syntax=docker/dockerfile:1

FROM node:bookworm-slim as builder

ARG BUILD
ARG PYTHON_LOG_LEVEL

WORKDIR /src

# node modules installed in parent directory;
# see https://github.com/Kartikdot/TS-Node-Docker-Starter/tree/main
COPY package.json ./
RUN npm install && npm cache clean --force
ENV PATH=/src/node_modules/.bin:$PATH

# this is separated to take advantage of caching unless package.json / package-lock.json changes
# need to copy everything into docker to build and then can do a multi-stage docker build
WORKDIR /src
COPY . .
COPY .env.local .

FROM node:bookworm-slim as runner

WORKDIR /app

COPY --from=builder /src/node_modules node_modules

EXPOSE 3000
ENV BUILD_ENV=${BUILD}
CMD npm run start-$BUILD_ENV

# FROM build as python-build

# # Install python/pip# set env variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# RUN apt-get update && apt-get install -y \
#     python3 python3-pip git \
#     && ln -sf python3 /usr/bin/python \
#     && apt autoremove --purge -y \
#     && rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/*.list

# # Install application
# WORKDIR /app

# COPY ./requirements.txt .

# ENV BUILD_ENV=${BUILD}
# ENV LOG_LEVEL=${PYTHON_LOG_LEVEL}

# # --break-system-packages let you install non-debian packaged libraries
# # bypass `externally-managed-environment` error
# RUN pip3 install -r requirements.txt --break-system-packages
#     # && apt remove -y python3-pip git --> [prod only]


# # FROM nginx:bookworm-slim
# # COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
# # COPY --from=node-build /app/build /usr/share/nginx/html

# COPY ./start.sh .
# RUN chmod +x start.sh 

# # CMD ls /app && gunicorn -w 4 --reload --bind 0.0.0.0:8000 'app:create_app(None)'

# # CMD ["./start.sh"]
# CMD tail -f /dev/null