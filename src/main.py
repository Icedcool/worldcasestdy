import logging
import os
from datetime import datetime
from data_acquisition.l1_client import L1Client
from data_acquisition.batch_fetcher import BatchFetcher
from decoding.batch_decoder import BatchDecoder
from manipulation.batch_modifier import BatchModifier
from analysis.metrics import BatchMetrics
from analysis.visualizer import BatchVisualizer
from config.settings import START_BLOCK, END_BLOCK

def setup_logging():
    """Set up logging configuration."""
    log_dir = 'data/processed'
    os.makedirs(log_dir, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(log_dir, 'analysis.log')),
            logging.StreamHandler()
        ]
    )

def main():
    """Main execution function."""
    try:
        # Set up logging
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("Starting batch analysis process")

        # Initialize components
        l1_client = L1Client()
        batch_fetcher = BatchFetcher()
        batch_decoder = BatchDecoder()
        batch_modifier = BatchModifier()
        batch_metrics = BatchMetrics()
        visualizer = BatchVisualizer()

        # Fetch batches
        logger.info(f"Fetching batches from block {START_BLOCK} to {END_BLOCK}")
        batch_fetcher.fetch_batches(START_BLOCK, END_BLOCK)

        # Process unprocessed batches
        unprocessed_batches = batch_fetcher.get_unprocessed_batches()
        logger.info(f"Found {len(unprocessed_batches)} unprocessed batches")

        metrics_data = []
        original_sizes = []
        modified_sizes = []

        for batch in unprocessed_batches:
            try:
                # Decode batch
                decoded_batch = batch_decoder.decode_batch(batch)
                
                # Calculate original metrics
                original_metrics = batch_metrics.calculate_batch_metrics(decoded_batch)
                metrics_data.append(original_metrics)
                original_sizes.append(len(str(decoded_batch)))

                # Filter and modify transactions
                filtered_txs = batch_modifier.filter_transactions(
                    decoded_batch.get('transactions', []),
                    {
                        'type': ['TRANSFER', 'CONTRACT_CREATION'],
                        'min_value': 0,
                        'max_value': float('inf')
                    }
                )

                # Reconstruct batch with filtered transactions
                modified_batch = batch_modifier.reconstruct_batch(decoded_batch, filtered_txs)
                modified_sizes.append(len(str(modified_batch)))

                # Mark batch as processed
                batch_fetcher.mark_as_processed(batch.id)

            except Exception as e:
                logger.error(f"Error processing batch {batch.id}: {str(e)}")
                continue

        # Generate visualizations
        logger.info("Generating visualizations")
        
        # Create and save plots
        size_trend = visualizer.create_batch_size_trend(metrics_data)
        visualizer.save_plot(size_trend, 'data/processed/batch_size_trend.html')

        compression_plot = visualizer.create_compression_ratio_plot(metrics_data)
        visualizer.save_plot(compression_plot, 'data/processed/compression_ratio.html')

        type_dist = visualizer.create_transaction_type_distribution(metrics_data)
        visualizer.save_plot(type_dist, 'data/processed/transaction_types.html')

        size_comp = visualizer.create_size_comparison_plot(original_sizes, modified_sizes)
        visualizer.save_plot(size_comp, 'data/processed/size_comparison.html')

        dashboard = visualizer.create_metrics_dashboard(metrics_data)
        visualizer.save_plot(dashboard, 'data/processed/metrics_dashboard.html')

        # Analyze results
        analysis = batch_metrics.analyze_batch_series(metrics_data)
        logger.info("Analysis results:")
        logger.info(f"Total batches analyzed: {analysis['total_batches']}")
        logger.info(f"Average batch size: {analysis['average_batch_size']:.2f}")
        logger.info(f"Compression trend: {analysis['compression_trend']['trend']}")
        logger.info(f"Size trend: {analysis['size_trend']['trend']}")

        logger.info("Batch analysis process completed successfully")

    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    main() 