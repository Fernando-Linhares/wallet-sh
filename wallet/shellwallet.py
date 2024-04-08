from bitcoinlib.wallets import Wallet, Mnemonic, wallets_list, wallet_create_or_open, wallet_delete_if_exists
from bitcoinlib.services.services import Service
from wallet.shellmessages import primary, success, info, warn, danger
from wallet.shcolors import shcolors
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
    success('\n Wellcome to your shell wallet')
    print('\n --------------------------')
    print('\n overview commands ( h, ls, o, del, c, trans, clear, exit)\n')
    print('Wallets ')
    printwalletsonce()

def help():
    for key in commands_desc.keys():
        print(f'  .({key}) - {commands_desc[key]} .')

def printwalletsonce():

    wallets = listwallets()
    if len(wallets) > 0:
        wallet = Wallet(wallets[0]['id'])
        balance = wallet.balance()
        colors = shcolors()
        print(f' {colors.OKBLUE}::::::::::::::::::{colors.ENDC} {colors.WARNING}WALLET{colors.ENDC} {colors.OKBLUE}:::::::::::::::::::::::::::::::::{colors.ENDC}')
        primary(':::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
        print(f"  [{wallets[0]['id']}]   {colors.OKGREEN}{wallet.name}{colors.ENDC} - BCT {balance}")
        primary(':::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
        print('..')

        if len(wallets) > 1:
            print(f'(+ {len(wallets) - 1})')

def clear(w=None):
    system('clear')

def printwallets():

    for w in listwallets():
        id = w['id']

        wallet = Wallet(w['name'])
        balance = wallet.balance()
        colors = shcolors()
        print(f' {colors.OKBLUE}::::::::::::::::::{colors.ENDC} {colors.WARNING}WALLET{colors.ENDC} {colors.OKBLUE}:::::::::::::::::::::::::::::::::{colors.ENDC}')
        primary(':::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
        print(f"  [{id}]   {colors.OKGREEN}{w['name']}{colors.ENDC} - BCT {balance}                    ")
        primary(':::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
        print('')

def listwallets():
    return wallets_list()

def endapp():
    success('Good bye!')
    exit(0)

def open():
    wl = listwallets()

    if len(wl) == 1:
        w = Wallet(wl[0]['id'])
        walletinfo(wl[0]['id'])
        info('commands (out, addr, qrcode, transact)')
        return walletopen(w)

    id = input('wallet id >>> ')
    system('clear')

    w = Wallet(id)
    walletinfo(id, w)
    info('commands (out, addr, qrcode, transact)')
    walletopen(w)
    

def walletinfo(id, w: Wallet):
    warn("::::::::::::::::::::::::::::::::::::::::::::::::::::")
    warn(f"  Id:      {id}")
    warn(f"  Name:    {w.name}")
    warn(f"  Balance: {w.balance()} ₿")
    warn(f"  Address: {w.get_key().address}")
    primary(f"  Transactions: {len(w.transactions())}")
    warn("::::::::::::::::::::::::::::::::::::::::::::::::::::")

def showinfotransaction():
    txid = input("Insert Transaction Id: ")
    servicename = input("Insert Service Name: ")

    service = Service(network=servicename);
    t = service.gettransaction(txid)
    t.info()

def walletopen(wallet):
    cmd = input(f'{wallet.name} >>> ')
    matchwcmd(cmd, wallet)

def createwallet():
    name = input('Choose the wallet name: ')
    mnemonic = Mnemonic()
    pkeys = mnemonic.generate(strength=256, add_checksum=True)

    nw = input('Choose the wallet netowork: ')

    wallet_create_or_open(name, password=pkeys, network=nw)

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
    'del': deletewallet,
    'clear': clear,
    'trans': showinfotransaction
}

commands_desc = {
    'ls': 'List all wallets with his balance',
    'exit': 'Exit of application',
    'o': 'Open an wallet',
    'c': 'Create a wallet',
    'del': 'Delete some wallet',
    'trans': 'Trasaction Info Search',
    'clear': 'Clear shell content'
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
    'transact': transact,
    'clear': clear
}

wcommands_desc = {
    'out': 'Go back for the begin',
    'addr': 'Show the address of wallet', 
    'qrcode': 'Show Qrcode for transactions',
    'transact': 'Transact balance for another wallet',
    'clear': 'Clear shell content'
}

def matchwcmd(cmd, wallet):
    wcommands[cmd](wallet)
    walletopen(wallet)

def matchcmd(cmd):
    return commands[cmd]()

def showlogo():
    warn("#####################################################")
    warn("##  ###  ############################################")
    warn("##          #########################################")
    warn("##   ####   #########################################")
    warn("##   ####   #########################################")
    warn("##         ####       ###   ###   ###################")
    warn("##   ####   ###   #######   ###   ###################")
    warn("##   ####   ###       ###         ###################")
    warn("##          #######   ###   ###   ###################")
    warn("##  ###  ######       ###   ###   ### wallet sh #####")
    warn("#####################################################")