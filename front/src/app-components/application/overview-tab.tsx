import { useSelector } from "react-redux";
import { Separator } from "@/components/ui/separator";
import { getValueFromKeyPath } from "@/lib/utils";
import { ExternalLink } from "lucide-react";

export default function OverviewTab({ data }) {
  const az = useSelector(state => state.data.az)
  return <div className="space-y-4">
    <div className="pt-2 px-4">
      <span className="text-lg">App Overview</span>
    </div>
    
    <div className="py-2 px-4 border rounded-xl">
      <span className="text-sm">Underlying AWS Services</span>
      <Separator className="my-2" />
      <div className="space-y-4">
        {
          data.ecr && <div className="grid grid-cols-2 auto-cols-auto">
            <a href={`https://${az}.console.aws.amazon.com/ecr/repositories/private/${getValueFromKeyPath(data, "ecr.registryId")}/${getValueFromKeyPath(data, "ecr.repositoryName")}?region=${az}`}
              target="_blank" className="text-sm">
              <div className="flex space-x-2 place-items-center">
                <span className="text-sm font-semibold">Elastic Container Repository</span>
                <ExternalLink size={16} />
              </div>
            </a>
          </div>
        }
        {
          data.apigateway && <div className="grid grid-cols-2 auto-cols-auto">
            <a href={`https://${az}.console.aws.amazon.com/apigateway/main/develop/routes?api=${getValueFromKeyPath(data, "apigateway.ApiId")}&region=${az}`}
              target="_blank" className="text-sm">
              <div className="flex space-x-2 place-items-center">
                <span className="text-sm font-semibold">API Gateway</span>
                <ExternalLink size={16} />
              </div>
            </a>
          </div>
        }
      </div>
    </div>
  </div>
}