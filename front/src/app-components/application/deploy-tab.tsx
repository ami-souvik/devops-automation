import { Copy } from "lucide-react";
import { getValueFromKeyPath } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { useSelector } from "react-redux";

function LineItem({ data }) {
    return <div className="space-y-2">
        <span className="text-sm font-semibold">{data.label}</span>
        <div className="flex justify-between items-center py-2 px-4 space-x-2">
            <span className="text-sm">{data.script}</span>
            <Button size="icon" className="w-6 h-6 rounded"
                onClick={() => {
                    navigator.clipboard.writeText(data.script)
                }}>
                <Copy size={16} />
            </Button>
        </div>
    </div>
}

export default function DeployTab({ data }) {
    const az = useSelector(state => state.data.az)
    const repositoryUri = getValueFromKeyPath(data, "ecr.repositoryUri")
    if(!repositoryUri) return null
    const [dockerRegistry, appName] = repositoryUri?.split("/")
    const contents = [
        {
            label: "1. Retrieve an authentication token and authenticate your Docker client to your registry. Use the AWS CLI:",
            script: `aws ecr get-login-password --region ${az} | docker login --username AWS --password-stdin ${dockerRegistry}`
        },
        {
            label: "2. Build your Docker image using the following command. You can skip this step if your image is already built:",
            script: `docker build -t ${appName} .`
        },
        {
            label: "3. After the build completes, tag your image so you can push the image to this repository:",
            script: `docker tag ${appName}:latest ${dockerRegistry}/${appName}:latest`
        },
        {
            label: "4. Run the following command to push this image to your newly created AWS repository:",
            script: `docker push ${repositoryUri}:latest`
        }
    ]
    return <div className="space-y-4">
        <div className="pt-2 px-4">
            <span className="text-lg">Deploy Your App</span>
        </div>
        <div className="py-2 px-4 border rounded-xl space-y-2">
            <span className="text-sm">Push Docker Image to Repository</span>
            <Separator className="my-2" />
            {contents.map(item => <LineItem data={item} />)}
        </div>
    </div>
}