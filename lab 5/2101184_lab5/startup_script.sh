#!/bin/bash
sudo yum update -y
sudo yum install -y httpd

sudo su -
dnf -y localinstall https://dev.mysql.com/get/mysql80-community-release-el9-4.noarch.rpm
dnf -y install mysql mysql-community-client mysql-community-server

# sudo yum install python3 -y
# sudo yum install python3-pip
# sudo pip3 install Flask
# sudo pip3 install pymysql
# sudo pip3 install mod_wsgi==4.7.1
sudo yum install nodejs npm -y

sudo systemctl start httpd
sudo systemctl enable httpd

sudo systemctl start mysqld
sudo systemctl enable mysqld



aws configure set aws_access_key_id accesskey
aws configure set aws_secret_access_key secretaccesskey
aws configure set default.region ap-south-1

aws s3 cp s3://lab5-sarthak /var/www/html --recursive


chown -R apache:apache /var/www/html
chmod -R 755 /var/www/html

curl localhost:80
sudo systemctl restart httpd

