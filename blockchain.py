# blockchain_oop_images.py
import hashlib
import json
import sys
import os
from datetime import datetime
from pathlib import Path
from response import *
DB_FILE="database.json"

class Block:
    def __init__(self, index, uuid, timestamp, data, previous_hash, nonce, hash=None):
        self.index = index
        self.uuid = uuid
        self.timestamp = timestamp
        self.data = data  # سيحتوي على مسار الملف وهاشه
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = hash if hash is not None else self.compute_hash()

    def compute_hash(self):
        block_data = {
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }
        block_string = json.dumps(block_data, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    def __init__(self, difficulty=2, blockchain_file=DB_FILE):
        self.blockchain_file = blockchain_file
        self.difficulty = difficulty
        self.chain = []
        self.load_chain()

        if not self.chain:
            self._mine_block(None, {"type": "genesis", "message": "Genesis Block"})
            self.save_to_file()

    def load_chain(self):
        try:
            with open(self.blockchain_file, 'r') as f:
                chain_data = json.load(f)
                self.chain = [self._deserialize_block(block) for block in chain_data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.chain = []

    def _deserialize_block(self, block_dict):
        return Block(
            index=block_dict['index'],
            uuid=block_dict['uuid'],
            timestamp=block_dict['timestamp'],
            data=block_dict['data'],
            previous_hash=block_dict['previous_hash'],
            nonce=block_dict['nonce'],
            hash=block_dict['hash']
        )

    def save_to_file(self):
        chain_data = [block.__dict__ for block in self.chain]
        with open(self.blockchain_file, 'w') as f:
            json.dump(chain_data, f, indent=4, default=str)

    def is_valid_proof(self, block):
        return block.hash.startswith('0' * self.difficulty)

    def add_image_contract(self, uuid, image_path):
        """إضافة صورة العقد إلى السلسلة"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"الملف غير موجود: {image_path}")
            
        # حساب هاش الملف
        file_hash = self._calculate_file_hash(image_path)
        
        # تخزين البيانات الأساسية فقط
        contract_data = {
            'type': 'contract_image',
            'file_name': Path(image_path).name,
            'file_path': str(Path(image_path).resolve()),  # تخزين المسار الكامل
            'hash': file_hash
        }
        
        return self._mine_block(uuid, contract_data)

    def _calculate_file_hash(self, file_path):
        """حساب الهاش من محتوى الملف"""
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while chunk := f.read(4096):
                hasher.update(chunk)
        return hasher.hexdigest()

    def _mine_block(self, uuid, data):
        previous_block = self.chain[-1] if self.chain else None
        previous_hash = previous_block.hash if previous_block else '0'
        index = len(self.chain) + 1
        nonce = 0

        while True:
            timestamp = str(datetime.now())
            new_block = Block(
                index=index,
                uuid=uuid,
                timestamp=timestamp,
                data=data,
                previous_hash=previous_hash,
                nonce=nonce
            )
            if self.is_valid_proof(new_block):
                self.chain.append(new_block)
                return new_block
            nonce += 1

    def validate_chain(self):
        if not self.chain:
            return True

        # التحقق من الكتلة التأسيسية
        if self.chain[0].previous_hash != '0' or not self.is_valid_proof(self.chain[0]):
            return False

        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if (
                current.previous_hash != previous.hash
                or not self.is_valid_proof(current)
                or current.hash != current.compute_hash()
            ):
                return False

        return True
    def get_image_info(self, block_index):
        """استرجاع معلومات الصورة من الكتلة"""
        block = self.chain[block_index]
        if block.data.get('type') == 'contract_image':
            return {
                'file_path': block.data['file_path'],
                'file_name': block.data['file_name'],
                'stored_hash': block.data['hash']
            }
        return None

    def verify_image_integrity(self, block_index):
        """التحقق من سلامة الملف المخزن"""
        info = self.get_image_info(block_index)
        if not info:
            return False
            
        current_hash = self._calculate_file_hash(info['file_path'])
        return current_hash == info['stored_hash']
    
    def find_corrupted_block(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if (
                current.previous_hash != previous.hash
                or not self.is_valid_proof(current)
                or current.hash != current.compute_hash()
            ):
                return i  # رقم البلوك الفاسد
        return None  # السلسلة سليمة


if __name__ == '__main__':

    if len(sys.argv) < 2:
        send_not_found("you have to send the rout")
        sys.exit(404)

    route = sys.argv[1]  
    blockchain = Blockchain()

    match route : 
        case 'block_chain_file' :
            try:            
                if len(sys.argv) < 3:
                    send_not_found("you have to send the file_path")
                    sys.exit(400)
                if len(sys.argv) < 4:
                    send_not_found("you have to send the id")
                    sys.exit(400)
                
                file_path = sys.argv[2]
                uuid = sys.argv[3]

                if not blockchain.validate_chain():
                    
                    send_bad_request("the chain is broken")
                    sys.exit(400)

                new_block = blockchain.add_image_contract(uuid, file_path)
                blockchain.save_to_file()
                data = {
                    'hash': new_block.hash,
                    'index': new_block.index ,
                    'file_path': new_block.data['file_path'],
                    'stored_hash': new_block.data['hash']
                }
                send_ok(data)
            except FileNotFoundError as e:
                send_server_error(f"error : {e}")
                sys.exit(500)

        case "block_chain_check":     
            try:        
                if not blockchain.validate_chain():
                    
                    send_bad_request("the chain is broken")
                    sys.exit(400)  
                send_ok()
            except Exception as e:
                send_server_error(f"error : {e}")
                sys.exit(500)
        case _ :
            send_not_found()
         


    