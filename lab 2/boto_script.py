import boto3
import time

# AWS credentials and region
aws_access_key_id = 'accesskey'
aws_secret_access_key = 'secretaccesskey'
region = 'ap-south-1'

# User data script (replace with your script content)
user_data_script = '''#!/bin/bash
# Your startup script commands here
# Update the package repository
yum update -y

# Install Apache
yum install -y httpd

# Start Apache and enable it to start on boot
systemctl start httpd
systemctl enable httpd

# Configure AWS CLI with access keys
aws configure set aws_access_key_id accesskey
aws configure set aws_secret_access_key secretaccesskey
aws configure set default.region ap-south-1

# Copy website files from S3 to the Apache web root directory
aws s3 cp s3://boto-bucket84/website/ /var/www/html --recursive

# Ensure correct ownership and permissions
chown -R apache:apache /var/www/html
chmod -R 755 /var/www/html

# http port range =80 
curl localhost:80

# Restart Apache to apply changes
systemctl restart httpd

echo "Website setup complete!"
'''

# Security group settings
security_group_name = 'apacheee-server-group'
security_group_description = 'Security group for web server'
security_group_port = 80

# Launch an EC2 instance
def launch_ec2_instance():
    ec2 = boto3.resource('ec2', region_name=region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    # Create security group
    security_group = ec2.create_security_group(
        GroupName=security_group_name,
        Description=security_group_description
    )
    
    # Allow incoming traffic on port 80- http
    security_group.authorize_ingress(
        IpProtocol='tcp',
        FromPort=security_group_port,
        ToPort=security_group_port,
        CidrIp='0.0.0.0/0'
    )
    # Allow incoming traffic on port 22 - ftp
    security_group.authorize_ingress(
        IpProtocol='tcp',
        FromPort=22,
        ToPort=22,
        CidrIp='0.0.0.0/0'
    )
    # Allow incoming traffic on port 443 - https
    security_group.authorize_ingress(
        IpProtocol='tcp',
        FromPort=443,
        ToPort=443,
        CidrIp='0.0.0.0/0'
    )

    # Launch instance
    instance = ec2.create_instances(
        ImageId='ami-xxxxxxxxxxx',  # Replace with the appropriate AMI ID
        InstanceType='t2.micro',
        MinCount=1,
        MaxCount=1,
        SecurityGroups=[security_group_name],
        UserData=user_data_script,
        KeyName='sarthak'  # Replace with your EC2 key pair name
    )[0]

    print(f"Instance launched: {instance.id}")
    # Add a name tag to the instance
    ec2_client = boto3.client('ec2', region_name=region,
                              aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key)
    
    ec2_client.create_tags(Resources=[instance.id], Tags=[{'Key': 'Name', 'Value': 'lab2_practice4'}])
    
    print("Instance name tag added.")
    return instance

# Wait for instance to reach "running" state and return public DNS
def get_instance_public_dns(instance):
    instance.wait_until_running()
    instance.reload()
    public_dns = instance.public_dns_name
    return public_dns

def check_instance_status(instance):
    print("Waiting for instance to reach 'running' state...")
    while instance.state['Name'] != 'running':
        time.sleep(5)  # Wait for 5 seconds before checking again
        instance.reload()  # Refresh instance information
    print("Instance is now in 'running' state.")

if __name__ == '__main__':
    launched_instance = launch_ec2_instance()
    check_instance_status(launched_instance)
    public_dns_address = get_instance_public_dns(launched_instance)
    print(f"Instance public DNS: {public_dns_address}")
   