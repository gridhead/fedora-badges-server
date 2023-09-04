# Fedora Badges Server

## About

The backend service for the entire project and has direct interactions with its neighbouring internal entities (i.e. Collection, Database, Liberation, Messages Consumer, Accolades CLI)

This now also includes the schema and interactions for the central database entity related to the Fedora Badges system abstracted with libraries like SQLAlchemy, Alembic and Psycopg2.

## Setup

1. Install `git`, `podman`, `postgres`, `poetry` and `virtualenv` on your development environment.  
   Command
   ```
   $ sudo dnf install git podman postgres poetry virtualenv
   ```
2. Ensure that `podman` service is enabled and started.  
   Command
   ```
   $ sudo systemctl enable podman.service
   ```
   Sample output
   ```
   Created symlink /etc/systemd/system/default.target.wants/podman.service → /usr/lib/systemd/system/podman.service.
   ```
   Command
   ```
   $ sudo systemctl start podman.service
   ```
3. Download the official `postgres` image from `docker.io/library/quay.io` OCI images repository and start a container with your preferred settings.  
   Command
   ```
   $ podman pull docker.io/library/postgres:latest
   ```
   Sample output
   ```
   ✔ docker.io/library/postgres:latest
   Trying to pull docker.io/library/postgres:latest...
   Getting image source signatures
   Copying blob 1b47429b7c5f done  
   Copying blob 52d2b7f179e3 done  
   Copying blob aa8e32a16a69 done  
   Copying blob 8950a67e90d4 done  
   Copying blob ec0d4c36c7f4 done  
   Copying blob d9c06b35c8a5 done  
   Copying blob a773f7da97bb done  
   Copying blob 7bddc9bbcf13 done  
   Copying blob 60829730fa39 done  
   Copying blob f3d9c845d2f3 done  
   Copying blob cfcd43fe346d done  
   Copying blob 576335d55cdb done  
   Copying blob caad4144446c done  
   Copying config 43677b39c4 done  
   Writing manifest to image destination
   43677b39c446545c6ce30dd8e32d8c0c0acd7c00eac768a834e10018f5e38c32
   ```
   Command
   ```
   $ docker run \
       --name <CONTAINER-NAME> \
       --env POSTGRES_USER=<DATABASE-USERNAME> \
       --env POSTGRES_PASSWORD=<DATABASE-PASSWORD> \
       --env POSTGRES_DB=<DATABASE-NAME> \
       --env PGDATA=/var/lib/postgresql/data/pgdata \
       --volume <MOUNT-LOCATION>:/var/lib/postgresql/data \
       --publish <DATABASE-PORT>:5432 \
       --restart unless-stopped \
       --detach postgres:latest
   ```
4. Clone the repository to the local storage and make it the present working directory.  
   Command
   ```
   $ git clone https://gitlab.com/fedora/websites-apps/fedora-badges/server.git
   ```
   Sample output
   ```
   Cloning into 'server'...
   remote: Enumerating objects: 696, done.
   remote: Counting objects: 100% (401/401), done.
   remote: Compressing objects: 100% (387/387), done.
   remote: Total 696 (delta 235), reused 18 (delta 14), pack-reused 295
   Receiving objects: 100% (696/696), 1.46 MiB | 6.84 MiB/s, done.
   Resolving deltas: 100% (385/385), done.
   ```
   Command
   ```
   $ cd server
   ```
5. Make a copy of the default configuration file and add the preferred settings inside it.
   ```
   $ cp badges_server/config/standard.py badges_server/config/myconfig.py
   $ nano badges_server/config/myconfig.py
   ```
   Index
   - `database` = `<DATABASE-NAME>` as mentioned while setting up the database container
   - `jsyncurl` = `127.0.0.1` if the database container is started on the same device or the reachable IP address of the device where the database service is running
   - `dtbsport` = `<DATABASE-PORT>` as mentioned previously while setting up the database container
   - `username` = `<DATABASE-USERNAME>` as mentioned previously while setting up the database container
   - `password` = `<DATABASE-PASSWORD>` as mentioned previously while setting up the database container
   - `servhost` = `127.0.0.1` if the service is intended to be accessible only on the same device, `0.0.0.0` if the service is intended to be accessible on all interfaces with IPv4 addressing or `::` if the service is intended to be accessible on all interfaces with IPv6 addressing
   - `servport` = `8080` if the service is intended to be accessible on the port number `8080` or `[1-65535]` depending on your choice. Ensure that the firewall rules have been set accordingly to allow traffic through the said port
   - `cgreload` = `False` for use in production environments where the service is not required to reload whenever changes are made in the codebase or `True` for use in development environments where the changes are actively tested as they are introduced to the codebase
   - `logrconf` = The default logging configuration for the entire application service. It is for the best to leave it as defined by the default configuration if the settings do not make any sense although it is encouraged to play around with it for a better understanding.
   - `wsgiconf` = The default logging configuration for the web server gateway interface library. It is for the best to leave it as defined by the default configuration if the settings do not make any sense although it is encouraged to play around with it for a better understanding.
6. Create a virtual environment in the said directory and activate it.  
   Command
   ```
   $ virtualenv venv
   ```
   Sample output
   ```
   created virtual environment CPython3.11.3.final.0-64 in 303ms
     creator CPython3Posix(dest=/home/archdesk/Projects/venv, clear=False, no_vcs_ignore=False, global=False)
     seeder FromAppData(download=False, pip=bundle, setuptools=bundle, wheel=bundle, via=copy, app_data_dir=/home/archdesk/.local/share/virtualenv)
       added seed packages: pip==23.1.2, setuptools==68.0.0, wheel==0.40.0
     activators BashActivator,CShellActivator,FishActivator,NushellActivator,PowerShellActivator,PythonActivator
   ```
   Command
   ```
   $ source venv/bin/activate
   ```
   Sample output
   ```
   (venv) $
   ```
7. Check the validity of the project configuration and install the project dependencies.  
   Command
   ```
   (venv) $ poetry check
   ```
   Sample output
   ```
   All set!
   ```
   Command
   ```
   (venv) $ poetry install
   ```
   Sample output
   ```
   Installing dependencies from lock file
   No dependencies to install or update
   Installing the current project: badges-server (0.1.0)
   ```
8. View the version information and help topics of the installed `badges_server` project.  
   Command
   ```
   (venv) $ badges_server --version
   ```
   Sample output
   ```
   badges_server, version 0.1.0
   ```
   Command
   ```
   (venv) $ badges_server --help
   ```
   Sample output
   ```
   Usage: badges_server [OPTIONS] COMMAND [ARGS]...

   Options:
     -c, --conffile PATH  Read configuration from the specified Python file
     --version            Show the version and exit.
     --help               Show this message and exit.

   Commands:
     serve  Start the Badges Server application
     setup  Setup the database schema in the specified environment
   ```
9. Set up the database schema in the database configured by executing the following command.  
   Command
   ```
   (venv) $ badges_server -c badges_server/config/myconfig.py setup
   ```
   Sample output
   ```
   [FPBS] [2023-08-17 12:21:29 +0530] [INFO] Reading the configuration again
   [FPBS] [2023-08-17 12:21:30 +0530] [INFO] Creating database schema
   [FPBS] [2023-08-17 12:21:31 +0530] [INFO] Setting up database migrations
   [FPBS] [2023-08-17 12:21:32 +0530] [INFO] Context impl PostgresqlImpl.
   [FPBS] [2023-08-17 12:21:32 +0530] [INFO] Will assume transactional DDL.
   ```
10. Start the application service by executing the following command.  
    Command
    ```
    (venv) $ $ badges_server -c badges_server/config/myconfig.py serve
    ```
    Sample output
    ```
    [FPBS] [2023-08-17 12:41:27 +0530] [INFO] Reading the configuration again
    [FPBS] [2023-08-17 12:41:27 +0530] [INFO] Starting Badges Server ...
    [FPBS] [2023-08-17 12:41:27 +0530] [INFO] Host address     : 0.0.0.0
    [FPBS] [2023-08-17 12:41:27 +0530] [INFO] Port number      : 8080
    [FPBS] [2023-08-17 12:41:27 +0530] [INFO] Log level        : DEBUG / DEBUG
    [FPBS] [2023-08-17 12:41:27 +0530] [INFO] Reload on change : TRUE
    [FPBS] [2023-08-17 12:41:27 +0530] [INFO] Serving API docs on http://0.0.0.0:8080/docs
    [FPBS] [2023-08-17 12:41:27 +0530] [INFO] Will watch for changes in these directories: ['/home/archdesk/Projects/server']
    [FPBS] [2023-08-17 12:41:27 +0530] [INFO] Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
    [FPBS] [2023-08-17 12:41:27 +0530] [INFO] Started reloader process [10567] using StatReload
    [FPBS] [2023-08-17 12:41:28 +0530] [INFO] Started server process [10569]
    [FPBS] [2023-08-17 12:41:28 +0530] [INFO] Waiting for application startup.
    [FPBS] [2023-08-17 12:41:28 +0530] [INFO] Reading the configuration again
    [FPBS] [2023-08-17 12:41:28 +0530] [INFO] Application startup complete.
    ```

## Contributing

### Pre-commit Tool

This project utilizes the [`pre-commit`](https://pre-commit.com/) tool to maintain code quality and consistency. Before submitting a pull request or making any commits, it is crucial to run the `pre-commit` tool to ensure that your changes meet the project's guidelines.

To run the `pre-commit` tool, follow these steps:

1. Ensure that the project directory is the present working directory and that the virtual environment is enabled.
   ```
   $ cd server
   $ source venv/bin/activate
   ```
2. Execute the following command to run the `pre-commit` hooks for this project against all the modified files.
   ```
   (venv) $ pre-commit run --all-files
   ```
   If any issues are found that can automatically be resolved by the tool, the `pre-commit` tool will make those corrective changes but for those that cannot be automatically resolved by the tool, feedback will be provided as to how they can be manually resolved. Make the requested changes and run the same command again until all issues are resolved.
3. For a streamlined checking and committing workflow, you can also install the `pre-commit` Git hook by executing the following command.
   ```
   (venv) $ pre-commit install
   ```
   This will run the `pre-commit` tool automatically every single time a commit attempted to be made on the repository.

## Read more

* [Tahrir Database](https://gitlab.com/fedora/websites-apps/fedora-badges/server/-/blob/main/docs/TAHRIR.md?ref_type=heads)
* [Badges Database](https://gitlab.com/fedora/websites-apps/fedora-badges/server/-/blob/main/docs/BADGES.md?ref_type=heads)
