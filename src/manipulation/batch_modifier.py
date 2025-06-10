from typing import Dict, List, Any
import logging
import zlib
import brotli
from config.settings import COMPRESSION_ALGORITHMS

class BatchModifier:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def filter_transactions(self, transactions: List[Dict], criteria: Dict) -> List[Dict]:
        """
        Filter transactions based on specified criteria.
        
        Args:
            transactions: List of L2 transactions
            criteria: Dictionary of filtering criteria
                {
                    'type': ['TRANSFER', 'CONTRACT_CREATION', ...],
                    'min_value': float,
                    'max_value': float,
                    'exclude_addresses': List[str],
                    ...
                }
        """
        filtered_txs = []
        for tx in transactions:
            if self._matches_criteria(tx, criteria):
                filtered_txs.append(tx)
        return filtered_txs

    def _matches_criteria(self, transaction: Dict, criteria: Dict) -> bool:
        """Check if a transaction matches the filtering criteria."""
        try:
            # Check transaction type
            if 'type' in criteria and transaction.get('type') not in criteria['type']:
                return False

            # Check value range
            if 'min_value' in criteria and float(transaction.get('value', 0)) < criteria['min_value']:
                return False
            if 'max_value' in criteria and float(transaction.get('value', 0)) > criteria['max_value']:
                return False

            # Check excluded addresses
            if 'exclude_addresses' in criteria:
                if transaction.get('to') in criteria['exclude_addresses']:
                    return False
                if transaction.get('from') in criteria['exclude_addresses']:
                    return False

            return True
        except Exception as e:
            self.logger.error(f"Error checking transaction criteria: {str(e)}")
            return False

    def reconstruct_batch(self, original_batch: Dict, filtered_transactions: List[Dict]) -> Dict:
        """
        Reconstruct a batch with the filtered transactions.
        This is a placeholder - actual implementation would depend on the
        specific batch format and reconstruction requirements.
        """
        try:
            reconstructed_batch = {
                'block_number': original_batch['block_number'],
                'transaction_hash': original_batch['transaction_hash'],
                'transactions': filtered_transactions,
                'metadata': original_batch.get('metadata', {})
            }
            return reconstructed_batch
        except Exception as e:
            self.logger.error(f"Error reconstructing batch: {str(e)}")
            raise

    def compress_batch(self, batch_data: bytes, algorithm: str = 'zlib') -> bytes:
        """
        Compress batch data using the specified algorithm.
        
        Args:
            batch_data: Raw batch data to compress
            algorithm: Compression algorithm to use ('zlib' or 'brotli')
        """
        try:
            if algorithm not in COMPRESSION_ALGORITHMS:
                raise ValueError(f"Unsupported compression algorithm: {algorithm}")

            if algorithm == 'zlib':
                return zlib.compress(batch_data)
            elif algorithm == 'brotli':
                return brotli.compress(batch_data)
        except Exception as e:
            self.logger.error(f"Error compressing batch: {str(e)}")
            raise

    def decompress_batch(self, compressed_data: bytes, algorithm: str = 'zlib') -> bytes:
        """
        Decompress batch data using the specified algorithm.
        
        Args:
            compressed_data: Compressed batch data
            algorithm: Compression algorithm used ('zlib' or 'brotli')
        """
        try:
            if algorithm not in COMPRESSION_ALGORITHMS:
                raise ValueError(f"Unsupported compression algorithm: {algorithm}")

            if algorithm == 'zlib':
                return zlib.decompress(compressed_data)
            elif algorithm == 'brotli':
                return brotli.decompress(compressed_data)
        except Exception as e:
            self.logger.error(f"Error decompressing batch: {str(e)}")
            raise

    def calculate_size_difference(self, original_batch: bytes, modified_batch: bytes) -> Dict:
        """
        Calculate the size difference between original and modified batches.
        """
        try:
            original_size = len(original_batch)
            modified_size = len(modified_batch)
            difference = modified_size - original_size
            percentage = (difference / original_size) * 100 if original_size > 0 else 0

            return {
                'original_size': original_size,
                'modified_size': modified_size,
                'difference': difference,
                'percentage': percentage
            }
        except Exception as e:
            self.logger.error(f"Error calculating size difference: {str(e)}")
            raise 