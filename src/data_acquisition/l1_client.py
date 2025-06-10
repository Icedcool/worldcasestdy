from web3 import Web3
from typing import Optional, List, Dict
import logging
from config.settings import L1_RPC_URL, WORLD_CHAIN_ADDRESS

class L1Client:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(L1_RPC_URL))
        if not self.w3.is_connected():
            raise ConnectionError("Failed to connect to Ethereum node")
        
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def get_latest_block(self) -> int:
        """Get the latest block number."""
        return self.w3.eth.block_number

    def get_block(self, block_number: int) -> Dict:
        """Get block data for a specific block number."""
        return self.w3.eth.get_block(block_number, full_transactions=True)

    def get_blob_transactions(self, block_number: int) -> List[Dict]:
        """Get all blob transactions from a specific block."""
        block = self.get_block(block_number)
        blob_txs = []
        
        for tx in block['transactions']:
            if tx.get('type') == 3:  # EIP-4844 blob transaction type
                blob_txs.append(tx)
        
        return blob_txs

    def get_world_chain_batches(self, start_block: int, end_block: Optional[int] = None) -> List[Dict]:
        """Get all World Chain batch submissions between start_block and end_block."""
        if end_block is None:
            end_block = self.get_latest_block()

        batches = []
        for block_num in range(start_block, end_block + 1):
            try:
                blob_txs = self.get_blob_transactions(block_num)
                for tx in blob_txs:
                    if tx['to'] and tx['to'].lower() == WORLD_CHAIN_ADDRESS.lower():
                        batches.append({
                            'block_number': block_num,
                            'transaction_hash': tx['hash'].hex(),
                            'raw_data': tx
                        })
            except Exception as e:
                self.logger.error(f"Error processing block {block_num}: {str(e)}")
                continue

        return batches

    def get_transaction_receipt(self, tx_hash: str) -> Dict:
        """Get transaction receipt for a specific transaction."""
        return self.w3.eth.get_transaction_receipt(tx_hash) 