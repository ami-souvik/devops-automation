import { Link } from "react-router";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export function CreateApp({ className }) {
    return (
        <Button asChild>
            <Link to="/new-app" className={cn("w-full", className)}>
                <span className="font-semibold">Create New App</span>
            </Link>
        </Button>
    )
}