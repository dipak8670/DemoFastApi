from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_iam as iam,
    aws_logs as logs,
    aws_dynamodb as dynamodb,
)
import aws_cdk as cdk
from constructs import Construct


class ECSClusterStack(Stack):
    def __init__(
        self, scope: Construct, id: str, aws_account_id: str, aws_region: str, **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a VPC
        vpc = ec2.Vpc(self, "StudentApiVpc", max_azs=2)

        # Create an ECS cluster
        cluster = ecs.Cluster(
            self,
            id="StudentApiCluster",
            cluster_name="StudentApiCluster",
            container_insights=True,
            vpc=vpc,
        )

        dynamo_table = dynamodb.Table(
            self,
            "StudentApiDynamoDBTable",
            partition_key=dynamodb.Attribute(
                name="role_number", type=dynamodb.AttributeType.STRING
            ),
            table_name="StudentApiDynamoDBTable",
            sort_key=dynamodb.Attribute(
                name="name", type=dynamodb.AttributeType.STRING
            ),
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )

        # Define an IAM role for the task with the necessary permissions
        task_role = iam.Role(
            self,
            "StudentApiTaskRole",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
        )

        # Add DynamoDB policies to the role
        task_role.add_to_policy(
            iam.PolicyStatement(
                actions=[
                    "dynamodb:BatchGetItem",
                    "dynamodb:BatchWriteItem",
                    "dynamodb:DeleteItem",
                    "dynamodb:GetItem",
                    "dynamodb:PutItem",
                    "dynamodb:Query",
                    "dynamodb:Scan",
                    "dynamodb:UpdateItem",
                ],
                resources=[
                    f"arn:aws:dynamodb:{aws_region}:{aws_account_id}:table/StudentApiDynamoDBTable*"
                ],
            )
        )

        # Define an IAM execution role for the task to pull images from ECR
        execution_role = iam.Role(
            self,
            "StudentApiExecutionRole",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
        )

        # Attach the AmazonECSTaskExecutionRolePolicy to the execution role
        execution_role.add_managed_policy(
            iam.ManagedPolicy.from_managed_policy_arn(
                self,
                id="ManagedECSTaskExecutionPolicy",
                managed_policy_arn="arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy",
            )
        )

        # Create a Fargate task definition
        task_definition = ecs.FargateTaskDefinition(
            self,
            "StudentApiTaskDefinition",
            task_role=task_role,
            execution_role=execution_role,
        )

        # Add a container to the task definition
        container = task_definition.add_container(
            "StudentApiContainer",
            container_name="StudentApiContainer",
            image=ecs.ContainerImage.from_registry(
                f"{aws_account_id}.dkr.ecr.{aws_region}.amazonaws.com/student-api-ecr-repo:latest"
            ),
            memory_limit_mib=512,
            cpu=256,
            logging=ecs.LogDriver.aws_logs(
                stream_prefix="StudentApiContainer",
                log_group=logs.LogGroup(
                    self,
                    id="StudentApiLogGroup",
                    log_group_name=f"StudentApiLogGroup",
                    retention=logs.RetentionDays.ONE_DAY,
                    removal_policy=cdk.RemovalPolicy.DESTROY,
                ),
            ),
        )

        # Open the port your FastAPI app is listening on
        container.add_port_mappings(ecs.PortMapping(container_port=80))

        # Create a Fargate service with an Application Load Balancer
        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "StudentApiFargateService",
            service_name="StudentApiService",
            cluster=cluster,
            task_definition=task_definition,
            public_load_balancer=True,
            desired_count=1,  # Adjust desired count as needed
        )

        # Optionally set up health checks
        fargate_service.target_group.configure_health_check(path="/health")
