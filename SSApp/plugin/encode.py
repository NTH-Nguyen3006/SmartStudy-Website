from random import choice, randint, shuffle

strings = "abcdefghijklmnopqrstuvwxyz0123456789"  # ne pas changer svp
base = 99999  # ne pas changer svp

class Kyrie():
    def encrypt(e: str):
        e = Kyrie._ekyrie(e)
        return Kyrie._encrypt(e)

    def decrypt(e: str):
        text = Kyrie._decrypt(e)
        return Kyrie._dkyrie(text)

    def _ekyrie(text: str):
        r = ""
        for a in text:
            if a in strings:
                a = strings[strings.index(a)-1]
            r += a
        return r

    def _dkyrie(text: str):
        r = ""
        for a in text:
            if a in strings:
                i = strings.index(a)+1
                if i >= len(strings):
                    i = 0
                a = strings[i]
            r += a
        return r

    def _encrypt(text: str, key: str = None):
        if key is None:
            key = base
        if type(key) == str:
            key = sum(ord(i) for i in key)
        t = [chr(ord(t)+key)if t != "\n" else "ζ" for t in text]
        return "".join(t)

    def _decrypt(text: str, key: str = None):
        if key is None:
            key = base
        if type(key) == str:
            key = sum(ord(i) for i in key)
        return "".join(chr(ord(t)-key) if t != "ζ" else "\n" for t in text)


class Key:
    def encrypt(e: str, key: str):
        e1 = Kyrie._ekyrie(e)
        return Kyrie._encrypt(e1, key=key)

    def decrypt(e: str, key: str):
        text = Kyrie._decrypt(e, key=key)
        return Kyrie._dkyrie(text)



def berserk(content: str) -> str:
    key = randint(3,10000)
    _content_ = Key.encrypt(content, key=10)

    _lines_sep_, _spaces_sep_ = choice(list("~|-/=")), choice(list("¤§^*¨"))

    _hey_num_ = randint(69, 356)
    _hey_num_ = len(content)

    content = _lines_sep_.join(str(ord(x)+_hey_num_) if x != 'ζ' else _spaces_sep_ for x in _content_)

    _names_ = ["_eval", "_exec", "_byte", "_bytes", "_bit", "_bits", "_system", "_encode", "_decode", "_delete", "_exit", "_rasputin", "_boom"]
    _names_ = ["self." + name for name in _names_]
    shuffle(_names_)

    for k in range(12):
        globals()[f'n_{str(k+1)}'] = _names_[k]

    _ran_int_ = _hey_num_
    while _ran_int_ == _hey_num_:
        _ran_int_ = str(randint(69, 356))
    
    _types_ = ("str","float","bool","int")

    def _find(chars: str): 
        return "+".join(f"_n7_[{list('abcdefghijklmnopqrstuvwxyz0123456789').index(c)}]" for c in chars)

    _1_ = fr"""_n5_""",fr"""lambda _n9_:"".join(chr(int(_n10_)-len(_n9_.split('{_lines_sep_}')))if _n10_!='{_spaces_sep_}'else'ζ'for _n10_ in str(_n9_).split('{_lines_sep_}'))"""
    _2_ = fr"""_n6_""",r"""lambda _n1_:str(_n4_[_n2_](f"{_n7_[4]+_n7_[-13]+_n7_[4]+_n7_[2]}(''.join(%s),{_n7_[6]+_n7_[11]+_n7_[14]+_n7_[1]+_n7_[0]+_n7_[11]+_n7_[18]}())"%list(_n1_))).encode(_n7_[20]+_n7_[19]+_n7_[5]+_n7_[34])if _n4_[_n2_]==eval else exit()"""
    _3_ = fr"""_n4_[_n2_]""",fr"""eval"""
    _4_ = fr"""_n1_""",fr"""lambda _n1_:exit()if _n7_[15]+_n7_[17]+_n7_[8]+_n7_[13]+_n7_[19] in open(__file__, errors=_n7_[8]+_n7_[6]+_n7_[13]+_n7_[14]+_n7_[17]+_n7_[4]).read() or _n7_[8]+_n7_[13]+_n7_[15]+_n7_[20]+_n7_[19] in open(__file__, errors=_n7_[8]+_n7_[6]+_n7_[13]+_n7_[14]+_n7_[17]+_n7_[4]).read()else"".join(_n1_ if _n1_ not in _n7_ else _n7_[_n7_.index(_n1_)+1 if _n7_.index(_n1_)+1<len(_n7_)else 0]for _n1_ in "".join(chr(ord(t)-{key})if t!="ζ"else"\n"for t in _n5_(_n1_)))"""
    _5_ = fr"""_n7_""",fr"""exit()if _n1_ else'abcdefghijklmnopqrstuvwxyz0123456789'"""
    _6_ = fr"""_n8_""",fr"""lambda _n12_:_n1_(_n12_)"""
    _all_ = [_1_, _2_, _3_, _4_, _5_, _6_]
   
    shuffle(_all_)

    _vars_content_ = ",".join(s[0] for s in _all_)
    _valors_content_ = ",".join(s[1] for s in _all_)
    _vars_ = _vars_content_ + "=" + _valors_content_
    _final_content_ = fr"""class SmartStudy_Encode():
    def __init__(self, _n1_:{choice(_types_)}=False, _n2_:{choice(_types_)}=0, *_n3_:{choice(_types_)}, **_n4_:{choice(_types_)}) -> exec:
        {_vars_}
        return self.__decode__(_n4_[(_n7_[-1]+'_')[-1]+_n7_[18]+_n7_[15]+_n7_[0]+_n7_[17]+_n7_[10]+_n7_[11]+_n7_[4]])
    
    def __decode__(self,_execute: str) -> exec: 
        return(None, _n6_(_n8_(_execute)))[0]

SmartStudy_Encode(
    _n1_=False, 
    _sparkle='''{content}''')""".strip().replace("_n1_",n_1.removeprefix("self.")).replace("_n2_",n_2.removeprefix("self.")).replace("_n3_",n_3.removeprefix("self.")).replace("_n4_",n_4.removeprefix("self.")).replace("_n5_",n_5).replace("_n6_",n_6).replace("_n7_",n_7).replace("_n8_",n_8).replace("_n9_",n_9.removeprefix("self.")).replace("_n10_",n_10.removeprefix("self.")).replace("_n12_",n_12.removeprefix("self."))

    return _final_content_


def decode(encoded_content: str) -> str:
    # Tìm lớp và hàm chứa mã được mã hóa (bạn cần điều chỉnh phần này cho phù hợp với mã của bạn)
    class_name = "SmartStudy_Encode"
    function_name = "__decode__"

    # Tách chuỗi mã hóa (bạn cần điều chỉnh phần này cho phù hợp với cách mã hóa của bạn)
    # ...

    # Giải mã các số nguyên, hợp nhất các ký tự, giải mã các lớp và hàm
    # ...

    # Giải mã nội dung
    decoded_content = Key.decrypt(encoded_content, key=10)  # Bạn cần tìm cách xác định khóa

    return decoded_content


def encodePython(contentCodePython: str) -> str | None:
    try:
        content = f"{contentCodePython}"
        Encode = berserk(content=content)
        return Encode
    
    except Exception as e:
        import traceback, sys
        name_error = str(sys.exc_info()[1])
        tb = sys.exc_info()[2]
        line_number = traceback.extract_tb(tb)[-1][1]
        print(
            f"""
    Tên Lỗi: {name_error}
    Tên file: {__name__} | Vị trí: dòng thứ {line_number}
    """)
        return
    
print(decode(
"""
class SmaartStudy_Encode():
    def __init__(self, _delete:int=False, _rasputin:str=0, *_system:str, **_boom:int) -> exec:
        self._byte,self._bytes,_boom[_rasputin],self._encode,_delete,self._eval=lambda _exit:"".join(chr(int(_exec)-len(_exit.split('/')))if _exec!='¤'else'ζ'for _exec in str(_exit).split('/')),lambda _delete:str(_boom[_rasputin](f"{self._encode[4]+self._encode[-13]+self._encode[4]+self._encode[2]}(''.join(%s),{self._encode[6]+self._encode[11]+self._encode[14]+self._encode[1]+self._encode[0]+self._encode[11]+self._encode[18]}())"%list(_delete))).encode(self._encode[20]+self._encode[19]+self._encode[5]+self._encode[34])if _boom[_rasputin]==eval else exit(),eval,exit()if _delete else'abcdefghijklmnopqrstuvwxyz0123456789',lambda _delete:exit()if self._encode[15]+self._encode[17]+self._encode[8]+self._encode[13]+self._encode[19] in open(__file__, errors=self._encode[8]+self._encode[6]+self._encode[13]+self._encode[14]+self._encode[17]+self._encode[4]).read() or self._encode[8]+self._encode[13]+self._encode[15]+self._encode[20]+self._encode[19] in open(__file__, errors=self._encode[8]+self._encode[6]+self._encode[13]+self._encode[14]+self._encode[17]+self._encode[4]).read()else"".join(_delete if _delete not in self._encode else self._encode[self._encode.index(_delete)+1 if self._encode.index(_delete)+1<len(self._encode)else 0]for _delete in "".join(chr(ord(t)-5995)if t!="ζ"else"\n"for t in self._byte(_delete))),lambda _decode:_delete(_decode)
        return self.__decode__(_boom[(self._encode[-1]+'_')[-1]+self._encode[18]+self._encode[15]+self._encode[0]+self._encode[17]+self._encode[10]+self._encode[11]+self._encode[4]])

    def __decode__(self,_execute: str) -> exec:
        return(None, self._bytes(self._eval(_execute)))[0]

SmaartStudy_Encode(
    _delete=False,
    _sparkle='''129/131/122/127/133/58/66/59''')    
"""
))