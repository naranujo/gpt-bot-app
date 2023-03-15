from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

import datetime as dt

import openai
from twilio.rest import Client

account_sid = 'ACe53c89f870e6e888ae8288898354fd3e'
auth_token = 'eeae36ef14bf7d55fdf10ae5b3d0cfe8'
client = Client(account_sid, auth_token)
openai.api_key = "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"

def save_qaa(dict):
    flag:bool = True
    try:
        with open('qaa.csv', 'r', encoding="utf-8") as f:
            f.read()
            f.close()

        flag = False
    except:
        flag = True


    if flag == True:
        with open('myApp/qaa.csv', 'wt', encoding="utf-8") as f:
            f.write(f'"Date Time"\t"Question"\t"Answer"\n')
            f.close()

    with open('myApp/qaa.csv', 'a', encoding="utf-8") as f:
        for key,value in dict.items():
            f.write(f'"{dt.datetime.now().strftime("%Y-%b-%d %H:%M:%S")}"\t"{key}"\t"{value}"\n')
        f.close()
    return 200

@csrf_exempt
def post_json(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=data['q'],
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        res_string = response.choices[0].text.strip()

        msg = client.messages.create(
            from_ = 'whatsapp:+14155238886',
            to = "whatsapp:+5491135646079",
            body=res_string,
        )
        print("SID:",msg.sid)
        
        print(save_qaa({f"{data['q']}": f"{res_string}"}))
        return JsonResponse({f"{data['q']}": f"{res_string}"}, status=200)
    else:
        response_data = {
            'message': 'Esta vista solo admite solicitudes POST'
        }
        return JsonResponse(response_data, status=405)


def index(request):
    return HttpResponse("¡Hola, mundo!")
