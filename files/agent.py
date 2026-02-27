"""
Hyper-Local Food Trend Agent
Scrapes social media trends, identifies viral food items, and suggests weekend specials.
"""

import json
import random
from datetime import datetime, timedelta
from typing import Optional
import anthropic

# ── Mock scraper (replace with real scraping logic) ──────────────────────────

MOCK_POSTS = [
    # Instagram-style posts
    {"platform": "instagram", "text": "Obsessed with this truffle butter pasta at La Nonna! #food #truffle #pasta #foodie", "likes": 1240, "location": "Downtown"},
    {"platform": "instagram", "text": "Birria tacos are EVERYTHING right now 🔥 #birria #tacos #mexicanfood", "likes": 3400, "location": "Eastside"},
    {"platform": "instagram", "text": "Korean corn dogs > everything. Change my mind. #koreancorndog #streetfood", "likes": 2100, "location": "Koreatown"},
    {"platform": "instagram", "text": "Smash burgers with wagyu beef — this weekend's obsession #wagyu #smashburger", "likes": 1870, "location": "Westside"},
    {"platform": "instagram", "text": "Can't stop thinking about that miso caramel croissant #croissant #fusion #bakery", "likes": 4500, "location": "Northside"},
    {"platform": "twitter", "text": "birria tacos > all tacos. fight me", "likes": 890, "location": "City Center"},
    {"platform": "twitter", "text": "every restaurant needs a smash burger option. it's the law.", "likes": 560, "location": "Westside"},
    {"platform": "twitter", "text": "miso + caramel is the combo i didn't know i needed", "likes": 1200, "location": "Northside"},
    {"platform": "tiktok", "text": "Making viral Dubai chocolate at home #dubai #chocolate #viral #foodtok", "likes": 45000, "location": "Suburbs"},
    {"platform": "tiktok", "text": "Birria ramen fusion — the collab nobody asked for but everyone needed #fusion #ramen", "likes": 22000, "location": "Eastside"},
    {"platform": "tiktok", "text": "smash burger tutorial blew up 🍔 #smashburger #burger #foodtok", "likes": 31000, "location": "Westside"},
    {"platform": "tiktok", "text": "truffle everything is back. truffle fries, truffle pasta, truffle butter #truffle", "likes": 18000, "location": "Downtown"},
    {"platform": "yelp", "text": "The wagyu smash burger was incredible. Worth every penny.", "likes": 45, "location": "Westside"},
    {"platform": "yelp", "text": "Birria tacos — crispy, cheesy, and the consommé was perfect for dipping.", "likes": 67, "location": "Eastside"},
    {"platform": "yelp", "text": "Dubai chocolate dessert — unique and absolutely delicious.", "likes": 89, "location": "Suburbs"},
]

def scrape_local_trends(location: Optional[str] = None) -> list[dict]:
    """Simulate scraping local social media for food trends."""
    posts = MOCK_POSTS.copy()
    if location:
        posts = [p for p in posts if location.lower() in p["location"].lower()] or posts
    # Add some randomness to simulate live data
    for post in posts:
        post["likes"] += random.randint(-100, 500)
        post["scraped_at"] = datetime.now().isoformat()
    return posts


# ── Trend Analyzer ────────────────────────────────────────────────────────────

def analyze_trends(posts: list[dict]) -> dict:
    """Extract trending ingredients and dishes from scraped posts."""
    keywords = {}
    for post in posts:
        text = post["text"].lower()
        weight = post["likes"]
        # Simple keyword extraction
        food_terms = [
            "birria", "truffle", "wagyu", "smash burger", "miso", "caramel",
            "croissant", "tacos", "ramen", "korean corn dog", "dubai chocolate",
            "pasta", "burger", "chocolate", "fusion"
        ]
        for term in food_terms:
            if term in text:
                keywords[term] = keywords.get(term, 0) + weight

    sorted_trends = sorted(keywords.items(), key=lambda x: x[1], reverse=True)
    return {
        "top_ingredients": [k for k, v in sorted_trends[:5]],
        "all_scores": dict(sorted_trends),
        "total_posts_analyzed": len(posts),
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
        "weekend": (datetime.now() + timedelta(days=(5 - datetime.now().weekday()))).strftime("%B %d"),
    }


# ── LLM Dish Suggester ────────────────────────────────────────────────────────

def suggest_dishes(trends: dict, restaurant_type: str = "casual dining") -> dict:
    """Use Claude to generate dish suggestions based on trends."""
    client = anthropic.Anthropic()

    prompt = f"""You are a creative restaurant consultant helping design weekend specials.

Based on these local social media food trends:
- Top trending items: {', '.join(trends['top_ingredients'])}
- Trend scores: {json.dumps(trends['all_scores'], indent=2)}
- Weekend target: {trends['weekend']}
- Restaurant type: {restaurant_type}

Generate 4 creative weekend special dish suggestions that:
1. Incorporate the top trending ingredients/themes
2. Feel fresh and exciting but achievable
3. Have catchy names that will resonate on social media
4. Include a brief description and suggested price range

Return ONLY valid JSON in this exact format:
{{
  "dishes": [
    {{
      "name": "Dish Name",
      "description": "Brief appetizing description",
      "trending_element": "which trend it capitalizes on",
      "price_range": "$XX-$XX",
      "social_hook": "Instagram caption idea"
    }}
  ],
  "marketing_headline": "Weekend specials headline",
  "key_insight": "One sentence on why these trends are hot right now"
}}"""

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text.strip()
    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


# ── Weekly Report Generator ───────────────────────────────────────────────────

def generate_weekly_report(trends: dict, suggestions: dict) -> str:
    """Generate a markdown weekly trend report."""
    lines = [
        f"# 🍽️ Weekly Food Trend Report — {trends['analysis_date']}",
        f"\n## Weekend Special Focus: {trends['weekend']}",
        f"\n**Posts Analyzed:** {trends['total_posts_analyzed']}",
        f"\n---\n",
        "## 📈 Top Trending Ingredients & Dishes",
    ]
    for item, score in list(trends["all_scores"].items())[:5]:
        lines.append(f"- **{item.title()}** — Engagement Score: {score:,}")

    lines += [
        "\n---\n",
        "## 🍴 Weekend Special Recommendations",
        f"\n> {suggestions['marketing_headline']}\n",
    ]
    for i, dish in enumerate(suggestions["dishes"], 1):
        lines += [
            f"### {i}. {dish['name']} ({dish['price_range']})",
            f"{dish['description']}",
            f"- 🔥 Trend: *{dish['trending_element']}*",
            f"- 📸 Social Hook: *\"{dish['social_hook']}\"*\n",
        ]

    lines += [
        "---",
        f"## 💡 Key Insight",
        f"\n{suggestions['key_insight']}",
        f"\n\n*Report generated by Hyper-Local Food Trend Agent*"
    ]
    return "\n".join(lines)


# ── Main Orchestrator ─────────────────────────────────────────────────────────

def run_agent(location: Optional[str] = None, restaurant_type: str = "casual dining") -> dict:
    """Full agent pipeline: scrape → analyze → suggest → report."""
    print(f"🔍 Scraping local social media trends{' in ' + location if location else ''}...")
    posts = scrape_local_trends(location)

    print(f"📊 Analyzing {len(posts)} posts for trending food items...")
    trends = analyze_trends(posts)

    print(f"🤖 Consulting LLM for dish suggestions...")
    suggestions = suggest_dishes(trends, restaurant_type)

    print(f"📝 Generating weekly report...")
    report = generate_weekly_report(trends, suggestions)

    return {
        "trends": trends,
        "suggestions": suggestions,
        "report": report,
        "posts_sample": posts[:5]
    }


if __name__ == "__main__":
    result = run_agent(location="Downtown", restaurant_type="bistro")
    print("\n" + "="*60)
    print(result["report"])
    print("="*60)
    print("\n✅ Agent run complete!")
