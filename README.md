# World Chain Batch Analysis

This project analyzes Layer 2 batch submissions from World Chain to Ethereum L1, focusing on EIP-4844 blob data. It provides tools for fetching, decoding, modifying, and analyzing batch data to understand the impact of different transaction compositions on L1 data costs.

## Features

- Fetch and store L1 batch data from World Chain
- Decode EIP-4844 blob transactions
- Filter and modify L2 transactions within batches
- Analyze batch composition and compression ratios
- Generate visualizations of batch metrics
- Compare original and modified batch sizes

## Project Structure

```
worldcasestdy/
├── src/
│   ├── data_acquisition/
│   │   ├── l1_client.py
│   │   └── batch_fetcher.py
│   ├── decoding/
│   │   └── batch_decoder.py
│   ├── manipulation/
│   │   └── batch_modifier.py
│   ├── analysis/
│   │   ├── metrics.py
│   │   └── visualizer.py
│   └── main.py
├── tests/
│   └── unit/
├── data/
│   ├── raw/
│   └── processed/
├── config/
│   └── settings.py
└── requirements.txt
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/worldcasestdy.git
cd worldcasestdy
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your configuration:
```
L1_RPC_URL=your_ethereum_node_url
WORLD_CHAIN_ADDRESS=world_chain_contract_address
DATABASE_URL=your_database_url
```

## Usage

1. Configure settings in `config/settings.py`:
   - Set the start and end block numbers
   - Adjust batch size for data fetching
   - Configure compression algorithms

2. Run the main script:
```bash
python src/main.py
```

3. View the generated visualizations in the `data/processed` directory:
   - `batch_size_trend.html`
   - `compression_ratio.html`
   - `transaction_types.html`
   - `size_comparison.html`
   - `metrics_dashboard.html`

## Components

### Data Acquisition
- `L1Client`: Interacts with Ethereum L1 node
- `BatchFetcher`: Fetches and stores batch data

### Decoding
- `BatchDecoder`: Decodes EIP-4844 blob transactions

### Manipulation
- `BatchModifier`: Filters and modifies L2 transactions

### Analysis
- `BatchMetrics`: Calculates batch metrics and trends
- `BatchVisualizer`: Generates visualizations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OP Stack team for reference implementations
- L2BEAT for research and analysis tools
- Ethereum community for EIP-4844 specification 