# Utility Funtions

def makeGraph(percent: float) -> str:
    '''Make progress graph from API graph'''
    done_block = '█'
    empty_block = '░'
    pc_rnd = round(percent)
    return f"{done_block * int(pc_rnd / 4)}{empty_block * int(25 - int(pc_rnd / 4))}"


def makeLanguageList(data: list) -> str:
    '''Make List'''
    data_list = []
    for l in data:
        ln = len(l['name'])
        ln_text = len(l['text'])
        op = f"{l['name'][:25]}{' ' * (25 - ln)}{l['text']}{' ' * (20 - ln_text)}{makeGraph(l['percent'])}   {l['percent']}%"
        data_list.append(op)
    return ' \n'.join(data_list)


def makeCommitList(data: list) -> str:
    '''Make List'''
    data_list = []
    for l in data[:7]:
        ln = len(l['name'])
        ln_text = len(l['text'])
        op = f"{l['name']}{' ' * (13 - ln)}{l['text']}{' ' * (15 - ln_text)}{makeGraph(l['percent'])}   {l['percent']}%"
        data_list.append(op)
    return ' \n'.join(data_list)
