# LLM Benchmark for Oncology Treatment Planning
This repository contains the code to create the curated dataset from the original CORAL: expert-Curated medical Oncology Reports to Advance Language model inference provided by Physionet.

## Generate the dataset from the CORAL dataset
Download the following datasets:\
CORAL-Dataset: https://physionet.org/content/curated-oncology-reports/1.0/

We used the unannotated files:\
- breast cancer: brca_unannotated.csv
- pancretic cancer: pdac_unannotated.csv

To seperate the assessment and treatment plans from the rest of the clinical notes of the unstructured notes ```note_text``` run the following .py files:\
```split_assessmentplan_BRCA.py```\
```split_assessmentplan_PDAC.py```

This results into a column "clinical_case" and a column "assessment_plan"

Both columns were further structured using Claude 3.5 Sonnet to extract relevant information without changing the original text using the following .py files:\
to structure the clinical_case column:\
```structure_BRCA.py```\
```structure_PDAC.py```

to structure the assessment_plan column:\
```structure_plan_BRCA.py```\
```structure_plan_PDAC.py```


