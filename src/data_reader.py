import pandas as pd

df = pd.read_csv("./data/resume_data.csv")
df = df.drop(
    columns=[
        "address",
        "career_objective",
        "passing_years",
        "educational_results",
        "result_types",
        "major_field_of_studies",
        "company_urls",
        "start_dates",
        "end_dates",
        "locations",
        "responsibilities",
        "extra_curricular_activity_types",
        "extra_curricular_organization_names",
        "extra_curricular_organization_links",
        "role_positions",
        "online_links",
        "issue_dates",
        "expiry_dates",
        "languages",
        "proficiency_levels",
        "certification_providers",
        "certification_skills",
        "professional_company_names",
        "educationaL_requirements",
        "experiencere_requirement",
        "age_requirement",
        "responsibilities.1",
        "skills_required",
        "﻿job_position_name",
        "related_skils_in_job",
    ]
)
df.dropna(inplace=True)
print(df.head())
