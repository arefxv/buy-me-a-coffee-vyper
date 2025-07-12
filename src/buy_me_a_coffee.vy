# pragma version 0.4.1
# license MIT 

from interfaces import AggregatorV3Interface
import get_price_module

OWNER: immutable(address)
PRICE_FEED: immutable(AggregatorV3Interface)
MINIMUM_USD: constant(uint256) = as_wei_value(5, "ether")
funders: DynArray[address, 1000]
funder_to_amount_funded: HashMap[address, uint256]

@deploy 
def __init__(price_feed: address):
    OWNER = msg.sender
    PRICE_FEED = AggregatorV3Interface(price_feed)

@internal 
@payable 
def _fund():
    usd_value_of_eth: uint256 = get_price_module._get_eth_to_usd_rate(PRICE_FEED, msg.value)
    assert usd_value_of_eth >= MINIMUM_USD, "Minimum coffee is $5!"
    self.funders.append(msg.sender)
    self.funder_to_amount_funded[msg.sender] += msg.value

@internal 
def _only_owner():
    assert msg.sender == OWNER, "Only the owner can call this function"

@external 
@payable 
def __default__():
    self._fund()

@external 
@payable 
def fund():
    self._fund()

@external 
def withdraw():
    self._only_owner()

    for funder: address in self.funders:
        self.funder_to_amount_funded[funder] = 0
    self.funders = []

    raw_call(OWNER, b"", value = self.balance)


@external 
@view 
def get_eth_to_usd_rate(eth_amount: uint256) -> uint256:
    return get_price_module._get_eth_to_usd_rate(PRICE_FEED, eth_amount)

@external 
@view 
def get_owner() -> address:
    return OWNER

@external 
@view 
def get_price_feed() -> AggregatorV3Interface:
    return PRICE_FEED

@external 
@view 
def get_minimum_usd() -> uint256:
    return MINIMUM_USD

@external 
@view 
def get_number_of_funders() -> uint256:
    return len(self.funders)

@external 
@view 
def get_amount_funded_by_funder(funder: address) -> uint256:
    return self.funder_to_amount_funded[funder]

@external 
def get_funder_by_index(index: uint256) -> address:
    assert index <= len(self.funders) - 1, "Index out of bounds"
    return self.funders[index]