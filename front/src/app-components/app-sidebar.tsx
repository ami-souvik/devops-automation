import { Calendar, Home, Inbox, Search } from "lucide-react"

import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem
} from "@/components/ui/sidebar"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"
import { Separator } from "@/components/ui/separator"
import { Company, Settings, CreateApp } from "@/app-components/app-sidebar-item"

// Menu items.
let menuItems = [
  {
    title: "Personal",
    items: [
      {
        title: "Home",
        url: "/home",
        icon: Home,
      }
    ]
  },
  {
    title: "Pidilite (Team)",
    items: [
      {
        title: "Home",
        url: "/home2",
        icon: Home,
      }
    ]
  }
]


export function AppSidebar() {
  return (
    <Sidebar>
      <SidebarContent>
        <SidebarGroup>
          <div>
            <Company />
            <Separator className="my-2" />
            <CreateApp />
          </div>
          <div className="relative overflow-y-auto row-start-2">
            <div className="absolute w-full">
              {
                menuItems.map(({ title, items }) =>
                  (<>
                    <SidebarGroupLabel>{title}</SidebarGroupLabel>
                    <SidebarGroupContent>
                      <SidebarMenu>
                        {items.map((item) => (
                          <SidebarMenuItem key={item.title}>
                            <SidebarMenuButton asChild>
                              <a href={item.url}>
                                <item.icon />
                                <span>{item.title}</span>
                              </a>
                            </SidebarMenuButton>
                          </SidebarMenuItem>
                        ))}
                      </SidebarMenu>
                    </SidebarGroupContent>
                  </>)
                )
              }
            </div>
          </div>
          <Settings />
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  )
}
