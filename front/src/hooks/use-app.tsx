import { useLocation } from "react-router";

export function useAppname() {
    const { pathname } = useLocation();
    return pathname.startsWith("/apps/") ? pathname.split("/apps/").pop() : null
}