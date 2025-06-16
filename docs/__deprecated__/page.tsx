"use client";

import { getCurrentVersion } from "@/utils/versioning";
import { Button } from "@niagads/ui";

import { useRouter } from "next/navigation";

export default function Home() {
    const currentVersion = getCurrentVersion();
    const router = useRouter();
    const handleReadTheDocsClick = (e: any) => {
        e.preventDefault();
        router.push("/docs");
    };

    return (
        <>
            <div className="hero section">
                <div className="hero-header">NIAGADS Open Access API</div>
                <div className="hero-subheader">version {currentVersion}</div>
                <Button size="lg" variant="default" onClick={handleReadTheDocsClick}>
                    Read the Docs
                </Button>
            </div>
            <div className="section">
                <h1 className="section-header">About NIAGADS Open Access</h1>
                <div className="section-text">
                    The National Institute on Aging Genetics of Alzheimer&apos;s Disease Data Storage Site (
                    <a className="link" href="https://www.niagads.org/" target="_blank">
                        NIAGADS
                    </a>
                    ) stores and distributes genetics and genomics data from studies on Alzheimer&apos;s disease,
                    related dementias, and aging to qualified researchers globally.
                </div>
                <div className="section-text">
                    <a className="link" href="https://www.niagads.org/open-access/" target="_blank">
                        NIAGADS Open Access
                    </a>{" "}
                    is a collection of files and web-based knowledgebases made available to the public with no data
                    access restrictions. Our application programming interface (API) provides programmatic accesses to
                    these resources, allowing users to integrate our data and annotations into their own analysis
                    pipelines, facilitating investigations at chromosome- and genome-wide scales.{" "}
                </div>
                <div className="section-text">
                    The NIAGADS API uses HTTP requests to access and disseminate data from unrestricted, public NIAGADS
                    knowledgebases. It has predictable resource- and genomic-feature oriented URLs and returns
                    JSON-encoded responses, associated with standard HTTP response codes.
                </div>
            </div>
        </>
    );
}
