import "@/styles/globals.css";

import { RootLayout as StandardRootLayout, ThemeVariant } from "@niagads/ui/layouts";

import type { Metadata } from "next";
import __navConfig from "@/config/navigation.config";
import favicon from "@niagads/common/assets/images/favicon.ico";
import { getPageWrapperClass } from "@/utils/pageConfig";

export const metadata: Metadata = {
    title: "NIAGADS Open Access API",
    description: "Documentation and visualization endpoints for the NIAGADS Open Access API",
    icons: {
        icon: favicon.src,
    },
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    const theme: ThemeVariant = (process.env.NEXT_PUBLIC_THEME as ThemeVariant) || "primary";
    const bannerMsg = process.env.NEXT_PUBLIC_MESSAGE || undefined;
    const pageWrapperClass: string = getPageWrapperClass();
    return (
        <html>
            <body>
                <StandardRootLayout
                    theme={theme}
                    navigationContent={__navConfig}
                    fullWidth={true}
                    bannerMsg={bannerMsg}
                >
                    <div className={pageWrapperClass}>
                        <main>{children}</main>
                        <footer className="footer-bg-primary">
                            <div className="footer-content">
                                <div>
                                    Questions? Contact us at{" "}
                                    <span>
                                        <a
                                            className="text-white underline"
                                            href="mailto:help@niagads.org?subject=NIAGADS API"
                                        >
                                            help@niagads.org
                                        </a>
                                    </span>{" "}
                                    with the subject: <em>NIAGADS API</em>
                                </div>
                                <div>
                                    ©Copyright 2024-2025 University of Pennslyvania, School of Medicine. All rights
                                    reserved.
                                </div>
                            </div>
                        </footer>
                    </div>
                </StandardRootLayout>
            </body>
        </html>
    );
}
