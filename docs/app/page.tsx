import { MoveUpRightIcon, TerminalSquareIcon } from "lucide-react";

import Link from "next/link";
import { buttonVariants } from "@/components/ui/button";
import { page_routes } from "@/lib/routes-config";

export default function Home() {
    return (
        <div className="flex sm:min-h-[87.5vh] min-h-[82vh] flex-col sm:items-center justify-center text-center sm:py-8 py-14">
            <Link
                href="https://github.com/NIAGADS/niagads-api"
                target="_blank"
                className="mb-5 sm:text-lg flex items-center gap-2 underline underline-offset-4 sm:-mt-12"
            >
                Follow along on GitHub <MoveUpRightIcon className="w-4 h-4 font-extrabold" />
            </Link>
            <h1 className="text-[1.80rem] leading-8 sm:px-8 md:leading-[4.5rem] font-bold mb-4 sm:text-6xl text-left sm:text-center">
                The NIAGADS Open Access API
            </h1>
            <p className="mb-8 md:text-lg text-base  max-w-[1200px] text-muted-foreground text-left sm:text-center">
                Enhance your Alzheimer’s research with a simple, robust API that provides unrestricted programmatic
                access to curated genetic data, key variants, and insights into the genetics of neurodegenerative
                disease.
            </p>
            <div className="sm:flex sm:flex-row grid grid-cols-2 items-center sm;gap-5 gap-3 mb-8">
                <Link
                    href={`/docs${page_routes[0].href}`}
                    className={buttonVariants({ className: "px-6", size: "lg" })}
                >
                    Get Stared
                </Link>
            </div>
        </div>
    );
}
