// FIXME: most of this is in @niagads/common - after published
import * as path from "path";
import { NextRequest, NextResponse } from "next/server";

export function userAgentIsBrowser(userAgent: string): boolean {
	// checks if the user-agent for the request was a web browser
	const browsers = ["Mozilla", "Safari", "Edge", "Chrome"];
	return (
		userAgent !== null &&
		browsers.some((value) => userAgent.includes(value))
	);
}

/**
 *
 * @param requestUri
 * @param asText - if 'true' returns text response else returns jso response
 * @param skipErrorCheck  - defaults to 'true' b/c NIAGADS API calls will handle errors and return a JSON message
 * @returns - the response
 */
async function __fetch(
	requestUri: string,
	asText: boolean = false,
	skipErrorCheck: boolean = true
) {
	const response = await fetch(requestUri);
	if (!response.ok) {
		if (skipErrorCheck) {
			const error = await response.json();
			return Object.assign({}, error, { status: response.status });
		} else {
			throw new Error(
				`Fetch from ${requestUri} failed with status ${response.status}: ${response.statusText}`
			);
		}
	}
	const data = asText ? await response.text() : await response.json();
	return data;
}

export async function backendFetchFromRequest(
	request: NextRequest,
	base: string,
	asText = false
) {
	const incomingRequestUrl = new URL(request.url);
	const pathname = incomingRequestUrl.pathname;
	const queryParams = incomingRequestUrl.search;
	const baseUrl = base.startsWith("http")
		? base
		: new URL(base, incomingRequestUrl.origin).toString();
	const requestUri: string = new URL(
		path.join(pathname, queryParams),
		baseUrl
	).toString();
	return await __fetch(requestUri, asText);
}

export async function backendFetch(
	pathname: string,
	base: string | undefined,
	skipErrorCheck: boolean = true
) {
	const requestUri: string = base
		? new URL(pathname, base).toString()
		: new URL(pathname).toString();
	return await __fetch(requestUri, false, skipErrorCheck);
}

const TEXT_RESPONSES: string[] = ["TEXT", "VCF", "BED"];

export function caseInsensitiveIncludes(array: string[], value: string) {
	const lcValue = value.toLowerCase();
	return array.some((item) => item.toLowerCase().includes(lcValue));
}

export async function backendFetchResponseHandler(
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
				const redirectEndpoint = `/view/table?endpoint=${
					incomingRequestUrl.pathname
				}/${incomingRequestUrl.search.replace("?", "&")}`;
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
