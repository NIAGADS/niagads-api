// app/docs/StoplightDocs.tsx
"use client";

import "@stoplight/elements/styles.min.css";

import { API } from "@stoplight/elements";

export default function StoplightDocs() {
	return (
		<API apiDescriptionUrl="/openapi.json" router="hash" layout="sidebar" />
	);
}
