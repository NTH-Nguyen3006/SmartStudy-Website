import requests, random
# from ...Action import sendMessage, sendMedia
# from ...Sundry import Json

gooey_api_key = "sk-MbIlEcg4CzUFATNkYGzfbyJmljFg5W277JyjcMIv7ThCwqSr"

def qr_clear(sender_id, message_text):
    from urllib.parse import quote
    sendMessage(sender_id, "Vui lòng đợi trong giấy lát...")
    data = quote(message_text)
    urlIMG = f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={data}"
    sendMedia(
        sender_id, "image",
        urlIMG
    )
    sendMessage(send_to_id=sender_id, message_text=urlIMG)
    

def AI_art_QR(sender_id, message_text, prompt=None):
    # sendMessage(sender_id, "Xin đợi tôi trong vòng 15-30 giây...")
    list_seed = [4268277630, 1858283311, 1599532306, 1355020499, 1848776043, 843891565, 440482501, 3223249209, 4072185744, 2746317213, 3009170676, 679178490]
    payload = {
        "qr_code_data": message_text,
        "qr_code_input_image": None,
        "use_url_shortener": False,
        "text_prompt": "technology 3D, 8k, UHD" if (not prompt) else prompt,
        "negative_prompt": "ugly, disfigured, low quality, blurry, nsfw, text, words",
        "selected_model": "dream_shaper",
        "selected_controlnet_model": ["sd_controlnet_brightness", "sd_controlnet_tile"],
        "output_width": 512,
        "output_height": 512,
        "guidance_scale": 10,
        "controlnet_conditioning_scale": [0.4, 0.4],
        "num_outputs": 1,
        "quality": random.randint(100, 200),
        "scheduler": "euler_ancestral",
        "seed": random.choice(list_seed),
        "obj_scale": 0.65,
        "obj_pos_x": 0.5,
        "obj_pos_y": 0.5,
    }
    response = requests.post(
        "https://api.gooey.ai/v2/art-qr-code/",
        headers={"Authorization": "Bearer " + gooey_api_key},
        json=payload,
    )
    assert response.ok, response.content
    result = response.json()
    sendMedia(sender_id, "image", result["output"]["output_images"][0])
    sendMessage(sender_id, "Xin lỗi đã để bạn đợi 🥺.")
  
    if result.get("detail"):
        print("Error qr status:", response.status_code)
        sendMessage(sender_id, "Có vẻ có lỗi nên tạo QR Code không thành công, dùng lệnh .erorr <nội dung> để báo với admin")

# tạo prompt cho QR Code
def Prompt_QR_Code(sender_id, prompt):
    accounts = Json().load("Json/accounts.json") or {}
    if prompt.lower() == "not":
        prompt = None
    dataQR_Text = " ".join(accounts[sender_id].split()[1:])

    AI_art_QR(sender_id, dataQR_Text, prompt=prompt)
    accounts[sender_id] = "creat qr complete!"
    tools = Json().load("Json/tools.json") or {}
    tools["Creating_QR"].remove(sender_id)
    Json().save("Json/tools.json", tools)
    
    