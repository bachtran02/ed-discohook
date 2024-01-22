# ed-discohook

A Python program that listens to [edstem](https://edstem.org/) websockets for new threads and publish events to [Discord](https://discord.com/) via [webhooks](https://discord.com/developers/docs/resources/webhook).
This project mainly makes use of [edspy](https://github.com/bachtran02/edspy), a Python wrapper for edstem API which I also maintain. 

## Demo 
<img alt="ed-discohook demo" src="https://github.com/bachtran02/ed-discohook/assets/83796054/8f4c53b1-4a36-4ce2-b39b-1ebdd32a248d" width="550">

## How to set up

### Docker (highly recommended)
> I have been running this program in a [Docker](https://docs.docker.com/engine/install/) container. [`docker-compose.yml`](https://github.com/bachtran02/ed-discohook/blob/main/docker-compose.yml) is included in the repo which
> makes building & running the program with [Docker Compose](https://docs.docker.com/compose/install/) inside of Docker very straightforward.

1. Clone the repo.
2. Create an .env file using [this template](https://github.com/bachtran02/ed-discohook/blob/main/.env.example) and enter your Ed API token, which can be created [here](https://edstem.org/us/settings/api-tokens).
3. In `.env` file, also enter Discord webhook URLs of the channels you want to send the payload to. 
> Read more about Discord wehooks [here](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)

It is a good practice not to put Discord webhook URLs in the `main.py`, so you may want to store them in the `.env` as well. You can use any variable name as you like, just make sure
the names are matched in [`this part`](https://github.com/bachtran02/ed-discohook/blob/main/main.py#L13) of `main.py` so the secrets can be looked up and retrieved correctly in the main file.

4. Run `docker compose build` to build the project and then `docker compose up` to start running it.
