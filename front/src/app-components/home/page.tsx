import Layout from "@/layout"
import { CreateApp } from "@/app-components/app-sidebar-item"

export default function Page() {
    return <Layout>
      <div className="flex flex-col place-items-center place-content-center space-y-4">
        <span className="text-4xl">Welcome to <strong>Kobidh</strong></span>
        <span>Helps to automate your <strong>"Development Operation"</strong> processes.</span>
        <CreateApp className="w-auto" />
      </div>
    </Layout>
}