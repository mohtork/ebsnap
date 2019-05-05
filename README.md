# EBSnap
Automate EBS Snapshots<br/>
- Create ebs snapshot<br/>
- Delete ebs snapshot<br/> 
- Copy ebs snapshot across regions<br/>
- Delete snapshots older than x days <br/>


# Installation
1. git clone https://github.com/mohtork/ebsnap.git
2. pip install -r requirements.txt

# EBSnap in action
- ./ebs.py ec2 --snapshot --voulme VolumeID --region RegionName<br/>
- ./ebs.py ec2 --snapshot --delete Snap-Id --region RegionName<br/>
- ./ebs ec2 --snapshot --copy Snap-Id --dest RegionName<br/>


