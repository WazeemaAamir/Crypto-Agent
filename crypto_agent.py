import os
import requests
from openai import AsyncOpenAI
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("⚠️ OPENAI_API_KEY is not set in your .env file!")

# Initialize OpenAI client
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# Function to fetch crypto price from CoinGecko
def get_crypto_price(symbol="bitcoin"):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data.get(symbol, {}).get("usd", None)

# AI-powered crypto agent
async def crypto_agent(query: str):
    # Ask OpenAI to reason about the query
    ai_response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful crypto assistant."},
            {"role": "user", "content": query}
        ]
    )
    return ai_response.choices[0].message.content

# Example usage
async def main():
    btc_price = get_crypto_price("bitcoin")
    print(f"💰 Current BTC Price: ${btc_price}")

    response = await crypto_agent("What do you think about Bitcoin price trends?")
    print("🤖 Agent:", response)

if __name__ == "__main__":
    asyncio.run(main())
