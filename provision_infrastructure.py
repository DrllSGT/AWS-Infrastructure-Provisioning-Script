#!/usr/bin/env python3

import boto3


def create_instance():
    ec2_client = boto3.client('ec2')

    response = ec2_client.run_instances(
        ImageId='ami-xxxxxxxx',  # Specify the appropriate AMI ID
        InstanceType='t2.micro',
        MinCount=1,
        MaxCount=1,
        KeyName='my-keypair',  # Specify your key pair name
        SecurityGroupIds=['sg-xxxxxxxx'],  # Specify security group IDs
        SubnetId='subnet-xxxxxxxx'  # Specify the subnet ID
    )

    instance_id = response['Instances'][0]['InstanceId']
    print(f"Created instance with ID: {instance_id}")

    # Wait for the instance to be running
    waiter = ec2_client.get_waiter('instance_running')
    waiter.wait(InstanceIds=[instance_id])
    print("Instance is now running.")

    # Describe the instance to get its public IP address
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    public_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']

    # Connect to the instance using SSH
    ssh_command = f"ssh -i my-keypair.pem ec2-user@{public_ip}"
    print(f"Connect to the instance using the following command:\n{ssh_command}")


def create_security_group():
    ec2_client = boto3.client('ec2')

    response = ec2_client.create_security_group(
        GroupName='my-security-group',  # Specify the security group name
        Description='My security group',
        VpcId='vpc-xxxxxxxx'  # Specify the VPC ID
    )

    security_group_id = response['GroupId']
    print(f"Created security group with ID: {security_group_id}")


def create_vpc():
    ec2_client = boto3.client('ec2')

    response = ec2_client.create_vpc(
        CidrBlock='10.0.0.0/16',  # Specify the CIDR block for the VPC
    )

    vpc_id = response['Vpc']['VpcId']
    print(f"Created VPC with ID: {vpc_id}")


def main():
    create_security_group()
    create_vpc()
    create_instance()


if __name__ == '__main__':
    main()

