# Sciunit

[Sciunit](https://github.com/radiant-systems-lab/sciunit) is a command-line tool which creates efficient, lightweight, self-contained packages of computational experiments that can be guaranteed to reproduce. Sciunit creates a reusable research object that containerizes and stores applications, facilitates sharing and collaboration, and eases the task of executing, understanding, and building on shared work.

## Sciunit Workflow
A Sciunit container consists of multiple executions. Each execution refers to running a command under Linux. The command may be a single binary, may start with the name of a specific virtual machine for managed languages such as “java,” or may be a shell script that contains multiple commands.

Sciunit uses application virtualization to capture and repeat an execution and works in two modes: **audit** and **repeat**. During *audit* mode, the dependencies of an execution are determined including its code, data, and environment, which are saved to a container. During *repeat* phase, the containerized execution is repeated on the same or different machine at a later stage.

## Core Sciunit Commands
**sciunit create &lt;name&gt;**<br>
Create a new Sciunit project under `~/sciunit/<name>` and open it.

**sciunit open &lt;name>|<url&gt;**<br>
Open the Sciunit project under `~/sciunit/<name>` or designated by a url.

**sciunit exec &lt;executable&gt; &lt;args...&gt;**<br>
Capture the execution of the given executable with the command line arguments args. The newly-created execution is added to the currently-opened Sciunit project and assigned execution id `eN`, where N is a monotonically-increasing decimal.

**sciunit repeat &lt;execution id&gt;**<br>
Repeat the execution of execution id from the currently-opened Sciunit project exactly as it happened earlier.

**sciunit list**<br>
List the existing executions in the currently-opened Sciunit project.

**sciunit show &lt;execution id&gt;**<br>
Show detailed information about a specific execution in the currently-opened Sciunit project.

# FLINC
[FLINC](https://github.com/radiant-systems-lab/Flinc) is built on top of Sciunit. It enables users to audit and repeat programs executing in interactive notebook environments like Jupyter. FLINC creates two new kernels:
1. **Audit Kernel:** executes, audits, and containerizes notebook code
2. **Repeat Kernel:** repeats the containerized code


## Hands-on progression

### 1. Sciunit Quickstart

Start with the [**Sciunit Quickstart**](quickstart.md). You will use Sciunit to run basic Linux commands like `ls` and `date`, and learn how to run a very simple hello world script in bash and Python.

### 2. Executing a Workflow with Sciunit
Move on to [**Workflow Execution with Sciunit**](rag-lite.md). In this example, you will run a multi-step workflow using Sciunit audit and then reproduce it using Sciunit repeat.

### 3. Executing an Interactive Workflow with FLINC
Finally, you will open [**Notebook Execution with FLINC**](rag-lite-flinc.md). In this example, you will execute the same workflow as #2 above in an interactive Jupyter notebook environment.

These exercices demonstrate how to create a reproducible execution in a shell environment using Sciunit and in an interactive environment using FLINC. 