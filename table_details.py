import os
from dotenv import load_dotenv

import pandas as pd
import streamlit as st
from operator import itemgetter
#from langchain.chains.openai_tools import create_extraction_chain_pydantic
from langchain_core.pydantic_v1 import BaseModel, Field
#from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate

import google.generativeai as genai

from langchain_google_genai import ChatGoogleGenerativeAI


from typing import List

load_dotenv()
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
llm = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0,convert_system_message_to_human=True)

@st.cache_data
def get_table_details():
    # Read the CSV file into a DataFrame
    table_description = pd.read_csv("database_table_descriptions.csv")
    table_docs = []

    # Iterate over the DataFrame rows to create Document objects
    table_details = ""
    for index, row in table_description.iterrows():
        table_details = table_details + "Table Name:" + row['Table'] + "\n" + "Table Description:" + row['Description'] + "\n\n"

    return table_details


class Table(BaseModel):
    """Table in SQL database."""

    name: str = Field(description="Name of table in SQL database.")

table_details = get_table_details()

prompt2 = ChatPromptTemplate.from_template(
   """
  You are a helpful Data science assistant , Your objective is to analyze the following table descriptions and Return the names of ALL the SQL tables that MIGHT be relevant to the question: {user_question}
  \n\nRemember to include ALL POTENTIALLY RELEVANT tables, even if you're not sure that they're needed.and you should return the table names as a list
  for example question : which customers made the top 5 highest payments
  the desired answer should be ['customers','payments']
  \n\nThe tables descriptions are:
  Table Name:productlines
  Table Description:Stores information about the different product lines offered by the company, including a unique name, textual description, HTML description, and image. Categorizes products into different lines.

  Table Name:products
  Table Description:Contains details of each product sold by the company, including code, name, product line, scale, vendor, description, stock quantity, buy price, and MSRP. Linked to the productlines table.

  Table Name:offices
  Table Description:Holds data on the company's sales offices, including office code, city, phone number, address, state, country, postal code, and territory. Each office is uniquely identified by its office code.

  Table Name:employees
  Table Description:Stores information about employees, including number, last name, first name, job title, contact info, and office code. Links to offices and maps organizational structure through the reportsTo attribute.

  Table Name:customers
  Table Description:Captures data on customers, including customer number, name, contact details, address, assigned sales rep, and credit limit. Central to managing customer relationships and sales processes.

  Table Name:payments
  Table Description:Records payments made by customers, tracking the customer number, check number, payment date, and amount. Linked to the customers table for financial tracking and account management.

  Table Name:orders
  Table Description:Details each sales order placed by customers, including order number, dates, status, comments, and customer number. Linked to the customers table, tracking sales transactions.

  Table Name:orderdetails
  Table Description:Describes individual line items for each sales order, including order number, product code, quantity, price, and order line number. Links orders to products, detailing the items sold.

  """
)

from typing import List, Dict
import ast

# Assuming Table is a Pydantic model or similar
class Table:
    name: str

def get_tables(output: Dict) -> List[str]:
    # Extract the 'text' field from the output, which contains the list as a string
    text_output = output.get('text', '')
    
    try:
        # Safely evaluate the string representation of the list
        tables_list = ast.literal_eval(text_output)
        # Ensure that the result is indeed a list
        if isinstance(tables_list, list):
            # Extract the table names if 'tables_list' is a list of Table objects
            # If it's already a list of strings, you can return it directly
            return [table.name if isinstance(table, Table) else table for table in tables_list]
    except (ValueError, SyntaxError):
        # Handle the case where the text output is not a valid list representation
        return []

table_chain = {"user_question": itemgetter("question")} | LLMChain(llm=llm, prompt=prompt2) | get_tables


# table_names = "\n".join(db.get_usable_table_names())
# table_details = get_table_details()
# table_details_prompt = f"""Return the names of ALL the SQL tables that MIGHT be relevant to the user question. \
# The tables are:

# {table_details}

# Remember to include ALL POTENTIALLY RELEVANT tables, even if you're not sure that they're needed."""

# table_chain = {"input": itemgetter("question")} | create_extraction_chain_pydantic(Table, llm, system_message=table_details_prompt) | get_tables