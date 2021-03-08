# robo-advisor
## Intro to Python

This project is designed to allow the user to input a stock/crypto ticker of choice, and receive a recommendation on whether to buy or not. Additionally, we should get a chart of the recent closing prices of the stock. We will be pulling from the [alphavantage](https://www.alphavantage.co/) information, so you will need your own API.

### Setup:
To run, set up a virtual environment with conda:

```
conda create -n advisor-env python=3.8
conda activate advisor-env
```

Additionally, you will need to install package dependencies:

```
pip install -r requirements.txt
```

Finally, create a .env file in your respository, using the file to specify your Alphavantage API.

You will be required to get a [alphavantage](https://www.alphavantage.co/) API key:
```
ALPHAVANTAGE_API_KEY = yourkey
```

### To Run:

```
python app/robo_advisor.py
```
Then, follow the prompt to insert your chosen ticker.