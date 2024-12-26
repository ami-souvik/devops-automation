import { Button } from "@/components/ui/button";

export function CreateApp() {
    return (
        <Button asChild>
            <a href="/new-app" className="w-full">
                <span>Create App</span>
            </a>
        </Button>
    )
}