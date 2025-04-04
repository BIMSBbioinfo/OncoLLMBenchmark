# structure the clinical information into symptoms, medical history, diagnostic reports, pathology results and medications for the BRCA cases

## import libraries
import pandas as pd
from tqdm import tqdm
import os
import boto3
from langchain.prompts import PromptTemplate
from langchain_aws import ChatBedrock
import time

## import function
from functions.claude_response import get_claude_result


## define prompt to structure the clinical information of the BRCA cases into symptoms, medical history, diagnostic reports, pathology results and medications
prompt= """You are a cancer registrar tasked with extracting specific clinical information from the provided unstructured text for a tumor board.
At first, you will analyze the text to have an overview of the information.
Then, please extract the information according to the following sections:
1. Presenting Symptoms and Events: Extract details of the symptoms and events leading up to the patient’s current medical concern in a text (e.g. history of present illness, Oncology History).
2. Medical History: Extract information about the patient’s medical history, including:
    * Medical History, Surgical History, Gynecological History, Family History, Allergies.
3. Diagnostic Reports: Extract any available diagnostic reports, including:
    * Imaging: Extract relevant results from imaging studies.
    * Genetic Tests: Extract significant findings from any genetic tests conducted.
    * Lab Results: Mention pertinent lab results, including ranges for normal values where present.
4. Pathology Results: Extract critical results from pathology reports.
5. Medications: Extract Medication that are critical to the case.
It is of utmost importance to ensure that all extracted information aligns exactly with the original text. Keep terminologies, symbols, and signs exactly as they appear in the text. Please deliver the extracted information according to the guidelines above and between <start> and <end> tag, without introduction lines. The patient’s case details are provided here: {text}."""


prompt_chain = PromptTemplate(template=prompt, input_variables=["text"])

client = boto3.client(service_name="bedrock-runtime", region_name=str("us-east-1"))

## Claude Sonnet 3.5
llm_claude35 = ChatBedrock(model_id="anthropic.claude-3-5-sonnet-20240620-v1:0", model_kwargs={"temperature": 0, "max_tokens":6000}, client=client)

chain_cl35 = prompt_chain | llm_claude35

tqdm.pandas()

## load data
df = pd.read_csv("/brca_unstructured_plan_split.csv")

if 'clinical_case_structured' not in df.columns:
    df['clinical_case_structured'] = None

df.loc[:, "clinical_case_structured"] = df.progress_apply(lambda row: get_claude_result(row, chain_cl35, "clinical_case"), axis = 1)
df.to_csv("brca_structured.csv", index = False)