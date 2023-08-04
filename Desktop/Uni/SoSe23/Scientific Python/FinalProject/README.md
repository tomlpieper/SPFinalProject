# TelegramAPI powered Vinted.de scraping bot
## Final Project Scientific Python 23 - Tom Pieper Mtr. 982845


> If there is any questions regarding the functionality or implementation, please do not hesitate to contact me under tpieper@uos.de.

## Project description

This interactive automated analysis tool consists of 4 main parts:

* Webscraping vinted.de and sub-pages
* Data Handling, analysis and plotting of desired meta information about the platform
* Permanently saving this data to a NoSQL database (mongodb) 
* Interacting and distributing the analysis via telegram through a simple step-by-step guide

> All of these scripts and tools could be more elaborate and there is definitely rooms for more analysis. This is more to show the possibity of connecting different ends, to make analysis tools more acessible.

## How to use

The whole application incl. all of the scripts persists in a docker environment.
To launch the whole project, one simply needs docker and docker compose installed.

[Docker pownload page](https://docs.docker.com/desktop/install/windows-install/)

Inside the docker folder of the repo, run `docker compose up`.
Before running the docker container one needs to adjust the path in docker-compose.yml the the path where the project is stored/cloned.
This launches the bot as well as the scraper and database. 
MongoDB is launched in a seperate container, to simplyfy detaching the program itsafe from the permanent storage.

## Bot Interaction
To interact with the telegram-bot and retrieve analysis and images, one can simply open telegram and send a message to `@v_scraping_bot`. 
To start the process text `/init` or `/start`. The bot then guides you through the rest of the process and possibilities.
When data for the selected date is available, one can select which analysis the bot should prepare and then the bot send the done analysis as a .jpg to the user.
A custom keyboard was implemented for each decision the user has to make in order to simplify the process for the user. Screenshots of the bot interaction are in the screenshots folder.

## Scraping
The scraping is done in the spracing.py and basically consists of a lot of HTML requests and more parsing, splitting and sub-string creation to exctract the needed data.
> Note: The process of HTML retrieval - more specific, the looping over different html retrieval functions of sub-pages seems tedious and inefficient at first. However after some trying around, it was the most simple and straight forward way to retrieve the category IDs and values.

## Permanent Storage (MongoDB)
To be able to access data that was created before the day that the bot is running currently, the file db_connector.py uses the instance of MongoDB in a seperate docker container to store the dataframes with a date. This enables the user to also retrieve analysis of a different day.

## Automated scraping 6 am

Since the scraping itself takes about 2-3 hours (due to limitations of the server regarding the repeated access and rate limits) in the main.py there is a scheduled function that autmatically launches the scrape function so as long as the docker containers are running on a raspberry or something similar (even in the background of every normal pc) each morning there is an automated new data retrieval that is then stored in MongoDB.

 