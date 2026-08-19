import boto3
import moto


def test_describe_instances_key_name_filter():
    # Use Moto's EC2 mock to simulate AWS
    with moto.mock_ec2():
        client = boto3.client("ec2", region_name="us-east-1")
        # Launch a single instance with a known KeyName
        client.run_instances(ImageId="ami-1234abcd", MinCount=1, MaxCount=1, KeyName="test_key")

        # Attempt to filter instances by the key-name attribute
        result = client.describe_instances(
            Filters=[
                {"Name": "key-name", "Values": ["test_key"]},
            ]
        )

        # The filter should return exactly the instance we created
        assert len(result["Reservations"]) == 1
        instances = result["Reservations"][0]["Instances"]
        assert len(instances) == 1
        assert instances[0].get("KeyName") == "test_key"
