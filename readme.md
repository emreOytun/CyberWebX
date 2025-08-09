
# CyberWebX 🚀

**An Intelligent Cybersecurity Platform Using Machine Learning and OSINT**  
Modular platform combining malware detection, phishing URL classification, and secure password generation enhanced by scraping + LLM.


---

## 📺 Demo Video

▶ **Watch the demo:**  
[![CyberWebX Demo](https://img.youtube.com/vi/vsUeiiuE0kg/0.jpg)](https://www.youtube.com/watch?v=vsUeiiuE0kg)

---

## 📸 Screenshots

| Web Dashboard (Domain Check) | File Upload Scanner |
|-----------------------------|---------------------|
| ![Domain Check](https://raw.githubusercontent.com/Mens1s/CyberWebX/refs/heads/main/raw/main/assets/domain_check.png) | ![File Scanner](https://raw.githubusercontent.com/Mens1s/CyberWebX/refs/heads/main/raw/main/assets/file_scan.png) |

| Password Generator | Local Tkinter Scraper |
|--------------------|-----------------------|
| ![Password Generator](https://raw.githubusercontent.com/Mens1s/CyberWebX/refs/heads/main/raw/main/assets/password_generator.png) | ![Tkinter Scraper](https://raw.githubusercontent.com/Mens1s/CyberWebX/refs/heads/main/raw/main/assets/scraper.png) |

---

## 🌟 Key Features

✅ **Malware File Analysis** → Static PE header analysis using Random Forest  
✅ **Phishing Domain Classification** → Lexical + TF-IDF + Logistic Regression  
✅ **OSINT-Based Password Generation** → Uses scraped footprint + Gemini API + LLM  
✅ **Modular Flask REST API** → Extensible, separate endpoints  
✅ **Standalone Tkinter Scraper GUI** → Local scraping, no cloud exposure

---

## 🏛️ Architecture

```
Frontend (HTML, CSS, JS)  →  Flask Backend (REST API)  →  ML Models (Scikit-learn)
                                    ↓
                          Tkinter Local GUI (Scraper)
```

---

## 💾 Datasets

- Malware PE Header Dataset → [Kaggle Link](https://www.kaggle.com/datasets/dscclass/malware)
- Malicious & Benign URLs → [Kaggle Link](https://www.kaggle.com/datasets/samahsadiq/benign-and-malicious-urls)

---

## 🔍 Example Code Snippets

### 📦 Malware Detection Model

```python
df = pd.read_csv("MalwareData.csv", sep="|")
X = df.drop(["Name", "md5", "legitimate"], axis=1).values
y = df["legitimate"].values

extratrees = ExtraTreesClassifier().fit(X, y)
selector = SelectFromModel(extratrees, prefit=True)
X_selected = selector.transform(X)

clf = RandomForestClassifier(n_estimators=50)
clf.fit(X_train, y_train)
```

### 🌐 URL Classifier Model

```python
def sanitization(web):
    web = web.lower()
    tokens = set(web.replace('/', '.').replace('-', '.').split('.'))
    tokens.discard('com')
    return list(tokens)

pipeline = Pipeline([
    ('vectorizer', TfidfVectorizer(tokenizer=sanitization)),
    ('classifier', LogisticRegression(solver='lbfgs', max_iter=1000))
])
pipeline.fit(x_train, y_train)
```

### 🌍 Flask Endpoint (Check URL)

```python
@app.route('/check-url', methods=['POST'])
def check_url():
    url = request.get_json()['url'].strip().lower()
    if url in WHITELIST:
        return jsonify({'url': url, 'result': 'good'})
    result = url_model.predict([url])[0]
    return jsonify({'url': url, 'result': result})
```

### 🔐 Password Generation Prompt

```python
prompt = (
    "You are a password generation expert. Generate 500 unique, strong, and memorable passwords "
    "based on scraped user data. Avoid common patterns, use substitutions, camelCase, symbols."
)
response = requests.post(GEMINI_API_URL, headers=HEADERS, json=payload)
```

---

## ⚙️ Installation

```bash
git clone https://github.com/Mens1s/CyberWebX.git
cd CyberWebX

# (Optional) Virtual environment
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python app.py  # Start Flask backend

# Run local scraper (GUI)
python guimain.py
```

---

## 🌐 API Endpoints

| Route                  | Method | Description                                |
|------------------------|--------|------------------------------------------|
| `/`                   | GET    | Main dashboard view                      |
| `/check-url`          | POST   | Submit a URL for phishing check          |
| `/scan-file`          | POST   | Upload PE file for malware scanning      |
| `/generate-password`  | POST   | Generate passwords from OSINT footprint  |

---

## 📈 Performance

| Module                   | Accuracy  | Precision | Recall  |
|--------------------------|-----------|-----------|---------|
| Malware Detection        | 95.8%     | 94.6%     | 93.2%  |
| Phishing URL Detection   | 98.57%    | 98.11%    | 99.60% |

---

## 🔒 Security Considerations

✅ No cloud scraping (Tkinter runs locally)  
✅ Whitelisted domains bypass false positives  
✅ Gemini API securely integrated via backend  
✅ Password generation follows strong entropy rules  
✅ Designed for research & educational purposes

---

## 🔧 Future Work

- Dynamic malware sandbox integration  
- WHOIS and DNSBL-based domain enrichment  
- JWT + role-based access control  
- Mobile/desktop cross-platform expansion  
- Real-time notification system

---

## 👥 Contributors

- Ahmet Yiğit → a.yigit2020@gtu.edu.tr  
- Emre Oytun  
- Elif Deniz

---

> ✨ **Note:** If you use or modify this project, please cite the original authors or leave a GitHub star ⭐
