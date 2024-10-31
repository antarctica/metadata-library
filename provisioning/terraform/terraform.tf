## Core
##

terraform {
  required_version = "~> 1.9"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Remote state backend
  # Note: 'BAS-METADATA-GENERATOR' is a legacy name for this project kept for continuity.
  # Source: https://gitlab.data.bas.ac.uk/WSF/terraform-remote-state
  backend "s3" {
    bucket = "bas-terraform-remote-state-prod"
    key    = "v2/BAS-METADATA-GENERATOR/terraform.tfstate"
    region = "eu-west-1"
  }
}

provider "aws" {
  region = "eu-west-1"
}

## IAM
##

resource "aws_iam_user" "gitlab-ci" {
  name = "bas-gitlab-ci-bas-metadata-library"
}

resource "aws_iam_user_policy" "ci-testing" {
  name = "ci-policy-testing"
  user = aws_iam_user.gitlab-ci.name
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Sid" : "MinimalContinuousDeploymentPermissions",
        "Effect" : "Allow",
        "Action" : [
          "s3:ListBucket",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:GetObjectAcl",
          "s3:PutObjectAcl"
        ],
        "Resource" : [
          "arn:aws:s3:::metadata-resources-testing.data.bas.ac.uk/bas-metadata-generator-configuration-schemas",
          "arn:aws:s3:::metadata-resources-testing.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/*"
        ]
      }
    ]
  })
}

resource "aws_iam_user_policy" "ci-production" {
  name = "ci-policy-production"
  user = aws_iam_user.gitlab-ci.name
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Sid" : "MinimalContinuousDeploymentPermissions",
        "Effect" : "Allow",
        "Action" : [
          "s3:ListBucket",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:GetObjectAcl",
          "s3:PutObjectAcl"
        ],
        "Resource" : [
          "arn:aws:s3:::metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas",
          "arn:aws:s3:::metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/*"
        ]
      }
    ]
  })
}
