<<<<<<< HEAD
# Study Guide Agent

Study Guide Agent is an AI-based application that helps students study from uploaded course materials.

The system is built with CrewAI and includes a real AI Agent with a defined role, goal, backstory, and tool.

The user uploads a PDF through a Streamlit interface.

The agent reads the uploaded document, follows the personalized instructions defined in `SKILL.md`, and performs two main tasks:

1. Generate a personalized study guide.
2. Answer questions using only information found in the uploaded document.

## Agent

The system uses a CrewAI Agent.

### Role

Study Guide Agent

### Goal

Help students study course material by creating personalized study guides and answering questions based only on the uploaded document.

### Backstory

The Agent receives its study behavior and preferences from `SKILL.md`.

The content of `SKILL.md` is injected into the Agent's backstory.

### Tool

The Agent uses a custom Course Material Tool.

The tool allows the Agent to read and search information from the uploaded PDF.

## Main Features

- Upload course material in PDF format.
- Extract text and page numbers from the PDF.
- Use a CrewAI Agent.
- Inject `SKILL.md` into the Agent backstory.
- Generate a personalized study guide.
- Export the study guide as a PDF file.
- Ask questions about the uploaded document.
- Answer only from the uploaded material.
- Display relevant page numbers.
- Inform the user when information is not found in the document.

## Skill

The `SKILL.md` file defines how the Agent should prepare the study material.

For example:

- Use short and clear explanations.
- Divide the material into topics.
- Identify important concepts and definitions.
- Create review questions.
- Highlight important information for exams.
- Do not add information that does not appear in the uploaded document.

Changing `SKILL.md` changes the format and behavior of the generated study guide.

## Technologies

- Python
- CrewAI
- Streamlit
- OpenAI API
- PyPDF
- ReportLab
- python-bidi

## Project Structure

```text
study-agent/
│
├── app.py
├── agent.py
├── SKILL.md
├── README.md
├── requirements.txt
├── .gitignore
│
└── output/
    └── study_guide.pdf



    How It Works
1. The user uploads a course PDF.
2. The system extracts text and page numbers.
3. The Agent is created with:
   - Role
   - Goal
   - Backstory
   - Course Material Tool
4. SKILL.md is injected into the Agent's backstory.
5. The Agent uses the Course Material Tool to read the uploaded document.
6. The Agent creates a personalized study guide.
7. The system generates study_guide.pdf.
8. The user can also ask questions about the document.
9. If the answer is not found in the document, the Agent states that the information was not found.
Installation
Install the required packages:
pip install -r requirements.txt

Create a .env file:
OPENAI_API_KEY=YOUR_API_KEY

Run the application:
streamlit run app.py

Output
The generated study guide is saved as:
output/study_guide.pdf
=======
# study-guide-agent
>>>>>>> 0dd991ff55b857ab238b477078d9ed59407547b7
