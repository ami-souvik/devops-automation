resource "aws_dynamodb_table" "kobidh-app-describes" {
  name           = "AppDescribes"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "AppId"
  #   range_key      = "GameTitle"

  attribute {
    name = "AppId"
    type = "S"
  }

  attribute {
    name = "AppName"
    type = "S"
  }

  #   attribute {
  #     name = "AppId"
  #     type = "S"
  #   }

  attribute {
    name = "ApiGateway"
    type = "S"
  }

  attribute {
    name = "ECR"
    type = "S"
  }

  ttl {
    attribute_name = "TimeToExist"
    enabled        = true
  }

  #   global_secondary_index {
  #     name               = "GameTitleIndex"
  #     hash_key           = "GameTitle"
  #     range_key          = "TopScore"
  #     write_capacity     = 10
  #     read_capacity      = 10
  #     projection_type    = "INCLUDE"
  #     non_key_attributes = ["UserId"]
  #   }

  tags = {
    owner = "kobidh"
  }
}
