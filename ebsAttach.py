#!/usr/bin/python

# Attach an EBS volume to an EC2 instance
# Useful inside ASG's of single instances

import sys
import argparse
import urllib2
from subprocess import Popen, PIPE
from boto import ec2

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='This script attaches an EBS volume')
    parser.add_argument('-i','--instance', help='The EC2 instance ID.')
    parser.add_argument('-v','--volume', help='The EC2 Volume ID.', required=True)
    args = parser.parse_args()

    region = 'ap-southeast-2'
    dev = '/dev/xvdg'

    p = Popen('/bin/mount', stdout=PIPE, stderr=PIPE)
    output, errors = p.communicate()

    if dev not in output:
        # Get instance ID
        if args.instance:
            instance = args.instance
        else:
            try:
                instance = urllib2.urlopen("http://169.254.169.254/latest/meta-data/instance-id").read()
            except Exception as e:
                print "Error getting ID from AWS services. Exiting: ", e
                sys.exit(1)

        # Connect to EC2
        try:
            c = ec2.connect_to_region(region)
        except Exception as e:
            print "Error connecting to AWS API. Exiting: ", e
            sys.exit(1)

        # Attach volume
        try:
            c.attach_volume(args.volume, instance, dev)
            sys.exit(0)
        except Exception as e:
            print "Could not attach the volume. Exiting: ", e
            sys.exit(1)
    else:
        print 'Already mounted'
        sys.exit(0)

if __name__ == "__main__":
    main()
