from flask import Flask
from flask import request,jsonify
from mnemonic import Mnemonic
import pexpect

app = Flask(__name__)

@app.route("/account")

def getaddress():  

    index = request.args.get('index')
    seed = request.args.get('seed')
    
    child = pexpect.spawn ('solana-keygen pubkey prompt://?key={}/0'.format(index))
    child.expect ('seed phrase:')
    child.sendline (seed)
    child.expect('press ENTER to continue:')
    child.sendline('\n')
    temp = str(child.read())
    stemp = temp.replace("b' \\r\\n\\r\\n","")
    rtemp = stemp.replace("\\r\\n'","")            
    child.interact()

    address = jsonify({        
        "address": rtemp
        })        
    
    return address

       

@app.route("/create")

def create():
    mnemo = Mnemonic("english")
    words = mnemo.generate(strength=256)

    seed = jsonify({        
        "seedphrase": words
        })  

    return seed

 

if __name__ == "__main__":
    app.run()
