# Wikipost
Wikipost is a web application that allows users to scrape and post articles from Wikipedia to their Instagram accounts.

## Features
- **Wikipedia Scraper**: Scrape articles from Wikipedia and extract relevant information such as title, content, and images.
- **Instagram Integration**: Post scraped articles to Instagram accounts using the Instagram API.

## Getting Started

### Prerequisites
- Docker 20.10+
- Docker Compose 2.2+

### Installation
- Clone the repository: `git clone https://github.com/marcorfilacarreras/wikipost.git`
- Navigate to the project directory: `cd wikipost`
- Start the containers: `docker-compose up -d`

> [!WARNING]
> The default WEB image uses the external API of this project, which is hosted on a public server. This means that any data sent to the API will be processed on a remote server and may be subject to the terms and conditions of that server.
>
> If you want to use a self-hosted API, you will need to build your own WEB image using the `web/Dockerfile` file and update the docker-compose.yml file to use your custom image.

### Configuration
- Update the docker-compose.yml file with your desired configuration.

## License
See the [LICENSE.md](LICENSE.md) file for details.

## Contributing
Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request with your changes.

### Reporting Issues
If you encounter any issues or bugs, please report them in the issue tracker.
