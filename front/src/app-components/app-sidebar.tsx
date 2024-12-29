import { useState, useEffect } from "react"
import { Link, useLocation, useNavigate } from "react-router"
import { useDispatch, useSelector } from "react-redux"
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
import { Separator } from "@/components/ui/separator"
import { Company, Settings, CreateApp } from "@/app-components/app-sidebar-item"
import Dropdown from "@/app-components/form/dropdown"
import api from "@/lib/webservices"
import { AvailabilityZones, availabilityZones } from "@/lib/aws-meta"
import { setAz } from "@/slices/data-slice"
import { useAppname } from "@/hooks/use-app"

function AppList({ apps }) {
  const appName = useAppname();
  const az = useSelector(state => state.data.az)
  return apps.map((app) => (
    <SidebarMenuItem key={app.name}>
      <SidebarMenuButton isActive={appName === app.index && az === app.az} asChild>
        <Link to={app.url}>
          <span>{app.name}</span>
        </Link>
      </SidebarMenuButton>
    </SidebarMenuItem>
  ))
}

export function AppSidebar() {
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const az = useSelector((state) => state.data.az)
  const dispatch = useDispatch()
  const [applist, setApplist] = useState([]);

  function onMount() {
    api.get(`/apps/list?az=${az}`).then(resp => {
      setApplist(resp.data.apps.map(item => ({
        name: item.name,
        az: resp.data.availability_zone,
        index: item.name,
        url: `/apps/${item.name}`
      })))
    })
  }
  useEffect(() => {
    onMount()
  }, [az])
  function onAzChange(az: AvailabilityZones) {
    dispatch(setAz(az))
    if(pathname !== "/") navigate("/")
  }
  return (
    <Sidebar>
      <SidebarContent>
        <SidebarGroup>
          <div>
            <Company />
            <Separator className="my-2" />
            <CreateApp />
          </div>
          <div className="relative py-2 overflow-y-auto row-start-2">
            <div className="absolute w-full">
              <SidebarGroupLabel asChild>
                <div className="w-full flex justify-between my-1">
                  <span>Applications</span>
                  <Dropdown value={az} onChange={onAzChange} choices={availabilityZones}
                    buttonProps={{
                      className: "h-auto w-auto px-4 py-1 focus-visible:ring-0 focus-visible:ring-offset-0",
                      variant: "outline"
                    }}
                  />
                </div>
              </SidebarGroupLabel>
              <SidebarGroupContent>
                <SidebarMenu>
                  <AppList apps={applist} />
                </SidebarMenu>
              </SidebarGroupContent>
            </div>
          </div>
          <Settings />
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  )
}
