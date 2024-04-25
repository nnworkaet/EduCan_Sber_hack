#from whisper_old.whisper_txt import texter as audio2txt
from txt_processing.pre.pre_text import start_text_processing as text_processing
from txt_processing.past import summarization_processing,termins_processing,test_processing
from gpt import giga_summary,giga_qa,giga_glossary

import time

def start(audio_path):
    #txt = text_processing(audio2txt(audio_path)) # в аллокейт токенс поменять максимальное количество токенов Проверить достоверностьподсчетов

    text = ['00:00:0.00 - 00:00:11.40     Друзья, привет, с вами снова я, Денис. Рад вас приветствовать на лекции. Сегодня мы будем говорить о массиво.', '00:00:11.40 - 00:00:17.00     На прошлой лекции мы познакомились с языком программирования C-Sharp, с его основными характеристиками,', '00:00:17.00 - 00:00:22.68     а также решили блок базовых задач. На семинарах вы попрактиковались разработки циклических', '00:00:22.68 - 00:00:27.68     условных конструкций, применяли арифметические операторы, а также операции водовывода.', '00:00:27.68 - 00:00:33.72     Сегодня мы вспомним основные понятия, связанные с массивами, их характеристики. Поговорим о том,', '00:00:33.72 - 00:00:39.44     в каких задачах массивы могут применяться. Познакомимся, как осуществляется операция', '00:00:39.44 - 00:00:45.24     создания, заполнения, а также вывода массивов на экран. И решим блок задач на их обработку.', '00:00:45.24 - 00:00:50.24     Ближе к концу лекции мы познакомимся с двумя разновидностями циклов For и For Each,', '00:00:50.24 - 00:00:56.60     а также, друзья, поговорим о таком важном аспекте, как изучение английского для программистов.', '00:00:56.96 - 00:01:1.68     Друзья, перед тем, как приступить к практике и начать решать задачи, давайте вспомним,', '00:01:1.68 - 00:01:7.28     а что из себя представляет массив и какими характеристиками он обладает. Начнем с ключевого', '00:01:7.28 - 00:01:12.72     термина этой лекции, массив. Массив представляет собой структуру данных, которая предназначена', '00:01:12.72 - 00:01:18.48     для охранения элементов, как правило, одного типа. Массив может состоять из целых чисел,', '00:01:18.48 - 00:01:24.36     вещественных, может состоять из символов, а также, например, из строк. Если приводить примеры из', '00:01:24.36 - 00:01:30.60     реальной жизни, то массива мы можем назвать упорядоченный набор инструментов или же набор', '00:01:30.60 - 00:01:36.04     елочных игрушек, который также обладает характеристикой упорядоченности. Второй важный термин', '00:01:36.04 - 00:01:40.60     это индекс элемента массива. Друзья, этот термин можно сформулировать по-разному']


    txt= text_processing(text)
    print(len(txt))
    print(txt)
    result_termins = []
    result_summarization = []
    result_test = []
    for index, part in enumerate(txt):
            part_in_list=[part]
            print(part_in_list)
            print('1=================================================================')

            try:
                sum_new=giga_summary.summary(part_in_list)
                print(sum_new)
                print('2=================================================================')
                result_summarization.append(sum_new)
            except Exception as e:
                print(f"go sleep {e}")

                time.sleep(60)
                sum_new = giga_summary.summary(part_in_list)
                result_summarization.append(sum_new)


            try:
                termins_new=giga_glossary.glossary(part_in_list)
                print(termins_new)
                print('3=================================================================')
                result_termins.append(termins_new)
            except Exception as e:
                print(f"go sleep {e}")

                time.sleep(60)
                termins_new = giga_glossary.glossary(part_in_list)
                result_termins.append(termins_new)


            try:
                test_new=giga_qa.qa_generator(part_in_list)
                print(test_new)
                print('4=================================================================')
                result_test.append(test_new)

            except Exception as e:
                print(f"go sleep {e}")

                time.sleep(60)
                test_new = giga_qa.qa_generator(part_in_list)
                result_test.append(test_new)

    txt_summ = ' '.join(result_summarization)
    txt_termins = ' '.join(result_termins) #Список терминов, потом термины с определением, проверка соответствия с контекстом
    txt_test = ' '.join(result_test)


    try:
        txt_summ= summarization_processing.summar_post_process([txt_summ])
    except Exception as e:
        print(f"go sleep {e}")

        time.sleep(60)
        txt_summ= summarization_processing.summar_post_process([txt_summ])


    try:

        txt_termins=termins_processing.termins_processing(str(txt_termins).replace("\n",""))
    except Exception as e:
        print(f"go sleep {e}")

        time.sleep(60)

        txt_termins=termins_processing.termins_processing(str(txt_termins).replace("\n",""))

    try:
        print(str(txt_test).replace("\n", ""))
        txt_test=test_processing.test_post_process(str(txt_test))
    except Exception as e:
        print(f"go sleep {e}")

        time.sleep(60)
        print(str(txt_test).replace("\n", ""))
        txt_test=test_processing.test_post_process(str(txt_test))

    print('+++++++++++++++++++++++++++RESULTS++++++++++++++++++++++++++++++++')
    print('MAIN TXT ____________________________________')
    print(txt)
    print('\n\n\n')
    print('SUM TXT ____________________________________')
    print(txt_summ)
    print('\n\n\n')

    print('TERMINS TXT ____________________________________')
    print(txt_termins)
    print('\n\n\n')
    print('TEST TXT ____________________________________')
    print(txt_test)
    print('\n\n\n')
    return {'main_txt':txt,'sum':txt_summ,'termins':txt_termins,'test':txt_test}




def make_summarize_gpt(txt):
    txt = text_processing(txt)
    result_summarization = []
    for index, part in enumerate(txt):
            part_in_list=[part]
            try:
                sum_new=giga_summary.summary(part_in_list)
                print('===========SUMMARIZATION========================')
                print(sum_new)
                print('=================================================================')
                result_summarization.append(sum_new)
            except Exception as e:
                print(f"go sleep {e}")

                time.sleep(60)
                sum_new = giga_summary.summary(part_in_list)
                result_summarization.append(sum_new)
    print(result_summarization)
    txt_summ = ' '.join(result_summarization)
    try:
        txt_summ= summarization_processing.summar_post_process([txt_summ])
    except Exception as e:
        print(f"go sleep {e}")

        time.sleep(60)
        txt_summ= summarization_processing.summar_post_process([txt_summ])
    return txt_summ
def make_summarize(txt):
    txt2giga=' '.join(txt)
    result_summarization=[]
    try:
        print("PARTIN LIST", txt2giga)
        sum_new=giga_summary.summary(txt2giga)
        print('===========SUMMARIZATION========================')
        print(sum_new)
        print('=================================================================')
        result_summarization.append(sum_new)
    except Exception as e:
        print(f"go sleep {e}")

        time.sleep(60)
        sum_new = giga_summary.summary(txt2giga)
        result_summarization.append(sum_new)
    print(result_summarization)
    txt_summ = ' '.join(result_summarization)
    try:
        txt_summ= summarization_processing.summar_post_process([txt_summ])
    except Exception as e:
        print(f"go sleep {e}")

        time.sleep(60)
        txt_summ= summarization_processing.summar_post_process([txt_summ])
    return txt_summ
def make_termins(txt):
    print(txt)
    txt_giga = ' '.join(txt)

    result_termins = []


    termins_new = giga_glossary.glossary(txt_giga)
    print('=====================TERMINS================================')
    print(termins_new)
    print('=====================================================')
    result_termins.append(termins_new)

    txt_termins = result_termins  # Список терминов, потом термины с определением, проверка соответствия с контекстом
    print("TXT termins", result_termins[0])


    return txt_termins[0]
def make_termins_gpt(txt):
    txt = text_processing(txt)
    result_termins = []
    for index, part in enumerate(txt):
        part_in_list = [part]
        try:

            termins_new = giga_glossary.glossary(part_in_list)
            print('=====================TERMINS================================')
            print(termins_new)
            print('=====================================================')
            result_termins.append(termins_new)

        except Exception as e:
            print(f"go sleep {e}")

            time.sleep(60)
            termins_new = giga_glossary.glossary(part_in_list)
            result_termins.append(termins_new)

    txt_termins = ' '.join(result_termins)  # Список терминов, потом термины с определением, проверка соответствия с контекстом
    termins_new = (txt_termins.replace("\n", ""))
    try:
        txt_termins=termins_processing.termins_processing(termins_new)

    except Exception as e:
        print(f"go sleep {e}")

        time.sleep(60)
        txt_termins=termins_processing.termins_processing(termins_new)

    return txt_termins
def make_test_gpt(txt_sum):
    txt_sum = text_processing(txt_sum)

    test_new = giga_qa.qa_generator(txt_sum)
    print('=====================TEST================================')
    print(test_new)
    print('=================================================================')




    test_new= (test_new.replace("\n",""))
    #txt_test = test_processing.test_post_process(test_new)
    return test_new
def make_test(txt_sum):
    print(txt_sum)
    txt_giga = ' '.join(txt_sum)

    test_new = giga_qa.qa_generator(txt_giga)
    print('=====================TEST================================')
    print(test_new)
    print('=================================================================')




    test_new= (test_new.replace("\n",""))
    #txt_test = test_processing.test_post_process(test_new)
    return test_new

def launch(txt):
    txt = text_processing(txt)
    return make_termins(txt)



data =[ '00:08:59.00 - 00:09:1.00     Возможно, наша целевая аудитория', '00:09:1.00 - 00:09:3.00     вырастет, появятся', '00:09:3.00 - 00:09:5.00     новые сегменты', '00:09:5.00 - 00:09:7.00     потребителей, которым нужно', '00:09:7.00 - 00:09:9.00     будет применять иной подход', '00:09:9.00 - 00:09:11.00     в продажах. Каким будет сам продукт', '00:09:11.00 - 00:09:13.00     через один год, через', '00:09:13.00 - 00:09:15.00     3 года, через 5 лет? Что мы', '00:09:15.00 - 00:09:17.00     будем делать с продуктом?', '00:09:17.00 - 00:09:19.00     Какие планы у нас в рамках', '00:09:19.00 - 00:09:21.00     разработки продукта? И здесь это', '00:09:21.00 - 00:09:23.00     пересекается, конечно,', '00:09:23.00 - 00:09:25.00     с стратегией самого продукта.', '00:09:25.00 - 00:09:27.00     Как мы будем менять продукт', '00:09:27.00 - 00:09:29.00     и соответственно, какие новые', '00:09:29.00 - 00:09:31.00     фичи появятся в продукте?', '00:09:31.00 - 00:09:33.00     Как он вырастет?', '00:09:33.00 - 00:09:35.00     Как он адаптируется к новым', '00:09:35.00 - 00:09:37.00     реалиям времени?', '00:09:37.00 - 00:09:39.00     И, соответственно, как это будет', '00:09:39.00 - 00:09:41.00     влиять на продукт? И где мы', '00:09:41.00 - 00:09:43.00     будем продавать продукт через', '00:09:43.00 - 00:09:45.00     определенный период времени?', '00:09:45.00 - 00:09:47.00     Как будут развиваться наши каналы', '00:09:47.00 - 00:09:49.00     продаж? И какие у нас цели', '00:09:49.00 - 00:09:51.00     и задачи по', '00:09:51.00 - 00:09:53.00     развитию в тех или иных', '00:09:53.00 - 00:09:55.00     каналах продаж? Далее,', '00:09:55.00 - 00:09:57.00     стратегия продвижения.', '00:09:57.00 - 00:09:59.00     Стратегия продвижения по каналам.', '00:09:59.00 - 00:10:1.00     И здесь важно понимать, во-первых,', '00:10:1.00 - 00:10:3.00     зачем мы используем те или иные', '00:10:3.00 - 00:10:5.00     каналы продаж, связать эти', '00:10:5.00 - 00:10:7.00     каналы продаж со своей целевой', '00:10:7.00 - 00:10:9.00     аудитории, со своим продуктом,', '00:10:9.00 - 00:10:11.00     со своими планами, со своей', '00:10:11.00 - 00:10:13.00     стратегией развития', '00:10:13.00 - 00:10:15.00     продукта и продаж продукта', '00:10:15.00 - 00:10:17.00     как таковых? Кому мы рассказываем', '00:10:17.00 - 00:10:19.00     в этих каналах продвижения', '00:10:19.00 - 00:10:21.00     о своем продукте?', '00:10:21.00 - 00:10:23.00     Кто наш потребитель?', '00:10:23.00 - 00:10:25.00     Как мы рассказываем потребителю?', '00:10:25.00 - 00:10:27.00     Какой рост мы ожидаем', '00:10:27.00 - 00:10:29.00     в этих каналах продвижения?', '00:10:29.00 - 00:10:31.00     Соответственно, нужно понимать', '00:10:31.00 - 00:10:33.00     что нам дают сейчас', '00:10:33.00 - 00:10:35.00     эти каналы продвижения', '00:10:35.00 - 00:10:37.00     и как мы будем в них расти?', '00:10:37.00 - 00:10:39.00     Какие инструменты мы будем', '00:10:39.00 - 00:10:41.00     использовать для роста в канале?', '00:10:41.00 - 00:10:43.00     Как мы будем достигать этого роста?', '00:10:43.00 - 00:10:45.00     И где мы окажемся в рамках', '00:10:45.00 - 00:10:47.00     финансовых целей', '00:10:47.00 - 00:10:49.00     по завершению', '00:10:49.00 - 00:10:51.00     годичного периода, трехгодичного', '00:10:51.00 - 00:10:53.00     и пятилетнего периода?', '00:10:53.00 - 00:10:55.00     Что мы планируем?', '00:10:55.00 - 00:10:57.00     Какой прирост нам даст', '00:10:57.00 - 00:10:59.00     решение в тех или иных каналах?', '00:10:59.00 - 00:11:1.00     И, соответственно, что', '00:11:1.00 - 00:11:3.00     мы будем иметь', '00:11:3.00 - 00:11:5.00     фактически финансово', '00:11:5.00 - 00:11:7.00     в рамках наших', '00:11:7.00 - 00:11:9.00     продаж, нашего продукта', '00:11:9.00 - 00:11:11.00     в тех каналах, где', '00:11:11.00 - 00:11:13.00     мы его продвигаем?', '00:11:13.00 - 00:11:15.00     Работа с персоналом.', '00:11:15.00 - 00:11:17.00     Зачем нам нужен персонал, который', '00:11:17.00 - 00:11:19.00     вовлечен в разработку продукта?', '00:11:19.00 - 00:11:21.00     Насколько сейчас персонал', '00:11:21.00 - 00:11:23.00     реализует все потребности', '00:11:23.00 - 00:11:25.00     разработки продукта', '00:11:25.00 - 00:11:27.00     и мы можем изменить', '00:11:27.00 - 00:11:29.00     этот', '00:11:29.00 - 00:11:31.00     процесс? Возможно,', '00:11:31.00 - 00:11:33.00     мы кому-то больше доверяем', '00:11:33.00 - 00:11:35.00     из команды, возможно, кому-то', '00:11:35.00 - 00:11:37.00     меньше. Возможно, кто-то', '00:11:37.00 - 00:11:39.00     из персонала может больше', '00:11:39.00 - 00:11:41.00     и его можно привлекать', '00:11:41.00 - 00:11:43.00     каким-то более интересным,', '00:11:43.00 - 00:11:45.00     более важным задачем.', '00:11:45.00 - 00:11:47.00     Какой персонал нам потребуется', '00:11:47.00 - 00:11:49.00     на те или иные дальнейшие', '00:11:49.00 - 00:11:51.00     задачи, которые мы планируем', '00:11:51.00 - 00:11:53.00     сделать? И нужно ли', '00:11:53.00 - 00:11:55.00     мы будем, соответственно,']

#print(make_test(data))
