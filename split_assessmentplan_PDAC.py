# This script processes a the note text of each PDAC patient case and splits each note into clinical notes and assessment/plan

## import libraries
import re
import pandas as pd

## import functions
from functions.split_assessmentplan import split_note_text
from functions.split_assessmentplan import split_note_text_manual


## load CORAL dataset
df = pd.read_csv("/coral-expert-curated-medical-oncology-reports-to-advance-language-model-inference-1.0/coral/unannotated/data/pdac_unannotated.csv")


# Patterns to look for, converted to lowercase
patterns = ["assessment and plan", "ASSESSMENT & PLAN", "Impression and Recommendations:", "ASSESSMENT/PLAN:", "Assessment/Plan", "IMPRESSION/PLAN", "Impression and Plan", "assessment:"]

# Apply the function to each row and create new columns
df[['clinical_case', 'assessment_plan']] = df['note_text'].apply(lambda x: pd.Series(split_note_text(x, patterns)))

## Check which rows need manual splitting
mask = (df["assessment_plan"]=="")
df[mask].index

## String "IMP "
indices = [63]
split_note_text_manual(df,indices, "IMPRESSION")

indices = [21]
split_note_text_manual(df, indices, "Assessment")

df.to_csv("/pdac_unstructured_plan_split.csv", index = False)