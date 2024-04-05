import requests
import random
def recognition_of_insults(mes): 
    # Функция для распознования оскорблений 
    # возвращает True, если есть оскорбления
    # и False, если оскорбления не обнаружено 
    try:
        API_URL = 'https://7032.deeppavlov.ai/model'
        data = {"x": [ mes ]}
        res = requests.post(API_URL, json=data).json()
        res = True if res[0][0] == 'insult' else False
    except:
        res = False
    return res

"https://7031.deeppavlov.ai/model"

emotions = {
'joy':['Я рад, что ты рад'],
'sadness':['Не грусти, а то сиси не будут расти'],
'anger':[' быть злым не круто'],
'surprise':['Вау я тоже в шоке'],
'fear':['Не боись я с тобой!']
}
def get_emotion(mes): 
    # Функция для распознования оскорблений 
    # возвращает True, если есть оскорбления
    # и False, если оскорбления не обнаружено 
    try:
        API_URL = 'https://7031.deeppavlov.ai/model'
        data = {"x": [ mes ]}
        res = requests.post(API_URL, json=data).json()
        print(mes, res)
        res = random.choice(emotions[res[0][0]])
            
    except:
        res = 'Ничего не могу сказать'
    return res

