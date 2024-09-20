RomanNumerals: dict = { 1000: 'M',      900: 'CM',      500: 'D',   
              400: 'CD',      100: 'C',       90: 'XC',
              50: 'L',        40: 'XL',       10: 'X',
              9: 'IX',        5: 'V',         4: 'IV',
              1: 'I'}

# num -> roman
def Num_toRoman(number:str) -> str | None :
    if int(number) > 10**6:
        return "Vui lòng nhập số nhỏ hơn 1 000 000"
    number = int(number) if str(number).isdigit() else None
    if number:
        roman = ''  
        for value, num in RomanNumerals.items():
            count = number // value 
            roman += num * count 
            number -= (count * value)
        return roman
    return
	
# return roman -> num
def Roman_toNum(roman:str) -> int | None:
    try:
        integer = 0
        strRoman = str(roman)
        for value, numeral in RomanNumerals.items():
            while strRoman.startswith(numeral):
                integer += value
                strRoman = strRoman[len(numeral):]
        return integer if integer != 0 else None
    except:
        return "Lỗi nhập vào !"