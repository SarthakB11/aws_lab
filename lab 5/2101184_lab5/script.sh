#!/bin/bash
# Your startup script commands here
# Update the package repository
sudo yum update -y

# Configure AWS CLI with access keys
aws configure set aws_access_key_id accesskey
aws configure set aws_secret_access_key secretaccesskey
aws configure set default.region ap-south-1

# Copy website files from S3 to the Apache web root directory
aws s3 cp s3://akshatlab5/ /home --recursive

# Ensure correct ownership and permissions
chown -R apache:apache /var/www/html
chmod -R 755 /var/www/html

# Install Python 3 and pip
sudo yum install python3 -y
sudo yum install python3-pip -y

# Install Flask and other dependencies
pip3 install Flask
pip3 install pymysql

sudo rpm --import https://repo.mysql.com/RPM-GPG-KEY-mysql-2022
sudo yum install -y https://dev.mysql.com/get/mysql57-community-release-el7-11.noarch.rpm
sudo yum install -y mysql-community-client

echo "Website setup complete!"