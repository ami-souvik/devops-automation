import { z } from "zod"
import { useForm } from "react-hook-form"
import { useSelector } from "react-redux"
import { zodResolver } from "@hookform/resolvers/zod"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import Loader from "@/components/ui/custom-loader"
import Dropdown from "@/app-components/form/dropdown"
import { availabilityZones } from "@/lib/aws-meta"

const formSchema = z.object({
  app_name: z.string().min(2, {
    message: "Username must be at least 2 characters.",
  }),
  availability_zone: z.string()
})

function InputFormField({ form, name, label, description, placeholder }) {
  return <FormField
      control={form.control}
      name={name}
      render={({ field }) => (
        <FormItem>
          <FormLabel>{label}</FormLabel>
          <FormDescription>{description}</FormDescription>
          <FormControl>
            <Input placeholder={placeholder} {...field} />
          </FormControl>
          <FormMessage />
        </FormItem>
      )}
    />
}

function DropdownFormField({ form, name, label, description, choices }) {
  return <FormField
    control={form.control}
    name={name}
    render={({ field }) => (
      <FormItem>
        <FormLabel>{label}</FormLabel>
        <FormDescription>{description}</FormDescription>
        <FormControl>
          <Dropdown {...field} choices={choices} />
        </FormControl>
        <FormMessage />
      </FormItem>
    )}
  />
}

export default function NewAppForm({ loading, onSubmit }) {
  const availability_zone = useSelector((state) => state.data.az)
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      app_name: "",
      availability_zone,
    },
  })
  return <Form {...form}>
    <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-2">
      <InputFormField
        {...{
          form,
          name: "app_name",
          label: "App Name",
          description: "Give this app a globally unique name. For example, acme-production-app.",
          placeholder: "app-name"
        }}
      />
      <DropdownFormField
        {...{
          form,
          name: "availability_zone",
          label: "Availability Zone",
          description: "Choose an availability zone for this app.",
          choices: availabilityZones
        }}
      />
      <Button type="submit">Create App{loading && <Loader />}</Button>
    </form>
  </Form>
}