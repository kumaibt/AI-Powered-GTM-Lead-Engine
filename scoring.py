def score_lead(company):

	score = 50

	industry = company.get("industry", "").lower()
	name = company.get("name", "").lower()

	if "saas" in industry or "tech" in industry:
		score += 20

	if any(x in name for x in ["stripe", "notion", "shopify"]):
		score += 20

	if "software" in company.get("description", "").lower():
		score += 10

	if "small" in industry:
		score -= 15

	return max(0, min(100, score))
