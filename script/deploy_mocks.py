from src.mocks import mock_v3_aggregator

STARTING_DECIMALS = 8 
STARTING_PRICE = int(2000e8)

def deploy_feed():
    print("Deploying Mock V3 Aggregator...")
    return mock_v3_aggregator.deploy(STARTING_DECIMALS, STARTING_PRICE)

def moccasin_main():
    return deploy_feed()