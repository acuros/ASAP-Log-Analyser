    # -*-coding: utf8-*-
import ssl, json, datetime
from socket import socket
from struct import pack
from django.conf import settings


def send_push (content, device_token_list, arguments={}):
    for device_token in device_token_list:
        if device_token == None:
            continue
        payload = dict(aps=dict(alert=content, badge=1, sound='bingbong.aiff'))
        for key, value in arguments.iteritems():
            payload[key] = value
        payload = json.dumps(payload)
     
        device_token = byte_string_from_hex(device_token)
        device_token_length_bin = packed_ushort_big_endian(len(device_token))
        payload_length_bin = packed_ushort_big_endian(len(payload))
     
        packet = ('\0' + device_token_length_bin + device_token + payload_length_bin + payload)    
        try:
            _socket = socket()
            conn = ssl.wrap_socket(_socket, ssl_version=ssl.PROTOCOL_SSLv3, certfile=settings.PROJECT_PATH+'/apns.pem')
            conn.connect(('gateway.sandbox.push.apple.com', 2195))
            conn.write(packet)
            conn.close()
            _socket.close()
        except Exception, error_message:
            from django.core.mail import EmailMessage
            EmailMessage("Push 실패", "%s<br />%s"%(str(datetime.datetime.now()), error_message), "push_failed@aimovement.co.kr", ["ksy567890@gmail.com"])

def send_push_test_with_token (content, device_token):
    if len(device_token) != 64: 
        pass
    payload = dict(aps=dict(alert=content, badge=1, sound='bingbong.aiff'))
    payload = json.dumps(payload)
 
    device_token = byte_string_from_hex(device_token)
    device_token_length_bin = packed_ushort_big_endian(len(device_token))
    payload_length_bin = packed_ushort_big_endian(len(payload))
 
    packet = ('\0' + device_token_length_bin + device_token + payload_length_bin + payload)    
    try:
        _socket = socket()
        conn = ssl.wrap_socket(_socket, ssl_version=ssl.PROTOCOL_SSLv3, certfile=settings.PROJECT_PATH+'/apns.pem')
        conn.connect(('gateway.sandbox.push.apple.com', 2195))
        conn.write(packet)
        conn.read()
        conn.close()
        _socket.close()
    except Exception, error_message:
        from django.core.mail import EmailMessage
        EmailMessage("Push 실패", "%s<br />%s"%(str(datetime.datetime.now()), error_message), "push_failed@aimovement.co.kr", "ksy567890@gmail.com")


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
