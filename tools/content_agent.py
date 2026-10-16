import json
import asyncio

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


analysis_file = "output/analysis_results.json"


with open(
    analysis_file,
    "r",
    encoding="utf-8"
) as file:

    analysis_results = json.load(file)


print("Analysis results loaded successfully.")



root_agent = Agent(
    name="novaretail_content_agent",

    model="gemini-2.5-flash-lite",

    description=(
        "Creates executive PowerPoint content "
        "from verified NovaRetail business metrics."
    ),

    instruction="""
You are an executive business presentation analyst.

The business metrics supplied to you have already been
calculated and verified by Python.

IMPORTANT RULES:

1. Never invent any number.
2. Never change any supplied number.
3. Never recalculate supplied metrics.
4. Use only facts available in the supplied analysis.
5. Write concise executive presentation language.
6. Clearly highlight growth, deterioration and risk.
7. Generate content for exactly five slides.
8. Keep slide content concise enough for PowerPoint.

Create content for:

Slide 1 - Executive Summary
Slide 2 - Regional Performance
Slide 3 - Customer Experience
Slide 4 - Operational Risk
Slide 5 - Recommended Actions
"""
)

print("Google ADK agent created successfully.")
print("Agent name:", root_agent.name)

analysis_json = json.dumps(
    analysis_results,
    indent=2
)


user_prompt = f"""
Create executive slide content using the verified
NovaRetail analysis below.

IMPORTANT RULES:

1. Use only the verified data provided below.
2. Never invent any number.
3. Never modify any supplied number.
4. Never estimate missing numbers.
5. Never recalculate supplied metrics.
6. Keep the language concise and executive-friendly.
7. Return VALID JSON ONLY.
8. Do not include Markdown or code fences.
9. Generate exactly five slides.

Return exactly this JSON structure:

{{
    "slide_1": {{
        "title": "",
        "review_period": "",
        "kpi_1": {{
            "value": "",
            "label": ""
        }},
        "kpi_2": {{
            "value": "",
            "label": ""
        }},
        "kpi_3": {{
            "value": "",
            "label": ""
        }},
        "executive_summary": ""
    }},

    "slide_2": {{
        "headline": "",
        "insights": [
            "",
            "",
            ""
        ]
    }},

    "slide_3": {{
        "headline": "",
        "insights": [
            "",
            "",
            ""
        ]
    }},

    "slide_4": {{
        "headline": "",
        "insights": [
            "",
            "",
            ""
        ]
    }},

    "slide_5": {{
        "headline": "",
        "actions": [
            "",
            "",
            ""
        ],
        "forward_looking_statement": ""
    }}
}}

VERIFIED DATA:

{analysis_json}
"""


async def generate_content():

    session_service = InMemorySessionService()

    app_name = "novaretail_capstone"
    user_id = "arpit"
    session_id = "novaretail_content_session"

    await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )

    runner = Runner(
        agent=root_agent,
        app_name=app_name,
        session_service=session_service
    )

    message = types.Content(
        role="user",
        parts=[
            types.Part(
                text=user_prompt
            )
        ]
    )

    final_response = ""

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=message
    ):

        if event.content and event.content.parts:

            for part in event.content.parts:

                if getattr(part, "text", None):
                    final_response += part.text

    return final_response

async def main():

    print("\nSending verified business data to Gemini...")

    response_text = await generate_content()

    print("\nGemini response received.")

    cleaned_response = response_text.strip()

    # Remove Markdown fences if model returns them
    if cleaned_response.startswith("```json"):
        cleaned_response = cleaned_response[7:]

    elif cleaned_response.startswith("```"):
        cleaned_response = cleaned_response[3:]

    if cleaned_response.endswith("```"):
        cleaned_response = cleaned_response[:-3]

    cleaned_response = cleaned_response.strip()

    try:

        slide_content = json.loads(
            cleaned_response
        )

    except json.JSONDecodeError:

        print("\nERROR: Gemini response was not valid JSON.")

        print("\nRaw Gemini response:")
        print(response_text)

        return

    output_path = "output/slide_content.json"

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            slide_content,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nSUCCESS!")
    print("Slide content saved to:")
    print(output_path)


if __name__ == "__main__":
    asyncio.run(main())

    