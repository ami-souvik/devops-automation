import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { Building2 } from "lucide-react"

export function Tenant() {
    return (
        <Popover>
            <PopoverTrigger>
                <div className="flex items-center space-x-4">
                    <div className="flex aspect-square size-8 items-center justify-center rounded-lg bg-[#1d4ed8]">
                        <Building2 size={18} strokeWidth={1} />
                    </div>
                    <div className="text-sm">
                        <p className="truncate font-semibold">Acme Inc</p>
                        <p className="truncate text-xs text-left">Enterprise</p>
                    </div>
                </div>
            </PopoverTrigger>
            <PopoverContent>
                <p className="text-sm">Your company details.</p>
            </PopoverContent>
        </Popover>
    )
}