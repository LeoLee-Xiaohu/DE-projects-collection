terraform {
  backend "s3" {
    bucket = "8893-leo-jenkins-app"
    region = "us-east-1"
    key = "jenkins-server/terraform.tfstate"
  }
}