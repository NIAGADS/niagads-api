export function Footer() {
	const currentYear = new Date().getFullYear();
	return (
		<footer className="border-t w-full h-16">
			<div className="container flex items-center sm:justify-between justify-center sm:gap-0 gap-4 h-full text-muted-foreground text-sm flex-wrap sm:py-0 py-3 max-sm:px-4">
				<div className="flex items-center gap-3">
					<p className="text-center">
						© {currentYear} NIAGADS. All rights reserved.
					</p>
				</div>

				<div className="gap-4 items-center hidden md:flex">
					<FooterButtons />
				</div>
			</div>
		</footer>
	);
}

export function FooterButtons() {
	return <></>;
}
