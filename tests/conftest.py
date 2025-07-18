import pytest
from script.deploy_mocks import deploy_feed
from script.deploy import deploy_coffee
from moccasin.config import get_active_network
from eth_utils import to_wei
import boa

SEND_VALUE = to_wei(1, "ether") 
USER = boa.env.generate_address("user") 

@pytest.fixture(scope="session")
def eth_usd():
    return deploy_feed()

@pytest.fixture(scope="function")
def coffee(eth_usd):
    return deploy_coffee(eth_usd)

@pytest.fixture(scope="session")
def account():
    return get_active_network().get_default_account()

@pytest.fixture(scope="function")
def coffee_funded(coffee):
    boa.env.set_balance(coffee.get_owner(), SEND_VALUE * 2)
    with boa.env.prank(coffee.get_owner()):
        coffee.fund(value=SEND_VALUE)
    return coffee

@pytest.fixture(scope="function")
def user_has_balance():
    boa.env.set_balance(USER, SEND_VALUE * 2)