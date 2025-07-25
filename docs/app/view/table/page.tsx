// /view/table/page.tsx

import { backendFetch, jsonSyntaxHighlight } from "@niagads/common";

import { Alert } from "@niagads/ui";
import TableWrapper from "@/component_wrappers/TableWrapper";

type ParameterObj = { [key: string]: string | string[] | undefined };

interface PageProps {
    searchParams: Promise<ParameterObj>;
}

const __buildQuery = (params: ParameterObj) => {
    const { endpoint, ...queryParams } = params;

    const paramStrings: string[] = [];
    for (const [key, value] of Object.entries(queryParams)) {
        paramStrings.push(`${key}=${value}`);
    }

    return `${endpoint}?${paramStrings.join("&")}`;
};

export default async function Page({ searchParams }: PageProps) {
    const params: ParameterObj = await searchParams;
    const query: string = __buildQuery(params);
    const response = await backendFetch(query, process.env.API_INTERNAL_URL);

    const page = response?.pagination?.page;
    const totalNpages = response?.pagination?.total_num_pages;
    const resultSize = response?.pagination?.total_num_records;
    const showPaginationWarning = page !== null && totalNpages > 1;
    // check for error; e.g. empty response

    if (!response.table) {
        return (
            <div className="alert padded">
                <Alert variant="danger" message="Unable to render table view">
                    <p>
                        {response?.request?.message ||
                            "Runtime Error: please report this issue to the NIAGADS Open Access API Issue Tracker at https://github.com/NIAGADS/niagads-api"}
                    </p>
                    <p>Unable to render table for: {query}</p>
                </Alert>
            </div>
        );
    }
    return (
        <>
            {showPaginationWarning && (
                <div className="alert">
                    <Alert variant="info" message={`Large result size (n = ${resultSize} records).`}>
                        <div>
                            <p>
                                Displaying page <span className="underline font-medium">{page}</span> out of{" "}
                                <span className="font-medium underline">{totalNpages}</span>.
                            </p>
                            <p>
                                To explore additional pages of the response data, update or add the{" "}
                                <span className="font-bold underline">page</span> parameter in your original request
                                (see below table) and resubmit to the API.
                            </p>
                        </div>
                    </Alert>
                </div>
            )}
            <TableWrapper {...response.table} />;
            <div className="alert">
                <Alert variant="default" message="Originating request">
                    <pre
                        className="json"
                        dangerouslySetInnerHTML={{
                            __html: jsonSyntaxHighlight(JSON.stringify(params, undefined, 4)),
                        }}
                    ></pre>
                </Alert>
            </div>
        </>
    );
}
