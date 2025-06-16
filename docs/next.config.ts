import type { NextConfig } from "next";

const nextConfig: NextConfig = {
	turbopack: {
		//root: path.join(__dirname, '..'), // include files outside of app
	},
	experimental: {
		serverSourceMaps: true,
	},
	transpilePackages: ["next-mdx-remote"],

	/* async rewrites() {
		return [
			{
				source: "/:slug*",
				destination: "https://www.niagads.org/",
			},
		];
	}, */
};

export default nextConfig;
