import Home from "@/app-components/home/page";
import CreateAppPage from "@/app-components/create-app/page";
import Application from "@/app-components/application/page";
import Settings from "@/app-components/settings/page";

export const routesMap = {
    "": {
        href: "/",
        label: "Home",
        page: Home
    },
    "new-app": {
        href: "/new-app",
        label: "Create New App",
        page: CreateAppPage
    },
    "apps": {
        label: "Application",
        page: Application
    },
    "settings": {
        href: "/settings",
        label: "Settings",
        page: Settings
    }
}

export const routes = [
    {
        path: "/",
        page: Home
    },
    {
        path: "/new-app",
        page: CreateAppPage
    },
    {
        path: "/apps/*",
        page: Application
    },
    {
        path: "/settings",
        page: Settings
    }
]
