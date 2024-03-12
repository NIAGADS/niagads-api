// adapted from https://github.com/digitros/nextjs-fastapi/blob/main/next.config.js

/** @type {import('next').NextConfig} */

const nextConfig = {
    rewrites: async () => {
        return [
            {
                source: "/api/:path*",
                destination:
                    process.env.NODE_ENV === "development"
                        ? "http://127.0.0.1:8000/api/:path*"
                        : "/api",
            },
            {
                source: "/api/docs",
                destination:
                    process.env.NODE_ENV === "development"
                        ? "http://127.0.0.1:8000/docs"
                        : "/docs",
            },
            {
                source: "/api/openapi.json",
                destination:
                    process.env.NODE_ENV === "development"
                        ? "http://127.0.0.1:8000/openapi.json"
                        : "/openapi.json",
            },
        ];
    },
};

module.exports = nextConfig;