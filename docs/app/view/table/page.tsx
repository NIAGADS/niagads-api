// /view/table/page.tsx

import "@niagads/common/dist/assets/pretty-print-json.css";

import { backendFetch, jsonSyntaxHighlight } from "@niagads/common";

import { Alert } from "@niagads/ui";
import TableWrapper from "@/components/TableWrapper";

type ParameterObj = { [key: string]: string | string[] | undefined };

interface PageProps {
	searchParams: Promise<ParameterObj>;
}

function parseOriginatingRequest(request: string) {
	// Ensure input starts with a slash for relative URLs
	const url = new URL(request, "http://dummy");
	const path = url.pathname;
	const params: { [key: string]: string } = {};
	url.searchParams.forEach((value, key) => {
		params[key] = value;
	});

	return { path, params };
}

export default async function Page({ searchParams }: PageProps) {
	const params: ParameterObj = await searchParams;
	const query: string = atob(params["query"] as string);

	const response = await backendFetch(query, process.env.API_INTERNAL_URL);

	const page = response?.pagination?.page;
	const totalNpages = response?.pagination?.total_num_pages;
	const resultSize = response?.pagination?.total_num_records;
	const showPaginationWarning = page !== null && totalNpages > 1;

	if (!response.table) {
		return (
			<Alert
				variant="error"
				message="Unable to render table view"
				style={{ marginTop: "2rem", marginBottom: "1rem" }}
			>
				<p>
					{response?.request?.message ||
						"Runtime Error: please report this issue to the NIAGADS Open Access API Issue Tracker at https://github.com/NIAGADS/niagads-api"}
				</p>
				<p>Unable to render table for: {query}</p>
			</Alert>
		);
	}
	return (
		<>
			{showPaginationWarning && (
				<div className="alert">
					<Alert
						variant="info"
						message={`Large result size (n = ${resultSize} records).`}
						style={{ marginTop: "2rem", marginBottom: "1rem" }}
					>
						<div>
							<p>
								Displaying page{" "}
								<span className="underline font-medium">
									{page}
								</span>{" "}
								out of{" "}
								<span className="font-medium underline">
									{totalNpages}
								</span>
								.
							</p>
							<p>
								To explore additional pages of the response
								data, update or add the{" "}
								<span className="font-bold underline">
									page
								</span>{" "}
								parameter in your original request (see below
								table) and resubmit to the API.
							</p>
						</div>
					</Alert>
				</div>
			)}
			<TableWrapper {...response.table} />

			<Alert
				variant="info"
				message="Originating request"
				style={{ marginTop: "2rem", marginBottom: "2rem" }}
			>
				<pre
					className="json"
					dangerouslySetInnerHTML={{
						__html: jsonSyntaxHighlight(
							JSON.stringify(
								parseOriginatingRequest(query),
								undefined,
								4
							)
						),
					}}
				></pre>
			</Alert>
		</>
	);
}
