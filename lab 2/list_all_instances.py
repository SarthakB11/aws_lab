import boto3

# AWS credentials and region
aws_access_key_id = 'accesskey'
aws_secret_access_key = 'secretaccesskey'
region = 'ap-south-1'

# Connect to EC2 service
ec2_client = boto3.client('ec2', region_name=region,
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key)

def list_existing_instances():
    # List all instances
    response = ec2_client.describe_instances()

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_state = instance['State']['Name']
            instance_type = instance['InstanceType']
            instance_public_dns = instance.get('PublicDnsName', 'N/A')
            instance_private_ip = instance.get('PrivateIpAddress', 'N/A')
            instance_name = 'N/A'
            for tag in instance.get('Tags', []):
                if tag['Key'] == 'Name':
                    instance_name = tag['Value']

            print(f"Instance ID: {instance_id}")
            print(f"Instance Name: {instance_name}")
            print(f"Instance State: {instance_state}")
            print(f"Instance Type: {instance_type}")
            print(f"Public DNS: {instance_public_dns}")
            print(f"Private IP: {instance_private_ip}")
            print("=" * 40)

if __name__ == '__main__':
    list_existing_instances()