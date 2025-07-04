from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langserve import add_routes
import uvicorn
import os
from dotenv import load_dotenv
load_dotenv()

#getting groq api key
groq_api_key = os.getenv('GROQ_API_KEY')
model = ChatGroq(model = 'gemma2-9b-it', groq_api_key = groq_api_key)

#prompt template
system_teplate = "Translate the following into {language}"
prompt_tepmlate = ChatPromptTemplate.from_messages([
    ('system', system_teplate),
    ('user', "{text}")
])

parser = StrOutputParser()
#chain
chain = prompt_tepmlate|model|parser

# App defination
app = FastAPI(
    title = "Langchain Server",
    version = "1.0",
    description = "A simple API server using Langchain runnable interfaces"
)

# Adding chain routes
add_routes(
    app,
    chain,
    path = "/chain"
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port = 8000)

