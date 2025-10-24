# 📊 AI Data Visualization Agent (Gemini + Local Execution)

This Streamlit app allows you to **analyze and visualize datasets using AI**.
Simply upload a CSV file and ask natural language questions — Google’s **Gemini model** will automatically generate and execute Python code locally to produce insights and plots.

---

## 🚀 Features

✅ Upload any CSV file
✅ Ask natural questions like *“Compare average age by gender”* or *“Show correlation heatmap”*
✅ Gemini (free API) generates runnable Python code
✅ Executes safely on your machine — no data is sent to any external server
✅ Supports `matplotlib`, `seaborn`, and `plotly` for visualizations
✅ Displays AI-generated charts, tables, and code outputs interactively

---

## 🧠 How It Works

1. You upload a dataset (e.g., `titanic.csv`).
2. You type a query (e.g., *“Group by Pclass and show survival rate”*).
3. The Gemini API generates Python analysis code.
4. The app executes the generated code locally using your `df` DataFrame.
5. Results and visualizations appear right in the Streamlit dashboard.

---

## 🧪 Tech Stack

* **Frontend:** Streamlit
* **LLM:** Google Gemini API (`gemini-2.0-flash`)
* **Visualization:** Matplotlib, Seaborn, Plotly
* **Data:** Pandas

---

## 🛠️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ai-data-visualization-agent.git
cd ai-data-visualization-agent
```

### 2. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate   # on macOS/Linux
venv\Scripts\activate      # on Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Get a free Gemini API key

* Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
* Create a free API key
* Copy it — you’ll need it inside the app’s sidebar.

### 5. Run the Streamlit app

```bash
streamlit run app.py
```

---

## 🧩 Example Usage

#### Example Query:

> “Group by ‘Pclass’ and show average fare and age using a bar chart.”

#### Output:

* Gemini generates Python code using Pandas & Matplotlib.
* The code runs locally.
* The app displays a bar chart comparing average age and fare per passenger class.

---

## 🧠 Notes & Safety

* This app **executes AI-generated code locally** on your machine.
  Avoid running it on shared or public servers.
* Your data and API key remain private — no data is uploaded externally.
* Works best with well-formatted CSV datasets.

---

## 📦 Requirements

All dependencies are listed in `requirements.txt`:

```txt
streamlit>=1.37.0
pandas>=2.0.0
matplotlib>=3.7.0
seaborn>=0.12.2
plotly>=5.15.0
Pillow>=10.0.0
google-generativeai>=0.7.2
```

---

## 💡 Future Improvements

* Add AI-generated data summaries
* Export analysis reports as PDF
* Support for Excel & JSON files
* Memory for multi-step queries



### ⭐ If you like this project, consider starring the repo!
