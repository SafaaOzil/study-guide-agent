import os
import html
from crewai import Agent, Task, Crew
from crewai.tools import tool
from dotenv import load_dotenv
from pypdf import PdfReader
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import re

from bidi.algorithm import get_display

from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

load_dotenv()



def read_skill():
    with open("SKILL.md", "r", encoding="utf-8") as file:
        return file.read()


def extract_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text:
            pages.append({
                "page": page_number,
                "text": text
            })

    return pages


def pages_to_text(pages):
    full_text = []

    for page in pages:
        full_text.append(
            f"""
--- PAGE {page["page"]} ---
{page["text"]}
"""
        )

    return "\n".join(full_text)



def create_document_tool(pages):

    document_text = pages_to_text(pages)

    @tool("Course Material Tool")
    def course_material_tool(query: str) -> str:
        """
        Reads the uploaded course material.
        Use 'ALL' to read the entire document.
        """

        if query.strip().upper() == "ALL":
            return document_text

        query_words = query.lower().split()
        results = []

        for page in pages:
            page_text = page["text"]

            if any(
                word in page_text.lower()
                for word in query_words
            ):
                results.append(
                    f"""
PAGE {page["page"]}

{page_text}
"""
                )

        if not results:
            return "No relevant information was found in the uploaded document."

        return "\n".join(results)

    return course_material_tool



def create_study_agent(pages):

    skill = read_skill()

    document_tool = create_document_tool(pages)

    agent = Agent(
        role="Study Guide Agent",

        goal=(
            "Help students study course material by creating "
            "personalized study guides and answering questions "
            "using only the uploaded document."
        ),

        backstory=f"""
You are an AI study assistant specialized in transforming
course material into clear and useful study resources.

You must never use external knowledge when working with
the student's document.

You have a personalized study Skill that defines exactly
how study material should be prepared.

PERSONALIZED SKILL:

{skill}

Always follow this Skill when creating study material.
""",

        tools=[document_tool],

        verbose=True,

        allow_delegation=False
    )

    return agent

def generate_study_guide(pages):

    agent = create_study_agent(pages)

    task = Task(
        description="""
Create a complete study guide from the uploaded course material.

You MUST use the Course Material Tool to read the document.

Start by using the tool with:
ALL

Follow all instructions from your personalized Skill.

STRICT RULES:

1. Use only information from the uploaded document.
2. Do not use external knowledge.
3. Do not invent information.
4. Follow the Skill defined in your backstory.
5. Write in the same language as the uploaded document.
6. Keep the guide structured and easy to study.

Return only the final study guide.
""",

        expected_output=(
            "A structured personalized study guide based only "
            "on the uploaded course material."
        ),

        agent=agent
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True
    )

    result = crew.kickoff()

    return str(result)





def clean_markdown(text):
    # Remove markdown bold markers
    text = text.replace("**", "")

    # Remove markdown italic markers
    text = text.replace("__", "")

    return text.strip()


def rtl_text(text):
    """
    Convert Hebrew text to correct visual RTL order.
    English text remains readable.
    """
    return get_display(text)


def create_pdf(study_guide):

    os.makedirs("output", exist_ok=True)

    output_path = os.path.join(
        "output",
        "study_guide.pdf"
    )

    # Windows Arial fonts support Hebrew
    regular_font = r"C:\Windows\Fonts\arial.ttf"
    bold_font = r"C:\Windows\Fonts\arialbd.ttf"

    pdfmetrics.registerFont(
        TTFont("ArialHebrew", regular_font)
    )

    pdfmetrics.registerFont(
        TTFont("ArialHebrewBold", bold_font)
    )

    document = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=55,
        leftMargin=55,
        topMargin=55,
        bottomMargin=55
    )

    title_style = ParagraphStyle(
        "HebrewTitle",
        fontName="ArialHebrewBold",
        fontSize=20,
        leading=27,
        alignment=TA_CENTER,
        spaceAfter=18
    )

    heading_style = ParagraphStyle(
        "HebrewHeading",
        fontName="ArialHebrewBold",
        fontSize=15,
        leading=22,
        alignment=TA_RIGHT,
        spaceBefore=12,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        "HebrewBody",
        fontName="ArialHebrew",
        fontSize=11,
        leading=18,
        alignment=TA_RIGHT,
        spaceAfter=7
    )

    bullet_style = ParagraphStyle(
        "HebrewBullet",
        fontName="ArialHebrew",
        fontSize=11,
        leading=18,
        alignment=TA_RIGHT,
        rightIndent=12,
        spaceAfter=5
    )

    story = []

    for line in study_guide.split("\n"):

        line = line.strip()

        if not line:
            story.append(Spacer(1, 7))
            continue

        line = clean_markdown(line)

        # Main title
        if line.startswith("# "):

            text = line[2:].strip()

            story.append(
                Paragraph(
                    rtl_text(text),
                    title_style
                )
            )

        # Section heading
        elif line.startswith("## "):

            text = line[3:].strip()

            story.append(
                Paragraph(
                    rtl_text(text),
                    heading_style
                )
            )

        # Bullet
        elif line.startswith("- "):

            text = line[2:].strip()

            story.append(
                Paragraph(
                    rtl_text("• " + text),
                    bullet_style
                )
            )

        # Numbered item
        elif re.match(r"^\d+\.", line):

            story.append(
                Paragraph(
                    rtl_text(line),
                    body_style
                )
            )

        # Normal text
        else:

            story.append(
                Paragraph(
                    rtl_text(line),
                    body_style
                )
            )

    document.build(story)

    return output_path





def answer_question(pages, question):

    agent = create_study_agent(pages)

    task = Task(
        description=f"""
Answer the following student's question:

{question}

You MUST use the Course Material Tool to search the uploaded document.

STRICT RULES:

1. Answer only from the uploaded document.
2. Do not use external knowledge.
3. Do not make assumptions.
4. Mention the relevant page number when possible.

If the answer cannot be found in the uploaded document,
respond exactly with:

The answer was not found in the uploaded document.
""",

        expected_output=(
            "A concise answer based only on the uploaded document, "
            "including the relevant page number when available."
        ),

        agent=agent
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True
    )

    result = crew.kickoff()

    return str(result)