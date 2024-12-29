import { Link } from "react-router";
import { Button } from "@/components/ui/button";

export function Settings() {
    return (
        <Button variant="outline" asChild>
            <Link to="/settings" className="w-full">
                <span>Settings</span>
            </Link>
        </Button>
    )
}