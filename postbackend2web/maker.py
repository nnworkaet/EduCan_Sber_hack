from main import make_termins,make_test,make_summarize
#from whisper_new.faster_whisp import audio_to_text
#from whisper_old.whisper_txt import texter as audio_to_text
from speech2textmodule import texter as audio_to_text
from request2serv import req
from txt_processing.pre.pre_text import start_text_processing as text_processing
from txt_processing.past import summarization_processing,termins_processing,test_processing
from main import make_termins,make_test,make_summarize
from docers.docser import txt2docx
def req_trans(identity,audio_path):
    txt = audio_to_text(audio_path)
    txt_time=txt[0]
    print(txt_time)
    txt_def=txt[1]
    txt_time = str(txt_time)
    txt_def = ' '.join(txt_def)
    print("=========")
    print(identity,txt_def,txt_time)
    req.trans2serv(identity,txt_def,txt_time)

def req_termins(identity,txt):
    txt = str(make_termins(txt)).replace("'", '"')
    req.glos2serv(identity,txt)

def req_test(identity,txt):

    txt = str(make_test(txt)).replace("'",'"')
    req.test2serv(identity,txt)

def req_sum(identity,txt):

    txt = str(make_summarize(txt))
    name= txt2docx(txt)
    req.sum2serv(identity,txt,name)

