import boto3
import time


def main():
    ec2 = boto3.resource('ec2')
    ssm_client = boto3.client('ssm')
    print(ssm_client.describe_sessions(State='Active'))

    for instance in ec2.instances.all():
        print(f'instance.id: {instance.id}, instance.state: {instance.state}')
        if instance.state['Name'] == 'running':
            response = ssm_client.send_command(
                        InstanceIds=[instance.id],
                        DocumentName="AWS-RunShellScript",
                        Parameters={'commands': ['echo "Hello World!"']}, )
            command_id = response['Command']['CommandId']
            output = ssm_client.get_command_invocation(
                  CommandId=command_id,
                  InstanceId=instance.id,
                )
            while output['Status'] == 'InProgress':
                time.sleep(1)
                print('Waiting for the command to end...')
                output = ssm_client.get_command_invocation(CommandId=command_id, InstanceId=instance.id)
            print(f'Output: {output}')
            print(f'Output[StandardOutputContent]: {output["StandardOutputContent"]}')


if __name__ == '__main__':
    main()

