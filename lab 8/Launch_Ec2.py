import boto3

aws_access_key = 'xxxxxxxxxxxxx'
aws_secret_key = 'xxxxxxxxxxxxxx'
aws_region = 'ap-south-1' 

def ec2_init():
    user_data_1 = """#!/bin/bash
    yum update -y
    yum install -y docker
    service docker start
    mkdir newfolder
    cd newfolder
    aws s3 sync s3://lab8-page-1 .
    cd main
    docker build -t webapp .
    docker run -dit -p 80:55000  webapp
    """
    user_data_2 = """#!/bin/bash
    yum update -y
    yum install -y docker
    service docker start
    mkdir newfolder
    cd newfolder
    aws s3 sync s3://lab8-page-2 .
    cd another
    docker build -t webapp .
    docker run -dit -p 80:45000 webapp   
    """
    user_data_3 = """#!/bin/bash
    yum update -y
    yum install -y docker
    service docker start
    mkdir newfolder
    cd newfolder
    aws s3 sync s3://lab8-page-3 .
    cd third
    docker build -t webapp .
    docker run -dit -p 80:50000 webapp   
    """
    ec2 = boto3.resource("ec2", aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)
    api = boto3.client("apigatewayv2", aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)
    instances1 = ec2.create_instances(
        ImageId="ami-xxxxxxxxxxx",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        KeyName="sarthak",
        SecurityGroupIds=["sg-09f7xxxxxxxxxxxx"],
        IamInstanceProfile={
           "Arn":"arn:aws:iam::xxxxxxxxxx:instance-profile/ec2-instance-profile"
        },
        TagSpecifications=[{'ResourceType': 'instance', 'Tags': [{'Key': 'Name', 'Value': 'Web_1'}]}],
        UserData=user_data_1,
    )
    instances2 = ec2.create_instances(
        ImageId="ami-xxxxxxxxxxx",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        KeyName="sarthak",
        SecurityGroupIds=["sg-09f7xxxxxxxxxxxx"],
        IamInstanceProfile={
           "Arn":"arn:aws:iam::xxxxxxxxxxxxxxx:instance-profile/ec2-instance-profile"
        },
        TagSpecifications=[{'ResourceType': 'instance', 'Tags': [{'Key': 'Name', 'Value': 'Web_2'}]}],
        UserData=user_data_2,
    )
    instances3 = ec2.create_instances(
        ImageId="ami-xxxxxxxxxxx",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        KeyName="sarthak",
        SecurityGroupIds=["sg-09f7xxxxxxxxxxxx"],
        IamInstanceProfile={
           "Arn":"arn:aws:iam::xxxxxxxxxxxxxxx:instance-profile/ec2-instance-profile"
        },
        TagSpecifications=[{'ResourceType': 'instance', 'Tags': [{'Key': 'Name', 'Value': 'Web_3'}]}],
        UserData=user_data_3,
    )

    instance_one = instances1[0]
    instance_one.wait_until_running()
    instance_two = instances2[0]
    instance_two.wait_until_running()
    instance_three = instances3[0]
    instance_three.wait_until_running()
    instance_one.load()
    print(instance_one.public_dns_name)
    instance_two.load()
    print(instance_two.public_dns_name)
    instance_three.load()
    print(instance_three.public_dns_name)

    
    response1 = api.create_api(
        Name="one",
        ProtocolType="HTTP",
        Target="http://"+instance_one.public_dns_name
    )
    response2 = api.create_api(
        Name="two",
        ProtocolType="HTTP",
        Target="http://"+instance_two.public_dns_name
    )
    response3 = api.create_api(
        Name="three",
        ProtocolType="HTTP",
        Target="http://"+instance_three.public_dns_name
    )
    api_one = response1["ApiEndpoint"]
    api_two = response2["ApiEndpoint"]
    api_three = response3["ApiEndpoint"]
    print("api_one endpoint: "+api_one+"\n")
    print("api_two endpoint: "+api_two+"\n")
    print("api_three endpoint: "+api_three+"\n")

    user_data_4 = """#!/bin/bash
yum update -y
yum install -y docker
service docker start
mkdir newfolder
cd newfolder
aws s3 sync s3://lab8-main-page .
cd storefront
cd playground
cat >> views.py <<EOL
from django.shortcuts import render
from django.http import HttpResponse
import requests
def index(request):
    return render(request, "index.html")
response_one = requests.get("%s")
response_two = requests.get("%s")
response_three = requests.get("%s")
def one(request):
    return HttpResponse(response_one.text)
def two(request):
    return HttpResponse(response_two.text)
def three(request):
    return HttpResponse(response_three.text)
EOL
cd ..
docker build -t webapp .
docker run -dit -p 80:8000 webapp"""%(api_one, api_two, api_three)

    instances4 = ec2.create_instances(
        ImageId="ami-xxxxxxxxxxx",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        KeyName="sarthak",
        SecurityGroupIds=["sg-09f7xxxxxxxxxxxx"],
        IamInstanceProfile={
           "Arn":"arn:aws:iam::xxxxxxxxxxxxxxx:instance-profile/ec2-instance-profile"
        },
        TagSpecifications=[{'ResourceType': 'instance', 'Tags': [{'Key': 'Name', 'Value': 'main'}]}],
        UserData=user_data_4,
    )

    instance_four = instances4[0]
    instance_four.wait_until_running()
    instance_four.load()
    print(instance_four.public_dns_name)


ec2_init()
