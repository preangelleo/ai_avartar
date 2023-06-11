from c101variables import *

current_file = 'c101format.py'

def debuging(file_name, func_name, status, result='', debug=False):
    if debug:
        print(f"{file_name} : {func_name}() : {status} : {result}")
    return

def round_value(input_value):
    if input_value > 100:
        a = int(input_value)
        return a
    elif input_value > 1:
        a = round(input_value, 2)
        return a
    elif input_value > 0.01:
        a = round(input_value, 4)
        return a
    elif input_value > 0.0001:
        a = round(input_value, 6)
        return a
    else:
        a = round(input_value, 8)
        return a

def format_eth(eth_address, token='wallet'):
    eth_address_list = re.findall(r'0[xX][a-zA-Z0-9]{40}?', eth_address)
    if not eth_address_list:
        return eth_address
    eth_address = eth_address_list[0]
    start = ''.join(eth_address[:6])
    end = ''.join(eth_address[-4:])
    ellipsis_eth = start + "......" + end
    if token.upper() == 'WALLET':
        base_url = "https://debank.com/profile/"
        formated_eth = f"[{ellipsis_eth}]({base_url}{eth_address})"
    else:
        base_url = "https://etherscan.io/token/"
        formated_eth = f"[{ellipsis_eth}]({base_url}{eth_address})"
    return formated_eth

# eth_address = "0xb411B974c0ac75C88E5039ea0bf63a84aa7B5377"
# print(format_eth(eth_address, 'token'))


def format_bep(eth_address, token='wallet'):
    eth_address_list = re.findall(r'0[xX][a-zA-Z0-9]{40}?', eth_address)
    if not eth_address_list:
        return eth_address
    eth_address = eth_address_list[0]
    # print("eth_split: ", eth_address)
    start = ''.join(eth_address[:6])
    end = ''.join(eth_address[-4:])
    ellipsis_eth = start + "......" + end
    if token.upper() == 'WALLET':
        base_url = "https://debank.com/profile/"
        formated_eth = f"[{ellipsis_eth}]({base_url}{eth_address})"
    else:
        base_url = "https://bscscan.com/token/"
        formated_eth = f"[{ellipsis_eth}]({base_url}{eth_address})"
    return formated_eth


def format_short_url(link_core, base_url):
    start = ''.join(base_url[:8])
    end = ''.join(link_core[-4:])
    ellipsis_link = start + "......" + end
    formated_link = f"[{ellipsis_link}]({base_url}{link_core})"
    return formated_link


def format_mnemonic(mnemonic, debug=False):
    current_function = format_mnemonic.__name__
    started = datetime.now()
    debuging(current_file, current_function, 'started', result=started, debug=debug)
    start = mnemonic.split()[0]
    end = mnemonic.split()[-1]
    elps_mnemonic = start + "......" + end
    debuging(current_file, current_function, 'ellipsised', result=elps_mnemonic, debug=debug)
    return elps_mnemonic

def format_pvk(pvk, debug=False):
    current_function = format_pvk.__name__
    started = datetime.now()
    debuging(current_file, current_function, 'started', result=started, debug=debug)
    start = ''.join(pvk[:6])
    end = ''.join(pvk[-4:])
    ellipsis_pvk = start + "......" + end
    debuging(current_file, current_function, 'ellipsised', result=ellipsis_pvk, debug=debug)
    return ellipsis_pvk


def format_reply(dict_obj):
    r = '\n'.join("{}:\t {}".format(k, v) for k, v in dict_obj.items())
    return r

def format_reply_for_streamlit(dict_obj):
    r = '\n\n'.join("{}:\t {}".format(k, v) for k, v in dict_obj.items())
    return r

def format_reply_include_eth_address_with_elippis(dict_obj):
    r = '\n'.join(f"{k}:\t {v[:6] + '....' + v[-5:] if len(str(v)) >= 42 else v}" for k, v in dict_obj.items())
    return r


def format_reply_delete_null(dict_obj):
    for k, v in dict_obj.items():
        if not v:
            del(k)
    r = '\n'.join("{}:\t {}".format(k, v) for k, v in dict_obj.items())
    return r


def format_list_reply(list_str):
    r = '\n'.join("{}".format(l) for l in list_str)
    return r

def format_list_reply_for_streamlit(list_str):
    r = '\n\n'.join("{}".format(l) for l in list_str)
    return r

def format_list_reply_coma(list_str):
    r = ', '.join("{}".format(l) for l in list_str)
    return r


def format_list_reply_delete_usdt_suffix(list_str):
    r = ', '.join("{}".format(l[:-4]) for l in list_str)
    return r


def format_list_index_reply(list_str):
    r_list = []
    # r = '\n'.join("{}".format(l) for l in list_str)
    for i in range(len(list_str)):
        ri = f"{i}:\t {list_str[i]}"
        r_list.append(ri)
    r = '\n'.join("{}".format(l) for l in r_list)
    return r


def format_list_ellipsis_address_reply(list_str):
    r = '\n'.join(f"- {l[:6]}......{l[-4:]}" for l in list_str)
    return r


def format_list_address_reply(list_str):
    r = '\n'.join(f"- {l}" for l in list_str)
    return r


def format_number(num):
    if not num:
        return 0
    if type(num) is dict:
        print(num)
        return 0
    if type(num) is not str and not float and not int:
        return num
    if type(num) is str:
        try:
            num = float(num)
        except Exception as e:
            return num
    positive = 1 if num >= 0 else -1
    num = abs(num)
    if num >= 1000:
        num = int(num)
        num = num * positive
        num = format(num, ',')
        return num
    if num >= 100:
        num = int(num)
        return num * positive
    if num >= 1:
        num = round(num, 2)
        return num * positive
    if num < 0.0001:
        print("no_need_to_change: ", num)
        return num * positive
    if num < 1:
        after_0_num = str(num).split('.')[-1]
        list_number = list(after_0_num)
        for i in range(len(list_number)):
            if int(list_number[i]) != 0:
                zero_num = i
                break
        num = round(num, zero_num + 3)
        return num * positive


def format_big_number(num):
    if not num:
        return 0
    if type(num) is dict:
        print(num)
        return 0
    if type(num) is not str and not float and not int:
        return num
    if type(num) is str:
        try:
            num = float(num)
        except Exception as e:
            return num
    positive = 1 if num >= 0 else -1
    num = abs(num)
    if num >= 1000000000000:
        num = round((num / 1000000000000), 1)
        num = num * positive
        num = str(num)+' T'
    if num >= 1000000000:
        num = round((num / 1000000000), 1)
        num = num * positive
        num = str(num)+' B'
        return num
    if num >= 1000000:
        num = round((num / 1000000), 1)
        num = num * positive
        num = str(num)+' M'
        return num
    if num >= 1000:
        num = round((num / 1000), 2)
        num = num * positive
        num = str(num)+' K'
        return num
    if num >= 100:
        num = int(num)
        return num * positive
    if num >= 1:
        num = round(num, 2)
        return num * positive
    if num < 0.0001:
        print("no_need_to_change: ", num)
        return num * positive
    if num < 1:
        after_0_num = str(num).split('.')[-1]
        list_number = list(after_0_num)
        for i in range(len(list_number)):
            if int(list_number[i]) != 0:
                zero_num = i
                break
        num = round(num, zero_num + 3)
        return num * positive

def format_decimals_wei_number(big_number, decimals=18):
    std_number = big_number / (10 ** decimals)
    return format_big_number(std_number)

def format_reply_with_number(dict_obj):
    r = '\n'.join("{}:\t {}".format('- ' + k, format_number(v)) for k, v in dict_obj.items())
    return r


def format_reply_with_percent_number(dict_obj):
    r = '\n'.join("{}:\t {}".format('- ' + k, str(round(v, 2))+'%') for k, v in dict_obj.items())
    return r


def format_reply_positions(dict_obj):
    r = '\n'.join("{}:\t {}".format(k, format_number(v)) for k, v in dict_obj.items())
    return r


def format_dict(**kwargs):
    for k, v in kwargs.items():
        try:
            v = format_number(kwargs[k])
            kwargs[k] = v
        except Exception as e:
            print(k)
            print(e)
            continue
    return kwargs

# kwargs = {
#   "asset": "ETH",
#   "free": 50.80041394,
#   "locked": 0.000114555,
#   "total": -50.80041394,
#   "premium": -1594.078617941396,
#   "price_change": -0.0002709617305389589,
# }

# res = format_dict(**kwargs)
# print(format_reply(res))

def format_str_elippsis(from_address):
    address = from_address[:8]+'....'+from_address[-5:] if len(from_address) > 15 else from_address
    return address


def format_list_reply_with_type(list_str):
    r = '\n'.join(f"- {type(l)} : {l}" for l in list_str)
    return r


if __name__ == '__main__':
    print(f"{current_file} is running...")

