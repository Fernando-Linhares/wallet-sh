from wallet.shcolors import shcolors

def warn(text:str):
    colors = shcolors()
    print(colors.WARNING, text, colors.ENDC)

def info(text:str):
    colors = shcolors()
    print(colors.OKCYAN, text, colors.ENDC)

def success(text:str):
    colors = shcolors()
    print(colors.OKGREEN, text, colors.ENDC)

def primary(text:str):
    colors = shcolors()
    print(colors.OKBLUE, text, colors.ENDC)

def danger(text:str):
    colors = shcolors()
    print(colors.FAIL, text, colors.ENDC)
