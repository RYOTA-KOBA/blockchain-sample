# coding: UTF-8

import hashlib
import json
import time

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        ブロックチェーンに対し、新しいブロックを作る。
        :param proof: <int> プルーフ・オブ・ワークアルゴリズムから得られるプルーフ
        :param previous_hash: (オプション) <str> 前のブロックのハッシュ
        :return: <dict> 新しいブロック
        """

        block = {
          'index': len(self.chain) + 1,
          'timestamp': time(),
          'transactions': self.current_transactions,
          'proof': proof,
          'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        新しいトランザクションを作り、次に採掘されるブロックに加える処理
        トランザクション: 送信者のアドレス、受信者のアドレス、量、手数料、署名などの取引情報
        採掘:マイナーがトランザクションに含まれる署名を検証し、hash値の計算、ブロックの作成までを行うこと、
        採掘の後はネットワークにブロードキャストすることで、全てのノードが最新のhashを持つようになる。
        :param sender: <str> 送信者のアドレス
        :param recipient: <str> 受信者のアドレス
        :param amount: <int> 量
        :return: <int> このトランザクションを含むブロックのアドレス
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        ブロックの　SHA-256 ハッシュを作る
        :param block: <dict> ブロック
        :return: <str>
        """

        # 必ずディクショナリ（辞書型のオブジェクト）がソートされている必要がある。そうでないと、一貫性のないハッシュとなってしまう
        # ↑ブロックチェーンでは直前のブロックのhash値を前提条件として新しいブロックのhash値を計算していくため。RDBの外部キー的な感じでブロック同士が繋がっている
        # ブロックチェーン全体で見ると、過去の全ての取引のhash値が連なっている。
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
