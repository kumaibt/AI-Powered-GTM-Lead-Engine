from groq import Groq
import os

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def generate_email(company):
	score = company.get("score", 50)

	if score >= 80:
		tone = "direct and high-confidence"
	elif score >= 60:
		tone = "friendly and value-focused"
	else:
		tone = "light networking, low pressure"


	prompt = f"""
Write a short cold outreach email.

Company: {company['name']}
Industry: {company['industry']}
Score: {score}/100
Tone: {tone}
Pain point: {company['pain_point']}

Rules:
- under 120 words
- personalized look
- no spammy language
"""

	response = client.chat.completions.create(
		model="llama-3.1-8b-instant",
		messages=[
			{"role": "user", "content": prompt}
		]
	)

	return response.choices[0].message.content
