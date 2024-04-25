import tiktoken

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))

    return num_tokens

def allocate(text_list):
    tokens=0
    max_tokens = 2000
    string = []
    list_res=[]
    encoding_name="cl100k_base"
    for text in text_list:
            num_tokens= num_tokens_from_string(text,encoding_name)
            if  (num_tokens+tokens) <max_tokens:
                string.append(text)
                tokens+=num_tokens

            else:
                list_res.append(string)
                string=[]
                string.append(text)
                tokens=0

    list_res.append(string)
    list_res = [' '.join(sublist) for sublist in list_res]

    return list_res

