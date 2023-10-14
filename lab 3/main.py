import boto3
import time
import base64

def get_instance_public_dns(instance):
    instance.wait_until_running()
    instance.reload()
    public_dns = instance.public_dns_name
    return public_dns

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
aws s3 cp s3://s3-bucket/website/ /var/www/html --recursive

# Ensure correct ownership and permissions
chown -R apache:apache /var/www/html
chmod -R 755 /var/www/html

# http port range =80 
curl localhost:80

# Restart Apache to apply changes
systemctl restart httpd

echo "Website setup complete!"
'''

def launch_instance(ec2, image_id, instance_type, key_name):
    response = ec2.run_instances(
        ImageId=image_id,
        InstanceType=instance_type,
        MinCount=1,
        MaxCount=1,
        KeyName=key_name
    )
    return response['Instances'][0]['InstanceId']

def list_instances(ec2):
    instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    return list(instances)

def main():
    # AWS credentials and region
    aws_access_key_id = 'accesskey'
    aws_secret_access_key = 'secretaccesskey'
    region = 'ap-south-1'

    security_group_name = 'apache-security-group'
    security_group_description = 'Security group for web server'
    security_group_port = 80

    # Connect to EC2 service
    ec2_client = boto3.client('ec2', region_name=region,
                            aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key)
    ec2 = boto3.resource('ec2', region_name=region,aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key) 
    key_name = 'sarthak'
    
    while True:
        print("1. Launch an Amazon Linux instance")
        print("2. Launch two Ubuntu instances")
        print("3. List all running instances")
        print("4. Check instance health of all running instances")
        print("5. Host an HTTP server in an instance")
        print("6. Stop instances")
        print("7. Terminate instances")
        print("8. Exit")
        
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            instance_id = launch_instance(ec2_client, 'ami-xxxxxxxx', 't2.micro', key_name)  
            print(f"Launched Amazon Linux instance with ID: {instance_id}")
            time.sleep(3)
        elif choice == 2:
            for _ in range(2):
                instance_id = launch_instance(ec2_client, 'ami-xxxxxxxxx', 't2.micro', key_name)  
                print(f"Launched Ubuntu instance with ID: {instance_id}")
                time.sleep(3)
        elif choice == 3:
            instances = list_instances(ec2)
            for instance in instances:
                print(f"Instance ID: {instance.id}, State: {instance.state['Name']}")
                time.sleep(3)
        elif choice == 4:
            
            # response = ec2_client.describe_instances()

            # for reservation in response['Reservations']:
            #     for instance in reservation['Instances']:
            #         if instance['State']['Name']=="running":
            #             instance_id = instance['InstanceId']
            #             instance_state = instance['State']['Name']
            #             instance_type = instance['InstanceType']
            #             instance_public_dns = instance.get('PublicDnsName', 'N/A')
            #             instance_private_ip = instance.get('PrivateIpAddress', 'N/A')
            #             instance_name = 'N/A'
            #             for tag in instance.get('Tags', []):
            #                 if tag['Key'] == 'Name':
            #                     instance_name = tag['Value']

            #             print(f"Instance ID: {instance_id}")
            #             print(f"Instance Name: {instance_name}")
            #             print(f"Instance State: {instance_state}")
            #             print(f"Instance Type: {instance_type}")
            #             print(f"Public DNS: {instance_public_dns}")
            #             print(f"Private IP: {instance_private_ip}")
            #             print("=" * 40)
            #             time.sleep(3)
            instance_id = input("Enter instance ID: ")
            response = ec2_client.describe_instance_status(InstanceIds=[instance_id])

            if len(response['InstanceStatuses']) > 0:
                status = response['InstanceStatuses'][0]['InstanceStatus']['Status']
                if status == 'ok':
                    print("Instance is healthy and responding to network requests")
                else:
                    print("Instance is running, but not responding to network requests")
            else:
                print("Instance is not running or does not exist")

        elif choice == 5:
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
            instance = ec2.create_instances(
                ImageId='ami-xxxxxxxx',  
                InstanceType='t2.micro',
                MinCount=1,
                MaxCount=1,
                UserData=user_data_script,
                SecurityGroups=[security_group_name],
                KeyName='sarthak'  
            )[0]

            print(f"Instance launched: {instance.id}") 
            instance = ec2.Instance(instance.id) 
            print(f"HTTP server hosted on instance ID: {instance.id}")
            public_dns_address = get_instance_public_dns(instance)
            print(f"Instance public DNS: {public_dns_address}")
        elif choice == 6:
            instance_ids = input("Enter instance IDs to stop (comma-separated): ").split(",")
            ec2.instances.filter(InstanceIds=instance_ids).stop()
            print(f"Stopping instances with IDs: {', '.join(instance_ids)}")
        elif choice == 7:
            instance_ids = input("Enter instance IDs to terminate (comma-separated): ").split(",")
            ec2.instances.filter(InstanceIds=instance_ids).terminate()
            print(f"Terminating instances with IDs: {', '.join(instance_ids)}")
        elif choice == 8:
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
