-- Create the database if it doesn't exist
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'aayus') THEN
        CREATE DATABASE aayus;
    END IF;
END $$;

-- Connect to the database
\c mydatabase;

-- Create the table if it doesn't exist
CREATE TABLE IF NOT EXISTS rss_table (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL CHECK (title <> ''),
    link TEXT NOT NULL CHECK (link <> ''),
    datetime TIMESTAMPTZ NOT NULL,
    image_data BYTEA,
    tags TEXT[],
    summary TEXT,
    UNIQUE(link)
);

CREATE INDEX IF NOT EXISTS idx_pubtime ON rss_table(datetime);