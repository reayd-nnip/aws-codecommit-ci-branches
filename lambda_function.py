import boto3
import os


def handler(event, context) -> dict:
    environment = os.environ["ENVIRONMENT"]
    reference_name = event['detail']['referenceName']
    reference_type = event['detail']['referenceType']
    repository_name = event['detail']['repositoryName']
    detail_event = event['detail']['event']

    if reference_type == 'branch':
        cloudformation = boto3.client('cloudformation')
        stack_name = f"{repository_name}-{reference_name}"

        if detail_event == 'referenceCreated':
            template_body = open('codebuild.yaml', 'r').read()

            response = cloudformation.create_stack(
                StackName=stack_name,
                Parameters=[
                    {
                        'ParameterKey': 'Environment',
                        'ParameterValue': environment
                    },
                    {
                        'ParameterKey': 'BranchName',
                        'ParameterValue': reference_name
                    },
                    {
                        'ParameterKey': 'RepositoryName',
                        'ParameterValue': repository_name
                    },
                ],
                TemplateBody=template_body,
                DisableRollback=True,
                Capabilities=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM'],
                Tags=[
                    {
                        'Key': 'Name',
                        'Value': stack_name
                    }
                ]
            )

        if detail_event == 'referenceDeleted':
            response = cloudformation.delete_stack(StackName=stack_name)

        return response
