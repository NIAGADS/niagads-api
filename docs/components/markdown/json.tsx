"use client";
import React from "react";
import dynamic from "next/dynamic";

const ReactJson = dynamic(() => import("react-json-view"), { ssr: false });

export const Json = ({ src }: { src: object }) => {
	return (
		<div
			className="json-viewer-wrapper"
			style={{
				padding: "1rem",
				backgroundColor: "#f9f9f9",
				borderRadius: "8px",
			}}
		>
			<ReactJson
				src={src}
				collapsed={true}
				enableClipboard={true}
				displayDataTypes={false}
			/>
		</div>
	);
};
