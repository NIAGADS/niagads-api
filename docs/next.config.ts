import type { NextConfig } from "next";

const nextConfig: NextConfig = {
	turbopack: {
		//root: path.join(__dirname, '..'), // include files outside of app
	},
	experimental: {
		serverSourceMaps: true,
	},
	transpilePackages: ["next-mdx-remote"],

	async rewrites() {
		return [
			{
				source: "/docs",
				destination: "/docs/introduction/niagads-open-access",
			},
			{
				source: "/redoc",
				destination: `${process.env.API_INTERNAL_URL}/redoc`,
			},
		];
	},
};

export default nextConfig;
