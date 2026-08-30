# Connect to the Tutorial Server

Your credential card contains your **username**, **password**, and **server**.

## macOS and Linux

Open Terminal and connect with:

```bash
ssh USERNAME@SERVER
```

Replace `USERNAME` and `SERVER` with the values printed on your card.

## Windows — unverified

> **These Windows instructions have not been verified yet.** We will remove this notice after testing password login and SSH tunneling on a Windows computer.

Open PowerShell or Windows Terminal and check whether the OpenSSH client is available:

```powershell
ssh -V
```

If that prints an OpenSSH version, connect with:

```powershell
ssh USERNAME@SERVER
```

Replace `USERNAME` and `SERVER` with the values printed on your card.

The first connection may ask whether you want to trust the server. Enter:

```text
yes
```

Then enter your password.

> Your password will not appear on screen while you type. This is normal.

## 1. Check your account

After logging in, run:

```bash
whoami
hostname
pwd
```

`whoami` should show the username printed on your card, and your home directory should be:

```text
/home/USERNAME
```

Now confirm that your tutorial workspace is writable:

```bash
printf 'access works\n' > ~/tutorial/access-test.txt
cat ~/tutorial/access-test.txt
```

You should see:

```text
access works
```

Your home directory and tutorial workspace belong to your account. Always use the username and server assigned to you.

## 2. Activate the tutorial tools

The tutorial software is installed in a shared, read-only environment.

Activate it with:

```bash
source /opt/tutorial/activate.sh
```

Confirm that the environment is active:

```bash
python --version
echo "$CONDA_PREFIX"
```

`CONDA_PREFIX` should point somewhere under:

```text
/opt/tutorial/
```

## 3. Check TaskVine and Floability

Run:

```bash
vine_worker --version
python -c "import ndcctools.taskvine; print('TaskVine: OK')"
floability --help >/dev/null && echo "Floability: OK"
```

You should finish with:

```text
TaskVine: OK
Floability: OK
```

## You are ready

Your setup now has two separate areas:

```text
/opt/tutorial/       shared tutorial software
~/tutorial/          your exercises and files
```

Later, Floability will create and cache backpack-specific software environments inside your own user space.

These environments are separate from the shared tutorial tools. Repeated runs of the same backpack may reuse your cached environment, but environments are not shared between participants.

## SSH tunneling for notebook exercises

Later notebook exercises will use SSH tunneling so Jupyter does not need a public network port. The instructions will provide the local and remote port numbers and use this pattern:

```bash
ssh -L LOCAL_PORT:localhost:REMOTE_PORT USERNAME@SERVER
```

The Windows version is expected to use the same options in PowerShell, but it remains unverified until tested on a Windows computer.

Continue to [**Your First TaskVine Program**](../02-taskvine/README.md).
