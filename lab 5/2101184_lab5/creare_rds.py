import boto3

# Define your AWS region and credentials (you can also use IAM roles if running on EC2)
region = 'ap-south-1'
access_key = 'accesskey'
secret_key = 'secretaccesskey'

# Initialize the RDS client
client = boto3.client('rds', region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)

# Define RDS instance parameters
db_instance_identifier = 'lab5'
db_instance_type = 'db.t2.micro'  # Adjust the instance class as needed
db_engine = 'MySQL'
db_engine_version = '8.0.33'  # MySQL version
db_name = 'lab5_db'
db_master_username = 'root'
db_master_password = 'pwdxxxxx'


# Create the RDS instance
response = client.create_db_instance(
    DBInstanceIdentifier=db_instance_identifier,
    AllocatedStorage=20,  # Adjust storage size as needed
    DBInstanceClass=db_instance_type,
    Engine=db_engine,
    EngineVersion=db_engine_version,
    MasterUsername=db_master_username,
    MasterUserPassword=db_master_password,
    DBName=db_name,
    MultiAZ=False,  # Set to True for Multi-AZ deployment
    PubliclyAccessible=True,  # Allow public access for testing
    VpcSecurityGroupIds=['sg-xxxxxxxxx'],  # Replace with your security group ID
    #CACertificateIdentifier=
    Port=3306

)

print("Creating MySQL RDS instance...")

# Wait for the RDS instance to be created
waiter = client.get_waiter('db_instance_available')
waiter.wait(DBInstanceIdentifier=db_instance_identifier)

print("MySQL RDS instance created.")

# Retrieve the RDS instance endpoints
response = client.describe_db_instances(DBInstanceIdentifier=db_instance_identifier)
db_instance = response['DBInstances'][0]

print("RDS Instance Details:")
print(f"DB Instance Identifier: {db_instance['DBInstanceIdentifier']}")
print(f"DB Instance Class: {db_instance['DBInstanceClass']}")
print(f"Engine: {db_instance['Engine']}")
print(f"Engine Version: {db_instance['EngineVersion']}")
print(f"DB Name: {db_instance['DBName']}")
print(f"Master Username: {db_instance['MasterUsername']}")
print(f"Allocated Storage (GiB): {db_instance['AllocatedStorage']}")
print(f"Multi-AZ Deployment: {db_instance['MultiAZ']}")
print(f"Publicly Accessible: {db_instance['PubliclyAccessible']}")
print(f"DB Subnet Group: {db_instance['DBSubnetGroup']['DBSubnetGroupName']}")
print(f"Endpoint Address: {db_instance['Endpoint']['Address']}")
print(f"Endpoint Port: {db_instance['Endpoint']['Port']}")
print(f"Availability Zone: {db_instance['AvailabilityZone']}")
print(f"Preferred Maintenance Window: {db_instance['PreferredMaintenanceWindow']}")
print(f"Backup Retention Period (days): {db_instance['BackupRetentionPeriod']}")
print(f"Preferred Backup Window: {db_instance['PreferredBackupWindow']}")
print(f"Port: {db_instance['Endpoint']['Port']}")
print(f"Engine Version: {db_instance['EngineVersion']}")
print(f"Auto Minor Version Upgrade: {db_instance['AutoMinorVersionUpgrade']}")
print(f"License Model: {db_instance['LicenseModel']}")
print(f"IOPS: {db_instance['Iops'] if 'Iops' in db_instance else 'N/A'}")

