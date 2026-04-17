def enrich_company(company):
	return {
		**company,
		"industry": "SaaS / Tech",
		"description": f"{company['name']} is a software company.",
		"pain_point": "Improving user acquisition and onboarding",
	}
