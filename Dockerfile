FROM conda/miniconda3:latest

###	Expose main port and use bash for variables management
EXPOSE 5002
SHELL ["/bin/bash", "-c"]

###	Software requirements install/update
RUN apt update && apt install -y apt-utils gcc build-essential
RUN pip install --upgrade pip
RUN pip install PyHamcrest==1.9.0
RUN conda update -y conda

### Set working directory and copy project to that folder
WORKDIR /bot/
COPY . /bot/

###	Create virtual environment
RUN conda create -y -n py36 python=3.6 --name idm-bot --file requirements_anaconda.txt

###	Setting the following environment variables allows to effectively use the
###	virtual environment that we just created.
###	source activate idm-bot will not work since it only works for the current
###	shell session, therefore resetting at every intermediate iteration
ENV CONDA_DEFAULT_ENV idm-bot
ENV CONDA_PREFIX /usr/local/envs/$CONDA_DEFAULT_ENV
ENV PATH $CONDA_PREFIX/bin:$PATH

###	Project requirement libraries install
RUN pip install --ignore-installed -r requirements_pip.txt

###	Train core and nlu (N.B. it is possible not to execute training at every
###	build by mounting the models/ folder as an external volume)
RUN make train-core
RUN make train-nlu

###	Run the bot
ENTRYPOINT make run-actions & make run-bot-facebook
