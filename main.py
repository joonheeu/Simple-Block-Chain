import hashlib
import time
from datetime import datetime

class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=0):
        # 블록의 초기 속성을 설정합니다.
        self.index = index  # 블록의 번호 (블록체인에서의 위치)
        self.previous_hash = previous_hash  # 이전 블록의 해시 값
        self.timestamp = timestamp  # 블록이 생성된 시간
        self.data = data  # 블록에 저장된 데이터
        self.nonce = nonce  # 논스 값, 채굴 과정에서 변경됨
        self.hash = self.calculate_hash()  # 블록의 해시 값을 계산하여 설정합니다.

    def calculate_hash(self):
        # 블록의 모든 정보를 조합하여 SHA-256 해시 값을 생성합니다.
        # 해시 값은 블록의 고유한 식별자로 사용됩니다.
        value = (str(self.index) + str(self.previous_hash) +
                 str(self.timestamp) + str(self.data) + str(self.nonce)).encode('utf-8')
        return hashlib.sha256(value).hexdigest()

    def formatted_timestamp(self):
        # 타임스탬프를 사람이 읽기 좋은 형식으로 변환합니다.
        return datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M:%S')

    def __repr__(self):
        # 블록의 내용을 보기 좋게 출력하기 위한 문자열을 반환합니다.
        return (f"블록 번호: {self.index}\n"
                f"이전 해시: {self.previous_hash[:10]}...{self.previous_hash[-10:]}\n"
                f"타임스탬프: {self.formatted_timestamp()}\n"
                f"데이터: {self.data}\n"
                f"논스: {self.nonce}\n"
                f"해시: {self.hash[:10]}...{self.hash[-10:]}\n"
                "-------------------------------")

class Blockchain:
    def __init__(self):
        print("블록체인을 초기화합니다...")
        self.chain = [self.create_genesis_block()]  # 제네시스 블록을 생성하여 체인에 추가합니다.
        self.difficulty = 5 # 기본 난이도 설정

    def create_genesis_block(self):
        print("제네시스 블록을 생성합니다... (제네시스 블록은 블록체인의 첫 번째 블록입니다.)")
        # 제네시스 블록은 블록체인의 첫 번째 블록으로, 특별한 블록입니다.
        return Block(0, "0", time.time(), "제네시스 블록")

    def get_latest_block(self):
        # 체인의 마지막 블록을 반환합니다.
        return self.chain[-1]

    def add_block(self, data):
        print(f"새로운 블록을 추가합니다. 입력된 데이터: {data}")
        # 이전 블록을 가져와 새로운 블록을 생성합니다.
        previous_block = self.get_latest_block()
        new_block = Block(index=previous_block.index + 1,
                          previous_hash=previous_block.hash,
                          timestamp=time.time(),
                          data=data)
        # 새 블록을 채굴하여 유효한 해시를 생성합니다.
        try:
            new_block = self.mine_block(new_block)
            self.chain.append(new_block)
            print(f"{new_block.index}번 블록이 성공적으로 추가되었습니다. 해시: {new_block.hash[:10]}...{new_block.hash[-10:]}\n")
        except KeyboardInterrupt:
            print(f"\n{new_block.index}번 블록의 채굴이 중단되었습니다. 메뉴로 돌아갑니다.\n")
        print("-------------------------------")

    def count_leading_zeros(self, hash_value):
        # 해시 값의 처음부터 연속된 '0'의 개수를 센다.
        count = 0
        for char in hash_value:
            if char == '0':
                count += 1
            else:
                break
        return count

    def mine_block(self, block):
        print(f"{block.index}번 블록을 채굴 중입니다...")
        # 채굴이란 블록의 해시 값이 특정 조건(난이도)을 만족하도록 만드는 과정입니다.
        # 이 과정에서 논스(nonce)를 조정해가며 조건을 충족하는 해시를 찾습니다.
        required_prefix = '0' * self.difficulty  # 난이도에 따라 해시가 '0'으로 시작해야 합니다.
        
        # 논스(nonce)란?
        # 논스는 "number only used once"의 약자로, 블록의 해시 값을 바꾸기 위해 사용되는 임의의 숫자입니다.
        # 채굴 과정에서 논스가 변경될 때마다 새로운 해시 값이 계산됩니다.
        
        while not block.hash.startswith(required_prefix):
            block.nonce += 1
            block.hash = block.calculate_hash()  # 논스를 증가시키며 올바른 해시를 찾습니다.
            
            # 채굴 과정을 로깅하여 실시간으로 확인할 수 있도록 합니다.
            if block.nonce % 10000 == 0:
                leading_zeros = self.count_leading_zeros(block.hash)
                print(f"현재 논스: {block.nonce}, 현재 해시: {block.hash[:10]}...{block.hash[-10:]}  [{'0' * leading_zeros}{' ' * (self.difficulty - leading_zeros)}]")
        
        # 채굴의 목적은?
        # 블록체인의 채굴 과정은 해시 계산을 통해 블록의 무결성을 보장하고, 동시에 블록을 생성하는 데 필요한 작업 증명을 제공합니다.
        # 이 과정은 블록체인의 보안과 분산화를 유지하는 데 중요합니다.
        
        leading_zeros = self.count_leading_zeros(block.hash)
        print(f"현재 논스: {block.nonce}, 현재 해시: {block.hash[:10]}...{block.hash[-10:]}  [{'0' * leading_zeros}{' ' * (self.difficulty - leading_zeros)}]")
        print(f"{block.index}번 블록이 채굴되었습니다! ")
        return block

    def is_chain_valid(self):
        print("블록체인의 유효성을 검사합니다...")
        # 블록체인의 각 블록이 유효한지 확인하는 과정입니다.
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # 현재 블록의 해시가 올바른지 확인합니다.
            if current_block.hash != current_block.calculate_hash():
                print(f"{i}번 블록의 해시가 유효하지 않습니다.")
                print("-------------------------------")
                return False

            # 현재 블록의 이전 해시가 이전 블록의 해시와 일치하는지 확인합니다.
            if current_block.previous_hash != previous_block.hash:
                print(f"{i}번 블록의 이전 해시가 유효하지 않습니다.")
                print("-------------------------------")
                return False

        print("블록체인은 유효합니다.")
        return True

    def adjust_difficulty(self, new_difficulty):
        # 난이도 조절 메서드
        if new_difficulty > 0:
            self.difficulty = new_difficulty
            print(f"난이도가 {self.difficulty}(으)로 변경되었습니다.")
        else:
            print("유효하지 않은 난이도 값입니다. 난이도는 1 이상의 정수여야 합니다.")

# 블록체인 생성
simple_chain = Blockchain()

# 사용자 입력을 통한 블록 추가 시나리오
while True:
    print("\n메뉴:")
    print("1. 새로운 블록 추가")
    print("2. 블록체인 보기")
    print("3. 블록 데이터 변조")
    print("4. 블록체인 유효성 검사")
    print("5. 난이도 조절")
    print("6. 종료")
    
    choice = input("원하는 작업을 선택하세요 (1-6): ")

    if choice == "1":
        data = input("블록에 저장할 데이터를 입력하세요: ")
        print("\n")
        simple_chain.add_block(data)

    elif choice == "2":
        print("\n현재 블록체인 상태:")
        print("-------------------------------")
        for block in simple_chain.chain:
            print(block)

    elif choice == "3":
        block_index = int(input("변조할 블록의 번호를 입력하세요: "))
        if 0 < block_index < len(simple_chain.chain):
            new_data = input(f"{block_index}번 블록의 새로운 데이터를 입력하세요: ")
            simple_chain.chain[block_index].data = new_data
            print(f"{block_index}번 블록의 데이터가 변경되었습니다: {simple_chain.chain[block_index].data}")
        else:
            print("유효하지 않은 블록 번호입니다.")

    elif choice == "4":
        print("블록체인의 유효성을 검사 중입니다...")
        print("블록체인은 유효한가요?", simple_chain.is_chain_valid())

    elif choice == "5":
        new_difficulty = int(input("새로운 난이도를 입력하세요 (1 이상의 정수): "))
        simple_chain.adjust_difficulty(new_difficulty)

    elif choice == "6":
        print("프로그램을 종료합니다.")
        break

    else:
        print("유효하지 않은 선택입니다. 다시 시도하세요.")
