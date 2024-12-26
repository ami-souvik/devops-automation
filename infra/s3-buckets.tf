resource "aws_s3_bucket" "kobidh-apps-describe" {
  bucket = "kobidh-apps-describe"

  tags = {
    owner = "kobidh"
  }
}
