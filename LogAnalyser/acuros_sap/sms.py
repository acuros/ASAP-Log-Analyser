from struct import pack

def send_sms (phone_number, sms_message):
    if phone_number == '':
        return 0
    from socket import AF_INET, SOCK_STREAM, socket
    sms_username = "offera"
    sms_password = "dhvpfkdhvpfk"
    sms_callback = phone_number
    sms_phone = phone_number
    sms_sendtime = "0"# now
    sms_message = sms_message + " " # space for fucking gabia server we don't know why but neccesarry
    data_len = len(("%s%s%s%s%s%s"%(sms_username, sms_password, sms_phone, sms_callback, sms_sendtime, sms_message)).encode('euc-kr'))
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(("sms.gabia.com", 5000))
        s.send(("GS,%d,%s,%s,%s,%s,1,%s,%s"%(data_len, sms_username, sms_password, sms_phone, sms_callback, sms_sendtime, sms_message)).encode('euc-kr')) # send a message
        err_code = s.recv(1024)
        s.close()
        if err_code == '0':
            err_code = 1
        return int(err_code)
    except Exception:
        return 0

def byte_string_from_hex(hstr): 
   byte_array = [] 
        
   if len(hstr) % 2: 
      hstr = '0' + hstr 
        
   for i in range(0, len(hstr)/2): 
      byte_hex = hstr[i*2:i*2+2] 
      byte = int(byte_hex, 16) 
      byte_array.append(byte) 
   return pack('%iB' % len(byte_array), *byte_array) 

def packed_ushort_big_endian(num): 
   return pack('>H', num)
