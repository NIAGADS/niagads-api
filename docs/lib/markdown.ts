import { compileMDX } from "next-mdx-remote/rsc";
import path from "path";
import { promises as fs } from "fs";
import remarkGfm from "remark-gfm";
import rehypePrism from "rehype-prism-plus";
import rehypeAutolinkHeadings from "rehype-autolink-headings";
import rehypeSlug from "rehype-slug";
import rehypeCodeTitles from "rehype-code-titles";
import { page_routes, ROUTES } from "./routes-config";
import { visit } from "unist-util-visit";
import matter from "gray-matter";
import { getIconName, hasSupportedExtension } from "./utils";

// custom components imports
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import Pre from "@/components/markdown/pre";
import Note from "@/components/markdown/note";
import { Stepper, StepperItem } from "@/components/markdown/stepper";
import Image from "@/components/markdown/image";
import Link from "@/components/markdown/link";
import Outlet from "@/components/markdown/outlet";
import Files from "@/components/markdown/files";

// custom niagads
import { Json } from "@/components/markdown/json";
import { JsonSchema } from "@/components/markdown/json-schema";

import {
	Table,
	TableBody,
	TableCell,
	TableHead,
	TableHeader,
	TableRow,
} from "@/components/ui/table";

// add custom components
const components = {
	Json,
	JsonSchema,
	Tabs,
	TabsContent,
	TabsList,
	TabsTrigger,
	pre: Pre,
	Note,
	Stepper,
	StepperItem,
	img: Image,
	a: Link,
	Outlet,
	Files,
	table: Table,
	thead: TableHeader,
	th: TableHead,
	tr: TableRow,
	tbody: TableBody,
	t: TableCell,
};

// can be used for other pages like blogs, Guides etc
async function parseMdx<Frontmatter>(rawMdx: string) {
	return await compileMDX<Frontmatter>({
		source: rawMdx,
		options: {
			parseFrontmatter: true,
			mdxOptions: {
				rehypePlugins: [
					preProcess,
					rehypeCodeTitles,
					rehypeCodeTitlesWithLogo,
					rehypePrism,
					rehypeSlug,
					rehypeAutolinkHeadings,
					postProcess,
				],
				remarkPlugins: [remarkGfm],
			},
		},
		components,
	});
}

// logic for docs

export type BaseMdxFrontmatter = {
	title: string;
	description: string;
};

export async function getCompiledDocsForSlug(slug: string) {
	try {
		const contentPath = getDocsContentPath(slug);
		const rawMdx = await fs.readFile(contentPath, "utf-8");
		return await parseMdx<BaseMdxFrontmatter>(rawMdx);
	} catch (err) {
		console.log(err);
	}
}

export async function getDocsTocs(slug: string) {
	const contentPath = getDocsContentPath(slug);
	const rawMdx = await fs.readFile(contentPath, "utf-8");
	// captures between ## - #### can modify accordingly
	const headingsRegex = /^(#{2,4})\s(.+)$/gm;
	let match;
	const extractedHeadings = [];
	while ((match = headingsRegex.exec(rawMdx)) !== null) {
		const headingLevel = match[1].length;
		const headingText = match[2].trim();
		const slug = sluggify(headingText);
		extractedHeadings.push({
			level: headingLevel,
			text: headingText,
			href: `#${slug}`,
		});
	}
	return extractedHeadings;
}

export function getPreviousNext(path: string) {
	const index = page_routes.findIndex(({ href }) => href == `/${path}`);
	return {
		prev: page_routes[index - 1],
		next: page_routes[index + 1],
	};
}

function sluggify(text: string) {
	const slug = text.toLowerCase().replace(/\s+/g, "-");
	return slug.replace(/[^a-z0-9-]/g, "");
}

function getDocsContentPath(slug: string) {
	return path.join(process.cwd(), "/contents/docs/", `${slug}/index.mdx`);
}

function justGetFrontmatterFromMD<Frontmatter>(rawMd: string): Frontmatter {
	return matter(rawMd).data as Frontmatter;
}

export async function getAllChilds(pathString: string) {
	const items = pathString.split("/").filter((it) => it != "");
	let page_routes_copy = ROUTES;

	let prevHref = "";
	for (const it of items) {
		const found = page_routes_copy.find(
			(innerIt) => innerIt.href == `/${it}`
		);
		if (!found) break;
		prevHref += found.href;
		page_routes_copy = found.items ?? [];
	}
	if (!prevHref) return [];

	return await Promise.all(
		page_routes_copy.map(async (it) => {
			const totalPath = path.join(
				process.cwd(),
				"/contents/docs/",
				prevHref,
				it.href,
				"index.mdx"
			);
			const raw = await fs.readFile(totalPath, "utf-8");
			return {
				...justGetFrontmatterFromMD<BaseMdxFrontmatter>(raw),
				href: `/docs${prevHref}${it.href}`,
			};
		})
	);
}

// for copying the code in pre
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const preProcess = () => (tree: any) => {
	visit(tree, (node) => {
		if (node?.type === "element" && node?.tagName === "pre") {
			const [codeEl] = node.children;
			if (codeEl.tagName !== "code") return;
			node.raw = codeEl.children?.[0].value;
		}
	});
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const postProcess = () => (tree: any) => {
	visit(tree, "element", (node) => {
		if (node?.type === "element" && node?.tagName === "pre") {
			node.properties["raw"] = node.raw;
		}
	});
};

export type Author = {
	avatar?: string;
	handle: string;
	username: string;
	handleUrl: string;
};

export type BlogMdxFrontmatter = BaseMdxFrontmatter & {
	date: string;
	authors: Author[];
	cover: string;
};

export async function getAllBlogStaticPaths() {
	try {
		const blogFolder = path.join(process.cwd(), "/contents/blogs/");
		const res = await fs.readdir(blogFolder);
		return res.map((file) => file.split(".")[0]);
	} catch (err) {
		console.log(err);
	}
}

export async function getAllBlogsFrontmatter() {
	const blogFolder = path.join(process.cwd(), "/contents/blogs/");
	const files = await fs.readdir(blogFolder);
	const uncheckedRes = await Promise.all(
		files.map(async (file) => {
			if (!file.endsWith(".mdx")) return undefined;
			const filepath = path.join(
				process.cwd(),
				`/contents/blogs/${file}`
			);
			const rawMdx = await fs.readFile(filepath, "utf-8");
			return {
				...justGetFrontmatterFromMD<BlogMdxFrontmatter>(rawMdx),
				slug: file.split(".")[0],
			};
		})
	);
	return uncheckedRes.filter((it) => !!it) as (BlogMdxFrontmatter & {
		slug: string;
	})[];
}

export async function getCompiledBlogForSlug(slug: string) {
	const blogFile = path.join(
		process.cwd(),
		"/contents/blogs/",
		`${slug}.mdx`
	);
	try {
		const rawMdx = await fs.readFile(blogFile, "utf-8");
		return await parseMdx<BlogMdxFrontmatter>(rawMdx);
	} catch {
		return undefined;
	}
}

export async function getBlogFrontmatter(slug: string) {
	const blogFile = path.join(
		process.cwd(),
		"/contents/blogs/",
		`${slug}.mdx`
	);
	try {
		const rawMdx = await fs.readFile(blogFile, "utf-8");
		return justGetFrontmatterFromMD<BlogMdxFrontmatter>(rawMdx);
	} catch {
		return undefined;
	}
}

export async function getDocFrontmatter(path: string) {
	try {
		const contentPath = getDocsContentPath(path);
		const rawMdx = await fs.readFile(contentPath, "utf-8");
		return justGetFrontmatterFromMD<BlogMdxFrontmatter>(rawMdx);
	} catch {
		return undefined;
	}
}

function rehypeCodeTitlesWithLogo() {
	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	return (tree: any) => {
		visit(tree, "element", (node) => {
			if (
				node?.tagName === "div" &&
				node?.properties?.className?.includes("rehype-code-title")
			) {
				const titleTextNode = node.children.find(
					// eslint-disable-next-line @typescript-eslint/no-explicit-any
					(child: any) => child.type === "text"
				);
				if (!titleTextNode) return;

				// Extract filename and language
				const titleText = titleTextNode.value;
				const match = hasSupportedExtension(titleText);
				if (!match) return;

				const splittedNames = titleText.split(".");
				const ext = splittedNames[splittedNames.length - 1];
				const iconClass = `devicon-${getIconName(
					ext
				)}-plain text-[17px]`;

				// Insert icon before title text
				if (iconClass) {
					node.children.unshift({
						type: "element",
						tagName: "i",
						properties: { className: [iconClass, "code-icon"] },
						children: [],
					});
				}
			}
		});
	};
}
