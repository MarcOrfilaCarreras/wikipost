# Contributing

## Development Process

### Frontend Development

#### Prerequisites
- Node.js
- NPM (Node Package Manager)

#### Step 1: Clone the Wikipost Repository
- Clone the Wikipost repository by running the command git clone `https://github.com/marcorfilacarreras/wikipost.git` in your terminal.
- Navigate to the cloned repository by running the command `cd wikipost/web` in your terminal.

#### Step 2: Install Dependencies
- Install the dependencies by running the command `npm install` in your terminal.

#### Step 3: Configure the Application
- Configure the application by copying the `.env.example` file to a new file named `.env` by running the command `cp .env.example .env` in your terminal.
- Update the `.env` file with your desired configuration.

#### Step 5: Start the Application
- Start the application by running the command `npm start` in your terminal.
- You should see the Wikipost application running.

> [!IMPORTANT]
> Make sure you have the Wikipost API running on your machine and accessible at the URL specified in the REACT_APP_API_URL variable.

### Backend Development

#### Prerequisites
- Python 3.8+

#### Step 1: Clone the Wikipost Repository
- Clone the Wikipost repository by running the command git clone `https://github.com/marcorfilacarreras/wikipost.git` in your terminal.
- Navigate to the cloned repository by running the command `cd wikipost/api` in your terminal.

#### Step 2: Create a Virtual Environment
- Create a virtual environment by running the command `python -m venv .venv` in your terminal.
- Activate the virtual environment by running the command `source .venv/bin/activate` in your terminal.

#### Step 3: Install Dependencies
- Install the dependencies by running the command `pip install -r requirements.txt` in your terminal.

#### Step 4: Configure the Application
- Configure the application by copying the `.env.example` file to a new file named `.env` by running the command `cp .env.example .env` in your terminal.
- Update the `.env` file with your desired configuration, including your OpenRouter API credentials.

#### Step 5: Start the Application
- Start the application by running the command `python wsgi.py` in your terminal.
- You should see the Wikipost application running.
