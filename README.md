# 🌅 KNM Horizon — 56-Day Dutch Life Learning Path

A **native Streamlit** learning app covering an eight-week / 56-day KNM course, grounded in the user's uploaded **130-page TaalCompleet KNM** textbook.

**Status: code tested and packaged; NOT YET HOSTED on Streamlit Community Cloud.** Deployment requires the owner's GitHub repository and Streamlit Community Cloud authorisation. Do not mistake this source package for a live `*.streamlit.app` URL.

## Contents

- **56 clickable 120-minute lessons** on an 8-week roadmap, with downloadable CSV plan.
- **48 actual source-textbook sections** across seven themes with source section IDs and printed book page numbers.
- Expanded **A2 Dutch readings** and **English explanations**, including 48 new detailed concept studies, confusion warnings, A2 sentence models and three realistic situations per chapter.
- **Seven visual memory routes**, theme images, memory chains, interactive bilingual flashcards and active recall prompts.
- **Nine 20-question auto-scored practice sets** (Days 48–56) = **180 unique questions** with topic breakdown and English corrections.
- Chapter checkpoints, daily reflection notes, revision suggestions, user-confirmed day completion and a weak-topic queue based only on actually scored question attempts.
- **Manual JSON progress backup and restore**. Prior chat quiz scores are **never assumed** to be known.

This is independent educational content. The seven book themes and their exact section titles come from the uploaded book, while the 56-day curriculum, longer explanations, examples, memory guides, and questions are **original learning additions**. The labels “Final KNM preparation” and “Mock test 1–3” are not separate book chapters or official DUO mock examinations. The app does not distribute a copy of the source PDF.

## Run locally

Requires Python 3.10+:

```bash
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

The browser should open at `http://localhost:8501`.

## Deploy to Streamlit Community Cloud

1. Create a **new GitHub repository**, for example `knm-horizon-streamlit`. Do not upload to an unrelated existing app repository.
2. Upload the project contents into the **root of that repository**, including the hidden `.streamlit/config.toml` configuration and the `assets/` directory. You can upload files via the GitHub browser interface or use the Git command line.
3. Go to **https://share.streamlit.io/** and sign in with GitHub, authorising access to the new repository.
4. Choose **Create app → Yup, I have an app**. Select your repository, its main branch, and use `streamlit_app.py` as the **Main file path**.
5. Click **Deploy**. Community Cloud creates a `*.streamlit.app` URL when deployment is successful. Copy that actual URL to share your app; never guess the subdomain.

Official instructions: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy

### Required deployment structure

```text
knm-horizon-streamlit/
├── streamlit_app.py
├── course_content.json
├── study_depth.py
├── requirements.txt
├── README.md
├── assets/
│   ├── nederland.webp
│   ├── wonen.webp
│   ├── gezondheid.webp
│   ├── onderwijs.webp
│   ├── werk.webp
│   ├── instanties.webp
│   └── bestuur.webp
└── .streamlit/
    └── config.toml
```

All application content is bundled: no API token, proprietary paid API, personal dataset, or external database is required. The app imports only `streamlit` and Python's standard library.

## Progress and privacy

The app uses Streamlit **per-session state**; it does not silently persist progress across visits, share scores with DUO or collect users' personal information. Export your JSON study record on **My progress** and import it when you return. Do **not** use the app to store highly sensitive information in the free-text notes. Course completion, self-assessed confidence, and quiz evidence are tracked separately; **no quiz result is fabricated**.

## Official exam: important distinctions

DUO currently describes KNM as a **45-minute computer-based exam** covering multiple themes. DUO changed its KNM content on **1 July 2025**. The uploaded book contains older references to **40 questions** and a **70% pass mark** that we have not independently verified as current. Horizon's tests each have 20 questions, and the suggested 16/20 study goal is **not** an official pass threshold.

- Official KNM format: https://www.inburgeren.nl/examen-doen/inhoud-kennisexamens.jsp
- Official DUO practice: https://www.inburgeren.nl/examen-doen/oefenen.jsp
- DUO announcement: https://www.inburgeren.nl/nieuwsberichten/artikel.jsp?cid=tcm%3A94-225285

## Validation

Tested by running `python check_project.py`, which checks:

- 56 daily lessons in consecutive order, mapped to all 48 actual source chapters exactly once.
- Seven themes, all 48 additional detailed explanation cards and source-page references.
- All nine practice quizzes with 20 questions each, three distinct choices each, and valid answer keys.
- A Streamlit-API offline smoke test of all seven app views, all 56 daily lesson pages and all nine scored-result pages.

**Runtime caveat:** The sandbox used to package the app did not have `streamlit` installed, and external package installation was unavailable. It passed structural and stub-based checks, but an actual Community Cloud browser run still needs to verify final rendering.
