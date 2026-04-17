import csv
import json
import statistics
from pathlib import Path

from email_generator import generate_email
from scoring import score_lead


OUTPUT_DIR = Path("benchmark_results")
OUTPUT_DIR.mkdir(exist_ok=True)

INDUSTRIES = [
    "SaaS / Tech",
    "Fintech",
    "E-commerce Software",
    "Developer Tools",
    "HR Tech",
    "Health Tech",
    "EdTech",
    "Cybersecurity",
    "Marketing Tech",
    "Productivity Software",
]

PAIN_POINTS = [
    "Improving user acquisition and onboarding",
    "Reducing churn during the first 30 days",
    "Driving more product-qualified leads",
    "Increasing demo-to-trial conversion",
    "Improving activation for self-serve users",
    "Scaling outbound personalization without manual research",
    "Shortening sales cycles for mid-market prospects",
    "Improving retention for new enterprise accounts",
    "Increasing expansion revenue from existing customers",
    "Re-engaging dormant trial users",
]

COMPANY_NAMES = [
    "Stripe", "Notion", "Shopify", "Figma", "Airtable", "Miro", "Webflow", "Rippling", "Zapier", "Clerk",
    "Vercel", "Linear", "Canva", "Brex", "Asana", "Gusto", "Snyk", "Datadog", "HubSpot", "Intercom",
    "Amplitude", "Mixpanel", "Segment", "Plaid", "Mercury", "Retool", "ClickUp", "Monday", "Loom", "Deel",
    "Ramp", "Coda", "Attio", "Apollo", "Gong", "Outreach", "OpenPhone", "Typeform", "Calendly", "Notable",
    "Pendo", "Drata", "PostHog", "Supabase", "Replit", "Anthropic", "Perplexity", "Carta", "Clari", "Salesloft",
    "Cloudflare", "Twilio", "Okta", "Maven", "Teachable", "Kajabi", "Mural", "Lucid", "Deel Engage", "Airbyte",
]


def build_scenarios(limit: int = 60):
    scenarios = []
    for idx in range(limit):
        company = {
            "name": COMPANY_NAMES[idx % len(COMPANY_NAMES)],
            "website": f"{COMPANY_NAMES[idx % len(COMPANY_NAMES)].lower().replace(' ', '')}.com",
            "industry": INDUSTRIES[idx % len(INDUSTRIES)],
            "description": f"{COMPANY_NAMES[idx % len(COMPANY_NAMES)]} builds software for modern teams.",
            "pain_point": PAIN_POINTS[idx % len(PAIN_POINTS)],
        }
        company["score"] = score_lead(company)
        scenarios.append(company)
    return scenarios


def run_benchmark(limit: int = 60):
    scenarios = build_scenarios(limit)
    rows = []

    for idx, scenario in enumerate(scenarios, start=1):
        generated = generate_email(scenario)
        rows.append(
            {
                "scenario_id": idx,
                "company": scenario["name"],
                "industry": scenario["industry"],
                "pain_point": scenario["pain_point"],
                "score": scenario["score"],
                "latency_ms": generated["latency_ms"],
                "model": generated["model"],
                "prompt": generated["prompt"],
                "email": generated["email"],
            }
        )
        print(f"[{idx}/{limit}] {scenario['name']} - {generated['latency_ms']} ms")

    csv_path = OUTPUT_DIR / "prompt_benchmark_results.csv"
    json_path = OUTPUT_DIR / "prompt_benchmark_results.json"
    summary_path = OUTPUT_DIR / "prompt_benchmark_summary.json"

    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    with json_path.open("w", encoding="utf-8") as json_file:
        json.dump(rows, json_file, indent=2)

    summary = {
        "scenarios_tested": len(rows),
        "average_latency_ms": round(statistics.mean(r["latency_ms"] for r in rows), 2),
        "median_latency_ms": round(statistics.median(r["latency_ms"] for r in rows), 2),
        "max_latency_ms": round(max(r["latency_ms"] for r in rows), 2),
        "min_latency_ms": round(min(r["latency_ms"] for r in rows), 2),
        "model": rows[0]["model"],
    }

    with summary_path.open("w", encoding="utf-8") as summary_file:
        json.dump(summary, summary_file, indent=2)

    print("\nSaved:")
    print(csv_path)
    print(json_path)
    print(summary_path)
    print("\nResume-safe metric:")
    print(f"Tested {summary['scenarios_tested']} prompt scenarios with average latency of {summary['average_latency_ms']} ms.")


if __name__ == "__main__":
    run_benchmark(limit=60)