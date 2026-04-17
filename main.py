from data import companies
from enrich import enrich_company
from email_generator import generate_email
from scoring import score_lead


def run_pipeline():
	results = []

	for company in companies:
		enriched = enrich_company(company)

		score = score_lead(enriched)
		enriched["score"] = score

		email = generate_email(enriched)

		results.append({
			"company": company["name"],
			"score": score,
			"email": email
		})

		print("\n====================")
		print("Company:", company["name"])
		print("Score:", score)
		print("\nEMAIL:\n", email)

	avg_score = sum(r["score"] for r in results) / len(results)
	print("\n====================")
	print(f"Processed {len(results)} leads")
	print(f"Average score: {avg_score:.1f}")

if __name__ == "__main__":
	run_pipeline()
