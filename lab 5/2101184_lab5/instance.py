import boto3
user_data_script = '''#!/bin/bash
# Your startup script commands here
# Update the package repository
sudo yum update -y

# Configure AWS CLI with access keys
aws configure set aws_access_key_id accesskey
aws configure set aws_secret_access_key secretaccesskey
aws configure set default.region ap-south-1

# Copy website files from S3 to the Apache web root directory
aws s3 cp s3://lab5/ /home --recursive

# Ensure correct ownership and permissions
chown -R apache:apache /var/www/html
chmod -R 755 /var/www/html

# Install Python 3 and pip
sudo yum install python3 -y
sudo yum install python3-pip -y

# Install Flask and other dependencies
pip3 install Flask
pip3 install pymysql

sudo rpm --import https://repo.mysql.com/RPM-GPG-KEY-mysql-2022
sudo yum install -y https://dev.mysql.com/get/mysql57-community-release-el7-11.noarch.rpm
sudo yum install -y mysql-community-client

echo "Website setup complete!"'''
# AWS credentials and region
aws_access_key = 'accesskey'
aws_secret_key = 'secretaccesskey'
aws_region = 'ap-south-1'  # Change to your desired region

# ---------------------------------------------------------------------------------------------------------------------------------------

# EC2 settings
ec2_instance_type = 't2.micro'  # Modify as needed
ec2_ami_id = 'ami-xxxxxx'  # Replace with the AMI ID for your desired OS
ec2_security_group_id = 'xxxxxxxx'  # Specify the security group ID
ec2_key_pair_name = 'sarthak'  # Replace with your key pair name
ec2_instance_user_data = user_data_script  # Read the startup script

# Create EC2 client
ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)

# Launch EC2 instance
ec2_response = ec2_client.run_instances(
    ImageId=ec2_ami_id,
    InstanceType=ec2_instance_type,
    SecurityGroupIds=[ec2_security_group_id],
    KeyName=ec2_key_pair_name,
    UserData=ec2_instance_user_data,
    MinCount=1,
    MaxCount=1,
)

print("EC2 instance creation response:", ec2_response)


