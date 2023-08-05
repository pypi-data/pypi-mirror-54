# Bedrock - Building blocks for composable Cloud architectures 

[principle of least privilege]: https://en.wikipedia.org/wiki/Principle_of_least_privilege

[Docker]: https://docker.com
[Terraform]: https://terraform.io
[Cloudformation]: https://aws.amazon.com/cloudformation/
[Terragrunt]: https://github.com/gruntwork-io/terragrunt
[Astro]: https://github.com/uber/astro

[Introduction]: #introduction

[Features]: #features

[Getting started]: #getting-started
[Requirements]: #requirements
[Configuring]: #configuring


[Examples]: #examples

[Development]: #development

[Contributing]: #contributing

#### Table of Contents

1. [Introduction - What is Bedrock?][Introduction]
2. [Features][Features]
3. [Getting started - How to use Bedrock][Getting started]
	- [Requirements]
	- [Configuring]
    - [Examples - common usage scenarios][Examples]
4. [Development - Guide for contributing to the Bedrock project][Development]
    - [Contributing to Bedrock][Contributing]

## Introduction

Bedrock is a collection of managed role-based policies and Terraform-based blueprints to assist with provisioning 
infrastructure and services. When we design modern computing architectures it is important to consider security, 
reliability and efficiency as equally important concerns. With public Cloud architectures in particular, security must 
be addressed throughout the entire architecture, and not just at the perimiter.

Role-based access control (RBAC) allows us to restrict actors to the minimum required permissions, which is commonly 
referred to as the [principle of least privilege], and is the basis for the architectural blueprints provided by 
Bedrock. 

### Terraform

The Bedrock blueprints are based on popular tools such as [Terraform] and [Cloudformation], and provide both an 
informative and practical approach to infrastructure provisioning. You are encouraged to explore and critique these 
blueprints as they should continue to evolve over time.

## Features

The purpose of Bedrock is not only to provide best-practice blueprints for modern architectures, but to explore and
educate about the challenges, decisions and opinions behind the designs themselves. As such, Bedrock aims to avoid
a "black box" approach and is designed to encourage hacking and examining the underlying code.

### Blueprint

Blueprints provide an opinionated approach to provisioning an infrastructure component based on common and/or best-
practice approaches. 

Blueprints may be either platform-based (i.e. AWS, Azure, Openstack, etc.) or service-based (i.e
NGINX, Bastion, Squid Proxy, etc.). Typically they are identified using one of the following naming conventions:

    <platform>-<service>[-<component>]
    
    examples: aws-ec2-autoscaling, aws-ecs-cluster, azure-cdn, openstack-network, etc.
    
    or;
    
    <service>[-<component>][-<platform>]
    
    examples: nginx-reverseproxy-aws, bastion-do, rancher-stack, squidproxy-aws, etc.
    
  

### Manifest

A manifest provides a way to define one or more collections of blueprints (a constellation) and associated 
configurations that make up a complete architecture.

Often a single blueprint is not sufficient to define a Cloud architecture as they are more likely to be distributed 
across multiple services. For example, you might have an ECS cluster for web/API applications, RDS or DynamDB for 
persistence, and S3 for archiving.

Within each of these tiers are additional ancillary services such as route53 for well-known endpoints and/or service 
discovery, cloudwatch events/triggers, etc. The collection of blueprints that encapsulates and independent function is 
called a constellation. Multiple constellations may be defined in a single manifest such that an entire architecture may 
be provisioned.

A manifest also provides a higher-order language that can be used to unambiguously describe novel Cloud architectures 
that are composed of well-defined blueprints.


### Exploration

Each Bedrock module is designed to exist independently from the rest, to allow maximum portability and sharing of code.
You can go into any module directory and run `terraform init && terraform apply` to execute a blueprint in your
configured environment.

For example, if you require a Bastion host in your AWS account, do the following:

    # provision IAM roles for creating Bastion host
    cd terraform/blueprints/bastion/roles
    terraform init && terraform apply
     
    # provision a new Bastion EC2 host
    cd ../aws
    terraform init && terraform apply -var bastion_user=bedrock   
    

### Run Anywhere

You can also build any Bedrock module as a [Docker] image, that can be run anywhere Docker is supported. Building images
is supported via a Makefile in the root directory, which you can execute as follows:

    # Build Docker images for Bastion roles and instance
    make bastion-roles bastion-aws
    
The Makefile will ensure dependencies are build in the right order, and includes support for tagging and push to a
remote Docker registry:

    # Tag and push to AWS ECR
    REGISTRY=<aws_account_id>.dkr.ecr.ap-southeast-2.amazonaws.com make tag push bastion-aws
    
After building an image you can now use the provided scripts to execute the blueprint in the current working directory:

    # provision a new Bastion EC2 host
    export BEDROCK_REGISTRY=<aws_account_id>.dkr.ecr.ap-southeast-2.amazonaws.com
    bastion/scripts/bastion-aws.sh init && bastion/scripts/bastion-aws.sh apply
     

### Automation

As the Docker images for Bedrock blueprints can be run anywhere that supports Docker, it is now possible to integrate
with automated deployment and provisioning tools also. This might include build tools such as Jenkins or Bamboo, and
also integrated with Cloud platforms such as AWS via the AWS Developer Tools (CodeBuild, CodePipeline, etc.).

As an example, we might configure a CodeBuild project to provision a blueprint using configuration from an S3 Bucket.
Using S3 Bucket notifications we can trigger a build by simply updating a blueprint configuration. This allows for a
very minimal effort approach to provisioning sophisticated and secure architectures whilst retaining the ability to
maintain and evolve the designs.

### Comparison with other tools

#### Terragrunt

[Terragrunt] provides a wrapper to Terraform that enforces consistency and reduces code duplication across multiple 
modules. Whilst Bedrock offers similar module grouping via the manifest file, it does not impose constraints on the code
 in each module, nor does it hide the underlying Terraform code.

#### Astro

[Astro] offers dependency mapping between Terraform modules and concurrent execution. Bedrock provides rudimentary 
dependency mapping (via sequential execution of the manifest), it doesn't yet support concurrent execution.

## Getting started

The prerequisites for running the examples below are as follows:

### Environment variables

Ensure you have set the following environment variables:

	AWS_ACCESS_KEY_ID = <your AWS access key>
	AWS_SECRET_ACCESS_KEY = <your AWS secret key>
	AWS_DEFAULT_REGION = <your AWS region>

### Build Docker images

	$ cd blueprints && make all
	
### Initial manifests

The following manifests are required to configure appropriate IAM roles/permissions

	$ bin/bedrock.py -m manifests/iam.yml init && bin/bedrock.py -m manifests/iam.yml apply


### Bedrock Manifest Tool

A collection of helper tools for Bedrock are available in the Python Package Index (pypi.org),
and can be installed as follows:

    $ pip install brock

The first manifest you run should initialise your environment, for example:

    ## Contents of bedrock-init.yml
    name: AWS Initialisation
    
    description: Create Bedrock IAM roles and an S3 bucket for storing Terraform state
    
    constellations:
      policies:
        iam-policies:
    
      roles:
        iam-roles:
    
      default:
        terraform-state-aws:

You can then run this using the Bedrock Manifest Tool:

    $ bmt init -m bedrock-init.yml
    $ TF_APPLY_ARGS=-auto-approve bmt apply -m bedrock-init.yml
    
The first command will initialise the Terraform providers/plugins, whilst the second will provision the IAM roles
and S3 bucket required for Bedrock provisioning.

_NOTE: As of this writing the above manifest will create 15 IAM policies, 2 IAM roles and 1 S3 bucket._

If you ever need to switch accounts where Terraform state is stored you can do this by reconfiguring
the Terraform backend as follows:

    TF_INIT_ARGS=-reconfigure bmt init -m bedrock-init.yml
    

### Examples

#### Provision a Bastion host

The following manifest file describes how to deploy an EC2 instance as a Bastion host:

    name: AWS Bastion Host
    
    description: Provision an EC2 instance for Bastion
    
    constellations:
      bastion:
        bastion-roles:
        bastion-aws:
          bastion_user: fortuna

You can execute this file as follows:

    $ bmt apply -m bastion.yml -c ssh_key=@~/.ssh/id_rsa.pub
    
This command will apply the manifest in your AWS account, overriding the `ssh_key`
input variable using the public SSH key from your local SSH configuration.

#### Deploy Lambda Layers

The following manifest will create common Lambda Layers for use in Lambda functions:

    name: Lambda Layers
    
    description: Create Lambda Layers to support Bedrock Lambda blueprints
    
    constellations:
      aws-java-sdk-lambda:
        lambda-layer:
          layer_name: aws-java-sdk-lambda
          description: Support for the AWS Lambda SDK for Java
          content_path: /tools/aws-java-sdk-lambda/build/layer
          runtimes:
            - java8
    
      groovy-runtime:
        lambda-layer:
          layer_name: groovy-runtime
          description: Support for the Groovy JVM language
          content_path: /tools/groovy-runtime/build/layer
          runtimes:
            - java8
    
      python-requests:
        lambda-layer:
          layer_name: python-requests
          description: Python requests package plus dependencies
          content_path: /tools/python-requests/packages
          runtimes:
            - python3.6

Note that this manifest requires an additional volume to provide input for the `content_path` variable:

    $ bmt apply -m lambda-layers.yml -v "$PWD/tools:/tools"
    
    
### Requirements

To make use of Bedrock you must have access to a public Cloud and a local
environment with [Docker] installed.

If you intend to build the Docker images from source you will also require
make to be installed.

### Configuring

Configuration will depend on the Cloud environment(s) available, but typically
will involve setting an API key in your environment that allows [Terraform]
access to resources in your account.

When using API keys we want to restrict access to the bare minimum required
to perform the required tasks (Principle of least privilege). As such you
should ensure the associated user has just the permissions outlined in the
table below:

| Cloud Provider | Service | Permission |
|----------------|:-------:|:----------:|
|AWS|Codebuild|Execute|
|Digital Ocean|API|Full access|

### Terraform

You can manage your Terraform state using either local storage or with an AWS S3 bucket.
It is advisable to use S3 to protect your state, in which case you will require a user with
the following IAM permissions:

| IAM Permission | Description | ARN |
|----------------|-------------|-----|
|S3 Bucket create|Creates an S3 bucket containing Terraform state|arn:aws:iam::&lt;AWS account ID&gt;:policy/bedrock-terraform-state|
|IAM Policy create|Creates an IAM policy to allow access to read/write to the S3 Bucket|arn:aws:iam::&lt;AWS account ID&gt;:policy/bedrock-terraform-state|


### AWS

For provisioning blueprints in AWS you will require a user with the following IAM permissions:

| IAM Permission | Description | ARN |
|----------------|-------------|-----|
|Terraform state (*)|Read/write permissions to S3 bucket containing Terraform state|arn:aws:iam::&lt;AWS account ID&gt;:policy/bedrock-terraform-state|
|Assume role|Can assume role required for blueprint provisioning|arn:aws:iam::&lt;AWS account ID&gt;:role/*-bedrock-*|

* Note that the `Terraform state` permission is only required when state is stored in AWS.

## Development

### Building Docker images

If you want to build the blueprint Docker images locally a `Makefile` is provided that supports the following
goals:

    # Build all blueprints with the default settings
    make all 

    # Build a specific set of blueprints    
    make <blueprint> [<blueprint>...]
    
    # Build blueprints with a specific Terraform version
    BUILD_ARGS="--build-arg TERRAFORM_VERSION=0.11.4" make all    
    
    # Generate documentation (README) for all blueprints
    make docs
    
    # Tag and push blueprints to a custom registry
    REGISTRY="https://my.docker.registry/bedrock" make tag push 


### Contributing

Open source software is made stronger by the community that supports it. Through participation you not only contribute 
to the quality of the software, but also gain a deeper insight into the inner workings.

Contributions may be in the form of feature enhancements, bug fixes, test cases, documentation and forum participation. 
If you have a question, just ask. If you have an answer, write it down.

And if you are somehow constrained from participation, through corporate policy or otherwise, consider financial 
support. After all, if you are profiting from open source it's only fair to give something back to the community that 
make it all possible.

## Developer Environment

Use the following tools to provision a pre-configured developer environment.

### Vagrant

    $ vagrant up
    $ ssh -p 2222 -L 8080:localhost:8080 vagrant@localhost  # password: vagrant

### Docker

    $ docker build -t bedrock-env .
    $ ./developer-env.sh
