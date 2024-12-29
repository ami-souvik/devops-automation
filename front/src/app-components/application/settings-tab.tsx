import { useSelector } from "react-redux";
import { Button } from "@/components/ui/button";
import { getValueFromKeyPath } from "@/lib/utils";
import api from "@/lib/webservices";
import { Confirm } from "@/app-components/ui/alert";
import { useNavigate } from "react-router";
import { useAppname } from "@/hooks/use-app";
import { Separator } from "@/components/ui/separator";

const appSchema = [
    {
      label: "App Name",
      key: "appName"
    },
    {
      label: "Availability Zone",
      key: "availability_zone"
    },
    {
      label: "Stack",
      key: "stack",
      value: "Container"
    },
    {
      label: "Domain",
      key: "apigateway.ApiEndpoint"
    }
]

export default function SettingsTab({ data }) {
  const navigate = useNavigate();
  const appName = useAppname();
  const az = useSelector((state) => state.data.az)
  function deleteApp() {
    api.delete(`/apps/delete/${appName}?az=${az}`).then(resp => {
      navigate('/')
    })
  }
  return <div className="space-y-4">
    <div className="pt-2 px-4">
      <span className="text-lg">App Settings</span>
    </div>
    <div className="py-2 px-4 border rounded-xl">
      <span className="text-sm">App Information</span>
      <Separator className="my-2" />
      <div className="grid grid-cols-2 auto-cols-auto gap-y-4">
        {
          appSchema.map(item => <>
            <span className="text-sm font-semibold">{item.label}</span>
            <span className="text-sm">{getValueFromKeyPath(data, item.key) || item.value}</span>
          </>)
        }
      </div>
    </div>
    <Confirm title="Are you absolutely sure?"
      description="This action cannot be undone. This will permanently delete your account and remove your data from our servers."
      onContinue={deleteApp}>
      <Button className="border-rose-700 text-rose-700 hover:text-rose-700 hover:bg-rose-500/10" variant="outline">
        Delete App
      </Button>
    </Confirm>
  </div>
}