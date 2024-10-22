# syntax=docker/dockerfile:1

FROM node:20.18.0-bookworm-slim as builder

RUN apt-get update && apt-get install -y git 

WORKDIR /src

# node modules installed in parent directory;
# see https://github.com/Kartikdot/TS-Node-Docker-Starter/tree/main
COPY package.json ./
RUN npm install --legacy-peer-deps --loglevel verbose --force && npm cache clean --force
ENV PATH=/src/node_modules/.bin:$PATH

# this is separated to take advantage of caching unless package.json / package-lock.json changes
# need to copy everything into docker to build and then can do a multi-stage docker build
WORKDIR /src
COPY . .
COPY .env.local .

FROM node:bookworm-slim as runner

ARG BUILD

WORKDIR /app
COPY --from=builder /src/node_modules node_modules

ENV BUILD_ENV=${BUILD}
EXPOSE 3000
CMD npm run start-$BUILD_ENV
