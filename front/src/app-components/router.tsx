import { Route } from "react-router";
import { BrowserRouter, Routes } from "react-router";
import { ThemeProvider } from "@/components/theme-provider";
import Home from "@/app-components/home/page";
import CreateAppPage from "@/app-components/create-app/page";

const router = [
    {
        path: "/",
        page: Home
    },
    {
        path: "/new-app",
        page: CreateAppPage
    }
]

export default function Router() {
    return <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
        <BrowserRouter>
            <Routes>
                {
                    router.map(route => (
                        <Route path={route.path} element={<route.page />} />
                    ))
                }
            </Routes>
        </BrowserRouter>
    </ThemeProvider>
}
