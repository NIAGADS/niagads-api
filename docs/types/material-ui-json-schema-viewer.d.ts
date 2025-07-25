declare module "material-ui-json-schema-viewer" {
	import * as React from "react";

	interface SchemaViewerProps {
		schema: object;
		references?: object;
		className?: string;
		style?: React.CSSProperties;
	}

	const SchemaViewer: React.FC<SchemaViewerProps>;
	export default SchemaViewer;
}
