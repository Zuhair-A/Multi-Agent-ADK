import datetime
import re
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
import yfinance as yf

# =========================================================================
# 1. DEFINE CORE TOOLS (With output cleaning filters)
# =========================================================================

def respond_to_user(message: str) -> str:
    """
    Use this tool for general chat, greetings, pleasantries, or questions 
    that do NOT involve looking up stocks or the current time.

    Args:
        message (str): The conversational response to send back to the user. Do not include raw json or tags.
    """
    clean_text = str(message)
    
    # Aggressively strip out any structural model artifacts like <|python_tag|> or json dumps
    clean_text = re.sub(r'<\|.*?\|>', '', clean_text)
    clean_text = re.sub(r'\{.*?"name".*?\}', '', clean_text)
    
    # Fallback default text if it tried to return ONLY a leaked token block
    if not clean_text.strip():
        return "I am doing well, thank you! How can I help you today?"
        
    return clean_text.strip()


def get_current_time() -> str:
    """
    Use this tool ONLY when the user explicitly asks for the current time, 
    the clock, or today's date.
    """
    now = datetime.datetime.now()
    return f"The current date and time is: {now.strftime('%Y-%m-%d %H:%M:%S')}"


def get_stock_price(ticker: str) -> str:
    """
    Use this tool ONLY when the user explicitly asks for a company's stock price,
    market valuation, or provides a financial ticker symbol (e.g., AAPL, IBM, DELL).

    Args:
        ticker (str): The stock ticker symbol.
    """
    if not ticker or len(str(ticker).strip()) < 1:
        return "Please provide a valid stock ticker symbol."
        
    try:
        clean_ticker = str(ticker).strip().split()[-1].replace("'", "").replace('"', '').upper()
        stock = yf.Ticker(clean_ticker)
        info = stock.info
        price = info.get('currentPrice') or info.get('regularMarketPrice')
        
        if price:
            return f"The current stock price of {clean_ticker} is ${price:.2f}."
        return f"Could not find market data for ticker '{clean_ticker}'."
    except Exception:
        return "Stock data is currently unavailable."

# =========================================================================
# 2. THE SINGULAR UTILITY ASSISTANT
# =========================================================================

base_agent = Agent(
    model=LiteLlm(model="ollama_chat/llama3.2:latest"),
    name='utility_assistant',
    description='An assistant that handles chat, time queries, and stock tracking.',
    instruction=(
        "You are an automated utility assistant. You must process every user message by picking the matching tool:\n"
        "1. For general greetings or chat (like 'Hi', 'How are you?'), use `respond_to_user`.\n"
        "2. For the clock or date, use `get_current_time`.\n"
        "3. For market prices or stock symbols, use `get_stock_price`.\n\n"
        "CRITICAL RULES:\n"
        "- Never output special internal tags like '<|python_tag|>' or raw JSON text.\n"
        "- When using the `respond_to_user` tool, only provide standard, conversational prose sentence words inside the message field."
    ),
    tools=[respond_to_user, get_current_time, get_stock_price]
)

root_agent = base_agent