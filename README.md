# Ship AI Agent

Ship AI Agent is an AI-powered chatbot designed to assist with technical engineering queries related to ship machinery and equipment. It processes ship manuals in PDF format, extracts relevant information, and provides precise responses based on the manuals.

## Features

- **PDF Processing**: Extracts text from both digital and scanned PDFs using OCR.
- **Vector Database**: Stores extracted text in a Chroma vector database for efficient retrieval.
- **Conversational Memory**: Maintains chat history for contextual responses.
- **Streamlit UI**: Provides an interactive chat interface.
- **Integration with OpenAI API**: Uses GPT-4o-mini for answering queries.

## Folder Structure

```
ship-ai-agent/
│── data/                   # Folder containing PDF manuals
│── chroma_db/              # Directory for storing the vector database
│── src/
│   │── config.py           # Configuration settings (API keys, paths, etc.)
│   │── pdf_processor.py    # Handles PDF processing and OCR
│   │── vector_db.py        # Manages the Chroma vector database
│   │── query_engine.py     # Constructs and handles query logic
│   │── ui.py               # Streamlit UI implementation
│── tests/                  # Folder containing unit tests
│── app.py                  # Main entry point for the Streamlit application
│── pyproject.toml          # Poetry configuration file
│── .env                    # Environment variables (API keys)
│── README.md               # Project documentation
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- Poetry (for dependency management)
- OpenAI API Key (store in a `.env` file)
- Tesseract OCR (for processing scanned PDFs)

### Step 1: Clone the Repository
```sh
git clone git@github.com:grmarag/ship-ai-agent.git
cd ship-ai-agent
```

### Step 2: Install Dependencies using Poetry
```sh
poetry install
eval $(poetry env activate)
```

### Step 3: Configure API Keys
Create a `.env` file and add your OpenAI API key:
```env
OPENAI_API_KEY=your-api-key-here
```

### Step 4: Run the Application
```sh
poetry run streamlit run app.py
```

## Usage

1. Place your ship manuals (PDFs) inside the `data/` folder.
2. Start the application (`poetry run streamlit run app.py`).
3. Ask technical questions related to the manuals, and the AI will fetch accurate answers.

## Running Tests

To run unit tests from the `tests/` directory:
```sh
poetry run pytest tests/
```

## System Architecture Flowchart
[![](https://mermaid.ink/img/pako:eNqNVmtv2zYU_SuEihYuYGeyLD-kAQP0BAIkaFa3-zC7CBiJsolKlEZSSdw4_31XpCyrrhdPsGHx8pzD-9C91ouRlCkxXGPNsrx8SraYS_QlXDME1_v3aFk_bDiuti4KSpbRTc2xpCVDH9A1o5LinP5QBk0QLboFtyi0epv7TZObK16tjZY7SNTvVbX7uDa-ua6r10esB1hcVQBAg6XkBBc5nOVVVYsnTPJdTxqNRn8gTxsIS9fsTJBhmdQFENEdLxMiBGWbk8gA0eyh1RloLxAfnLsL43av5GhQpdl9dVgeowJzjzUG2k2JUwRcgTJeFujqtxRL3IGXklQ9ggWEZdUEfvBHoMFnktRc0EcSQDlxIgn_Qp6lgsH9x__SUgnyx313tMl6O2l_kURChCG4-YAFOUmY3g19tDrB9bIVQBR6dwlfggaPanGfPhwTpU1ve_JnTfgOnq-bm9sTL9QOmNFKYyK2oYxoaM-REBxRgHZ_8E-zuCdqdfRFWXuspmyQa_mpIsy7bjTRYFPJkV2OCspoy8rzosex9KP-SLhQXeDXWUb4LSlKkFb4Qt8fKaoa4fgXy4X6fBWEQ8tB6TOcnJbn6zVa_QzopSMCHwEwqOkx9pqeO60pKophgjStz6BUEJHQu17j5L5reSKahxtVXdfska-BvqWQd1gIAKWH_kq2Nfsu9ijQqECDePlIU4BxIjklkMU9CvvnLQl0Ql0h0RwCQ0dILMkeRRoTtRiWAqiJnrKqlp2Eyus-JjLZNp40sX1AG8IITDB1pqggPNL5pPGfiaw5Ewgz8dT4E_WrIXc5xIqSXEWn7WoRkgypUYUymufuuziM_NAcCsnL78R9F83mkWW1y9ETTeXWtarngyHFAnqc452Lpmj6-4muHpmtcDiLvHjRCU9sZxH6vwifSsCYODgWxU407_jxOLDN-P_wmzFz0IhjLwiPGhMnGJ8ENz4bnIWsU2U9EFrhaBEv4mknPPb8wAkuOqf6-KDgx9PY7xSmoRdG1kUF6OlDaHYUxMf0LCLb9sKLfN3jx9KHUXAs_dwOJpeDqOmB7kR-5HX0wJw41tkCG0OjILzANIU__pdGbm3ILSnI2nDhNiUZrnO5hneCV4DiWpbLHUsMV_KaDA1e1put4WY4F7CqK2gPElIM46TorBVmf5flT2vDfTGeDXc0mVxN5pZpzq2xY80c0xkaO8N1zCtnujBnC9OczuzJ4nVo_FACYJ9NrKltT8dz-DRwklIo_K1-b1GvL6__Aj30x0c?type=png)](https://mermaid.live/edit#pako:eNqNVmtv2zYU_SuEihYuYGeyLD-kAQP0BAIkaFa3-zC7CBiJsolKlEZSSdw4_31XpCyrrhdPsGHx8pzD-9C91ouRlCkxXGPNsrx8SraYS_QlXDME1_v3aFk_bDiuti4KSpbRTc2xpCVDH9A1o5LinP5QBk0QLboFtyi0epv7TZObK16tjZY7SNTvVbX7uDa-ua6r10esB1hcVQBAg6XkBBc5nOVVVYsnTPJdTxqNRn8gTxsIS9fsTJBhmdQFENEdLxMiBGWbk8gA0eyh1RloLxAfnLsL43av5GhQpdl9dVgeowJzjzUG2k2JUwRcgTJeFujqtxRL3IGXklQ9ggWEZdUEfvBHoMFnktRc0EcSQDlxIgn_Qp6lgsH9x__SUgnyx313tMl6O2l_kURChCG4-YAFOUmY3g19tDrB9bIVQBR6dwlfggaPanGfPhwTpU1ve_JnTfgOnq-bm9sTL9QOmNFKYyK2oYxoaM-REBxRgHZ_8E-zuCdqdfRFWXuspmyQa_mpIsy7bjTRYFPJkV2OCspoy8rzosex9KP-SLhQXeDXWUb4LSlKkFb4Qt8fKaoa4fgXy4X6fBWEQ8tB6TOcnJbn6zVa_QzopSMCHwEwqOkx9pqeO60pKophgjStz6BUEJHQu17j5L5reSKahxtVXdfska-BvqWQd1gIAKWH_kq2Nfsu9ijQqECDePlIU4BxIjklkMU9CvvnLQl0Ql0h0RwCQ0dILMkeRRoTtRiWAqiJnrKqlp2Eyus-JjLZNp40sX1AG8IITDB1pqggPNL5pPGfiaw5Ewgz8dT4E_WrIXc5xIqSXEWn7WoRkgypUYUymufuuziM_NAcCsnL78R9F83mkWW1y9ETTeXWtarngyHFAnqc452Lpmj6-4muHpmtcDiLvHjRCU9sZxH6vwifSsCYODgWxU407_jxOLDN-P_wmzFz0IhjLwiPGhMnGJ8ENz4bnIWsU2U9EFrhaBEv4mknPPb8wAkuOqf6-KDgx9PY7xSmoRdG1kUF6OlDaHYUxMf0LCLb9sKLfN3jx9KHUXAs_dwOJpeDqOmB7kR-5HX0wJw41tkCG0OjILzANIU__pdGbm3ILSnI2nDhNiUZrnO5hneCV4DiWpbLHUsMV_KaDA1e1put4WY4F7CqK2gPElIM46TorBVmf5flT2vDfTGeDXc0mVxN5pZpzq2xY80c0xkaO8N1zCtnujBnC9OczuzJ4nVo_FACYJ9NrKltT8dz-DRwklIo_K1-b1GvL6__Aj30x0c)

## Potential Issues, Challenges, and Limitations
[![](https://mermaid.ink/img/pako:eNqNVl1z2joQ_Ss76jRtZ0xLIHy5TwFDoIF7mdLehxv6oNgCq7UljyQnuJn8966EQ5wGGDwMg452V3t2zwo_kFBGjPhklcj7MKbKwLdgKQCft29hHoxgKmnExRrOYK5kyLS2i4nWOdNbO53frhXNYlgSa__aisDNoUA_tiHsc3mzJP9Ie6SGkcxFBJ9gIJXKM8MiBy_JD9_3uQ0aMEN58uzcd86ipg0VEVXOHqOolJpDbkxES7Fj-u_gKwximiRMrPcQ-2sbGVlECliEVIgyvwqZAeYzETQMc0UNc9Hfs41RNDQcvZhSUukPRwgFGGDM1zF8ZVrmKmRYC6HzNLP-JzFCezxdMREWh9q1xwSZ7VDj8t7brCGmV27AXMoERphFrpi2NEPmstSfDE-ZzM1RoiOMNOUpt00ezL_v-J7Wtv9YaKSCoO_oMiVek9xjgiSf0TlTmmuDRWAozRkVdM1SJF9he4U5Blw5lwKENHCvuKG3CUONDrEnxRGCY3ReGIq2ATUU-GorcVQTSumI3wT9vsVY0lgmESyY0NzwO24K4Cg7rFhClV0tGFVhfFK1ptPZdvow5WNqP2SHdbNb5QZOmu1Whp1mMMZV8lIjX26cwgzqHmZ8Y0efhkpaxRwf5mt0nOGtlIATBnVicreBNpUmnkB4YYWL83YG3yeHhmCfDRJ9grF1xgoDz71DpbhkYMZSVEKF6xRTvsRpT_OEOiVXrccoLyuc9xlTK3snIYNjIzGzI2HrJFflSXDLzD1j4onQaeyvlMwzMDGDlP5EsTtzCDHBtVQcZ9XINcNt9bomBQ5E-qL8Z3_ff8gP1xW0epdDrVaDfuU-dEBQuUAcMKrMmAPG7ntSEZEDriuVdsBsb7dNYSUIYUK1RnqrJ85l0x0esFUJwoonif9mNBr2h0NPGyV_Mf_NoN3oNrrlsnbPIxP7jWzzeV-Ibel3cQZB0NjFGbY6zU7zZZzzbPMERFTjn62ihQ9NaJbRd0wusywpXOfebXN9tz0ZO_bcJsNNUrK84zqnCaxtw7EClVzh0ut7Ay_wht7Iu_LG3sT74l17U29WVuEz8UjKUJQ8wreAB-u6JHhyineTjz8jtqJ5YpZkKR7RlOZGLgoREt-onHkET1zHxF_RROMqzyJUV8ApZpju0IyK_6V8sSb-A9kQv9Zsfmx2GvV6p3Hea7R79Z5HCuL36h97rW693a3XW-2LZvfRI79dAMTbzUbr4qJ13sGPNWcRx-GabV9i3LvM4x9Y9NFK?type=png)](https://mermaid.live/edit#pako:eNqNVl1z2joQ_Ss76jRtZ0xLIHy5TwFDoIF7mdLehxv6oNgCq7UljyQnuJn8966EQ5wGGDwMg452V3t2zwo_kFBGjPhklcj7MKbKwLdgKQCft29hHoxgKmnExRrOYK5kyLS2i4nWOdNbO53frhXNYlgSa__aisDNoUA_tiHsc3mzJP9Ie6SGkcxFBJ9gIJXKM8MiBy_JD9_3uQ0aMEN58uzcd86ipg0VEVXOHqOolJpDbkxES7Fj-u_gKwximiRMrPcQ-2sbGVlECliEVIgyvwqZAeYzETQMc0UNc9Hfs41RNDQcvZhSUukPRwgFGGDM1zF8ZVrmKmRYC6HzNLP-JzFCezxdMREWh9q1xwSZ7VDj8t7brCGmV27AXMoERphFrpi2NEPmstSfDE-ZzM1RoiOMNOUpt00ezL_v-J7Wtv9YaKSCoO_oMiVek9xjgiSf0TlTmmuDRWAozRkVdM1SJF9he4U5Blw5lwKENHCvuKG3CUONDrEnxRGCY3ReGIq2ATUU-GorcVQTSumI3wT9vsVY0lgmESyY0NzwO24K4Cg7rFhClV0tGFVhfFK1ptPZdvow5WNqP2SHdbNb5QZOmu1Whp1mMMZV8lIjX26cwgzqHmZ8Y0efhkpaxRwf5mt0nOGtlIATBnVicreBNpUmnkB4YYWL83YG3yeHhmCfDRJ9grF1xgoDz71DpbhkYMZSVEKF6xRTvsRpT_OEOiVXrccoLyuc9xlTK3snIYNjIzGzI2HrJFflSXDLzD1j4onQaeyvlMwzMDGDlP5EsTtzCDHBtVQcZ9XINcNt9bomBQ5E-qL8Z3_ff8gP1xW0epdDrVaDfuU-dEBQuUAcMKrMmAPG7ntSEZEDriuVdsBsb7dNYSUIYUK1RnqrJ85l0x0esFUJwoonif9mNBr2h0NPGyV_Mf_NoN3oNrrlsnbPIxP7jWzzeV-Ibel3cQZB0NjFGbY6zU7zZZzzbPMERFTjn62ihQ9NaJbRd0wusywpXOfebXN9tz0ZO_bcJsNNUrK84zqnCaxtw7EClVzh0ut7Ay_wht7Iu_LG3sT74l17U29WVuEz8UjKUJQ8wreAB-u6JHhyineTjz8jtqJ5YpZkKR7RlOZGLgoREt-onHkET1zHxF_RROMqzyJUV8ApZpju0IyK_6V8sSb-A9kQv9Zsfmx2GvV6p3Hea7R79Z5HCuL36h97rW693a3XW-2LZvfRI79dAMTbzUbr4qJ13sGPNWcRx-GabV9i3LvM4x9Y9NFK)

## Demo
![ship_ai_agent_demo](https://github.com/user-attachments/assets/a399cb53-629e-4874-a09e-98c4c5731321)

## License
This project is licensed under the MIT License.

## Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request.
