# 🚀 QUICK SETUP GUIDE - InvoiceAI Pro

## ⏱️ Total Time: 30 Minutes

---

## STEP 1: DOWNLOAD THE CODE (5 min)

You have all the code files! Extract the `invoiceai-pro-code` folder to your computer.

---

## STEP 2: INSTALL PYTHON (If not installed)

### Windows:
1. Download Python 3.9+ from: https://www.python.org/downloads/
2. ✅ Check "Add Python to PATH"
3. Click "Install Now"
4. Verify: Open CMD and type `python --version`

### Mac:
```bash
# Install using Homebrew
brew install python@3.9
```

### Linux:
```bash
sudo apt update
sudo apt install python3.9 python3-pip
```

---

## STEP 3: SETUP PROJECT (10 min)

### Open Terminal/CMD in project folder:

```bash
# Navigate to project
cd invoiceai-pro-code

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# Install dependencies (will take 2-3 minutes)
pip install -r requirements.txt
```

**You should see:**
```
Successfully installed streamlit-1.31.0 pandas-2.1.4 ...
```

---

## STEP 4: AWS SETUP (10 min)

### Get AWS Credentials:

1. **Go to:** https://console.aws.amazon.com
2. **Sign in** (or create free account)
3. **Navigate to:** IAM → Users → Your Username → Security Credentials
4. **Click:** "Create Access Key"
5. **Select:** "Application running on AWS compute service"
6. **Copy both keys!**

### Request Bedrock Access:

1. **Go to:** AWS Console → Search "Bedrock"
2. **Click:** "Model Access" (left sidebar)
3. **Click:** "Request Model Access" (orange button)
4. **Enable:** Anthropic Claude 3.5 Sonnet
5. **Click:** "Save Changes"
6. **Wait:** 5-10 minutes for approval ⏳

### Configure Credentials:

```bash
# Create .env file
cp .env.example .env

# Edit .env file (use Notepad/TextEdit/nano)
# Add your AWS credentials:
AWS_ACCESS_KEY_ID=AKIA...your_key
AWS_SECRET_ACCESS_KEY=abc123...your_secret
AWS_DEFAULT_REGION=us-east-1
```

---

## STEP 5: RUN THE APP (5 min)

### Start Streamlit:

```bash
streamlit run app.py
```

**You should see:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

### Open Browser:
- Go to: `http://localhost:8501`
- App should load! 🎉

---

## STEP 6: TEST WITH SAMPLE INVOICE

### Create Sample Excel File:

**In Excel/Google Sheets, create this:**

| Invoice Number | Invoice Date | GSTIN Seller | GSTIN Buyer | Place of Supply | Item Name | HSN Code | Quantity | Unit Price | GST Rate |
|----------------|--------------|--------------|-------------|-----------------|-----------|----------|----------|------------|----------|
| INV/2025/001 | 2025-02-13 | 29AABCU9603R1ZV | 27AABCU9603R1ZX | 27 | Rice | 1006 | 100 | 50 | 5 |
| INV/2025/001 | 2025-02-13 | 29AABCU9603R1ZV | 27AABCU9603R1ZX | 27 | Mobile Phone | 8517 | 1 | 20000 | 18 |

**Save as:** `sample_invoice.xlsx`

### Test in App:

1. **Upload** the sample invoice
2. **Click** "Validate Against GST Rules"
3. **See** results with AI explanations! 🤖
4. **Try** AI Assistant tab - ask "What HSN code for rice?"

---

## ✅ SUCCESS CHECKLIST

- [ ] Python installed (version 3.9+)
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] AWS account created
- [ ] Bedrock access approved
- [ ] Credentials in .env file
- [ ] App running at localhost:8501
- [ ] Sample invoice uploaded
- [ ] Validation working
- [ ] AI explanations showing

---

## 🔧 TROUBLESHOOTING

### Problem 1: "Command 'python' not found"
**Solution:** Use `python3` instead of `python`

### Problem 2: "streamlit: command not found"
**Solution:** 
```bash
pip install streamlit --upgrade
```

### Problem 3: "AWS credentials not found"
**Solution:** Check `.env` file exists and has correct keys

### Problem 4: "Bedrock access denied"
**Solution:** 
1. Check if model access is approved (wait 5-10 min)
2. Go to AWS Console → Bedrock → Model Access
3. Verify "Anthropic Claude 3.5 Sonnet" is "Available"

### Problem 5: "Module not found"
**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### Problem 6: App not loading
**Solution:**
```bash
# Clear Streamlit cache
streamlit cache clear

# Restart app
streamlit run app.py
```

---

## 📞 NEED HELP?

1. **Check README.md** - Full documentation
2. **Check AWS Console** - Verify Bedrock access
3. **Check Terminal** - Look for error messages
4. **Ask me!** - I'm here to help 💙

---

## 🎯 NEXT STEPS

Once working locally:

1. **Test thoroughly** - Upload different invoices
2. **Take screenshots** - For your PPT
3. **Deploy to cloud** - Follow deployment guide
4. **Record video** - Show it working
5. **Submit to hackathon** - Win! 🏆

---

## 📦 FILE STRUCTURE

Your folder should look like this:

```
invoiceai-pro-code/
├── app.py                    ✅ Main file
├── requirements.txt          ✅ Dependencies
├── .env                      ✅ Your credentials (create this)
├── .env.example             ✅ Template
├── .gitignore               ✅ Git ignore
├── README.md                ✅ Documentation
├── SETUP.md                 ✅ This file
│
├── src/
│   ├── __init__.py
│   ├── parsers/
│   │   ├── __init__.py
│   │   └── excel_parser.py  ✅ Invoice parser
│   ├── validators/
│   │   ├── __init__.py
│   │   └── gst_validator.py ✅ Validator
│   └── utils/
│       ├── __init__.py
│       ├── gst_rules.py     ✅ Rules database
│       ├── ai_explainer.py  ✅ AI explanations
│       └── ai_chat.py       ✅ Chat assistant
│
├── .streamlit/
│   └── config.toml          ✅ Streamlit config
│
└── venv/                    ⚠️ (created by you)
    └── ...
```

---

## 🎉 YOU'RE READY!

If you see the app running with validation working, **CONGRATULATIONS!** 🎊

You now have a working AI-powered GST validator!

**Next:** Deploy to cloud and submit to hackathon! 🚀

---

**Good Luck! 💪**
