balances = Hash(default_value=0)

@construct
def seed():
    balances['jeff'] = 1000000
    balances['stu'] = 1000000
    balances['alex'] = 1000000

@export
def transfer(amount: float, to: str):
    sender = ctx.caller
    assert balances[sender] >= amount, 'Not enough coins to send!'
    balances[sender] -= amount
    balances[to] += amount

@export
def transfer_from(amount: float, to: str, main_account: str):
    sender = ctx.caller
    assert balances[main_account, sender
           ] >= amount, 'Not enough coins approved to send! You have {} and are trying to spend {}'.format(
        balances[main_account, sender], amount)
    assert balances[main_account] >= amount, 'Not enough coins to send!'
    balances[main_account, sender] -= amount
    balances[main_account] -= amount
    balances[to] += amount

@export
def approve(amount: float, to: str):
    sender = ctx.caller
    balances[sender, to] += amount
    return balances[sender, to]

@export
def get_balance(who: str):
    return balances[who]
