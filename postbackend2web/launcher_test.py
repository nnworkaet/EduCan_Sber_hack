import json

import openai
import requests
import httpx
from openai import OpenAI
from fake_useragent import UserAgent
# Provide your proxy details here
# if needed
import httpx_socks
import socks


proxy_new="185.244.36.245:25426"

ua = UserAgent()
user_agent=str(ua.chrome)


#'socks5://user:password@127.0.0.1:1080'
proxy = "socks5://104.36.231.251:57905"
proxy_auth = ('r6Hb7Gdu', 'Caw1eppm')


# Set the session in the OpenAI client
api_key = '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'
headers = {'User-Agent': user_agent}

proxies = {'socks5://': 'http://185.244.36.245:25426'}


prompt_test = [

    'У тебя есть текст. Тебе нужно сделать тестирование состоящее из 10 вопросов с 4 вариантами ответа \n Пиши опираясь на этот шаблон, отходить от него нельзя, писать дополнительные слова вне шаблона строго запрещено!!!  \n Шаблон \n [{"question": "вопрос", "variant1": "вариант ответа 1", "variant2": "вариант ответа 2", "variant3": "вариант ответа 3", "variant4": "вариант ответа 4", "answer": ответ в виде имени, например "variant1" },{"question": "вопрос", "variant1": "вариант ответа 1", "variant2": "вариант ответа 2", "variant3": "вариант ответа 3", "variant4": "вариант ответа 4", "answer": ответ в виде имени, например "variant1" },{"question": "вопрос", "variant1": "вариант ответа 1", "variant2": "вариант ответа 2", "variant3": "вариант ответа 3", "variant4": "вариант ответа 4", "answer": ответ в виде имени, например "variant1" }] P.S В значении словарей нельзя использовать кавычки',
    'У тебя есть список вопросов, выбери из них 10 самых интересных. И выведи в том же формате (кодом), в каком я тебе прислал это. Если что вот тот же формат просто кодом: [{"question": "вопрос", "variant1": "вариант ответа 1", "variant2": "вариант ответа 2", "variant3": "вариант ответа 3", "variant4": "вариант ответа 4", "answer": ответ в виде имени, например "variant1" },{"question": "вопрос", "variant1": "вариант ответа 1", "variant2": "вариант ответа 2", "variant3": "вариант ответа 3", "variant4": "вариант ответа 4", "answer": ответ в виде имени, например "variant1" },{"question": "вопрос", "variant1": "вариант ответа 1", "variant2": "вариант ответа 2", "variant3": "вариант ответа 3", "variant4": "вариант ответа 4", "answer": ответ в виде имени, например "variant1" }]P.S В значении словарей нельзя использовать кавычки'
]

example_json = {
    "questions":[
    {
        "question": "вопрос",
        "variant1": "вариант ответа 1",
        "variant2": "вариант ответа 2",
        "variant3": "вариант ответа 3",
        "variant4": "вариант ответа 4",
        "answer": "variant1"
    },
    {
        "question": "вопрос",
        "variant1": "вариант ответа 1",
        "variant2": "вариант ответа 2",
        "variant3": "вариант ответа 3",
        "variant4": "вариант ответа 4",
        "answer": "variant1"
    }]
}
prompt_1="Представь, что ты опытный методист, перед тобой образовательный текст тебе нужно составить"
prompt_2="вопросов к этому тексту с ответами (ключами на подобии `variant1`). Разрешено спрашивать только ту информацию, которая была в тексте. Варианты ответов должны подходить по контексту.Не используй вариант ответа `все вышеперечисленное` "
n="10"
data="Венчание на царствование» Иван IV Васильевич (Грозный) был внуком Ивана III и сыном Василия III и фактически правил в 1547-1584гг. Царь Иван родился в 1530 г. От природы он получил ум бойкий и гибкий, вдумчивый и немного насмешливый, настоящий великорусский, московский ум. Но обстоятельства, среди которых протекло детство Ивана, рано испортили этот ум, дали ему неестественное, болезненное развитие. Иван рано осиротел - на четвертом году лишился отца (Василий III), а на восьмом потерял и мать (Елена Глинская). Он с детства видел себя среди чужих людей. В душе его рано и глубоко врезалось и всю жизнь сохранялось чувство сиротства, брошенности, одиночества, о чем он твердил при всяком случае: Родственники мои не заботились обо мне. Отсюда его робость, ставшая основной чертой его характера. Как все люди, выросшие среди чужих, без отцовского призора и материнского привета, Иван рано усвоил себе привычку ходить оглядываясь и прислушиваясь. Это развило в нем подозрительность, которая с летами превратилась в глубокое недоверие к людям. В детстве ему часто приходилось испытывать равнодушие или пренебрежение со стороны окружающих. Он сам вспоминал после в письме к князю Курбскому, как его с младшим братом Юрием в детстве стесняли во всем, держали как убогих людей, плохо кормили и одевали, ни в чем воли не давали, все заставляли делать насильно и не по возрасту. В торжественные, церемониальные случаи - при выходе или приеме послов - его окружали царственной пышностью, становились вокруг него с раболепным смирением, а в будни те же люди не церемонились с ним, порой баловали, порой дразнили. Его ласкали как государя и оскорбляли как ребенка. Но в обстановке, в какой шло его детство, он не всегда мог тотчас и прямо обнаружить чувство досады или злости, сорвать сердце. Эта необходимость сдерживаться, дуться в рукав, глотать слезы питала в нем раздражительность и затаенное, молчаливое озлобление против людей, злость со стиснутыми зубами. К тому же он был испуган в детстве. В 1542 г., когда правила партия князей Бельских, сторонники князя И. Шуйского ночью врасплох напали на стоявшего за их противников митрополита Иоасафа. Владыка скрылся во дворце великого князя. Мятежники разбили окна у митрополита, бросились за ним во дворец и на рассвете вломились с шумом в спальню маленького государя, разбудили и напугали его. ВЛИЯНИЕ БОЯРСКОГО ПРАВЛЕНИЯ. После его смерти матери Ивана на Руси началось боярское правление. Суть боярского правления 1538-1547гг. в следующем: воспользовавшись тем, что наследнику престола - Ивану (Иоанну)4 Васильевичу было 3 года, власть в стране взяла группировка бояр; был создан регентский совет во главе с матерью Ивана 4 Еленой Глинской; фактическим правителем стал ее фаворит боярин Овчина-Телепнев-Оболенский; после смерти Елены Глинской в 1538году началась ожесточенная борьба за власть между боярами; сложилось два враждебных клана, сгруппировавшихся вокруг боярских родов Шуйских и Бельских; в период борьбы боярских группировок (приходившейся на юность Ивана Грозного) власть великого князя значительно ослабла и стала номинальной. Безобразные сцены боярского своеволия и насилий, среди которых рос Иван, были первыми политическими его впечатлениями. Они превратили его робость в нервную пугливость, из которой с летами развилась наклонность преувеличивать опасность, образовалось то, что называется страхом с великими глазами. Вечно тревожный и подозрительный, Иван рано привык думать, что окружен только врагами, и воспитал в себе печальную наклонность высматривать, как плетется вокруг него бесконечная сеть козней, которою, чудилось ему, стараются опутать его со всех сторон. Это заставляло его постоянно держаться настороже; мысль, что вот-вот из-за угла на него бросится недруг, стала привычным, ежеминутным его ожиданием. Всего сильнее работал в нем инстинкт самосохранения. Все усилия его бойкого ума были обращены на разработку этого грубого чувства. В 1547году по достижении 17 лет Иван IV вступил на престол. Особенностью его прихода к власти было то, что впервые в истории Руси великий князь был венчан на царство и получил титул царя: термин «царь» пришел на Русь от монголо-татар. до падения ига царем называл себя главный хан Золотой Орды; данным титулом золотоордынский царь подчеркивал свою власть над всеми; впервые приняв титул «царь», Иван Грозный показал свою абсолютную суверенность, независимость от всех других властей; в этом шаге была определенная правопреемственность с Византией- монголо-татары заимствовали термин «царь» у византийцев (царь- сокращенный монголами вариант слова «цезарь», а «цезарями» именовали себя императоры Рима и Византии. Московский правитель мог претендовать на титул царя по двум причинам. Во-первых, он формально объявил о своей независимости перед своим прежним сюзереном - монгольским царем. Во-вторых, Византийская империя была разрушена турками, и таким образом, греческий православный мир жил без царя. И к тому же согласно византийской теории «гармонии» церкви и государства христианское общество нуждалось в двух главах - царе и патриархе."
transport = httpx_socks.SyncProxyTransport.from_url('socks5://gPmpmanQ:hYgKstWT@46.151.177.114:63017')
http_client=httpx.Client(transport=transport,headers=headers)
client = OpenAI(api_key=api_key,http_client=http_client)

chat_completion = client.chat.completions.create(
           model="gpt-3.5-turbo-1106",
           response_format={"type":"json_object"},
           messages=[
               {"role": "system","content": "Provide output in valid JSON. The data schema should be like this: "+ json.dumps(example_json)
                },
               {"role":"user","content":data},
               {"role":"user","content":prompt_1+n+prompt_2},
                     ],


       )
data=chat_completion.choices[0].message.content
print(data)
questions=json.loads(data)

for question in questions["questions"]:
    print(question["question"]+"\n|"+question["variant1"]+"|"+question["variant2"]+"|"+question["variant3"]+"|"+question["variant4"]+"|\n", question["answer"])