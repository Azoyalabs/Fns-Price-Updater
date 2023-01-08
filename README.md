# Fetch Name Service Automated Price Update  

As the Fetch blockchain is currently lacking Oracles at the moment, we're updating prices using data from CoinGecko.  

This repo contains the algorithm responsible for updating the price:  
- Get Fetch price data from CoinGecko  
- Compute new prices in Fetch for the different pricing segments of domains  
- Send a transaction using Cosmpy to update the Smart Contract  

[Docs for the Fetch Name Service are available here.](https://docs.azoyalabs.com/)
