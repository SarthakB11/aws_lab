import boto3

aws_access_key = 'xxxxxxxx'
aws_secret_key = 'xxxxxxx'
aws_region = 'ap-south-1' 
cf_client = boto3.client('cloudfront', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)

cf_client.create_distribution(
    DistributionConfig={
        "CallerReference": "09-09-2023",
        "DefaultRootObject": "image1.jpg",

        'Origins': {
            'Quantity': 1,
            'Items': [
                {
                    'Id': 'xxxxxx-origin',
                    'DomainName': 'xxxxxxxx.s3.ap-south-1.amazonaws.com',
                    'S3OriginConfig': {
                        'OriginAccessIdentity': ''
                    },
                },
            ]
        },
        'DefaultCacheBehavior': {
            'TargetOriginId': 'xxxxxxxx-origin',
            'ViewerProtocolPolicy': 'allow-all',
            'ForwardedValues': {
                'QueryString': False,
                'Cookies': {
                    'Forward': 'all',
                },
                'Headers': {
                    'Quantity': 0,
                },
                'QueryStringCacheKeys': {
                    'Quantity': 0,
                }
            },
            'MinTTL': 1000,
        },
        "Enabled": True,
        "Comment": "distribution to host portfolio",
    }
)