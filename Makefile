.PHONY: clean test lint

TEST_PATH=./

train-core:
	python -m rasa_core.train -d domain.yml -s data/stories.md -o models/dialogue
train-nlu:
	python -m rasa_nlu.train -c nlu_config.yml --data data/nlu_data.md -o models --fixed_model_name nlu --project current --verbose
run-actions:
	python -m rasa_core_sdk.endpoint --actions actions
run-bot:
	python -m rasa_core.run -d models/dialogue -u models/current/nlu --endpoints endpoints.yml
run-bot-debug:
	python -m rasa_core.run -d models/dialogue -u models/current/nlu --debug --endpoints endpoints.yml
run-bot-facebook:
	python -m rasa_core.run -d models/dialogue -u models/current/nlu --port 5002 --credentials fb_credentials.yml --endpoints endpoints.yml --debug
run-bot-interactive:
	python -m rasa_core.train --online -o models/dialogue -d domain.yml -s data/stories.md --endpoints endpoints.yml --nlu models/current/nlu
