import logging
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any
import pandas as pd
from datetime import datetime

class BatchVisualizer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def create_batch_size_trend(self, metrics_data: List[Dict]) -> go.Figure:
        """
        Create a line plot showing batch size trends over time.
        
        Args:
            metrics_data: List of batch metric dictionaries
        """
        try:
            df = pd.DataFrame(metrics_data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['batch_size'],
                mode='lines+markers',
                name='Batch Size'
            ))
            
            fig.update_layout(
                title='Batch Size Trend Over Time',
                xaxis_title='Timestamp',
                yaxis_title='Batch Size',
                showlegend=True
            )
            
            return fig
        except Exception as e:
            self.logger.error(f"Error creating batch size trend: {str(e)}")
            raise

    def create_compression_ratio_plot(self, metrics_data: List[Dict]) -> go.Figure:
        """
        Create a line plot showing compression ratio trends.
        
        Args:
            metrics_data: List of batch metric dictionaries
        """
        try:
            df = pd.DataFrame(metrics_data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['compression_ratio'],
                mode='lines+markers',
                name='Compression Ratio'
            ))
            
            fig.update_layout(
                title='Compression Ratio Trend Over Time',
                xaxis_title='Timestamp',
                yaxis_title='Compression Ratio (%)',
                showlegend=True
            )
            
            return fig
        except Exception as e:
            self.logger.error(f"Error creating compression ratio plot: {str(e)}")
            raise

    def create_transaction_type_distribution(self, metrics_data: List[Dict]) -> go.Figure:
        """
        Create a pie chart showing distribution of transaction types.
        
        Args:
            metrics_data: List of batch metric dictionaries
        """
        try:
            # Aggregate transaction type counts
            type_counts = {}
            for metric in metrics_data:
                for tx_type, count in metric['transaction_types'].items():
                    type_counts[tx_type] = type_counts.get(tx_type, 0) + count
            
            # Create pie chart
            fig = go.Figure(data=[go.Pie(
                labels=list(type_counts.keys()),
                values=list(type_counts.values()),
                hole=.3
            )])
            
            fig.update_layout(
                title='Transaction Type Distribution',
                showlegend=True
            )
            
            return fig
        except Exception as e:
            self.logger.error(f"Error creating transaction type distribution: {str(e)}")
            raise

    def create_size_comparison_plot(self, original_sizes: List[int], modified_sizes: List[int]) -> go.Figure:
        """
        Create a bar chart comparing original and modified batch sizes.
        
        Args:
            original_sizes: List of original batch sizes
            modified_sizes: List of modified batch sizes
        """
        try:
            fig = go.Figure(data=[
                go.Bar(name='Original Size', x=list(range(len(original_sizes))), y=original_sizes),
                go.Bar(name='Modified Size', x=list(range(len(modified_sizes))), y=modified_sizes)
            ])
            
            fig.update_layout(
                title='Batch Size Comparison',
                xaxis_title='Batch Index',
                yaxis_title='Size (bytes)',
                barmode='group'
            )
            
            return fig
        except Exception as e:
            self.logger.error(f"Error creating size comparison plot: {str(e)}")
            raise

    def create_metrics_dashboard(self, metrics_data: List[Dict]) -> go.Figure:
        """
        Create a dashboard with multiple metrics visualizations.
        
        Args:
            metrics_data: List of batch metric dictionaries
        """
        try:
            # Create subplots
            fig = go.Figure()
            
            # Add batch size trend
            df = pd.DataFrame(metrics_data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['batch_size'],
                mode='lines+markers',
                name='Batch Size'
            ))
            
            # Add compression ratio
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['compression_ratio'],
                mode='lines+markers',
                name='Compression Ratio',
                yaxis='y2'
            ))
            
            # Update layout
            fig.update_layout(
                title='Batch Metrics Dashboard',
                xaxis_title='Timestamp',
                yaxis_title='Batch Size',
                yaxis2=dict(
                    title='Compression Ratio (%)',
                    overlaying='y',
                    side='right'
                ),
                showlegend=True
            )
            
            return fig
        except Exception as e:
            self.logger.error(f"Error creating metrics dashboard: {str(e)}")
            raise

    def save_plot(self, fig: go.Figure, filename: str) -> None:
        """
        Save a plot to a file.
        
        Args:
            fig: Plotly figure object
            filename: Output filename
        """
        try:
            fig.write_html(filename)
        except Exception as e:
            self.logger.error(f"Error saving plot: {str(e)}")
            raise 