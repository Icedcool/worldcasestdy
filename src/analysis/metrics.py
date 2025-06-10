from typing import Dict, List, Any
import logging
import pandas as pd
import numpy as np
from datetime import datetime

class BatchMetrics:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def calculate_batch_metrics(self, batch_data: Dict) -> Dict:
        """
        Calculate various metrics for a batch.
        
        Args:
            batch_data: Dictionary containing batch information
        """
        try:
            metrics = {
                'timestamp': datetime.utcnow().isoformat(),
                'batch_size': len(batch_data.get('transactions', [])),
                'total_value': self._calculate_total_value(batch_data),
                'transaction_types': self._count_transaction_types(batch_data),
                'compression_ratio': self._calculate_compression_ratio(batch_data),
                'average_transaction_size': self._calculate_avg_tx_size(batch_data)
            }
            return metrics
        except Exception as e:
            self.logger.error(f"Error calculating batch metrics: {str(e)}")
            raise

    def _calculate_total_value(self, batch_data: Dict) -> float:
        """Calculate total value of all transactions in the batch."""
        try:
            transactions = batch_data.get('transactions', [])
            return sum(float(tx.get('value', 0)) for tx in transactions)
        except Exception as e:
            self.logger.error(f"Error calculating total value: {str(e)}")
            return 0.0

    def _count_transaction_types(self, batch_data: Dict) -> Dict[str, int]:
        """Count occurrences of different transaction types."""
        try:
            transactions = batch_data.get('transactions', [])
            type_counts = {}
            for tx in transactions:
                tx_type = tx.get('type', 'UNKNOWN')
                type_counts[tx_type] = type_counts.get(tx_type, 0) + 1
            return type_counts
        except Exception as e:
            self.logger.error(f"Error counting transaction types: {str(e)}")
            return {}

    def _calculate_compression_ratio(self, batch_data: Dict) -> float:
        """Calculate compression ratio of the batch."""
        try:
            original_size = batch_data.get('original_size', 0)
            compressed_size = batch_data.get('compressed_size', 0)
            if original_size == 0:
                return 0.0
            return (original_size - compressed_size) / original_size * 100
        except Exception as e:
            self.logger.error(f"Error calculating compression ratio: {str(e)}")
            return 0.0

    def _calculate_avg_tx_size(self, batch_data: Dict) -> float:
        """Calculate average transaction size in the batch."""
        try:
            transactions = batch_data.get('transactions', [])
            if not transactions:
                return 0.0
            sizes = [len(str(tx)) for tx in transactions]
            return sum(sizes) / len(sizes)
        except Exception as e:
            self.logger.error(f"Error calculating average transaction size: {str(e)}")
            return 0.0

    def analyze_batch_series(self, batch_metrics: List[Dict]) -> Dict:
        """
        Analyze a series of batch metrics to identify trends and patterns.
        
        Args:
            batch_metrics: List of batch metric dictionaries
        """
        try:
            df = pd.DataFrame(batch_metrics)
            
            analysis = {
                'total_batches': len(batch_metrics),
                'average_batch_size': df['batch_size'].mean(),
                'total_value': df['total_value'].sum(),
                'compression_trend': self._analyze_compression_trend(df),
                'transaction_type_distribution': self._analyze_transaction_types(df),
                'size_trend': self._analyze_size_trend(df)
            }
            
            return analysis
        except Exception as e:
            self.logger.error(f"Error analyzing batch series: {str(e)}")
            raise

    def _analyze_compression_trend(self, df: pd.DataFrame) -> Dict:
        """Analyze compression ratio trends over time."""
        try:
            return {
                'mean': df['compression_ratio'].mean(),
                'std': df['compression_ratio'].std(),
                'min': df['compression_ratio'].min(),
                'max': df['compression_ratio'].max(),
                'trend': self._calculate_trend(df['compression_ratio'])
            }
        except Exception as e:
            self.logger.error(f"Error analyzing compression trend: {str(e)}")
            return {}

    def _analyze_transaction_types(self, df: pd.DataFrame) -> Dict:
        """Analyze distribution of transaction types."""
        try:
            type_counts = {}
            for types in df['transaction_types']:
                for tx_type, count in types.items():
                    type_counts[tx_type] = type_counts.get(tx_type, 0) + count
            
            total = sum(type_counts.values())
            return {
                'counts': type_counts,
                'percentages': {k: (v/total)*100 for k, v in type_counts.items()}
            }
        except Exception as e:
            self.logger.error(f"Error analyzing transaction types: {str(e)}")
            return {}

    def _analyze_size_trend(self, df: pd.DataFrame) -> Dict:
        """Analyze batch size trends over time."""
        try:
            return {
                'mean': df['batch_size'].mean(),
                'std': df['batch_size'].std(),
                'min': df['batch_size'].min(),
                'max': df['batch_size'].max(),
                'trend': self._calculate_trend(df['batch_size'])
            }
        except Exception as e:
            self.logger.error(f"Error analyzing size trend: {str(e)}")
            return {}

    def _calculate_trend(self, series: pd.Series) -> str:
        """Calculate trend direction from a series of values."""
        try:
            if len(series) < 2:
                return 'insufficient_data'
            
            slope = np.polyfit(range(len(series)), series, 1)[0]
            if slope > 0.1:
                return 'increasing'
            elif slope < -0.1:
                return 'decreasing'
            else:
                return 'stable'
        except Exception as e:
            self.logger.error(f"Error calculating trend: {str(e)}")
            return 'unknown' 