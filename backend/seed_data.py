import requests
import time
import sys
import asyncio
import asyncpg
import os

# Добавляем корневую директорию в sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from app.config import DATABASE_URL


async def seed_data():
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute("INSERT INTO products (name, price) VALUES ($1, $2)", "Test Product", 100.0)
    await conn.close()


def wait_for_server(url, max_attempts=10, delay=5):
    attempts = 0
    while attempts < max_attempts:
        try:
            response = requests.get(url, timeout=5)
            print(f"Server response status: {response.status_code}")
            if response.status_code == 200:
                return True
        except requests.exceptions.ConnectionError as e:
            attempts += 1
            print(f"Attempt {attempts}/{max_attempts} failed: {e}")
            time.sleep(delay)
    print(f"Max retries exceeded. Exiting.")
    sys.exit(1)


if __name__ == "__main__":
    url = "http://localhost:8000/api/products"
    if wait_for_server(url):
        asyncio.run(seed_data())
        response = requests.get(url)
        print(f"Seed response: {response.status_code} - {response.text}")
    else:
        sys.exit(1)
