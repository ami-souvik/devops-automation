import React from "react";
import { Link } from "react-router";
import {
    Breadcrumb,
    BreadcrumbItem,
    BreadcrumbLink,
    BreadcrumbList,
    BreadcrumbPage,
    BreadcrumbSeparator,
} from "@/components/ui/breadcrumb"
import { routesMap } from "@/app-components/routes";

export default function Breadcrumbs() {
    function crumbs() {
        const parts = window.location.pathname === '/' ? [""] : window.location.pathname.split('/')
        const endpart = parts.pop()
        const data = parts.map((item, idx) => (
            <React.Fragment key={`crumb-${idx}`}>
                <BreadcrumbItem key={`breadcrumb-${idx}`}>
                    <BreadcrumbLink disabled={!routesMap[item].href} asChild>
                        <Link to={routesMap[item].href}>{routesMap[item]?.label || item}</Link>
                    </BreadcrumbLink>
                </BreadcrumbItem>
                <BreadcrumbSeparator key={`separator-${idx}`} />
            </React.Fragment>
        ))
        data.push(
            <BreadcrumbItem key="breadcrumb-end">
                <BreadcrumbPage>{routesMap[endpart]?.label || endpart}</BreadcrumbPage>
            </BreadcrumbItem>
        )
        return data
    }
    return (
        <Breadcrumb className="mx-2">
            <BreadcrumbList>
                {crumbs()}
            </BreadcrumbList>
        </Breadcrumb>
    )
}