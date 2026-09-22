# Running Multi-Step Workflow with FLINC

Workflows are most commonly executed in interactive environments like Jupyter notebooks. In order to achieve reproducibility in these environments, we use FLINC, which is built on top of Sciunit and extends the concept of application virtualization to such environments. It creates two new kernels: audit and repeat.

First, move into this directory:
```bash
cd ~/tutorial/examples/sciunit/flinc
```
This directory will have the `.ipynb` file to run.

Install the `raglite-flinc-env` environment:
```bash
conda env create --file environment.yml
conda activate raglite-flinc-env
```

## Install FLINC
Change directory:
```bash
cd Flinc
```
Install jupyter kernel to execute your notebook. This kernel will connect with the existing conda environment to access all necessary dependencies to run the notebook code:
```bash
python -m ipykernel install --sys-prefix --name=raglite-flinc-env --display-name=rag-lite
```
This will show an output similar to this:
```
Installed kernelspec raglite-flinc-env in /home/user02/.conda/envs/raglite-flinc-env/share/jupyter/kernels/raglite-flinc-env
```

See the newly installed rag-lite kernel in the list of Jupyter kernels:
```bash
jupyter kernelspec list
```
The output will be shown similar to this:
```
Available kernels:
  python3    /home/user02/.conda/envs/raglite-flinc-env/share/jupyter/kernels/python3
  rag-lite   Installed kernelspec raglite-flinc-env in /home/user02/.conda/envs/raglite-flinc-env/share/jupyter/kernels/raglite-flinc-env
```

Install FLINC and pass it the full path of the rag-lite kernel:
```bash
./install.sh /home/user02/.conda/envs/raglite-flinc-env/share/jupyter/kernels/rag-lite
```

## Starting the Notebook Server 
Move into the correct directory:
```bash
cd ~/tutorial/examples/sciunit/flinc
```
You can start the Jupyter server to open the notebook:
```
jupyter notebook
```
This will start the server and an output similar to this will be displayed:
```
[I 2026-09-22 17:05:06.967 ServerApp] jupyter_lsp | extension was successfully linked.
[I 2026-09-22 17:05:06.969 ServerApp] jupyter_server_terminals | extension was successfully linked.
[I 2026-09-22 17:05:06.971 ServerApp] jupyterlab | extension was successfully linked.
[I 2026-09-22 17:05:06.973 ServerApp] notebook | extension was successfully linked.
[I 2026-09-22 17:05:06.974 ServerApp] Writing Jupyter server cookie secret to /home/user02/.local/share/jupyter/runtime/jupyter_cookie_secret
[I 2026-09-22 17:05:06.996 ServerApp] notebook_shim | extension was successfully linked.
[I 2026-09-22 17:05:07.035 ServerApp] notebook_shim | extension was successfully loaded.
[I 2026-09-22 17:05:07.036 ServerApp] jupyter_lsp | extension was successfully loaded.
[I 2026-09-22 17:05:07.036 ServerApp] jupyter_server_terminals | extension was successfully loaded.
[I 2026-09-22 17:05:07.050 LabApp] JupyterLab extension loaded from /home/user02/.conda/envs/raglite-flinc-env/lib/python3.11/site-packages/jupyterlab
[I 2026-09-22 17:05:07.050 LabApp] JupyterLab application directory is /home/user02/.conda/envs/raglite-flinc-env/share/jupyter/lab
[I 2026-09-22 17:05:07.051 LabApp] Extension Manager is 'pypi'.
[I 2026-09-22 17:05:07.155 ServerApp] jupyterlab | extension was successfully loaded.
[I 2026-09-22 17:05:07.157 ServerApp] notebook | extension was successfully loaded.
[I 2026-09-22 17:05:07.157 ServerApp] Serving notebooks from local directory: /home/user02/tutorial/examples/sciunit/flinc/Flinc
[I 2026-09-22 17:05:07.157 ServerApp] Jupyter Server 2.21.1 is running at:
[I 2026-09-22 17:05:07.157 ServerApp] http://localhost:8888/tree?token=e5540ab7284f7c02bbbc6374aac9ebe37ad21e2f228bfaf7
[I 2026-09-22 17:05:07.157 ServerApp]     http://127.0.0.1:8888/tree?token=e5540ab7284f7c02bbbc6374aac9ebe37ad21e2f228bfaf7
[I 2026-09-22 17:05:07.157 ServerApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[W 2026-09-22 17:05:07.162 ServerApp] No web browser found: Error('could not locate runnable browser').
[C 2026-09-22 17:05:07.162 ServerApp] 
    
    To access the server, open this file in a browser:
        file:///home/user02/.local/share/jupyter/runtime/jpserver-22381-open.html
    Or copy and paste one of these URLs:
        http://localhost:8888/tree?token=e5540ab7284f7c02bbbc6374aac9ebe37ad21e2f228bfaf7
        http://127.0.0.1:8888/tree?token=e5540ab7284f7c02bbbc6374aac9ebe37ad21e2f228bfaf7
[I 2026-09-22 17:05:07.171 ServerApp] Skipped non-installed server(s): basedpyright, bash-language-server, dockerfile-language-server-nodejs, javascript-typescript-langserver, jedi-language-server, julia-language-server, pyrefly, pyright, python-language-server, python-lsp-server, r-languageserver, sql-language-server, texlab, typescript-language-server, unified-language-server, vscode-css-languageserver-bin, vscode-html-languageserver-bin, vscode-json-languageserver-bin, yaml-language-server
```

You will copy paste the above link starting with `http://localhost:` and paste it in your local machine's browser. 

**If the URL does NOT open**<br>
You may need to set up SSH tunneling first. You will need to run a command with the following pattern on your local machine:
```bash
ssh -L <LOCAL_PORT>:localhost:<REMOTE_PORT> <USERNAME>@<SERVER>
```
Your `USERNAME` and `SERVER` are already provided to you. `REMOTE_PORT` will be given in the output shown above for the previous command. For example, the actual command to run on your local machine will look similar to this:
```bash
ssh -L localhost:8891:localhost:8891 user02@34.250.253.140
```
You will be asked to enter your password. 

**If the URL opens**<br>
Navigate to the browser link where you can visualize and open the notebook `rag-lite_workflow.ipynb`.


## Auditing with FLINC
Select the `Sciunit Audit(rag-lite)` kernel in the notebook and execute your notebook code. FLINC will audit this entire notebook execution. After execution completes, select 'No Kernel' from the list to explicitly mark the end of audit process. Wait a few seconds to let the audit process complete and create the container in the background. Each audit run will create a new Sciunit execution.

## Repeating with FLINC
You can repeat your notebook code on the same or different machine. Select the `Sciunit Repeat` kernel and execute the notebook code. This will repeat the last audited execution successfully. After using the repeat kernel, select 'No Kernel' from the list of kernels to finish. 

Go back to the terminal and press Ctrl+C to terminate the Jupyter server process.

## Inspecting Notebook Executions
FILNC will store your notebook as an executable which you can view from the command line:
```bash
sciunit list
```
This will show a single execution with an output similar to this:
```
   e1 Sep 22 17:13 /home/user02/.conda/envs/raglite-flinc-env/bin/python -Xfrozen_modules=off -m ipykernel_launcher -f /home/user02/.local/share/jupyter/runtime/kernel-0a74de29-2cd6-4ab8-9ce8-c006de09dd37.json
```
