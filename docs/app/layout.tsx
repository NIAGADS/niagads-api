import "@/styles/globals.css";

import { Space_Grotesk, Space_Mono } from "next/font/google";

import { Footer } from "@/components/footer";
import type { Metadata } from "next";
import { Navbar } from "@/components/navbar";

const sansFont = Space_Grotesk({
	subsets: ["latin"],
	variable: "--font-geist-sans",
	display: "swap",
	weight: "400",
});

const monoFont = Space_Mono({
	subsets: ["latin"],
	variable: "--font-geist-mono",
	display: "swap",
	weight: "400",
});

export const metadata: Metadata = {
	title: "NIAGADS Open Access API",
	description: "Documentation for the NIAGADS Open Access API",
	/* icons: {
		icon: favicon.src,
	}, */
};

export default function RootLayout({
	children,
}: Readonly<{
	children: React.ReactNode;
}>) {
	return (
		<html lang="en" suppressHydrationWarning>
			<head>
				<link
					rel="stylesheet"
					type="text/css"
					href="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/devicon.min.css"
				/>
			</head>
			<body
				className={`${sansFont.variable} ${monoFont.variable} font-regular antialiased tracking-wide`}
				suppressHydrationWarning
			>
				<Navbar />
				<main className="sm:container mx-auto w-[90vw] h-auto scroll-smooth">
					{children}
				</main>
				<Footer />
			</body>
		</html>
	);
}
