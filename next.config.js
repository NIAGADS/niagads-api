// adapted from https://github.com/digitros/nextjs-fastapi/blob/main/next.config.js

/** @type {import('next').NextConfig} */

const nextConfig = {
    distDir: 'build',
    webpack: (config, { dev }) => {
        if (dev) {
            config.devtool = 'eval-source-map';
        }
        return config;
    },

};

module.exports = nextConfig;