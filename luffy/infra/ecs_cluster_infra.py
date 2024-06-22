from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_iam as iam,
)
from constructs import Construct


class ECSClusterStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a VPC
        vpc = ec2.Vpc(self, "MyVpc", max_azs=2)

        # Create an ECS cluster
        cluster = ecs.Cluster(self, "MyCluster", vpc=vpc)

        # Define an IAM role for the task with the necessary permissions
        task_role = iam.Role(
            self,
            "MyTaskRole",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
        )

        # Add necessary policies to the role
        task_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonS3ReadOnlyAccess"
            )  # Example policy
        )
        # Add more policies as needed

        # Create a Fargate task definition
        task_definition = ecs.FargateTaskDefinition(
            self, "MyTaskDef", task_role=task_role
        )

        # Add a container to the task definition
        container = task_definition.add_container(
            "MyContainer",
            image=ecs.ContainerImage.from_registry(
                "my-docker-repo/my-fastapi-image:latest"
            ),
            memory_limit_mib=512,
            cpu=256,
        )

        # Open the port your FastAPI app is listening on
        container.add_port_mappings(ecs.PortMapping(container_port=80))

        # Create a Fargate service
        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "MyFargateService",
            cluster=cluster,
            task_definition=task_definition,
            public_load_balancer=True,
        )

        # Optionally set up health checks
        fargate_service.target_group.configure_health_check(path="/health")
