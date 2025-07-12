from eth_utils import to_wei
import boa
from conftest import USER, SEND_VALUE



def test_eth_usd_fixture(eth_usd, coffee):
    assert coffee.get_price_feed() == eth_usd.address

def test_owner_is_correct(coffee, account):
    assert coffee.get_owner() == account.address

def test_minimum_usd_is_correct(coffee):
    minimum_usd = to_wei(5, "ether")
    assert coffee.get_minimum_usd() == minimum_usd

def test_one_user_can_fund(coffee, user_has_balance):
    starting_contract_balance = boa.env.get_balance(coffee.address)
    starting_user_balance = boa.env.get_balance(USER)
    with boa.env.prank(USER):
        coffee.fund(value=SEND_VALUE)

    ending_contract_balance = boa.env.get_balance(coffee.address)
    ending_user_balance = boa.env.get_balance(USER)

    assert starting_contract_balance == 0
    assert ending_contract_balance == SEND_VALUE
    assert ending_user_balance == starting_user_balance - SEND_VALUE

def test_increase_numbet_of_funders_after_fund(coffee, user_has_balance):
    starting_number_of_funders = coffee.get_number_of_funders()

    with boa.env.prank(USER):
        coffee.fund(value=SEND_VALUE)

    ending_number_of_funders = coffee.get_number_of_funders()
    expected_number_of_funders = 1

    assert ending_number_of_funders > starting_number_of_funders
    assert starting_number_of_funders == 0
    assert ending_number_of_funders == expected_number_of_funders

def test_track_funder_funded_amount_correctly(coffee, user_has_balance):
    starting_user_funded_amount = coffee.get_amount_funded_by_funder(USER)

    with boa.env.prank(USER):
        coffee.fund(value=SEND_VALUE)

    ending_user_funded_amount = coffee.get_amount_funded_by_funder(USER)

    assert ending_user_funded_amount == starting_user_funded_amount + SEND_VALUE

def test_multiple_funders_can_fund(coffee):
    number_of_funders = 10
    for i in range(number_of_funders):
        user = boa.env.generate_address(i)
        boa.env.set_balance(user, SEND_VALUE * 2)
        with boa.env.prank(user):
            coffee.fund(value=SEND_VALUE)

    actual_number_of_funders = coffee.get_number_of_funders()
    contract_balance = boa.env.get_balance(coffee.address)

    assert actual_number_of_funders == number_of_funders
    assert contract_balance == SEND_VALUE * 10

def test_non_owner_cannot_withdraw(coffee_funded):
    with boa.env.prank(USER):
        with boa.reverts("Only the owner can call this function"):
            coffee_funded.withdraw()

def test_owner_can_withdraw(coffee_funded):
    starting_contract_balance = boa.env.get_balance(coffee_funded.address)
    starting_owner_balance = boa.env.get_balance(coffee_funded.get_owner())

    with boa.env.prank(coffee_funded.get_owner()):
        coffee_funded.withdraw()

    ending_contract_balance = boa.env.get_balance(coffee_funded.address)
    ending_owner_balance = boa.env.get_balance(coffee_funded.get_owner())

    assert ending_contract_balance == 0
    assert ending_owner_balance == starting_owner_balance + starting_contract_balance