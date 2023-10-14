import boto3

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
#755: 7 for owner(4+2+1), 5 for file group and others(4+1) rwx r-read,w-write,x-execute
aws_access_key = 'accesskey'
aws_secret_key = 'secretaccesskey'
aws_region = 'ap-south-1' 

security_group_name = 'lab4-server-group'
security_group_description = 'Security group for web server'
security_group_port = 80

autoscaling = boto3.client('autoscaling', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)

ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)
ec2 = boto3.resource('ec2', region_name=aws_region,aws_access_key_id=aws_access_key,aws_secret_access_key=aws_secret_key) 

# Create security group
security_group = ec2.create_security_group(
    GroupName=security_group_name,
    Description=security_group_description
)

# Allow incoming traffic on port 80 for http
security_group.authorize_ingress(
    IpProtocol='tcp',
    FromPort=security_group_port,
    ToPort=security_group_port,
    CidrIp='0.0.0.0/0'
)
# Allow incoming traffic on port 22 for ftp
security_group.authorize_ingress(
    IpProtocol='tcp',
    FromPort=22,
    ToPort=22,
    CidrIp='0.0.0.0/0'
)
# Allow incoming traffic on port 443 for https
security_group.authorize_ingress(
    IpProtocol='tcp',
    FromPort=443,
    ToPort=443,
    CidrIp='0.0.0.0/0'
)

autoscaling.create_launch_configuration(
    LaunchConfigurationName='lab4-launch-config',
    ImageId='ami-xxxxxxxxx', 
    InstanceType='t2.micro',  
    UserData=user_data_script,
    SecurityGroups=[security_group_name],  
)

auto_scaling_group_name = 'lab4-auto-scale-group'

autoscaling.create_auto_scaling_group(
    AutoScalingGroupName=auto_scaling_group_name,
    LaunchConfigurationName='lab4-launch-config',
    MinSize=1,
    MaxSize=3,
    DesiredCapacity=2,
    AvailabilityZones=['ap-south-1a','ap-south-1b'],  
    HealthCheckType='EC2',
)

scale_up_policy_name = 'scale-up-policy'
scale_down_policy_name = 'scale-down-policy'

response_scale_up = autoscaling.put_scaling_policy(
    PolicyName=scale_up_policy_name,
    AutoScalingGroupName=auto_scaling_group_name,
    AdjustmentType='ChangeInCapacity',
    ScalingAdjustment=1,
    Cooldown=15,
)

autoscaling_policy_arn_up = response_scale_up['PolicyARN']

response_scale_down = autoscaling.put_scaling_policy(
    PolicyName=scale_down_policy_name,
    AutoScalingGroupName=auto_scaling_group_name,
    AdjustmentType='ChangeInCapacity',
    ScalingAdjustment=-1,
    Cooldown=15,
)

autoscaling_policy_arn_down = response_scale_down['PolicyARN']

cloudwatch = boto3.client('cloudwatch',aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)

cloudwatch.put_metric_alarm(
    AlarmName='scale-up-alarm',
    ComparisonOperator='GreaterThanThreshold',
    EvaluationPeriods=1,
    MetricName='CPUUtilization',
    Namespace='AWS/EC2', # for using group of ec2 services
    Period=10,
    Statistic='Average',
    Threshold=25,
    ActionsEnabled=True,
    AlarmActions=[autoscaling_policy_arn_up],
)

cloudwatch.put_metric_alarm(
    AlarmName='scale-down-alarm',
    ComparisonOperator='LessThanThreshold',
    EvaluationPeriods=1,
    MetricName='CPUUtilization',
    Namespace='AWS/EC2',
    Period=10,
    Statistic='Average',
    Threshold=10,
    ActionsEnabled=True,
    AlarmActions=[autoscaling_policy_arn_down],
)

print("Created Auto Scaling Configurations for a Web-Tier Cloud Application.")