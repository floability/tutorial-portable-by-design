# Running Multi-Step Workflow with FLINC

Workflows are most commonly executed in interactive environments like Jupyter notebooks. In order to achieve reproducibility in these environments, we use FLINC, which is built on top of Sciunit and extends the concept of application virtualization to such environments. It creates two new kernels: audit and repeat.

<path to notebook comes here>


## Install FLINC
```
git clone https://github.com/radiant-systems-lab/Flinc
cd Flinc
```
Find the path of the kernel you wish to audit:
```
jupyter kernelspec list
```
Execute install.sh from the command line:
```
./install.sh <user kernel path>
```
`<user kernel path>` is the path of the kernel that will execute your notebook code.

## Auditing with FLINC
Select the audit kernel from within the notebook and execute your notebook code. After execution completes, select 'No Kernel' from the list or shutdown the kernel. Wait anywhere from few seconds to few minutes to complete auditing and container creation in the background. Each audit run will create a new Sciunit container in the background.

## Repeating with FLINC
Repeat your notebook code on the same or different machine by selecting the repeat kernel. It will repeat the last audited execution. After using the repeat kernel, select 'No Kernel' again to finish.

## Inspecting Notebook Executions
FILNC will store your notebook as an executable which you can view from the command line:
```
sciunit list
```

