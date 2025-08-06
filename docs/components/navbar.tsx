import { CommandIcon, GithubIcon, TwitterIcon } from "lucide-react";

import AlgoliaSearch from "./algolia-search";
import Anchor from "./anchor";
import Link from "next/link";
import { SheetClose } from "@/components/ui/sheet";
import { SheetLeftbar } from "./leftbar";
import { buttonVariants } from "./ui/button";
import { page_routes } from "@/lib/routes-config";

export const NAVLINKS = [
	{
		title: "Documentation",
		href: `/docs${page_routes[0].href}`,
	},
	{
		title: "Examples",
		href: "https://github.com/NIAGADS/niagads-api/tree/main/examples",
	},
	{
		title: "Community",
		href: "https://github.com/NIAGADS/niagads-api/discussions",
	},
];

const algolia_props = {
	appId: process.env.ALGOLIA_APP_ID!,
	indexName: process.env.ALGOLIA_INDEX!,
	apiKey: process.env.ALGOLIA_SEARCH_API_KEY!,
};

export function Navbar() {
	return (
		<nav className="w-full border-b h-16 sticky top-0 z-50 bg-background">
			<div className="sm:container mx-auto w-[95vw] h-full flex items-center sm:justify-between md:gap-2">
				<div className="flex items-center sm:gap-5 gap-2.5">
					<SheetLeftbar />
					<div className="flex items-center gap-6">
						<div className="lg:flex hidden">
							<Logo />
						</div>
						<div className="md:flex hidden items-center gap-4 text-sm font-medium text-muted-foreground">
							<NavMenu />
						</div>
					</div>
				</div>

				<div className="flex items-center sm:justify-normal justify-between sm:gap-3 ml-1 sm:w-fit w-[90%]">
					<div className="flex items-center justify-between sm:gap-2">
						<div className="flex ml-4 sm:ml-0">
							<Link
								href="https://github.com/NIAGADS/niagads-api"
								className={buttonVariants({
									variant: "ghost",
									size: "icon",
								})}
							>
								<GithubIcon className="h-[1.1rem] w-[1.1rem]" />
							</Link>
						</div>
					</div>
				</div>
			</div>
		</nav>
	);
}

export function Logo() {
	return (
		<Link href="/" className="flex items-center gap-2.5">
			<h2 className="text-md font-bold font-code">NIAGADS Open Access</h2>
		</Link>
	);
}

export function NavMenu({ isSheet = false }) {
	return (
		<>
			{NAVLINKS.map((item) => {
				const Comp = (
					<Anchor
						key={item.title + item.href}
						activeClassName="!text-primary dark:font-medium font-semibold"
						absolute
						className="flex items-center gap-1 sm:text-sm text-[14.5px] dark:text-stone-300/85 text-stone-800"
						href={item.href}
					>
						{item.title}
					</Anchor>
				);
				return isSheet ? (
					<SheetClose key={item.title + item.href} asChild>
						{Comp}
					</SheetClose>
				) : (
					Comp
				);
			})}
		</>
	);
}
