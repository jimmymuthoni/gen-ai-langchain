from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langserve import add_routes
import os
import uvicorn
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv("QROQ_API_KEY")
model = ChatGroq(model = "Gemma2-9b-It", groq_api_key=groq_api_key)


#creating prompt template
system_template = "Translate the following into language {language}"
prompt_template = ChatPromptTemplate([
    ("system", system_template),
    ("user", '{text}')

])

parser = StrOutputParser()
chain = prompt_template | model | parser

## App defination
app = FastAPI(title='Langchain Server',
              version="1.0",
              description='A simple API server using langchain runnable interfaces',
              openapi_url = None 
              )

add_routes(
    app,
    chain,
    path = "/chain"
)
  
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)


