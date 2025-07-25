// for page navigation & to sort on leftbar

export type EachRoute = {
	title: string;
	href: string;
	noLink?: true; // noLink will create a route segment (section) but cannot be navigated
	items?: EachRoute[];
	tag?: string;
};

export const ROUTES: EachRoute[] = [
	{
		title: "Introduction",
		href: "/introduction",
		noLink: true,
		items: [
			{ title: "NIAGADS Open Access", href: "/niagads-open-access" },
			{ title: "Getting Started", href: "/getting-started" },
		],
	},
];

type Page = { title: string; href: string };

function getRecurrsiveAllLinks(node: EachRoute) {
	const ans: Page[] = [];
	if (!node.noLink) {
		ans.push({ title: node.title, href: node.href });
	}
	node.items?.forEach((subNode) => {
		const temp = { ...subNode, href: `${node.href}${subNode.href}` };
		ans.push(...getRecurrsiveAllLinks(temp));
	});
	return ans;
}

export const page_routes = ROUTES.map((it) => getRecurrsiveAllLinks(it)).flat();
