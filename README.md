# A2rchi
An AI Augmented Research Chat Intelligence for MIT's subMIT project in the physics department

## Setup

### Keys and Passwords

A2rchi uses several other services in order to make it's operations possible. These include OpenAI, Cleo, and a mailbox manager. In order to use these services, A2rchi must be given acsess to the account usernames and passwords. You should add these as text files in a secure directory outside the A2rchi repository. You can find templates of what the text files look like in the config directory of the repo. These are then loaded as environment variables in the `setup.sh` script. You may have to modify the paths in `setup.sh` to fit the paths where you saved the keys and passwords. 

The `.imap`, `.sender`, and `.cleo ` file are only needed to run the mailbox/cleo service. The `.salt` file is only needed to run the uploader service. The OpenAI key is needed to run the GPT-4 model which A2rchi is based on. However A2rchi is also able to run on other models (found in `chain/models.py`). The exact model to use can be changed in `config/config.yaml `. 

Once all the account credentials are loaded into the places they need to be, simply run `./setup.sh`

### Conda Environment

The environment.yml file contains the needed requirements to run A2rchi. To create the A2rchi environment, simply run

```
conda env create -f environment.yml -n "A2rchi_env"
```

in the repository (this may take awhile). Then activate it using

```
conda activate A2rchi_env
```

(You need not create the environment everytime you log in, butyou do need to activate it)

## Usage

### Running Serivces

All the excecutables are in the `bin/` directory. Simply run them with python (i.e. with `python bin/service_chat.py`). You will need to run the upload service before anything else, otherwise A2rchi will not have any information to reference for context. The upload service first scrapes any public data which is specified in the `utils/scraper.py` script and then starts a web upload service to allow you to dynamically upload context via a flask application. If you do not need dynamic uploading, you can kill the upload service once it finished scraping. 

In order to use the web upload service, you must create an account. This account can be created by running the following commands in a ptyhon shell after `setup.sh` has been run and the conda environment has been activated:

```
from interfaces.uploader_app import add_username_password
add_username_password(yourusername, yourpassword)
```


### Running Tests

All tests are done using pytest. In the top level directory of the repo, run the command `pytest`. 
