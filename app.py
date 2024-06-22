import aws_cdk as cdk

from luffy.infra.ecr_infra import ECRStack
from luffy.infra.ecs_cluster_infra import ECSClusterStack


app = cdk.App()
ecr_stack = ECRStack(app, "ECRStack")
ecs_stack = ECSClusterStack(app, "ECSClusterStack")
ecs_stack.add_dependency(ecr_stack)

app.synth()
