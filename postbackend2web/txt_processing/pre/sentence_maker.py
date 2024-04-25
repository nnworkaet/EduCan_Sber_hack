def is_sentence_complete(sentence):
    punctuation_marks = ['.', '!', '?']
    last_char = sentence[-1] if len(sentence) > 0 else ''
    return last_char in punctuation_marks

def merge_incomplete_sentences(sentences_with_timing):
    merged_sentences = []
    current_sentence = {'timing': None, 'text': ''}
    #print(sentences_with_timing)
    for sentence in sentences_with_timing:
        timing, text = sentence.split('    ')
        if current_sentence['timing'] is None:
            current_sentence['timing'] = timing
            current_sentence['text'] = text
        else:
            current_sentence['timing'] = current_sentence['timing'][0:12]+timing[13:]
            current_sentence['text'] += ' ' + text

        if is_sentence_complete(text):
            merged_sentences.append(current_sentence)
            current_sentence = {'timing': None, 'text': ''}

    if current_sentence['timing'] is not None:
        merged_sentences.append(current_sentence)

    return merged_sentences

text_with_timing = [
    '00:00:0.00 - 00:00:5.80    Приветствую вас, друзья!',
    '00:00:5.80 - 00:00:8.36    Ролик получился достаточно длинный, поэтому перед',
    '00:00:8.36 - 00:00:11.36    началом давайте обговорим, что в этом ролике будет',
    '00:00:11.36 - 00:00:15.36    AI будет, IT будет все будет'
]
def sentense(text_with_timing):
    # Объединение незавершенных предложений с сохранением таймингов
    merged_sentences_with_timing = merge_incomplete_sentences(text_with_timing)
    combined_list = [ f"{item['timing']} {item['text']}" for item in merged_sentences_with_timing]
    return combined_list
