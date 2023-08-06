import json
import setuptools

kwargs = json.loads("""
{
    "name": "taimos-cdk",
    "version": "1.4.0",
    "description": "Higher level constructs for AWS CDK",
    "url": "https://github.com/taimos/cdk-constructs",
    "long_description_content_type": "text/markdown",
    "author": "Thorsten Hoeger<thorsten.hoeger@taimos.de>",
    "project_urls": {
        "Source": "https://github.com/taimos/cdk-constructs"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "taimos_cdk",
        "taimos_cdk._jsii"
    ],
    "package_data": {
        "taimos_cdk._jsii": [
            "taimos-cdk-constructs@1.4.0.jsii.tgz"
        ],
        "taimos_cdk": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii~=0.19.0",
        "publication>=0.0.3",
        "aws-cdk.alexa-ask~=1.15,>=1.15.0",
        "aws-cdk.aws-apigateway~=1.15,>=1.15.0",
        "aws-cdk.aws-certificatemanager~=1.15,>=1.15.0",
        "aws-cdk.aws-cloudformation~=1.15,>=1.15.0",
        "aws-cdk.aws-cloudfront~=1.15,>=1.15.0",
        "aws-cdk.aws-codebuild~=1.15,>=1.15.0",
        "aws-cdk.aws-codecommit~=1.15,>=1.15.0",
        "aws-cdk.aws-codepipeline~=1.15,>=1.15.0",
        "aws-cdk.aws-codepipeline-actions~=1.15,>=1.15.0",
        "aws-cdk.aws-ec2~=1.15,>=1.15.0",
        "aws-cdk.aws-ecr~=1.15,>=1.15.0",
        "aws-cdk.aws-elasticloadbalancingv2~=1.15,>=1.15.0",
        "aws-cdk.aws-events-targets~=1.15,>=1.15.0",
        "aws-cdk.aws-iam~=1.15,>=1.15.0",
        "aws-cdk.aws-logs~=1.15,>=1.15.0",
        "aws-cdk.aws-route53-patterns~=1.15,>=1.15.0",
        "aws-cdk.aws-s3-deployment~=1.15,>=1.15.0",
        "aws-cdk.aws-sam~=1.15,>=1.15.0",
        "aws-cdk.aws-secretsmanager~=1.15,>=1.15.0",
        "aws-cdk.aws-sns-subscriptions~=1.15,>=1.15.0",
        "aws-cdk.core~=1.15,>=1.15.0",
        "aws-cdk.custom-resources~=1.15,>=1.15.0"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
