import psycopg2
import psycopg2.extras
import ollama
from colorama import Fore
import threading
import queue
import time
import resource

# Set memory limit to 1GB (adjust as needed)
MAX_MEMORY = 1 * 1024 * 1024 * 1024  # 1GB in bytes
resource.setrlimit(resource.RLIMIT_AS, (MAX_MEMORY, MAX_MEMORY))

DB_PARAMS = {
    'dbname': 'memory_agent',
    'user': 'postgres',
    'password': 'admin',
    'host': 'localhost',
    'port': '5432'
}

def connect_db():
    return psycopg2.connect(**DB_PARAMS)

def store_conversation(prompt, response, embedding):
    try:
        with connect_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO conversations (prompt, response, embedding) VALUES (%s, %s, %s::vector)',
                    (prompt, response, embedding)
                )
            conn.commit()
    except psycopg2.Error as e:
        print(f"Database error: {e}")

def retrieve_similar_conversations(query, limit=5):
    try:
        embedding = ollama.embeddings(model='nomic-embed-text', prompt=query)['embedding']
        with connect_db() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute("""
                    SELECT prompt, response
                    FROM conversations
                    ORDER BY embedding <-> %s::vector
                    LIMIT %s
                """, (embedding, limit))
                return cursor.fetchall()
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return []
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return []

def process_query(query):
    similar_convos = retrieve_similar_conversations(query)
    context = "\n".join([f"Q: {c['prompt']}\nA: {c['response']}" for c in similar_convos])
    return f"Context:\n{context}\n\nUser Query: {query}"

def chat_with_ollama(messages):
    try:
        response = ollama.chat(model='phi3', messages=messages)
        return response['message']['content']
    except Exception as e:
        print(f"Error in chat_with_ollama: {e}")
        return "I'm sorry, I encountered an error while processing your request."

def worker(task_queue, result_queue):
    while True:
        task = task_queue.get()
        if task is None:
            break
        try:
            result = chat_with_ollama(task)
            result_queue.put(result)
        except Exception as e:
            result_queue.put(f"Error: {str(e)}")
        finally:
            task_queue.task_done()

def main():
    print(Fore.CYAN + "Welcome to the optimized RAG Assistant!")
    messages = []
    task_queue = queue.Queue()
    result_queue = queue.Queue()
    
    # Start worker thread
    worker_thread = threading.Thread(target=worker, args=(task_queue, result_queue))
    worker_thread.start()

    try:
        while True:
            prompt = input(Fore.WHITE + 'USER: \n')
            
            if prompt.lower() == 'exit':
                break
            elif prompt.lower().startswith('/recall'):
                recall_prompt = prompt[7:].strip()
                processed_prompt = process_query(recall_prompt)
                messages.append({"role": "user", "content": processed_prompt})
            elif prompt.lower() == '/forget':
                if len(messages) >= 2:
                    messages = messages[:-2]  # Remove the last user input and assistant response
                print(Fore.YELLOW + '\nLast conversation forgotten.\n')
                continue
            elif prompt.lower().startswith('/memorize'):
                memory_content = prompt[9:].strip()
                embedding = ollama.embeddings(model='nomic-embed-text', prompt=memory_content)['embedding']
                store_conversation(memory_content, "Memory stored.", embedding)
                print(Fore.YELLOW + '\nMemory stored successfully.\n')
                continue
            else:
                messages.append({"role": "user", "content": prompt})
            
            # Add task to queue
            task_queue.put(messages.copy())
            
            print(Fore.YELLOW + "Processing your request...")
            
            # Wait for result
            while result_queue.empty():
                time.sleep(0.1)
            
            response = result_queue.get()
            print(Fore.LIGHTGREEN_EX + '\nASSISTANT:')
            print(response + '\n')
            
            messages.append({"role": "assistant", "content": response})
            
            try:
                embedding = ollama.embeddings(model='nomic-embed-text', prompt=prompt)['embedding']
                store_conversation(prompt, response, embedding)
            except Exception as e:
                print(f"Error storing conversation: {e}")
    finally:
        # Stop worker thread
        task_queue.put(None)
        worker_thread.join()

if __name__ == "__main__":
    main()