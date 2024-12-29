import { Route } from "react-router";
import { BrowserRouter, Routes } from "react-router";
import { ThemeProvider } from "@/components/theme-provider";
import { routes } from "@/app-components/routes";

export default function Router() {
    return <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
        <BrowserRouter>
            <Routes>
                {
                    Object.values(routes).map((route, idx) => (
                        <Route key={idx} path={route.path} element={<route.page />} />
                    ))
                }
            </Routes>
        </BrowserRouter>
    </ThemeProvider>
}
