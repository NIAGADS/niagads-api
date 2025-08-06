import { NextRequest, NextResponse } from "next/server";
import {
	backendFetchFromRequest,
	caseInsensitiveIncludes,
} from "@niagads/common";

const TEXT_RESPONSES: string[] = ["TEXT", "VCF", "BED"];

export async function __apiFetch(
	request: NextRequest,
	headers: any | undefined = null
) {
	let asText = false; // default to expect JSON response
	const incomingRequestUrl = new URL(request.url);

	if (!process.env.NEXT_PUBLIC_HOST_URL) {
		throw Error(
			"Please specify `NEXT_PUBLIC_HOST_URL` in the .env.local file."
		);
	}

	const queryParams = Object.fromEntries(
		incomingRequestUrl.searchParams.entries()
	);
	if (queryParams.hasOwnProperty("format")) {
		if (caseInsensitiveIncludes(TEXT_RESPONSES, queryParams["format"])) {
			asText = true;
		}
	}
	if (queryParams.hasOwnProperty("view")) {
		// not default (i.e., JSON response)
		if (!caseInsensitiveIncludes(["DEFAULT"], queryParams["view"])) {
			if (caseInsensitiveIncludes(["TABLE"], queryParams["view"])) {
				// redirect to the correct view, passing the original query as an arg
				const encodedQuery = btoa(
					`${incomingRequestUrl.pathname}${incomingRequestUrl.search}`
				);
				/* const redirectEndpoint = `/view/table?endpoint=${
					incomingRequestUrl.pathname
				}/${incomingRequestUrl.search.replace("?", "&")}`; */
				const redirectEndpoint = `/view/table?query=${encodedQuery}`;
				const redirectUrl = new URL(
					redirectEndpoint,
					process.env.NEXT_PUBLIC_HOST_URL
				);
				return NextResponse.redirect(redirectUrl);
			}
		}
		/*
        // FIXME: does this matter anymore? just return the JSON for the view
        const userAgent = (await headers()).get("User-Agent");
        const validUserAgent: boolean = userAgentIsBrowser(userAgent!);
        if (!validUserAgent) {
            return NextResponse.json(
                {
                    error: "Invalid parameter",
                    msg: "interactive data views can only be generated if request is made in a web-browser; set `view=DEFAULT` and resubmit query",
                },
                { status: 422 }
            );
        } */

		/*
    
        */
	}
	// handle yaml files
	if (incomingRequestUrl.pathname.endsWith("yaml")) {
		headers = {
			"Content-Type": "text/yaml",
		};
		asText = true;
	}

	const response = await backendFetchFromRequest(
		request,
		process.env.API_INTERNAL_URL!,
		asText
	);

	// add text headers if text response expected
	if (asText) {
		return new NextResponse(response, {
			status: 200,
			headers: headers
				? headers
				: {
						"Content-Type": "text/plain",
				  },
		});
	}
	// otherwise return JSON
	return NextResponse.json(response, { status: 200 });
}
