terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket = "lensvault-terraform-state"
    key    = "prod/soc-platform/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = "us-east-1"
}

# --- VPC & Networking ---
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "lensvault-soc-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = false # High Availability
}

# --- EKS Cluster ---
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "19.15.3"

  cluster_name    = "lensvault-soc-prod"
  cluster_version = "1.28"

  vpc_id                   = module.vpc.vpc_id
  subnet_ids               = module.vpc.private_subnets
  control_plane_subnet_ids = module.vpc.private_subnets

  eks_managed_node_groups = {
    ai_workers = {
      min_size     = 3
      max_size     = 20
      desired_size = 5
      instance_types = ["m5.2xlarge"] # Beefy instances for LangGraph
      capacity_type  = "ON_DEMAND"
    }
    database_nodes = {
      min_size     = 3
      max_size     = 5
      desired_size = 3
      instance_types = ["i4i.4xlarge"] # NVMe instances for ClickHouse/Postgres
      capacity_type  = "ON_DEMAND"
    }
  }
}
