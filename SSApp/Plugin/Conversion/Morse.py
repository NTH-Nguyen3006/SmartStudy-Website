# from ...Sundry import Json

# Morses = Json().load("SSApp\SmartStudy\Json\data.json")["Morses"]

Morses = {
	"a": ".-",  "b": "-...", "c": "-.-.", "d": "-..", "e": ".", "f": "..-.", "g": "--.", "h": "....", "i": "..", "j": ".---", "k": "-.-", "l": ".-..", "m": "--", "n": "-.", "o": "---", "p": ".--.", "q": "--.-", "r": ".-.", "s": "...", "t": "-", "u": "..-", "v": "...-", "w": ".--", "x": "-..-", "y": "-.--", "z": "--..",

	"0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.",
	
	".": ".-.-.-", ",": "--..--", "?": "..--..", "'": ".----.", "!": "-.-.--", "/": "-..-.", "(": "-.--.", ")": "-.--.-", "&": ".-...", ":": "---...", ";": "-.-.-.", "=": "-...-", "+": ".-.-.", "-": "-....-", "_": "..--.-", "``": ".-..-.", "$": "...-..-", "@": ".--.-.", "¿": "..-.-", "¡": "--...-", " ": "/"
}

def allMorse() -> str:
	strMorse = ""
	for key, value in Morses.items():
		strMorse += f'" {key.upper()} " : {value}\n'
		if key == "/":
			strMorse += '(với khoảng trắng là: " / ")'
	return strMorse

# text to morse
def Text_toMorse(textInput:str) -> str:
	from unidecode import unidecode
	# chuyển sang chữ thường không dấu
	text = unidecode(textInput).lower() 
	strMorse = ""
	for char in text:
		morse = Morses.get(char)
		if not morse:
			return f'Kí tự " {char} " không có trong bảng mã Morse'
		strMorse += morse + " "
	return strMorse

# morse to text
def Morse_toText(morseInput: str) -> str:
	result = ""
	for morse in morseInput.split():
		for char in Morses: 
			if morse in Morses.values():
				if Morses.get(char) == morse:
					result += char
			else:
				return
	return result.upper()