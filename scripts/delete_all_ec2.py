import boto3
import time
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError


def disable_termination_protection(ec2_client, instance_id):
    try:
        ec2_client.modify_instance_attribute(
            InstanceId=instance_id, DisableApiTermination={"Value": False}
        )
        print(f"Termination protection disabled for instance {instance_id}")
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "InvalidInstanceID.NotFound":
            print(
                f"Instance ID {instance_id} not found. It might have been terminated already."
            )
        else:
            print(
                f"Unexpected error disabling termination protection for instance {instance_id}: {e}"
            )
        return False


def terminate_instance(ec2_client, instance_id):
    try:
        ec2_client.terminate_instances(InstanceIds=[instance_id])
        print(f"Instance {instance_id} terminated")
    except ClientError as e:
        if e.response["Error"]["Code"] == "InvalidInstanceID.NotFound":
            print(
                f"Instance ID {instance_id} not found. It might have been terminated already."
            )
        else:
            print(f"Error terminating instance {instance_id}: {e}")


def get_all_regions():
    ec2_client = boto3.client("ec2")
    response = ec2_client.describe_regions()
    return [region["RegionName"] for region in response["Regions"]]


def get_instances_in_region(ec2_client):
    instances = []
    paginator = ec2_client.get_paginator("describe_instances")
    for page in paginator.paginate(
        Filters=[{"Name": "instance-state-name", "Values": ["running", "stopped"]}]
    ):
        for reservation in page["Reservations"]:
            for instance in reservation["Instances"]:
                instances.append(instance["InstanceId"])
    return instances


def main():
    try:
        regions = get_all_regions()

        for region in regions:
            ec2_client = boto3.client("ec2", region_name=region)
            instance_ids = get_instances_in_region(ec2_client)

            if not instance_ids:
                print(f"No running or stopped instances found in region {region}")
                continue

            print(f"Found instances in region {region}: {instance_ids}")

            for instance_id in instance_ids:
                success = disable_termination_protection(ec2_client, instance_id)
                if success:
                    # Adding a small delay to ensure state synchronization
                    time.sleep(2)
                    terminate_instance(ec2_client, instance_id)
                else:
                    print(
                        f"Failed to disable termination protection for instance {instance_id}"
                    )
    except NoCredentialsError:
        print("Error: AWS credentials not found.")
    except PartialCredentialsError:
        print("Error: Incomplete AWS credentials.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
