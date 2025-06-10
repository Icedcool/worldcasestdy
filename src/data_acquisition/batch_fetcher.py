import logging
from typing import List, Dict
import json
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.settings import DATABASE_URL, START_BLOCK, END_BLOCK, BATCH_SIZE
from .l1_client import L1Client

Base = declarative_base()

class BatchSubmission(Base):
    __tablename__ = 'batch_submissions'
    
    id = Column(Integer, primary_key=True)
    block_number = Column(Integer, nullable=False)
    transaction_hash = Column(String, unique=True, nullable=False)
    raw_data = Column(JSON, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    processed = Column(Integer, default=0)  # 0: not processed, 1: processed

class BatchFetcher:
    def __init__(self):
        self.l1_client = L1Client()
        self.engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def fetch_batches(self, start_block: int = START_BLOCK, end_block: int = END_BLOCK) -> None:
        """Fetch and store batch submissions."""
        if end_block is None:
            end_block = self.l1_client.get_latest_block()

        current_block = start_block
        while current_block <= end_block:
            try:
                batch_end = min(current_block + BATCH_SIZE - 1, end_block)
                self.logger.info(f"Fetching batches from block {current_block} to {batch_end}")
                
                batches = self.l1_client.get_world_chain_batches(current_block, batch_end)
                
                for batch in batches:
                    submission = BatchSubmission(
                        block_number=batch['block_number'],
                        transaction_hash=batch['transaction_hash'],
                        raw_data=batch['raw_data']
                    )
                    self.session.add(submission)
                
                self.session.commit()
                self.logger.info(f"Stored {len(batches)} batches")
                
                current_block = batch_end + 1
                
            except Exception as e:
                self.logger.error(f"Error fetching batches: {str(e)}")
                self.session.rollback()
                current_block += BATCH_SIZE

    def get_unprocessed_batches(self) -> List[BatchSubmission]:
        """Get all unprocessed batch submissions."""
        return self.session.query(BatchSubmission).filter_by(processed=0).all()

    def mark_as_processed(self, batch_id: int) -> None:
        """Mark a batch submission as processed."""
        batch = self.session.query(BatchSubmission).get(batch_id)
        if batch:
            batch.processed = 1
            self.session.commit()

    def export_batches(self, output_file: str) -> None:
        """Export batch data to a JSON file."""
        batches = self.session.query(BatchSubmission).all()
        data = [{
            'block_number': b.block_number,
            'transaction_hash': b.transaction_hash,
            'raw_data': b.raw_data,
            'timestamp': b.timestamp.isoformat()
        } for b in batches]
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2) 