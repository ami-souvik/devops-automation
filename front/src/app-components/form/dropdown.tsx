import React from "react"
import { Button, ButtonProps } from "@/components/ui/button"
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger
} from "@/components/ui/dropdown-menu"

export default function Dropdown({ value, onChange, choices, buttonProps={ variant: "outline" } }: {
    buttonProps: ButtonProps
}) {
    return <DropdownMenu>
        <DropdownMenuTrigger className="w-full" asChild>
            <Button {...buttonProps}>{value}</Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent className="h-96 overflow-y-auto">
        {
            choices.map((menu, idx) => (
            <React.Fragment key={`dropdown-${idx}`}>
                <DropdownMenuLabel key={`dropdown-menu-label-${idx}`}>{menu.title}</DropdownMenuLabel>
                <DropdownMenuSeparator key={`dropdown-menu-separator-${idx}`} />
                {
                menu.items.map((item, idx) => (
                    <DropdownMenuItem key={`dropdown-menu-item-${idx}`} className="justify-between"
                    onClick={() => onChange(item.value)}>
                    <span>{item.label}</span>
                    <span>{item.value}</span>
                    </DropdownMenuItem>
                ))
                }
            </React.Fragment>
            ))
        }
        </DropdownMenuContent>
    </DropdownMenu>
}