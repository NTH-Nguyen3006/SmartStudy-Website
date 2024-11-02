def toBinary(dataInput: str|int) -> str:
		number = int(dataInput) if (dataInput.isdigit()) else None
		if number: # nếu như là số thì xét
			"""
			* thuật toán 
			while number > 0:
				surplus = number % 2  # số dư
				strBinary = str(surplus) + strBinary
				number //= 2 
			return strBinary """

			return format(number, "b")

		else:
			strBinary = ""
			for char in dataInput:
				ascii_char = ord(char)
				strBinary += f'{format(ascii_char, "b")} '
			return strBinary.strip()
		
# return binary -> number
def binary_toNumber(binary:str) -> str | None:
    try:
        strNums = ''
        for binary in binary.split():
            strNums += f'{int(binary, 2)} '
        return strNums or None
    except: 
        return

# return binary -> text
def binary_toText(binary:str) -> str|None:
    strNums = binary_toNumber(binary)
    
    if not strNums: 
        return
    
    strChar = ''
    for num in strNums.split():
        strChar += chr(int(num))
    return strChar


