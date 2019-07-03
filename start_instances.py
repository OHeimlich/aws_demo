import boto3


def start_instance(instance_id):
    ec2 = boto3.client('ec2')
    response = ec2.start_instances(InstanceIds=[instance_id])
    print(response)


def main():
    ec2 = boto3.resource('ec2')
    for instance in ec2.instances.all():
        print(f'instance.id: {instance.id}, instance.state: {instance.state}')
        if instance.state['Name'] != 'running':
            start_instance(instance.id)


if __name__ == '__main__':
    main()
