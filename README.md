# Open Data Hub chatbot

## Prerequisites
Two files must be added to this repository in order to successfully run the chatbot.
They both must be placed in the root folder of the project. Two demo files that contain the structure were inserted as a reference.

#### fb_credentials.yml
The file should be as follows:
```
channels.facebook.FacebookInput:
  verify: ""
  secret: ""
  page-access-token: ""
```

The data to be filled is found in the development console of the facebook application.
The `verify` token is arbitrarily chosen by the owner of the application, the `secret` and `page-access-token` will be provided in response by facebook.

#### api_credentials.txt
Such file is needed to connect to the OpenData Hub and contains three rows, in which (in this particular order, one per row) the following fields must be provided:
- username (email address)
- password
- generated token

The three fields must be entered **without** string-delimiting quotes. Also, please make sure that this file contains **just these three lines** and no other information.
If this is the first time you are running the bot you can leave the generated token line empty and your token will be stored there after it's generated.

## Software requirements
- Conda (developed with version 4.3.30)

The following requirements will be automatically installed with Conda

- Python version: 3.6.6
- pip version: 18.1

## Manual installation of RASA Core and all the packages used
1) Create virtual environment: ```$ conda create -y -n py36 python=3.6 --name idm-bot --file requirements_anaconda.txt```
2) Activate ```$ source idm-bot/bin/activate```
3) Install the RASA stack, environment dependencies and python modules: ```(idm-bot)$ pip install -r requirements_pip.txt```

The third step is very important so please monitor the process carefully.
Now you have a Python virtual environment ready to run the bot on.

**SEE BELOW FOR DOCKER IMPLEMENTATION!**

## Manually run the bot
To make the execution process easier a Makefile is provided in order to eliminate the need to write long commands over and over again. To execute bot functionalities all you need is to call `$ make <function_name>` (options below):

**If you are running the bot for the first time** then the first thing to do is *train it*. Also the bot must be re-trained everytime you make a change to the core or nlu files(covered below in more detail). That's because the bot needs to be trained in order to run and be able to respond. To do this simple run the commands: `$ make train-core` and `$make train-nlu`

Here is the full list of commands in the Makefile, with the description for each one:
- `train-core`: Performs the training for RASA core, which covers the dialogue. This command should be ran every time you make changes to the stories or domain file, since these files affect the bot-user dialogue (more info [here](https://www.rasa.com/docs/core/policies/))
- `train-nlu`: Performs NLU training. Should be ran every time you add/remove/change nlu data (more info [here](https://rasa.com/docs/nlu/dataformat/))
- `run-actions`: Calls the action.py file which contains our custom functionalities and registers those custom actions
In this custom action is where the API calls are made and also where we define the bot's response if the user asks for help (more info [here](https://www.rasa.com/docs/core/customactions/))
- `run-bot`: Runs the bot in the most basic mode (CLI mode)
- `run-bot-debug`: Runs the bot via CLI and shows debugging logs (very helpful, especially if you are missing files with the credentials)
- `run-bot-interactive`: Runs the bot via CLI and activates interactive learning (more info [here](https://www.rasa.com/docs/core/interactive_learning/))
- `run-bot-facebook`: Runs the bot on a Facebook Messenger channel using the credentials we provide (more info [here](https://www.rasa.com/docs/core/connectors/#facebook-setup))


## Use Docker
If you want to run the project on Docker, the version with which the project was developed and tested is `18.09.0`. To do so it is important to build and run the Docker image as found in `docker-cycle.sh`, with all the flags there specified. You can directly use that script, taking care of cleaning up unused images in case of redeployment.

Keep in mind that Docker itself is good for development and testing, but you may want to adapt the Dockerfile for production, as well as use more scalable solutions like [Docker Swarm](https://docs.docker.com/engine/swarm/)

Docker will automatically re-train the core and nlu at every image build, so that every build introduces some functionality or bugfixing. If that is not the case and you want your training to persist over rebuilds, you will need to mount the `models/` folder as an external module and remove from the Dockerfile the instructions
```
RUN make train-core
RUN make train-nlu
```
that will trigger the training.

## RASA Core and NLU: How to edit dialogue and NLU functionalities
RASA works as a stack. Core controls dialogue and NLU controls language understanding (as the name suggests).

The most important files that are related to development as far as **RASA Core** is concerned are data/stories.md and the domain.yml file. These files control your bot's dialogue flow and the way it will interact with the user. For detailed information on how to edit them and how RASA Core works visit the corresponding official documentation:
- [Quickstart](https://www.rasa.com/docs/core/quickstart/)
- [Domains](https://www.rasa.com/docs/core/domains/)
- [Stories](https://www.rasa.com/docs/core/stories/)

As for the **NLU part**, the data/nlu_data.md file is the most important file as here you define your user's intents and how the bot should process them. So you are basically telling your bot that if the user says something like X then he is trying to do intent Y. This bot uses the tensorflow pipeline for NLU. For detailed information on NLU pipelines and how to edit the nlu_data.md file visit the corresponding official documentation:
- [Choosing pipeline](https://www.rasa.com/docs/nlu/choosing_pipeline/)
- [Dataformat](https://www.rasa.com/docs/nlu/dataformat/)
