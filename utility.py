# Utility Funtions

def makeGraph(percent: float) -> str:
    '''Make progress graph from API graph'''
    pc_rnd = round(percent)
    done_block = f"![](https://via.placeholder.com/{(int(pc_rnd * 4))}x22/000000/000000?text=+)"
    empty_block = f"![](https://via.placeholder.com/{(400 - int(pc_rnd * 4))}x22/b8b8b8/b8b8b8?=text=+)"

    return done_block+empty_block


def makeLanguageList(data: list) -> str:
    '''Make List'''
    data_list = []
    for l in data:
        ln = len(l['name'])
        ln_text = len(l['text'])
        op = f"""
| | | | |
| --- | --- | --- | --- |
|{l['name'][:25]}{' ' * (25 - ln)}|{l['text']}|{' ' * (20 - ln_text)}{makeGraph(l['percent'])}|{l['percent']}%|
| | | | |
        """
        data_list.append(op)
    return ' \n'.join(data_list)


def makeCommitList(data: list) -> str:
    '''Make List'''
    data_list = []
    for l in data[:7]:
        ln = len(l['name'])
        ln_text = len(l['text'])
        op = f"""|{l['name']}{' ' * (13 - ln)}|{l['text']}{' ' * (15 - ln_text)}|{makeGraph(l['percent'])}|{l['percent']}%|\n"""
        data_list.append(op)
    return ' '.join(data_list)
