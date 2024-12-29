import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs"
import Layout from "@/layout"
import api from "@/lib/webservices"
import OverviewTab from "@/app-components/application/overview-tab";
import DeployTab from "@/app-components/application/deploy-tab";
import SettingsTab from "@/app-components/application/settings-tab";
import { useAppname } from "@/hooks/use-app";

export default function Application() {
  const az = useSelector((state) => state.data.az)
  const appName = useAppname();
  const [details, setDetails] = useState({});
  function onMount() {
    api.get(`/apps/get/${appName}?az=${az}`).then(resp => {
      setDetails({
        appName,
        ...resp.data
      })
    })
  }
  useEffect(() => {
    onMount()
  }, [appName])
  return <Layout>
    <Tabs defaultValue="overview">
      <div className="bg-muted">
        <TabsList className="grid w-full grid-cols-7 max-w-[800px] mx-auto my-3">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="resources">Resources</TabsTrigger>
          <TabsTrigger value="deploy">Deploy</TabsTrigger>
          <TabsTrigger value="metrics">Metrics</TabsTrigger>
          <TabsTrigger value="activity">Activity</TabsTrigger>
          <TabsTrigger value="access">Access</TabsTrigger>
          <TabsTrigger value="settings">Settings</TabsTrigger>
        </TabsList>
      </div>
      <TabsContent value="overview" className="max-w-[800px] mx-auto">
        <OverviewTab data={details} />
      </TabsContent>
      <TabsContent value="deploy" className="max-w-[800px] mx-auto">
        <DeployTab data={details} />
      </TabsContent>
      <TabsContent value="settings" className="max-w-[800px] mx-auto">
        <SettingsTab data={details} />
      </TabsContent>
    </Tabs>
  </Layout>
}