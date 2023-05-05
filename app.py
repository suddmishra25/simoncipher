from flask import Flask, render_template, request
#import encryption_module #import your python encryption module
from simon_cipher import SimonCipher
import binascii

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def encrypt_decrypt():
    message = request.form.get("message")
    message = bytes(message, 'utf-8')
    str1 = binascii.hexlify(message).decode("utf-8")
    str1 = int(str1,16)
    str1 = str(str1)
    rounds = len(str1)//16 if len(str1)//16 == len(str1)/16 else len(str1)//16 + 1
    
    print("msg type: ",type(str1))
    key = request.form.get("key")
    print(key)
    key = 0x1918111009080100
    print("key type: ",type(key))
    action = request.form.get("action")
    cipher = SimonCipher(key=key, key_size=128, block_size=128, mode='ECB')

    if action == "encrypt":
        
        t1 = ''
        l = []
        zero = []
        for i in range(rounds):
            #print("222",int(str1[i*16:(i+1)*16]))   Blocks of Size 128
            t = cipher.encrypt(int(str1[i*16:(i+1)*16]))
            t1 = t1 + str(t)
            l.append(len(str(t)))
            zero.append(len(str1[i*16:(i+1)*16])- len(str(int(str1[i*16:(i+1)*16]))))
        print(t1)
        print("l",l)
        result1 = t1
  
        fl = ''
        sm = 0
        for i in range(rounds):    
            z = cipher.decrypt(int(t1[sm:sm+l[i]]))
            #print("111",z)
            temp = '0'*zero[i]
            fl = fl + temp + str(z)
            sm += l[i]
        #print(fl)
        #print(fl)  #Decrpted Intger Format
        fl = hex(int(fl))
        #print(fl)  #Decrpted Hex Format
        z1 = binascii.unhexlify(fl[2:])
        print(z1) 
        result2 = str(z1)
    return render_template("index.html", result1=result1,result2=result2)

if __name__ == "__main__":
    app.run(debug=True)