import React from "react";
import { API_SCHEMAS } from "@/reference/schemas";

interface JsonSchemaProps {
	schema: string;
}

const JsonSchema: React.FC<JsonSchemaProps> = ({ schema }) => {
	const schemaObject = API_SCHEMAS[schema as keyof typeof API_SCHEMAS];

	if (!schemaObject) {
		return <div className="text-red-500">Schema not found: {schema}</div>;
	}

	return <JsonSchemaViewer schema={schemaObject} references={API_SCHEMAS} />;
};

interface JsonSchemaViewerProps {
	schema: Record<string, any>;
	references: Record<string, any>;
}

interface SchemaProperty {
	type?: string;
	description?: string;
	$ref?: string;

	[key: string]: any;
}

const JsonSchemaViewer: React.FC<JsonSchemaViewerProps> = ({
	schema,
	references,
}) => {
	const resolveRef = (ref: string, references: Record<string, any>): any => {
		const refKey = ref.replace("#/", "");
		const resolved = references[refKey];
		if (!resolved) {
			console.warn(`Reference not found: ${ref}`);
			return null;
		}
		// If the resolved schema contains another $ref, resolve it recursively
		if (resolved.$ref) {
			return resolveRef(resolved.$ref, references);
		}
		return resolved;
	};

	const parseAnyOfTypes = (anyOf: any[]): string => {
		if (!Array.isArray(anyOf)) return "unknown";

		const types = anyOf.map((item) => {
			if (item.type) return item.type;
			if (item.$ref) return item.$ref; // Handle references if present
			return "unknown";
		});

		const isOptional = types.includes("null");
		const filteredTypes = types.filter((type) => type !== "null");

		return `${filteredTypes.join(", ")}${isOptional ? " (optional)" : ""}`;
	};

	const renderSchema = (schema: Record<string, any>, path: string[] = []) => {
		if (!schema || typeof schema !== "object") return null;

		const rows = Object.entries(schema.properties || {}).map(
			([key, value]) => {
				const property = value as SchemaProperty;
				const ref = property.$ref
					? resolveRef(property.$ref, references)
					: null;
				const type = property.type || property.$ref;
				const description =
					property.description || (ref && ref.description) || "";

				let finalType = type;

				// If the property has an anyOf, parse its types
				if (property.anyOf) {
					finalType = parseAnyOfTypes(property.anyOf);
				}

				return (
					<tr key={key} className="border-b">
						<td className="px-4 py-2 font-medium text-gray-800">
							{[...path, key].join(".")}
						</td>
						<td className="px-4 py-2 text-gray-600">
							{finalType?.replaceAll("#/components/schemas/", "")}
						</td>
						<td className="px-4 py-2 text-gray-600">
							{description}
						</td>
					</tr>
				);
			}
		);

		return rows;
	};

	return (
		<div className="overflow-x-auto">
			<table className="min-w-full border-collapse border border-gray-300">
				<thead>
					<tr className="bg-gray-100">
						<th className="px-4 py-2 text-left text-gray-700">
							Field
						</th>
						<th className="px-4 py-2 text-left text-gray-700">
							Type
						</th>
						<th className="px-4 py-2 text-left text-gray-700">
							Description
						</th>
					</tr>
				</thead>
				<tbody>{renderSchema(schema)}</tbody>
			</table>
		</div>
	);
};

export { JsonSchema };
