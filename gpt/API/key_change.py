
from .key import keys as k
from time import sleep
def shift_list(lst):
   return lst[1:] + lst[:1]


def shift_keys():
    keys = shift_list(k)
    print(keys)
    with open('/Users/kirillpogozih/Desktop/intelligent-assistant-methodist-geekbrains-main/postbackend/gpt/API/key.py', 'w') as f:
        f.write('keys = [\n')
        for key in keys:
            f.write(f'    "{key}",\n')
        f.write(']\n')
def del_key():
    keys = k[1:]
    print('delete key...', keys)
    with open('/Users/kirillpogozih/Desktop/intelligent-assistant-methodist-geekbrains-main/postbackend/gpt/API/key.py', 'w') as f:
        f.write('keys = [\n')
        for key in keys:
            f.write(f'    "{key}",\n')
        f.write(']\n')
    sleep(1)
#print(del_key())