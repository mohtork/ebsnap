#!/usr/bin/env python3.7

'''
*Create an EC2 Volume Snapshots.
* 
* Delete Snapshots older than 30 days

AWSnap arguments:
	--service		# Probably ec2
	--snapshot		# Create Snapshot
	--delete		# Delete Snapshot
	--copy			# Copy snapshot between regions
	--region		# Region name
	--volume		# Volume ID
	--ami			# AMI ID
'''

import boto3
import argparse
from botocore.exceptions import ClientError
from datetime import datetime, timedelta

import config as cf

session=boto3.session.Session()
access_key=cf.yaml['aws_access_key']
secret_key=cf.yaml['aws_secret_key']
default_region=cf.yaml['aws_region']

d=datetime.today() - timedelta(days=30)
today=str(datetime.today())
		
def parse_args():
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('service',nargs='?',help=argparse.SUPPRESS)
	parser.add_argument('--snapshot',action='store_true',dest='snapshot',help=argparse.SUPPRESS)
	parser.add_argument('--delete',dest='delete',help=argparse.SUPPRESS,type=str)
	parser.add_argument('--copy',dest='copy',help=argparse.SUPPRESS,type=str)
	parser.add_argument('--region',dest='region',default=default_region,help=argparse.SUPPRESS,type=str)
	parser.add_argument('--volume',dest='volume', help=argparse.SUPPRESS,type=str)
	parser.add_argument('--ami',dest='ami',help=argparse.SUPPRESS,type=str)
	parser.add_argument('--s3',dest='s3',help=argparse.SUPPRESS,type=str)
	return parser.parse_args()

def EC2(region):
	ec2_client=boto3.client('ec2',aws_access_key_id=access_key,aws_secret_access_key=secret_key,region_name=region)
	return ec2_client

def Create_Snapshot(volID, region):
	ec2=EC2(region)
	response=ec2.create_snapshot(Description='Test by cli',VolumeId=volID,TagSpecifications=[{'ResourceType':'snapshot','Tags': [{'Key': 'name','Value': volID},{'Key': 'date','Value': today},]},],)
	return response

def Delete_Snapshot(snapID, region):
	ec2=EC2(region)
	response=ec2.delete_snapshot(SnapshotId=snapID)
	return response

def Waiter(snapshotid,region):
	ec2=EC2(region)
	snapshot_wait=ec2.get_waiter('snapshot_completed')
	result=snapshot_wait.wait(SnapshotIds=[snapshotid])
	return result

	
	
def Main():
	args=parse_args()
	if (args.service=='ec2' and args.snapshot and args.volume and args.region):
		try:
			volumeid=args.volume
			region=args.region
			Create_Snapshot(volumeid,region)
		except ClientError as e:
			if (e.response['Error']['Code'])=='InvalidVolume.NotFound':
				print("Error: Please check volume-id or try to specify region with --region argument")
	if (args.service=='ec2' and args.snapshot and args.delete and args.region):
		try:			
			delete=args.delete
			snapID=delete
			region=args.region
			Delete_Snapshot(snapID, region)
		except ClientError as e:
			if (e.response['Error']['Code'])=='InvalidSnapshot.NotFound':
				print("Error: Invalid Snapshot ID or maybe you did not provide the right region")
			if (e.response['Error']['Code'])=='InvalidSnapshotID.Malformed':
				print("Error: You Provided Malformed Snapshot ID")

if __name__ == '__main__':
        Main()

