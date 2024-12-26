import { Button } from "@/components/ui/button";

export function Settings() {
    return (
        <Button asChild>
            <a href="/settings" className="w-full">
                <span>Settings</span>
            </a>
        </Button>
    )
}