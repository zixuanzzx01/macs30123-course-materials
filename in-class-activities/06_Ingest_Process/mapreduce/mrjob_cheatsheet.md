# mrjob Cheat Sheet

To run/debug `mrjob` code locally from your command line:

```
python mapreduce.py sample_us.tsv
```

To run your `mrjob` code on an AWS EMR cluster, you should first ensure that your configuration file is set with your EC2 pem file name and file location, as well as your current credentials from AWS Academy. Note that the credentials are listed with ":" here and not "=" as they are in your `credentials` file. `mrjob` assumes that this (`.mrjob.conf`) file will be located in your home directory (at `~/.mrjob.conf`), so you will need to put the file there. Otherwise, you will need to designate your configuration [as a command line option](https://mrjob.readthedocs.io/en/latest/cmd.html#create-cluster) when you start your `mrjob` job using the `-c` flag.

~/.mrjob.conf
```
runners:
  emr:
    # Specify a pem key to start up an EMR cluster on your behalf
    ec2_key_pair: vockey
    ec2_key_pair_file: ~/.ssh/labsuser.pem

    # Specify type/# of EC2 instances you want your code to run on
    core_instance_type: m5.xlarge
    num_core_instances: 3
    region: us-east-1

    # if cluster idles longer than 60 minutes, terminate the cluster
    max_mins_idle: 60.0

    # to read from/write to S3; note ":" instead of "=" from `credentials`:
    aws_access_key_id: <your key ID>
    aws_secret_access_key: <your secret>
    aws_session_token: <your session token>
```

To run your `mrjob` code on an EMR cluster (of the size and type specified in your configuration file), you can run the following command on the command line to create a stand-alone EMR cluster:
```
mrjob create-cluster
```

When you create a cluster, `mrjob` will print out the ID number for the cluster ("j" followed by a bunch of numbers and characters). If you copy this job-id number and specify it after the `--cluster-id` flag on the command line, your code will be run on this already-running cluster. Here, we additionally write the results of our job out to a text file (`mr.out`) via the `> mr.out` addendum at the end of the line.

```
python mapreduce.py -r emr sample_us.tsv --cluster-id=<cluster-id #> > mr.out
```

When you're done running jobs on your cluster, you can terminate the cluster with the following command so that you don't have to pay for it any longer than you need to:

```
mrjob terminate-cluster <cluster-id #>
```

For additional configuration options, consult the [`mrjob` documentation](https://mrjob.readthedocs.io/en/latest/index.html).
