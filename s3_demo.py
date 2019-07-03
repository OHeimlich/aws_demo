import boto3
import uuid
import time


file_size = 0
finish_upload = False


def upload_callback(num_of_bytes):
    global finish_upload
    print(f'upload_callback: {num_of_bytes}/{file_size}')
    if num_of_bytes >= file_size:
        finish_upload = True


def generate_file(size, file_name):
    random_file_name = ''.join([str(uuid.uuid4().hex[:6]), file_name])
    with open(random_file_name, 'w') as f:
        content = str('just_a_test') * size
        f.write(content)
        file_size = len(content)
    return random_file_name, file_size


def main():
    global file_size
    s3_client = boto3.client('s3')
    session = boto3.session.Session()
    current_region = session.region_name
    s3_name = ''.join(['aws-demo', str(uuid.uuid4())])
    print(f's3_name: {s3_name}')

    bucket_response = s3_client.create_bucket(Bucket=s3_name, CreateBucketConfiguration={'LocationConstraint': current_region})
    print(f'bucket_response: {bucket_response}')

    # Upload file
    file_key = 'test_file'
    first_file_name, file_size = generate_file(size=300, file_name='first_file.txt')
    upload_file_response = s3_client.upload_file(Filename=first_file_name, Bucket=s3_name, Key=file_key, Callback=upload_callback)
    print(f'upload_file_response: {upload_file_response}')

    # Download file
    while not finish_upload:    # Ugly pooling
        print('waiting for upload to finish...')
        time.sleep(1)
    response = s3_client.download_file(s3_name, file_key, 'downloaded_file.txt')
    print(f'download file response: {response}')

    # Delete file
    response = s3_client.delete_object(Bucket=s3_name, Key=file_key)
    print(f'delete file response: {response}')

    # Delete bucket
    s3_client.delete_bucket(Bucket=s3_name)


if __name__ == '__main__':
    main()
