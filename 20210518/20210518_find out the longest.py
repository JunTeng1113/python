import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "192.168.220.133"
port = 80
s.connect((ip, port))

data = "email=c109156127@nkust.edu.tw&password=1234\r\n"

header = ("""
POST /test_get.php HTTP/1.1
Host: 192.168.220.133
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7
Accept-Encoding: gzip, deflate
Referer: http://google.com
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
""")

contentLength = "Content-Length: " + str(len(data)) + "\r\n"
request = header + contentLength + data
s.send(request)
print(s.recv(4096).decode('utf-8'))
s.close
