# This script processes a the note text of each BRCA patient case and splits each note into clinical notes and assessment/plan

## import libraries
import re
import pandas as pd


## import functions
## import functions
from functions.split_assessmentplan import split_note_text
from functions.split_assessmentplan import split_note_text_manual


## load data
df = pd.read_csv("/coral-expert-curated-medical-oncology-reports-to-advance-language-model-inference-1.0/coral/unannotated/data/breastca_unannotated.csv")

## Patterns to look for, converted to lowercase
patterns = ["assessment / plan", "assessment and plan", "assessment & plan", "assessment \\plan",
            "assessment and recommendations", "assessment/plan"]


## Apply the function to each row and create new columns
df[['clinical_case', 'assessment_plan']] = df['note_text'].apply(lambda x: pd.Series(split_note_text(x, patterns)))

## Check which rows need manual splitting
mask = (df["assessment_plan"]=="")
df[mask].index

## String "IMP "
indices = [6, 14, 17, 18, 56]
split_note_text_manual(df,indices, "IMP ")

## String "IMPRESSION"
indices = [16, 82]
split_note_text_manual(df, indices, "IMPRESSION")

## String "Assessment:"
indices = [20, 33, 34, 41, 52, 54, 61, 72, 86]
split_note_text_manual(df, indices, "Assessment:")

## String "ASSESSMENT:"
indices = [46]
split_note_text_manual(df, indices, "ASSESSMENT:")

## String "A/P"
indices = [59, 85, 89, 96]
split_note_text_manual(df, indices, "A/P")

## String "Additional Note & Follow-Up:"
indices = [50]
split_note_text_manual(df, indices, "Additional Note & Follow-Up:")

## Check which rows need manual splitting
mask = (df["assessment_plan"]=="")
df[mask].index

df.to_csv("/brca_unstructured_plan_split.csv", index = False)