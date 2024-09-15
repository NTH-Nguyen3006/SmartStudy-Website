import json, threading

# from .SmartStudy import centre
from fbapy import *
# from .SmartStudy.Plugin import commands

with open(r"SSApp\SmartStudy\Json\data.json", mode="r", encoding="utf8") as fi:
    appstate = json.load(fi)["APPSTATE"]

client = Client()
# docs tại https://github.com/RFS-ADRENO/fbapy/blob/main/DOCS.md
api = client.login(
    appstate = appstate,
    options={
        "user_agent": "Mozilla/5.0 (Linux; Android 9; SM-G973U Build/PPR1.180610.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36",
        "online": True,
        "update_presence": True
    },
)

def Reply(text, thread_id, message_id):
    # api.http.read_status(thread_id, True)
    api.send_message(text=text, thread_id=thread_id, message_id=message_id)

def change_emoji(thread_id, message_id, emoji):
    api.http.change_emoji(emoji=emoji, thread_id=thread_id)
     

def Callback(event, api):
    try:
        print("đây là " ,event)
        pass
        # if "message" in event["type"]:
        #     api.http.read_status(event["thread_id"], True)
        #     threading.Thread(target=centre.centre, args=(event,)).start()

        # if "message" in event["type"]:
        #     if not event["is_group"]:
        #         api.http.read_status(event["thread_id"], True)
        #         # centre.centre(data_event=event)
        #         threading.Thread(target=centre.centre, args=(event,)).start()

            else:
                # if event["args"][0].lower() == ".ai":
                #     api.http.read_status(event["thread_id"], True)
                #     event["body"] = ' '.join(event["args"][1:])
                #     threading.Thread(target=centre.centre, args=(event,)).start()
                
                if event["args"][0].lower() == ".change":
                    api.http.read_status(event["thread_id"], True)
                    api.http.change_emoji(emoji=event["args"][1], thread_id=event["thread_id"])

                # elif commands.get(event["args"][0].lower()): 
                #     api.http.read_status(event["thread_id"], True)
                #     threading.Thread(target=centre.centre, args=(event,)).start()
    
    except Exception as e:
        print(e)


def listen():
    api.listen_mqtt(callback=Callback)

# api.listen_mqtt(callback=Callback)

# threading.Thread(target=api.listen_mqtt, args=(Callback,)).start()


