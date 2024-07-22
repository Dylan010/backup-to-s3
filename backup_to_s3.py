import boto3
from botocore.exceptions import NoCredentialsError
import os
import shutil

def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print(f"Upload Successful: {local_file} to {bucket}/{s3_file}")
        return True
    except FileNotFoundError:
        print(f"The file was not found: {local_file}")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

def compress_directory(directory_path, output_filename):
    shutil.make_archive(output_filename, 'zip', directory_path)
    return output_filename + '.zip'

def backup_directory_to_s3(directory_path, bucket_name):
    zip_file = compress_directory(directory_path, 'backup')
    upload_to_aws(zip_file, bucket_name, os.path.basename(zip_file))
    os.remove(zip_file)  # Eliminar el archivo ZIP después de subirlo

if __name__ == "__main__":
    # Ruta del directorio que quieres respaldar
    directory_path = '/backup'
    # Nombre de tu bucket en S3
    bucket_name = 'your-s3-bucket-name'

    backup_directory_to_s3(directory_path, bucket_name)
