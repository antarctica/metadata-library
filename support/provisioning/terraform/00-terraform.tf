#
# This file is used to define Terraform core resources

terraform {
  required_version = "~> 0.11"

  # AWS S3 Remote state backend
  #
  # Implements a Terraform backend for storing state remotely so it can be used elsewhere.
  #
  # This backend is configured to use the common BAS Terraform Remote State project.
  #
  # This resource relies on the AWS Terraform provider being previously configured.
  #
  # Source: https://gitlab.data.bas.ac.uk/WSF/terraform-remote-state
  # Terraform source: https://www.terraform.io/docs/backends/types/s3.html
  backend "s3" {
    bucket = "bas-terraform-remote-state-prod"
    key    = "v2/BAS-METADATA-GENERATOR/terraform.tfstate"
    region = "eu-west-1"
  }
}
