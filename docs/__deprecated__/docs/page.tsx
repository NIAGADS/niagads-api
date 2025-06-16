"use client";

import { RedocStandalone, SideNavStyleEnum } from "redoc";

import React from "react";
import { getCurrentMajorVersion } from "@/utils/versioning";

//https://github.com/Redocly/redoc/blob/HEAD/docs/config.md

export default function Page() {
    const currentVersion = getCurrentMajorVersion();
    return (
        <div>
            <RedocStandalone
                specUrl={`v${currentVersion}/openapi.json`}
                options={{
                    scrollYOffset: 100,
                    nativeScrollbars: true,
                    pathInMiddlePanel: false,
                    //ownloadDefinitionUrl: "v0/openapi.yaml",
                    sideNavStyle: SideNavStyleEnum.PathOnly,
                    // hideSchemaTitles: false,
                    // menuToggle: true,
                    theme: { colors: { primary: { main: "#dd5522" } } },
                }}
            />
        </div>
    );
}
