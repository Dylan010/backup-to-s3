# Backup to S3 with Compression and Cron in Docker

This project creates a Docker container based on Ubuntu that compresses a specified directory and uploads it to an AWS S3 bucket using a Python script. The backup process is automated using cron.

## Prerequisites

- Docker installed on your system
- AWS CLI configured with appropriate credentials
- An AWS S3 bucket created for backups

## Setup Instructions

### 1. Clone the Repository

Clone this repository to your local machine:

```sh
git clone https://github.com/your-username/backup-to-s3.git
cd backup-to-s3
```

### 2. Configure AWS Credentials

Ensure your AWS credentials are accessible to the Docker container. You can either set them as environment variables or mount your AWS credentials file. Here's how you can set them as environment variables in your `Dockerfile` (you'll need to modify the Dockerfile):

```Dockerfile
# Add these lines to your Dockerfile
ENV AWS_ACCESS_KEY_ID your_access_key_id
ENV AWS_SECRET_ACCESS_KEY your_secret_access_key
```

Alternatively, you can mount the credentials file when running the container:

```sh
docker run -d -v ~/.aws:/root/.aws --name backup_to_s3 backup_to_s3
```

### 3. Build the Docker Image

Build the Docker image using the provided Dockerfile:

```sh
docker build -t backup_to_s3 .
```

### 4. Customize the Backup Script

Modify the `backup_to_s3.py` script to specify the directory you want to backup and the name of your S3 bucket:

```python
if __name__ == "__main__":
    # Path of the directory you want to backup
    directory_path = '/backup'
    # Name of your S3 bucket
    bucket_name = 'your-s3-bucket-name'

    backup_directory_to_s3(directory_path, bucket_name)
```

### 5. Add Files to Backup

Place the files you want to backup into the `backup` directory.

### 6. Run the Docker Container

Run the Docker container with the following command:

```sh
docker run -d --name backup_to_s3 backup_to_s3
```

### 7. Verify Backup Logs

You can check the logs to ensure the backup is running correctly:

```sh
docker logs backup_to_s3
```

### Customizing the Cron Job

The cron job is set to run every day at 2:00 AM by default. You can modify this in the `Dockerfile`:

```Dockerfile
# Modify this line in the Dockerfile to change the schedule
RUN (crontab -l ; echo "0 2 * * * /usr/bin/python3 /usr/local/bin/backup_to_s3.py >> /var/log/backup.log 2>&1") | crontab
```

Refer to [crontab.guru](https://crontab.guru/) for more information on how to schedule cron jobs.

## Cleaning Up

To stop and remove the container, run:

```sh
docker stop backup_to_s3
docker rm backup_to_s3
```

To remove the Docker image, run:

```sh
docker rmi backup_to_s3
```

## License

This project is licensed under the MIT License.

---

Feel free to customize the instructions and information as needed for your specific project and environment.