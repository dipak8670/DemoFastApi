import boto3


def delete_non_default_security_groups():
    ec2_client = boto3.client("ec2")

    # Get all regions
    regions = [
        region["RegionName"] for region in ec2_client.describe_regions()["Regions"]
    ]

    for region in regions:

        # Create EC2 client for the specific region
        ec2 = boto3.client("ec2", region_name=region)

        # Get all security groups
        response = ec2.describe_security_groups(
            Filters=[{"Name": "group-name", "Values": ["default"]}]
        )
        default_security_group_ids = [
            sg["GroupId"] for sg in response["SecurityGroups"]
        ]

        all_security_groups = ec2.describe_security_groups()["SecurityGroups"]

        for sg in all_security_groups:
            if sg["GroupId"] not in default_security_group_ids:
                print(f"Deleting non-default security groups in region {region}")
                try:
                    print(f"Deleting security group {sg['GroupId']}")
                    ec2.delete_security_group(GroupId=sg["GroupId"])
                    print(f"Deleted security group {sg['GroupId']} successfully")
                except Exception as e:
                    print(f"Failed to delete security group {sg['GroupId']}: {str(e)}")


if __name__ == "__main__":
    delete_non_default_security_groups()
