from bitcoinlib.wallets import Wallet, Mnemonic, wallets_list, wallet_create_or_open, wallet_delete_if_exists
from wallet.shellmessages import primary, success, info, warn, danger
from bitcoinlib.transactions import Transaction
from os import system
import qrcode_terminal

def application(cmd='init'):
    matchcmd(cmd)
    ncmd = input('>>>  ')
    application(ncmd)


def init():
    system('clear')
    showlogo()
    print('\n Wellcome for shell wallet')
    print('\n --------------------------')
    print('\n overview commands ( h, ls, o, del, c, exit)\n')
    printwallets()

def help():
    for key in commands_desc.keys():
        print(f'  .({key}) - {commands_desc[key]} .')

def printwallets():

    optraw = ''
    wraw = '|'

    for [i, w] in enumerate(listwallets()):
        n = i + 1
        wallet = Wallet(w['name'])
        balance = wallet.balance()
        wraw += f"{n} - {w['name']}, btn - {balance}|"

    primary(optraw)
    info(wraw)

def listwallets():
    return wallets_list()

def endapp():
    success('Good bye!')
    exit(0)

def open():
    wl = listwallets()

    if len(wl) == 1:
        w = Wallet(wl[0]['id'])
        w.info()
        info('commands (out, addr, qrcode, transact)')
        return walletopen(w)

    id = input('wallet id >>> ')
    system('clear')

    w = Wallet(id)
    w.info()
    info('commands (out, addr, qrcode, transact)')
    walletopen(w)
    

def walletopen(wallet):
    cmd = input(f'{wallet.name} >>> ')
    matchwcmd(cmd, wallet)

def createwallet():
    name = input('Choose the wallet name: ')
    mnemonic = Mnemonic()
    pkeys = mnemonic.generate(strength=256, add_checksum=True)

    wallet_create_or_open(name, password=pkeys)

    primary('\n\tWrite this private key to access the wallet\n')
    listpk = pkeys.split(' ')

    num = 0

    for rl in range(0, 6):
        raw = f'\t'

        for i in range(0, 4):
            raw += f'{listpk[num]}  '
            num += 1

        warn(raw)
    
def deletewallet():

    id = input('Wallet id >>> ')

    if wallet_delete_if_exists(Wallet(id).name):
        success('Wallet deleted')
    else:
        danger('Wallet cannot be deleted')

commands = {
    'init': init,
    'ls': printwallets,
    'exit': endapp,
    'h': help,
    'o': open,
    'c': createwallet,
    'del': deletewallet
}

commands_desc = {
    'ls': 'List all wallets with his balance',
    'exit': 'Exit of application',
    'o': 'Open an wallet',
    'c': 'Create a wallet',
    'del': 'Delete some wallet'
}

def out(wallet):
    application()

def showaddress(wallet):
    primary(f'Address Wallet: {wallet.get_key().address}')

def showqrcode(wallet):
    qrcode_terminal.draw(wallet.get_key().address)

def transact(wallet):

    addr = input(f"{wallet.name} >> Address: ")

    value = input(f"{wallet.name} >> Value: ")

    tx = wallet.send_to(addr, value)

    success(f"Broadcast has been sent")
    primary(f"- Transaction Id: {tx.id()}")
    primary(f"- Value: {value}")
    tx.info()


wcommands = {
    'out': out,
    'addr': showaddress,
    'qrcode': showqrcode,
    'transact': transact
}

wcommands_desc = {
    'out': 'Go back for the begin',
    'addr': 'Show the address of wallet', 
    'qrcode': 'Show Qrcode for transactions',
    'transact': 'Transact balance for another wallet'
}

def matchwcmd(cmd, wallet):
    wcommands[cmd](wallet)
    walletopen(wallet)

def matchcmd(cmd):
    return commands[cmd]()

def showlogo():
    warn("###############################################")
    warn("##   ##  ######################################")
    warn("##          ###################################")
    warn("##   ###    ###################################")
    warn("##   ###    ###################################")
    warn("##       ##########       ####   #####   ######")
    warn("##   ####   #######   ########   #####   ######")
    warn("##   ####   #######       ####           ######")
    warn("##          ##########    ####   #####   ######")
    warn("##   ##  ##########       ####   #####   ######")
    warn("###############################################")