# Sciunit Quickstart

Create your Sciunit project:
```
sciunit create project-pbd
```

Check how many executions are containerized within this project:
```
sciunit list
```
The result should be empty, since no program has been executed yet.

## Auditing Basic Linux Commands with Sciunit

### ls

Run the Linux command `ls`:
```
sciunit exec ls
```
This will display the contents of your current directory show you an output like this:
```
file.txt   image.png
[project-pbd e1] ls
 Date: Fri, 11 Sep 2026 17:07:13 +0000
```

### date

Run the Linux command `date`:
```
sciunit exec date
```
This will show an output like this:
```
Fri Sep 11 17:09:31 UTC 2026

[project-pbd e2] date
 Date: Fri, 11 Sep 2026 17:09:31 +0000
```

You can view the list of containerized executions through:
```
> sciunit list
   e1 Sep 11 17:07 ls
   e2 Sep 11 17:09 date
```
You can see more details for each container as well:
```
> sciunit show e1
     id: e1
sciunit: project-pbd
command: ls
   size: 178.01 MB
started: 2026-09-11 17:07
```
Now, let us create and run a simple hello world program in a script called `hello.sh`:
```
#!/bin/sh
echo 'hello, world'
```
Update its permissions to execution:
```
chmod u+x hello.sh
```
We can run this program to get its output:
```
> ./hello.sh
hello, world
```
Now, let’s try to capture this program with Sciunit:
```
> sciunit exec ./hello.sh
hello, world

[project-pbd e3] ./hello.sh
 Date: Fri, 11 Sep 2026 17:17:05 +0000
```
We can see that there are three containerized executions in this project now:
```
> sciunit list
   e1 Sep 11 17:07 ls
   e2 Sep 11 17:09 date
   e3 Sep 11 17:17 ./hello.sh
```

## Repeat Containerized Executions with Sciunit
We can pick and repeat any of the stored executions from this list. For example, repeat the last execution to get the same output:
```
> sciunit repeat e3
hello, world
```
Repeat the first execution:
```
> sciunit repeat e1
hello, world
```
