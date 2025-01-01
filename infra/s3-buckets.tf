resource "aws_s3_bucket" "kobidh-platform" {
  bucket = "kobidh-platform"

  tags = {
    owner = "kobidh"
  }
}
