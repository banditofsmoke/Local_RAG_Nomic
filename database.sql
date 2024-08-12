-- Drop the existing table
DROP TABLE IF EXISTS conversations;

-- Create the table with the correct vector dimension
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    prompt TEXT NOT NULL,
    response TEXT NOT NULL,
    embedding vector(768)
);

-- Create the index
CREATE INDEX embedding_idx ON conversations USING ivfflat (embedding vector_cosine_ops);

-- Grant necessary privileges
GRANT ALL PRIVILEGES ON TABLE conversations TO postgres;
GRANT USAGE, SELECT ON SEQUENCE conversations_id_seq TO postgres;
