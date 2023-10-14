import boto3


def ec2_init():
    user_data = """#!/bin/bash
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
    ec2 = boto3.resource("ec2")
    instances = ec2.create_instances(
        ImageId="ami-xxxxxxxxxxxx",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        KeyName="sarthak",
        SecurityGroupIds=["sg-xxxxxxxxxxx"],
        IamInstanceProfile={
            "Arn": "arn:aws:iam::xxxxxxxxxxxx:instance-profile/ec2-s3-ro"
        },
        UserData=user_data,
    )
    instance = instances[0]
    instance.wait_until_running()
    instance.load()
    print(instance.public_dns_name)


ec2_init()
