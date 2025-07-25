import { NextRequest } from "next/server";
import { backendFetchResponseHandler } from "@/lib/route-handlers";

export async function GET(request: NextRequest) {
	return await backendFetchResponseHandler(request);
}
