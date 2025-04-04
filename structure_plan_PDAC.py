# structure the treatment plan for the PDAC cases to extract the relevant information without changing the original text

## import libraries
import pandas as pd
from tqdm import tqdm
import os
import boto3
from langchain.prompts import PromptTemplate
from langchain_aws import ChatBedrock

## import function
from functions.claude_response import get_claude_result

# define the prompt to structure the treatment plan for the PDAC cases to extract the relevant information without changing the original text
prompt= """You are an expert medical writer tasked with restructuring and condensing a text about patient assessment and treatment plans for a tumor board. Your goal is to create a concise, well-organized text that clinicians can quickly review. Follow these guidelines:

1. Condense the information without omitting critical details.
2. It is of utmost importance to ensure that all extracted information aligns exactly with the original text.
3. Keep terminologies, symbols, and signs exactly as they appear in the text.
4. Limit the entire text to no more than 200 words.
5. If the task cannot be done, return the following: "I cannot help you with this case."
Deliver the extracted information according to the guidelines above, without introduction lines. The patient’s assessment and treatment plan are provided here: {text}."""

prompt_chain = PromptTemplate(template=prompt, input_variables=["text"])


client = boto3.client(service_name="bedrock-runtime", region_name=str("us-east-1"))

## Claude Sonnet 3.5
llm_claude35 = ChatBedrock(model_id="anthropic.claude-3-5-sonnet-20240620-v1:0", model_kwargs={"temperature": 0, "max_tokens":6000}, client=client)

chain_cl35 = prompt_chain | llm_claude35


tqdm.pandas()

## load data
df = pd.read_csv("/pdac_structured.csv")

if 'ass_plan_structured' not in df.columns:
    df['ass_plan_structured'] = None

df.loc[:, "ass_plan_structured"] = df.progress_apply(lambda row: get_claude_result(row, chain_cl35, "assessment_plan"), axis = 1)
df.to_csv("pdac_ass_plan_structured.csv", index = False)