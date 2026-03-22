from typing import Literal
from pydantic import BaseModel, Field
from google.adk.agents.llm_agent import Agent

class FinancialAnalysisResponse(BaseModel):
    company_name: str = Field(description="The full name of the primary company mentioned.")
    ticker_symbol: str = Field(description="The official stock ticker symbol (e.g., RELIANCE, AAPL). If none, output 'UNKNOWN'.")
    exchange: Literal["NSE", "BSE", "NASDAQ", "NYSE", "GLOBAL", "UNKNOWN"] = Field(
        description="Detect the stock exchange based on context (e.g., mentions of INR, RBI, or Indian cities usually imply NSE/BSE)."
    )
    sector: str = Field(description="The market sector (e.g., FinTech, Energy, E-Commerce).")
    
    sentiment: Literal["Bullish", "Bearish", "Neutral"] = Field(
        description="The overall market sentiment derived from the text."
    )
    confidence: Literal["High", "Medium", "Low"] = Field(
        description="How confident you are in this classification."
    )
    rationale: str = Field(
        description="Strictly one sentence explaining your sentiment choice."
    )

system_instruction = """
You are an elite dual-purpose Financial Analyst API. 
When given a financial news snippet, you must perform two tasks in order:

TASK 1 - EXTRACTION: 
Identify the primary company, their stock ticker, and their market sector. 
Crucially, use context clues (currency, regulatory bodies, geography) to determine if they trade on an Indian exchange (NSE/BSE) or a US exchange (NASDAQ/NYSE).

TASK 2 - SENTIMENT: 
Analyze the market sentiment (Bullish, Bearish, Neutral) based on the text provided.
"""

root_agent = Agent(
    model='gemini-2.5-flash',
    name='financial_analyst_agent',
    description='Extracts market data and classifies financial news sentiment.',
    instruction=system_instruction,
    output_schema=FinancialAnalysisResponse,
)