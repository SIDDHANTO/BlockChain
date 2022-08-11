# create a blockchain

import hashlib
import datetime
import json
from flask import Flask,jsonify
 
class Blockchain:
    
    #create a block main init function
    def __init__(self):
        self.chain=[]
        self.createBlock(proof=1, previousHash='0') 
    
    #a function to create blcok
    def createBlock(self,proof,previousHash):
        block={'index': len(self.chain)+1,
               'timestap': str(datetime.datetime.now()),
                'proof': proof,
               'previousHash': previousHash}
        self.chain.append(block)
        return block
    
    def getPreviousBlock(self):
        return self.chain[-1]
    
   # here we having the hasing implemmentation in our function
    def proofofWork(self,previousProof):
        newProof=1
        checkProof=False
        while checkProof is False:
            hasOperation=hashlib.sha256(str(newProof**2-previousProof**2).encode()).hexdigest()
            if hasOperation[:4]=='0000':
                checkProof=True
            else:
                newProof+=1
        return newProof
    
    def hash(self, block):
        encodedBlock=json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encodedBlock).hexdigest()
    
    def is_chain_valid(self,chain):
        previousBlock=chain[0]
        block_index=1
        while block_index<len(chain):
            block=chain[block_index]
            if block['previousHash']!=self.hash(previousBlock):
                return False
            previousProof=previousBlock['proof']
            proof=block['proof']
            hasOperation=hashlib.sha256(str(proof**2-previousProof**2).encode()).hexdigest()
            if hasOperation[:4]!='0000':
                return False
            previousBlock=block
            block_index+=1 
        return True
    
    # Mining the  blockChain
        
    #craeting a web app
app=Flask(__name__)
    
    #craeting a blockChain
blockchain = Blockchain()

@app.route('/mine_block', methods=['GET'])


def mine_block():
    previousBlock=blockchain.getPreviousBlock()
    
    previousProof=previousBlock['proof']
    
    proof=blockchain.proofofWork(previousProof)
    
    previousHash=blockchain.hash(previousBlock)
    
    block=blockchain.createBlock(proof, previousHash)
    
    response={'message':'Congratulations, you just mined a block',
              'index':block['index'],
              'timestap':block['timestap'],
              'proof':block['proof'],
              'previousHash':block['previousHash'],
              
        }
    return jsonify(response),200

#getting the full blockchain

@app.route('/get_chain', methods=['GET'])

def get_chain():
    response={
        'chain':blockchain.chain,
        'length':len(blockchain.chain)
        }
    return jsonify(response),200


@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200

app.run(host='0.0.0.0', port=5000)

        
            
            
        

        
        
        
        
        