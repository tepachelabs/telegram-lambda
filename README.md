# Telegram Lambda

This is a simple Telegram bot that runs on AWS Lambda. It uses the [Serverless Framework](https://serverless.com/) to deploy the bot to AWS.

## Setup

- Install serverless framework with `npm install -g serverless`
- Run `npm install` also to install serverless plugins
- Node 20.10 is used
- Python 3.10 is used.

## Development

- Poetry is used for dependency management.
- Python 3.10 is used.
- Use `poetry install` to install dependencies in a local environment

## Deployment

This is manually deployed by AWS administrators from Tepache.

Maybe in the future this will be deployed automatically.

Remember to run:

```shell
poetry export -f requirements.txt --output requirements.txt
```

if there is any new secret in doppler run:

```shell
doppler secrets substitute serverless.yaml.template > serverless.yaml
```

and run `doppler run -- sls deploy` to deploy the lambda.

## Environment Variables
Setup in Doppler

## How to use?
Create a JWT token with the correct claim for `app` (see Doppler apps) and you will be able to send telegram messages to the tepache group or the given chat id.