import boto3

aws_access_key = 'AKIA6F7IQZA6XPWKGTWW'
aws_secret_key = '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'
aws_region = 'ap-south-1' 
# Initialize the Elastic Beanstalk client
eb_client = boto3.client('elasticbeanstalk', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)
application_name = 'lab6sarthak'
version_label = 'v1'
source_bundle = {
    'S3Bucket': 'lab6sarthak',
    'S3Key': 'website.zip'  
}
# Create an Elastic Beanstalk application
response = eb_client.create_application(
    ApplicationName=application_name,
)
response = eb_client.create_application_version(
    ApplicationName=application_name,
    VersionLabel=version_label,
    SourceBundle=source_bundle,
    AutoCreateApplication=True  
)
# Create an Elastic Beanstalk environment
response = eb_client.create_environment(
    ApplicationName=application_name,
    CNAMEPrefix=application_name,
    EnvironmentName='cc-lab-6',
    SolutionStackName='64bit Amazon Linux 2023 v4.0.3 running Python 3.11',
    VersionLabel=version_label,
    OptionSettings = [
                {
                    'Namespace': 'aws:autoscaling:launchconfiguration',
                    'OptionName': 'IamInstanceProfile',
                    'Value': 'ec2-instance-profile'
                },{
                    'Namespace':'aws:autoscaling:launchconfiguration',
                    'OptionName': 'EC2KeyName',
                    'Value':'sarthak'
                },{
                    'Namespace': 'aws:autoscaling:asg',
                    'OptionName': 'MinSize',
                    'Value': '1'
                },{
                    'Namespace': 'aws:autoscaling:asg',
                    'OptionName': 'MaxSize',
                    'Value': '3'
                },{
                    "Namespace": "aws:autoscaling:trigger",
                    "OptionName": "MeasureName",
                    "Value": "CPUUtilization",
                },{
                    "Namespace": "aws:autoscaling:trigger",
                    "OptionName": "BreachDuration",
                    "Value": "5",
                },{
                    "Namespace": "aws:autoscaling:trigger",
                    "OptionName": "LowerThreshold",
                    "Value": "30",
                },{
                    "Namespace": "aws:autoscaling:trigger",
                    "OptionName": "LowerBreachScaleIncrement",
                    "Value": "-1",
                },{
                    "Namespace": "aws:autoscaling:trigger",
                    "OptionName": "Period",
                    "Value": "5",
                },{
                    "Namespace": "aws:autoscaling:trigger",
                    "OptionName": "EvaluationPeriods",
                    "Value": "2",
                },{
                    "Namespace": "aws:autoscaling:trigger",
                    "OptionName": "Statistic",
                    "Value": "Average",
                },{
                    "Namespace": "aws:autoscaling:trigger",
                    "OptionName": "Unit",
                    "Value": "Percent",
                },{
                    "Namespace": "aws:autoscaling:trigger",
                    "OptionName": "UpperBreachScaleIncrement",
                    "Value": "1",
                },{
                    "Namespace": "aws:autoscaling:trigger",
                    "OptionName": "UpperThreshold",
                    "Value": "80",
                }
                
    ]
    # Add other configurations as needed
)

