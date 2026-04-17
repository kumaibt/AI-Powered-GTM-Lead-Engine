from data import companies
from enrich import enrich_company
from email_generator import generate_email
from scoring import score_lead


def run_pipeline(company_list=None):
    results = []
    company_list = company_list or companies

    for company in company_list:
        enriched = enrich_company(company)
        score = score_lead(enriched)
        enriched["score"] = score
        generated = generate_email(enriched)

        results.append(
            {
                "company": company["name"],
                "score": score,
                "industry": enriched.get("industry", ""),
                "prompt": generated["prompt"],
                "email": generated["email"],
                "latency_ms": generated["latency_ms"],
                "model": generated["model"],
            }
        )

    return results


if __name__ == "__main__":
    results = run_pipeline()

    for r in results:
        print("\n====================")
        print("Company:", r["company"])
        print("Score:", r["score"])
        print("Latency (ms):", r["latency_ms"])
        print("\nEMAIL:\n", r["email"])

    avg_score = sum(r["score"] for r in results) / len(results)
    avg_latency = sum(r["latency_ms"] for r in results) / len(results)

    print("\n====================")
    print(f"Processed {len(results)} leads")
    print(f"Average score: {avg_score:.1f}")
    print(f"Average latency: {avg_latency:.2f} ms")
