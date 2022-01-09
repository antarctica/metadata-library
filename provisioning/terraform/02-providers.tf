#
# This file is used to define Terraform provider resources

# AWS provider
#
# The BAS preferred public cloud provider.
#
# See https://www.terraform.io/docs/providers/aws/index.html#authentication for how to
# configure credentials to use this provider.
#
# AWS source: https://aws.amazon.com/
# Terraform source: https://www.terraform.io/docs/providers/aws/index.html
provider "aws" {
  version = "~> 1.34"

  region = "eu-west-1"
}
