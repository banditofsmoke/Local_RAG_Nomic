# 🚀 Local RAG Assistant: Your Tiny Open-Source RAG Revolution! 🧠💬

Welcome to the Local RAG Assistant project - where big AI meets small hardware! This nifty little system brings the power of Retrieval-Augmented Generation (RAG) right to your local machine, no cloud required. Whether you're rockin' a beefy rig or a trusty old laptop, we've got you covered!

## 🌟 What's This All About?

Ever wanted to chat with an AI that remembers your conversations, but didn't want to send your data to the cloud? Say hello to your new best friend! This project uses:

- 🔍 Nomic Embed Text for local embeddings
- 🤖 Ollama for running language models locally
- 🐘 PostgreSQL with pgvector for efficient similarity search
- 🐍 Python magic to tie it all together

And the best part? It's designed to run on everything from your grandma's old laptop to your fancy dev machine!

## 🛠 Prerequisites

- Python 3.8+ (because we're not savages)
- PostgreSQL 16+ with pgvector extension (for those juicy vector operations)
- Ollama (your friendly neighborhood language model runner)
- A Linux environment (we used Ubuntu 24.04, but hey, we don't judge)

## 🏗 Setting Up Shop

### 1. PostgreSQL: The Data Dungeon

First, let's set up our data lair:

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib postgresql-16-pgvector
```

Now, let's create our secret database and set it up for action:

1. Create a file named `database.sql` with the following content:

```sql
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
```

2. Create a file named `create_database.sh` with the following content:

```bash
#!/bin/bash
sudo -u postgres psql -c "CREATE DATABASE memory_agent;"
sudo -u postgres psql -d memory_agent -c "CREATE EXTENSION IF NOT EXISTS vector;"
sudo -u postgres psql -d memory_agent -a -f database.sql
```

3. Make the script executable and run it:

```bash
chmod +x create_database.sh
./create_database.sh
```

This will create the database, enable the vector extension, and set up our conversation table with all the necessary permissions. It's like giving your AI a comfy home to store memories!

### 2. Python: The Glue That Holds Our Dreams Together

Create your virtual paradise:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the magic ingredients:

```bash
pip install psycopg2-binary ollama colorama cachetools tqdm numpy
```

### 3. Ollama: Your Local Language Model Tamer

Grab Ollama from their [GitHub page](https://github.com/jmorganca/ollama) and install it like a pro.

Then, let's summon our AI minions:

```bash
ollama pull phi3
ollama pull nomic-embed-text
```

## ⚙️ Configuration: Make It Your Own!

Customize the `DB_PARAMS` in the script to match your PostgreSQL setup:

```python
DB_PARAMS = {
    'dbname': 'memory_agent',
    'user': 'postgres',
    'password': 'your_super_secret_password',
    'host': 'localhost',
    'port': '5432'
}
```

## 🧠 Memory Management for the Low-End Warriors

We've got your back if you're running on a potato... I mean, a low-end device! The script uses a memory limit to keep things under control:

```python
MAX_MEMORY = 512 * 1024 * 1024  # 512MB in bytes
```

Feel free to adjust this based on your device's capabilities. Running on a toaster? Lower it. Got a supercomputer? Crank it up!

## 🧵 Threading: Keeping Things Smooth

We use threading to keep the UI responsive while your device crunches numbers in the background. It's like patting your head and rubbing your belly, but for computers!

## 🏃‍♂️ Running Your New AI Buddy

```bash
python RAG_ass_3.py
```

Then chat away! Your AI friend is ready to talk, and it'll remember your conversations (unless you tell it to forget, you mysterious person, you).

## 🎛 Special Features

Our Local RAG Assistant comes with some nifty built-in functions to make your life easier:

### 1. 🧠 /recall [prompt]
Want to jog your AI's memory? Use `/recall` followed by your prompt. This function will search for relevant past conversations before responding, giving you more context-aware answers.

### 2. 🗑️ /forget
Oops! Said something you wish you hadn't? No worries! Just type `/forget` to remove the last conversation from the AI's memory. It's like it never happened!

### 3. 📝 /memorize [content]
Got something important you want your AI to remember for future conversations? Use `/memorize` followed by the content you want to store. It's like leaving a sticky note for your AI buddy!

## 🚑 Troubleshooting: When Things Go Sideways

1. **Dimension Disaster**: If you see a dimension mismatch error, double-check your table setup. We're working with 768-dimensional embeddings here, not quantum physics!

2. **Memory Meltdown**: If your device is sweating, try lowering the `MAX_MEMORY` value. We want to assist you, not cook eggs on your CPU.

3. **Slowpoke Syndrome**: On a low-end device? Try reducing the number of similar conversations retrieved. Quality over quantity, folks!

4. **Database Drama**: Make sure PostgreSQL is up and running, and pgvector is installed. Also, check your `DB_PARAMS` - typos are the arch-nemesis of database connections.

5. **Ollama Outage**: Ensure Ollama is installed and your models are ready to roll. Check with `ollama list`. No models, no fun!

Quick Checks:
- Ensure PostgreSQL is running: `sudo systemctl status postgresql`
- Check Ollama status: `ollama list`
- Verify database connection: `psql -U postgres -d memory_agent -h localhost -W`

## 🎨 Customization: Make It Yours

- Want a different AI brain? Change the model in `chat_with_ollama`.
- Need more (or less) context? Adjust the `limit` in `retrieve_similar_conversations`.
- The world is your oyster! (Terms and conditions may apply)

## 🤝 Contributing: Join the RAG Tag Team!

Got ideas? Found a bug? Want to make this even more awesome? Contributions are super welcome! Fork, code, and hit us with those pull requests!

## 📜 License

This project is open source and available under the [MIT License](LICENSE). Use it, abuse it (the code, not the license), and make cool stuff!

## 🌟 Final Words

Remember, this is your tiny open-source RAG assistant. It might not be much, but it's honest work. Use it wisely, expand it wildly, and most importantly, have fun! Who said local AI can't be a blast?

Now go forth and chat with your new AI companion! May your conversations be ever insightful and your memory usage low. 🚀🧠💬

📬 Contact Information
For questions, suggestions, or collaborations, please reach out:
Wayne Sletcher (SledgeHumma)

LinkedIn: [Wayne Sletcher](https://www.linkedin.com/in/waynesletcheraisystemsbuilder)
Email: skeletonenglish@gmail.com
GitHub: [banditofsmoke](https://github.com/banditofsmoke)

Made in Sledge's Forge (Private Discord)
