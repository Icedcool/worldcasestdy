import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ethereum L1 Configuration
L1_RPC_URL = os.getenv('L1_RPC_URL', 'https://mainnet.infura.io/v3/your-api-key')
WORLD_CHAIN_ADDRESS = os.getenv('WORLD_CHAIN_ADDRESS', '0x...')  # Replace with actual World Chain address

# Database Configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/raw/batches.db')

# Data Collection Settings
BATCH_SIZE = 100  # Number of blocks to fetch per batch
START_BLOCK = 19400000  # Approximate start of EIP-4844
END_BLOCK = None  # Set to None for latest block

# Analysis Settings
COMPRESSION_ALGORITHMS = ['zlib', 'brotli']
TRANSACTION_TYPES = {
    'TRANSFER': '0x',
    'CONTRACT_CREATION': '0x',
    'CONTRACT_INTERACTION': '0x',
    # Add more transaction types as needed
}

# Logging Configuration
LOG_LEVEL = 'INFO'
LOG_FILE = 'data/processed/analysis.log' 