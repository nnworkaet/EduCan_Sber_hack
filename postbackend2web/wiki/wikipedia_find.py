import wikipediaapi

def create_wiki_objects():
   wiki_wiki_ru = wikipediaapi.Wikipedia('MyProjectName (ggg@gmail.com)', 'ru')
   wiki_wiki = wikipediaapi.Wikipedia('MyProjectName (gggg@gmail.com)', 'en')
   return wiki_wiki, wiki_wiki_ru

def clean_string(string):
   punctuation_marks = ['.', ',', '!', '?', '(', ')']
   for mark in punctuation_marks:
       string = string.replace(mark, '')
   return string

def split_string_into_words(string):
   return set(string.split())

def filter_words(words):
   return [word for word in words if len(word) > 3]

def check_words_in_wiki(words, wiki_wiki, wiki_wiki_ru):
   word_list = []
   word_list_ru = []
   for word in words:
       page = wiki_wiki.page(word)
       page_ru = wiki_wiki_ru.page(word)
       if page.exists():
           word_list.append(word)
       if page_ru.exists():
           word_list_ru.append(word)
   return word_list, word_list_ru

def wiki(string):
   wiki_wiki, wiki_wiki_ru = create_wiki_objects()
   string = clean_string(string)
   words = split_string_into_words(string)
   words = filter_words(words)
   word_list, word_list_ru = check_words_in_wiki(words, wiki_wiki, wiki_wiki_ru)
   words_all = word_list + word_list_ru
   return set(words_all)



