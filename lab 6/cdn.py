import boto3

aws_access_key = 'AKIA6F7IQZA6XPWKGTWW'
aws_secret_key = '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'
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
                    'Id': 'lab6sarthak-origin',
                    'DomainName': 'lab6sarthak.s3.ap-south-1.amazonaws.com',
                    'S3OriginConfig': {
                        'OriginAccessIdentity': ''
                    },
                },
            ]
        },
        'DefaultCacheBehavior': {
            'TargetOriginId': 'lab6sarthak-origin',
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