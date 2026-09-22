import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents  import create_agent
from src.tools.tools import web_search, scrape_url

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("Thiếu GOOGLE_API_KEY trong file .env!")

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0.2,  
)

# Search Agent
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search]
    )

# Reader Agent
def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url]
    )

# Writer Chain
writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert research writer. Your task is to synthesize the gathered research into a comprehensive, structured, and insightful report.\n\n"
        "STRICT LANGUAGE & FORMATTING RULES:\n"
        "1. Always respond in the SAME LANGUAGE as the user's topic (e.g., if the topic is in Vietnamese, write the entire report in natural, professional Vietnamese).\n"
        "2. Preserve all source URLs accurately. Do not invent or modify URLs.\n"
        "3. Output clean Markdown with well-formatted headings and bullet points."
    ),
    (
        "human",
        "Write a detailed research report on the topic below.\n\n"
        "Topic: {topic}\n\n"
        "Research Gathered:\n{research}\n\n"
        "Structure the report as:\n"
        "- Introduction\n"
        "- Key Findings (at least 3 detailed, well-explained points)\n"
        "- Conclusion\n"
        "- Sources (list all extracted URLs)\n\n"
        "Ensure the response is detailed, factual, and written in the language of the topic."
    )
])
writer_chain = writer_prompt | llm | StrOutputParser()

# Critic Chain
critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a sharp, constructive, and objective research critic. Be honest, rigorous, and specific.\n\n"
        "LANGUAGE RULE:\n"
        "- Always write your evaluation in the SAME LANGUAGE as the provided report (e.g., if the report is in Vietnamese, write the evaluation in natural, professional Vietnamese)."
    ),
    (
        "human",
        "Review the research report below and evaluate it strictly.\n\n"
        "Report:\n{report}\n\n"
        "Respond in this exact format:\n\n"
        "Score: X/10\n\n"
        "Strengths:\n"
        "- ...\n"
        "- ...\n\n"
        "Areas to Improve:\n"
        "- ...\n"
        "- ...\n\n"
        "One line verdict:\n"
        "..."
    )
])

critic_chain = critic_prompt | llm | StrOutputParser()

# Rewrite Chain 
rewrite_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an elite research editor and writer. Your job is to take an initial draft and the critical feedback it received, "
        "then rewrite and polish the report into a flawless, definitive final version.\n\n"
        "STRICT RULES:\n"
        "1. Address and fix every weak point mentioned in the critic's 'Areas to Improve'.\n"
        "2. Retain all strong points, factual depth, and valid citation URLs.\n"
        "3. Output in the SAME LANGUAGE as the draft (Vietnamese if the draft is Vietnamese).\n"
        "4. Output clean, publication-ready Markdown."
    ),
    (
        "human",
        "Please rewrite and improve the draft report based on the critic's feedback.\n\n"
        "Original Topic: {topic}\n\n"
        "Draft Report:\n{report}\n\n"
        "Critic Feedback:\n{feedback}\n\n"
        "Write the improved final report now:"
    )
])

rewrite_chain = rewrite_prompt | llm | StrOutputParser()