import {
	BadgeCheck,
	HardHat,
	Info,
	OctagonAlert,
	TriangleAlert,
} from "lucide-react";
import React, { ReactNode } from "react";

interface AlertProps {
	variant?: "info" | "error" | "warning" | "success" | "construction";
	message: string;
	children?: ReactNode;
	className?: string;
	style?: React.CSSProperties;
}

const ICONS = {
	info: Info,
	error: OctagonAlert,
	warning: TriangleAlert,
	success: BadgeCheck,
	construction: HardHat,
};

export const Alert = ({
	variant = "info",
	message,
	children,
	className = "",
	style = {},
}: AlertProps) => {
	const baseClasses =
		"flex p-4 text-sm rounded-lg flex-col shadow-md font-sans";
	const variantClasses = {
		info: "text-blue-800 border border-blue-800 bg-blue-100",
		warning: "text-yellow-800 border border-yellow-800 bg-yellow-100",
		error: "text-red-800 border border-red-800 bg-red-100",
		success: "text-green-800 border border-green-800 bg-green-100",
		construction: "text-yellow-800 border border-yellow-800 bg-yellow-100",
	};

	const Icon = ICONS[variant] || Info;

	return (
		<div
			className={`${baseClasses} ${variantClasses[variant]} ${className}`.trim()}
			role="alert"
			style={style}
		>
			<span className="sr-only">{variant}</span>
			<div className="flex items-center">
				<Icon size={18} className="mr-2" />
				<span className="font-bold text-lg">{message}</span>
			</div>
			{children && <div className="text-md">{children}</div>}
		</div>
	);
};
