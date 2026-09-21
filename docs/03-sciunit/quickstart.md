# Sciunit Quickstart

Activate the conda environment as the first step:
```bash
source /opt/tutorial/activate-raglite-sciunit.sh 
```

## Creating your Sciunit Project
Create your first Sciunit project. This will help to keep all related executions in one place:
```bash
sciunit create project-quickstart
```
This will show an output similar to this:
```
Opened empty sciunit at /home/user02/sciunit/project-quickstart
```

## Auditing Basic Linux Commands with Sciunit

### pwd

Run the Linux command `pwd`:
```bash
sciunit exec pwd
```
This will display the contents of your current directory show you an output similar to this:
```
/home/user02
[project-quickstart e1] pwd
 Date: Fri, 11 Sep 2026 17:07:13 +0000
```

### date

Run the Linux command `date`:
```bash
sciunit exec date
```
This will show an output similar to this:
```
Fri Sep 11 17:09:31 UTC 2026

[project-quickstart e2] date
 Date: Fri, 11 Sep 2026 17:09:31 +0000
```

You can view the list of containerized executions through:
```bash
sciunit list
```
This will show the list of containers similar to this:
```
   e1 Sep 11 17:07 pwd
   e2 Sep 11 17:09 date
```
You can see more details for each container as well:
```bash
sciunit show e1
```
This will show details of `e1` similar to this:
```
     id: e1
sciunit: project-quickstart
command: pwd
   size: 178.01 MB
started: 2026-09-11 17:07
```

### Hello World Script
Now, you can execute and audit a simple bash script. Open a new file in your favorite text editor and copy paste the following text into it. Save the file with the name `hello.sh`.
```bash
#!/bin/sh
echo 'hello, world'
```
Update file permissions to execute it:
```bash
chmod u+x hello.sh
```
You can run this program to get its output:
```bash
./hello.sh
```
This will show the following output:
```
hello, world
```
Now, you can capture its execution with Sciunit:
```bash
sciunit exec ./hello.sh
```
This will show you the following output:
```
hello, world

[project-quickstart e3] ./hello.sh
 Date: Fri, 11 Sep 2026 17:17:05 +0000
```
You can see that there are three containerized executions in this project now:
```bash
sciunit list
```
This will show you an output similar to this:
```
   e1 Sep 11 17:07 pwd
   e2 Sep 11 17:09 date
   e3 Sep 11 17:17 ./hello.sh
```

## Repeat Containerized Executions with Sciunit
You can pick and repeat any of the stored executions from this list. For example, repeat the last execution to get the same output:
```bash
sciunit repeat e3
```
This will show the following output:
```
hello, world
```
Repeat the first execution:
```bash
sciunit repeat e1
```
This will show an output similar to this:
```
/home/user02
```
