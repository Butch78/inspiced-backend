from aws_cdk import Stack
from constructs import Construct

import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_ecs as ecs
import aws_cdk.aws_ecs_patterns as ecs_patterns


class FastAPIStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        # Create VPC
        self.vpc = ec2.Vpc(self, "FastAPIInspicedVPC", max_azs=3)

        # Create Fargate Cluster
        self.ecs_cluster = ecs.Cluster(
            self,
            "FastAPIInspicedECSCluster",
            vpc=self.vpc,
        )

        # Create Fargate Service and ALB
        image = ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
            image=ecs.ContainerImage.from_asset(
                directory="../src",
            )
        )
        self.ecs_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "FastAPIInspicedService",
            cluster=self.ecs_cluster,
            cpu=512,
            memory_limit_mib=1024,
            desired_count=2,
            task_image_options=image,
        )
