from google.adk.agents.llm_agent import Agent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.agents.parallel_agent import ParallelAgent
from google.adk.runners import InMemoryRunner
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search
from google.genai import types

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)


title_researcher = Agent(
    name="TitleResearchAgent",
    model=Gemini(model="gemini-2.5-flash",retry_options=retry_config),
    instruction="""You are an advanced SEO keyword strategist.
    Use the google_search tool to identify:
    - high-performing keywords,
    - search intent,
    - trending queries,
    - competitor titles,

    all related to the user's topic.

    Output:
    1. A short summary of the search intent + trends.
    2. A list of exactly 5 high-volume, SEO-rich keywords or phrases.

    Do NOT include anything else.""",
    tools=[google_search],
    output_key="title_research",
)

title_generator = Agent(
    name="TitleGeneratorAgent",
    model=Gemini(model="gemini-2.5-flash",retry_options=retry_config),
    instruction="""Context: {title_research}

    Task: Create 5 highly clickable, SEO-optimized titles.
    Requirements:
    - Max 60 characters.
    - Must include at least one of the top keywords.
    - Prioritize high CTR, clarity, and emotional pull.
    - Avoid filler words.

    Output: ONLY a numbered list of titles (1–5), with no extra text.""",
    output_key="generated_title",
)

best_title_agent = Agent(
    name="BestTitleSelectorAgent",
    model=Gemini(model="gemini-2.5-flash",retry_options=retry_config),
    instruction="""Analyze the following title options: {generated_title}

    Task: Choose the single best title that maximizes:
    - SEO potential,
    - Click-through-rate,
    - Audience retention likelihood.

    Output: Return ONLY the chosen title text.
    No explanations, quotes, or added formatting.""",
    output_key="best_title",
)

title_agent = SequentialAgent(
    name="TitlePipeline",
    sub_agents=[title_researcher, title_generator, best_title_agent],
)

description_researcher = Agent(
    name="DescriptionResearchAgent",
    model=Gemini(model="gemini-2.5-flash",retry_options=retry_config),
    instruction="""You are a specialized agent focused on researching by using google_search tool.
Your task is to find accurate and relevant information for SEO friendly descriptions based on given topics.""",
    tools=[google_search],
    output_key="description_research",
)

description_generator = Agent(
    name="DescriptionGeneratorAgent",
    model=Gemini(model="gemini-2.5-flash",retry_options=retry_config),
    instruction="""You must generate a YouTube video description by STRICTLY following the structure below.
Do NOT add any explanations, questions, titles, headings, quotes, markdown, or extra text.
Return ONLY the final description content.

STRUCTURE (must be followed exactly in this order):

Part-1:
- Write a short, concise, SEO-friendly description of the video.
- Maximum length: 300 characters.
- Must be based ONLY on {description_research}.

(blank line)

Part-2:
- Leave placeholders ONLY for social media links in the exact format below:
insta: (add link here)
discord: (add link here)

(blank line)

Part-3:
- Write a detailed summary of the video content.
- Length: 600–700 words.
- SEO-friendly, engaging, and relevant to the target audience.
- Use ONLY the information from {description_research}.
- Do NOT invent facts or add external knowledge.

(blank line)

Part-4:
- Leave a placeholder for credits in the exact format below:
Music in this video: (add credits here)

CONSTRAINTS:
- Use ONLY {description_research} as the source of information.
- Do NOT ask questions.
- Do NOT include emojis.
- Do NOT add headings like “Part-1”, “Summary”, etc.
- Do NOT include any text before or after the description.
""",
    output_key="generated_description",
)

description_agent = SequentialAgent(
    name="DescriptionPipeline",
    sub_agents=[description_researcher, description_generator],
)

aggregator_agent = Agent(
    name="AggregatorAgent",
    model=Gemini(model="gemini-2.5-flash",retry_options=retry_config),
    instruction="""Task:
Combine the provided {best_title} and {generated_description} into ONE final output.

ABSOLUTE OUTPUT RULES (NON-NEGOTIABLE):
- Output ONLY the final formatted result.
- Do NOT add explanations, comments, questions, emojis, suggestions, or metadata.
- Do NOT rewrite, rephrase, summarize, expand, compress, or correct the title or description.
- Do NOT add any text before or after the required format.

MANDATORY FORMAT (MUST MATCH EXACTLY):
{best_title}
{generated_description}

The first line MUST be the title. The subsequent lines MUST be the description.

FAILURE CONDITIONS (ANY = INVALID OUTPUT):
- Asking questions
- Adding notes or suggestions
- Altering content in any way
- Outputting anything outside the required format
""",
    output_key="executive_summary",
)

Parallel_research_team = ParallelAgent(
    name="SequentialResearchTeam",
    sub_agents=[title_agent, description_agent],
)

root_agent = SequentialAgent(
    name="ResearchSystem",
    sub_agents=[Parallel_research_team, aggregator_agent],
)

runner = InMemoryRunner(agent=root_agent, app_name="agents")

