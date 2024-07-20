# a= {f"play{i}" : f"player{i}" for i in range(1,5)}
# print(a)
# print(a.update({f"over{i}": f"enemy{i}" for i in range(1,10)}))
# print(a)
# a = """
# ﴾code﴿
# print("hello world")
# print("gta")
# a = 3 +3
# ﴾/code﴿
# ﴾img﴿"""

# b = a[a.index("﴾code﴿"):a.index("﴾/code﴿")].replace("﴾code﴿","")
# print(a)
# print(b)
# print("﴾gfhf﴿")
import time
import json
def base10_to_base64(num):
    if num == 0:
        return 'A'
    
    base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    base64_string = ""
    while num > 0:
        remainder = num % 64
        base64_string = base64_chars[remainder] + base64_string
        num = num // 64
    
    return base64_string
def read_the_json():
    with open("data.json", 'r') as file:
        json_var = json.load(file)
    return json_var
def givename():
    info_dict = read_the_json()
    current_time= time.localtime()
    day = current_time.tm_mday
    month = current_time.tm_mon
    year = current_time.tm_year
    firstpart = base10_to_base64(day) + base10_to_base64(month) + base10_to_base64(year)
    projects = 0
    for i in info_dict:
        projects += len(info_dict[i])
    secondpart = str(projects)
    print(secondpart)
    return firstpart + secondpart
print(givename())