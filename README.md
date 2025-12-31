# Viral TB Studio 🎥

**Viral TB Studio** is a professional AI-powered tool designed to automate the creation of high-performing YouTube video metadata. It leverages a sequential multi-agent AI pipeline to research trending topics, brainstorm click-worthy titles, and generate SEO-optimized descriptions.

The application features a modern, responsive web interface with a glassmorphism design and dynamic theme switching.

## 🚀 Features

- **Multi-Agent AI Pipeline:** Orchestrates specialized agents for Research, Title Generation, Selection, and Description writing.
- **Powered by Gemini:** Utilizes Google's Gemini 2.5 Flash model for high-speed, intelligent reasoning and content generation.
- **Real-Time Research:** Integrated with Google Search to fetch current trends and keyword data.
- **Modern UI:** A beautiful, responsive interface built with Tailwind CSS, featuring Dark/Light/System modes and smooth animations.
- **FastAPI Backend:** Built on a robust, asynchronous Python backend.

## 🛠️ Tech Stack

- **Backend:** Python 3.10+, FastAPI, Uvicorn
- **AI Engine:** Google ADK (Agent Development Kit)
- **Models:** Google Gemini 2.5 Flash
- **Frontend:** HTML5, Vanilla JS, Tailwind CSS
- **Tools:** Google Search (via google-adk)

## 📦 Installation & Setup

### Prerequisites
- Python 3.10 or higher
- A Google Gemini API key (get it from [Google AI Studio](https://aistudio.google.com/app/apikey))

### 1. Clone the Repository
```bash
git clone <repository-url>
cd viral-tb-studio
```

### 2. Set Up Virtual Environment
It's recommended to use a virtual environment to manage dependencies.
```bash
# Create venv
python -m venv .venv

# Activate venv
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory (`viral-tb-studio/.env`) and add your API key:

```env
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=your_gemini_api_key
```

**Note:** The `google_search` tool from `google-adk` uses the same `GOOGLE_API_KEY` for both AI generation and search functionality.

### 5. Run the Application
Start the FastAPI server:
```bash
python server.py
```

The application will start at `http://127.0.0.1:8000`.

## 🖥️ Usage

1. Open your browser and navigate to **[http://127.0.0.1:8000](http://127.0.0.1:8000)** for the landing page.
2. Click **"Start Creating"** or go to `/generate` to access the tool.
3. Enter your video topic or raw idea (e.g., "A 10-minute review of the iPhone 16 for photographers").
4. Watch as the agents research, brainstorm, and generate your metadata in real-time.

## 🧩 Architecture

The system is powered by `google-adk` and consists of a sequential pipeline:

1. **TitleResearchAgent:** Analyzes search intent and keywords using Google Search.
2. **TitleGeneratorAgent:** Brainstorms 5 creative, high-CTR titles based on research.
3. **BestTitleSelectorAgent:** Selects the strongest title for maximum engagement.
4. **DescriptionResearchAgent:** Gathers deep context for the video description.
5. **DescriptionGeneratorAgent:** Writes a structured, SEO-friendly description.
6. **AggregatorAgent:** Formats the final output for easy copying.

These agents work in parallel teams and sequential pipelines to deliver optimized results.

## Credits & Disclosure

The user interface was AI-assisted.
All agent logic, architecture, and behavior were designed and implemented by me.

## 📄 License

This project is licensed under the MIT License.