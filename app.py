import aws_cdk as cdk
import os
from luffy.infra.ecr_infra import ECRStack
from luffy.infra.ecs_cluster_infra import ECSClusterStack

aws_account_id = os.environ["AWS_ACCOUNT_ID"]
aws_region = os.environ["AWS_REGION"]

app = cdk.App()
ecr_stack = ECRStack(app, "ECRStack")
ecs_stack = ECSClusterStack(
    app, "ECSClusterStack", aws_account_id=aws_account_id, aws_region=aws_region
)
ecs_stack.add_dependency(ecr_stack)

app.synth()
