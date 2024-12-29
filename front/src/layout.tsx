import { useState } from "react"
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"
import { AppSidebar } from "@/app-components/app-sidebar"
import Breadcrumbs from "@/app-components/breadcrumbs"
import { cn } from "@/lib/utils"

export default function Layout({ className, children }: { children: React.ReactNode }) {
  const [open, setOpen] = useState(true);
  return (
    <SidebarProvider open={open} onOpenChange={() => setOpen(!open)}>
      <AppSidebar />
      <main className={cn("grid grid-rows-[auto_1fr] my-2 mx-4", className)}>
        <div className="flex place-items-center">
          <SidebarTrigger />
          <Breadcrumbs />
        </div>
        {children}
      </main>
    </SidebarProvider>
  )
}
