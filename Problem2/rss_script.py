from sqlalchemy import create_engine, Column, Integer, String, Text, LargeBinary, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy_utils import database_exists, create_database
from datetime import datetime
from time import mktime
import requests
from bs4 import BeautifulSoup
from io import BytesIO
import logging
import feedparser
import time


Base = declarative_base()

class RSS_Table(Base):
    __tablename__ = 'rss_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text)
    link = Column(Text)
    datetime = Column(DateTime)
    image_data = Column(LargeBinary)
    tags = Column(Text)
    summary = Column(Text)
    __table_args__ = {'extend_existing': True}

# Set up logging
logging.basicConfig(
    filename='rss_reader.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',

)
logger = logging.getLogger('rss_reader')

def init_db():
    try:
        # Use environment variables for flexibility
        db_user = "aayus"
        db_password = "mypassword"
        db_host = "postgres" 
        db_name = "aayus"

        db_url = f"postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}"
        # db_url = "postgresql://aayus@localhost:5432/aayus"
        engine = create_engine(db_url)

        if not database_exists(engine.url):
            create_database(engine.url)
        Base.metadata.create_all(engine)
        logging.info("Database Connected Successfully")
        return engine
    except Exception as e:
        logging.error(f"Database Connection failed: {str(e)}")
        raise

        engine = create_engine(db_url)

        if not database_exists(engine.url):
            create_database(engine.url)
        Base.metadata.create_all(engine)
        logging.info("Database Connected Successfully")
        return engine
    except Exception as e:
        logging.error(f"Database Connection failed: {str(e)}")
        raise



def download_image_data(url):
    """Download image from URL and return as bytes"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.content
    except Exception as e:
        logging.error(f"Error downloading image: {e}")
        return None


def insert_article(entry):
    """Insert a single article into the database"""
    try:
        engine = init_db()
        Session = sessionmaker(bind=engine)
        session = Session()


        # Convert tags to string
        tags = [tag.term for tag in entry.tags] if 'tags' in entry else []

        # Create article object
        article = RSS_Table()
        article.title = entry.title
        article.link = entry.link
        article.datetime = datetime.fromtimestamp(mktime(entry.published_parsed))
        article.image_data = download_image_data(entry.media_content[0]['url']) if entry.get('media_content') else None
        article.tags = [tag.term for tag in entry.tags] 
        article.summary = entry.get('summary', '')



        # Check for existing entry
        exists = session.query(RSS_Table).filter_by(link=entry.link).first()
        session.add(article)
        session.commit()
        if not exists:
            session.add(article)
            print(article.link, article.title)
            session.commit()
            logging.info(f"Inserted article: {entry.title}")
        else:
            logging.info(f"Article already exists: {entry.title}")

    except Exception as e:
        session.rollback()
        logging.error(f"Error inserting article: {e}")
    finally:
        session.close()

# Example usage with The Hindu RSS feed
def process_feed(feed_url):
    feed = feedparser.parse(feed_url)
    for entry in feed.entries:
        insert_article(entry)

def main():
    """Main function to poll the RSS feed at regular intervals"""
    logger.info(f"RSS Reader started - Polling interval: {600} seconds")
    
    while True:
        try:
            feed_url = 'https://www.thehindu.com/news/national/?service=rss'
            process_feed(feed_url)
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            
        logger.info(f"Sleeping for {600} seconds")
        time.sleep(600)

if __name__ == "__main__":
    main()   




