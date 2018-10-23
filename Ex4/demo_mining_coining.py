# TODO: Instantiate miners
# TODO: (No network) Miners will take turns winning blocks. Infinite loop using luckyMiner = random.choice(otherMiners)
# TODO: (No network) Observe address balance of miners increase
# Mention mining difficulty



# Run command `$ python3 MinerServer.py -p 5000`
# Run command `$ python3 MinerServer.py -p 5010`

# Run command `$ python3 MinerClient.py -i 5000`
# Run command `$ python3 MinerClient.py -i 5010`

# Mining of new coins is done by the miner that found a block that satisfies the difficulty. 
# The miner will then propose a coinbase transaction with a reward of 100.
# This transaction will be verified by other miners. 
# Miner peers who found a invalid coinbase transaction will ignore the transaction and continue mining/query from other miners