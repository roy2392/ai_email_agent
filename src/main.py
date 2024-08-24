import os
import csv
import json
from dotenv import find_dotenv, load_dotenv
from openai import OpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationSummaryBufferMemory
from langchain.schema import SystemMessage
from custom_tools import CreateEmailDraftTool, GenerateEmailResponseTool, ReplyEmailTool, EscalateTool, ProspectResearchTool, CategoriseEmailTool
from email_cleaning import parse_email, process_csv

# Load environment variables
load_dotenv(find_dotenv())

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize LangChain agent
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

system_message = SystemMessage(
    content="""
    You are an email inbox assistant of an AI youtube channel called "AI Jason",
    who is creating AI educational content,
    Your goal is to handle all the incoming emails by categorising them based on
    guideline and decide on next steps
    """
)

tools = [
    CategoriseEmailTool(),
    ProspectResearchTool(),
    EscalateTool(),
    ReplyEmailTool(),
    CreateEmailDraftTool(),
    GenerateEmailResponseTool(),
]

agent_kwargs = {
    "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
    "system_message": system_message,
}
memory = ConversationSummaryBufferMemory(
    memory_key="memory", return_messages=True, llm=llm, max_token_limit=1000)

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
    agent_kwargs=agent_kwargs,
    memory=memory,
)

if __name__ == '__main__':
    input_csv_path = '../data/Sent.csv'
    output_csv_path = '../data/Sent_processed.csv'
    process_csv(input_csv_path, output_csv_path)

    test_email = """
    xxxxxxx
    """
    agent({"input": test_email})