from aws_cdk import Stack, aws_ecr as ecr, aws_iam as iam
from constructs import Construct


class ECRStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        repository = ecr.Repository(
            scope=self, id="FastApiEcrRepo", repository_name="student-api-ecr-repo"
        )

        # ecr_role = iam.Role(
        #     self, "FastApiEcrRole",
        #     assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
        #     description="Role to access ECR repository"
        # )

        # # Attach ECR full access policy to the role
        # ecr_role.add_managed_policy(
        #     iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2ContainerRegistryFullAccess")
        # )
