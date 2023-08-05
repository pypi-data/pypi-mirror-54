# DBIS Pipeline
This pipline can be used to run analyses in a structured way.

## Usage

the user writes a minimal configuration file which contains only the following
information:
 * "how do I get the data?", by providing a dataloader
 * "what to do with the data?", by providing a scikit pipeline
 * "what to do with the result?", by providing output handlers.

Please have a look at the examples for more information.

## Requirements

`pipenv`

everything else should be installed by pipenv.

## Installation

1. Create a fresh directory.
2. In that directory, call `pipenv install 'git+ssh://git@git.uibk.ac.at/dbis/software/dbispipeline#egg=dbispipeline'`
   This call will install a virtual environment as well as all dependencies.
3. Write your configuration(s)
4. call `pipenv run python -m dbispipeline <yourconfigurationfile.py>`

Enjoy!


## Configuration
The framework look in multiple directories for its configuration files.
* `/usr/local/etc/dbispipeline.ini` used for system wide default.
* `$HOME/.config/dbispipeline.ini` used for user specific configurations.
* `./dbispipeline.ini` for project sepcifig configurations.

And example configuration file looks like this:
```
[database]
host = db.dbis.lan
user = pipelineuser
port = 5432
password = <secure-password>
database = pipelineresults

[project]
name = dbispipeline-test

[mail]
sender = c703-dbis-ev@uibk.ac.at
recipient = c703XXXX@uibk.ac.at
smtp_server = smtp.uibk.ac.at
```
