export type AvailabilityZones = "us-east-1" | "us-east-2" | "us-west-1" | "us-west-2" | "ap-south-1" |
  "ap-northeast-3" | "ap-northeast-2" | "ap-southeast-1" | "ap-southeast-2" | "ap-northeast-1" |
  "ca-central-1" | "eu-central-1" | "eu-west-1" | "eu-west-2" | "eu-west-3" | "eu-north-1"

export const availabilityZones = [
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