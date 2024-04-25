import wikipediaapi

wiki_wiki_ru = wikipediaapi.Wikipedia('MyProjectName (kirill.pogozhikh@gmail.com)', 'ru')
wiki_wiki = wikipediaapi.Wikipedia('MyProjectName (kirill.pogozhikh@gmail.com)', 'en')
string='Основные свойства Python не требует явного объявления переменных, является регистро-зависим (переменная var не эквивалентна переменной Var или VAR — это три разные переменные) объектно-ориентированным языком.Синтаксис Во первых стоит отметить интересную особенность Python. Он не содержит операторных скобок (begin..end в pascal или {..}в Си), вместо этого блоки выделяются отступами: пробелами или табуляцией, а вход в блок из операторов осуществляется двоеточием. Однострочные комментарии начинаются со знака фунта «#», многострочные — начинаются и заканчиваются тремя двойными кавычками «"""». Чтобы присвоить значение пременной используется знак «=», а для сравнения — «==». Для увеличения значения переменной, или добавления к строке используется оператор «+=», а для уменьшения — «-=». Все эти операции могут взаимодействовать с большинством типов, в том числе со строками.'


word_list=[]
word_list_ru=[]
words=string.replace('.','').replace(',','').replace('!','').replace('?','').replace('(','').replace(')','')
words=set(words.split())
words = [word for word in words if len(word) > 3]
print(words)
for word in words:
    page = wiki_wiki.page(word)
    page_ru = wiki_wiki_ru.page(word)
    if page.exists():
        word_list.append(word)

    if page_ru.exists():
        word_list_ru.append(word)

words_all=word_list+word_list_ru
print(words_all)