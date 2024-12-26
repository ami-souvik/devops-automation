import { z } from "zod"
import { useForm } from "react-hook-form"
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
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger
} from "@/components/ui/dropdown-menu"

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

function DropdownFormField({ form, name, label, description, dropdownValues }) {
  return <FormField
    control={form.control}
    name={name}
    render={({ field }) => (
      <FormItem>
        <FormLabel>{label}</FormLabel>
        <FormDescription>{description}</FormDescription>
        <FormControl>
          <DropdownMenu>
            <DropdownMenuTrigger className="w-full" asChild>
              <Button variant="outline">{field.value}</Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent className="h-96 overflow-y-auto">
              {
                dropdownValues.map(menu => (
                  <>
                    <DropdownMenuLabel>{menu.title}</DropdownMenuLabel>
                    <DropdownMenuSeparator />
                    {
                      menu.items.map(item => (
                        <DropdownMenuItem className="justify-between" onClick={() => field.onChange(item.value)}>
                          <span>{item.label}</span>
                          <span>{item.value}</span>
                        </DropdownMenuItem>
                      ))
                    }
                  </>
                ))
              }
            </DropdownMenuContent>
          </DropdownMenu>
        </FormControl>
        <FormMessage />
      </FormItem>
    )}
  />
}

export default function NewAppForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      app_name: "",
      availability_zone: "us-east-1",
    },
  })
  function onSubmit(values: z.infer<typeof formSchema>) {
    // Do something with the form values.
    // ✅ This will be type-safe and validated.
    console.log(values)
  }
  return <Form {...form}>
    <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-2">
      <InputFormField
        {...{
          form,
          name: "app_name",
          label: "App name",
          description: "Give this app a globally unique name. For example, acme-production-app.",
          placeholder: "app-name"
        }}
      />
      <DropdownFormField
        {...{
          form,
          name: "availability_zone",
          label: "Availability zone",
          description: "Choose an Availability zone for this app.",
          dropdownValues: [
            {
              title: "United States",
              items: [
                {
                  label: "N. Virginia",
                  value: "us-east-1"
                },
                {
                  label: "Ohio",
                  value: "us-east-2"
                },
                {
                  label: "N. California",
                  value: "us-west-1"
                },
                {
                  label: "Oregon",
                  value: "us-west-2"
                }
              ]
            },
            {
              title: "Asia Pacific",
              items: [
                {
                  label: "Mumbai",
                  value: "ap-south-1"
                },
                {
                  label: "Osaka",
                  value: "ap-northeast-3"
                },
                {
                  label: "Seol",
                  value: "ap-northeast-2"
                },
                {
                  label: "Singapore",
                  value: "ap-southeast-1"
                },
                {
                  label: "Sydney",
                  value: "ap-southeast-2"
                },
                {
                  label: "Tokyo",
                  value: "ap-northeast-1"
                }
              ]
            },
            {
              title: "Canada",
              items: [
                {
                  label: "Central",
                  value: "ca-central-1"
                }
              ]
            },
            {
              title: "Europe",
              items: [
                {
                  label: "Frankfurt",
                  value: "eu-central-1"
                },
                {
                  label: "Ireland",
                  value: "eu-west-1"
                },
                {
                  label: "London",
                  value: "eu-west-2"
                },
                {
                  label: "Paris",
                  value: "eu-west-3"
                },
                {
                  label: "Stockholm",
                  value: "eu-north-1"
                }
              ]
            }
          ]
        }}
      />
      <Button type="submit">Create App</Button>
    </form>
  </Form>
}