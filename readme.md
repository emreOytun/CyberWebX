# CyberWebX

CyberWebX is a modular web-based cybersecurity platform combining machine learning and OSINT techniques to detect and mitigate digital threats. It includes:

✅ Malware detection (PE file analysis)  
✅ Domain trust evaluation (phishing URL detection)  
✅ OSINT-based password generation

---

## 🚀 Features

- **Malware File Detection**
  - Static analysis of Windows PE files
  - Random Forest classifier with 95.8% accuracy

- **Domain Trust Detection**
  - URL lexical feature analysis using Logistic Regression
  - TF-IDF vectorization for efficient text processing

- **OSINT-Based Password Generator**
  - Collects public footprint data (LinkedIn, Twitter, Instagram)
  - Locally hosted LLM for strong, personalized password suggestions

---

## 🏗️ Tech Stack

| Layer       | Technology                                     |
|-------------|-----------------------------------------------|
| Frontend    | HTML, CSS, JavaScript (Vanilla JS)            |
| Backend     | Python Flask, Scikit-learn, Joblib            |
| Machine Learning | Random Forest, Logistic Regression, TF-IDF |
| Utilities   | Requests, BeautifulSoup, Tkinter, Selenium, Instaloader |

---

## 📊 Datasets Used

- **Malware Dataset:** 10,000 PE files (50% benign, 50% malicious) → [Kaggle Source](https://www.kaggle.com/datasets/dscclass/malware)
- **URL Dataset:** 84,093 domains (benign + phishing) → [Kaggle Source](https://www.kaggle.com/datasets/samahsadiq/benign-and-malicious-urls)

---

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/Mens1s/CyberWebX.git

# Navigate to the project directory
cd CyberWebX

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Flask backend
python app.py

# For the local Tkinter GUI
python guimain.py
