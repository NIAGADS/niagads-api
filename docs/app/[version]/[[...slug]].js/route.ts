import { NextRequest } from "next/server";
import { __apiFetch } from "@/lib/route-handlers";

export async function GET(request: NextRequest) {
	return await __apiFetch(request);
}
