"""
InvoiceAI Pro - AI-Powered GST Invoice Validator
Main Streamlit Application
"""

import streamlit as st
import pandas as pd
import os

# Load secrets from Streamlit Cloud OR local .env
try:
    # For Streamlit Cloud deployment
    os.environ['AWS_ACCESS_KEY_ID'] = st.secrets['AWS_ACCESS_KEY_ID']
    os.environ['AWS_SECRET_ACCESS_KEY'] = st.secrets['AWS_SECRET_ACCESS_KEY']
    os.environ['AWS_DEFAULT_REGION'] = st.secrets['AWS_DEFAULT_REGION']
except:
    # For local development - load from .env
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except:
        pass

# Now import your modules (after environment is set)
from src.parsers.excel_parser import ExcelInvoiceParser
from src.validators.gst_validator import GSTValidator
from src.utils.ai_explainer import AIExplainer
from src.utils.ai_chat import AIChatAssistant


# Page configuration
st.set_page_config(
    page_title="InvoiceAI Pro - GST Validator",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #1E2761 0%, #028090 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .feature-box {
        padding: 1rem;
        border-radius: 8px;
        background-color: #f0f2f6;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize services
parser = ExcelInvoiceParser()
validator = GSTValidator()
ai_explainer = AIExplainer()
ai_chat = AIChatAssistant()

# Header
st.markdown("""
<div class="main-header">
    <h1>🇮🇳 InvoiceAI Pro</h1>
    <p>AI-Powered E-Invoice & Compliance Platform for Indian SMEs</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📋 About")
    st.write("""
    InvoiceAI Pro validates GST invoices against compliance rules
    and helps you fix errors before submission to the GST portal.
    """)
    
    st.divider()
    
    st.header("✨ Features")
    st.markdown("""
    - **Instant Validation** - Check invoices in seconds
    - **AI Explanations** - Understand errors in simple language
    - **Chat Assistant** - Ask GST questions anytime
    - **Smart Analytics** - Track compliance score
    - **Secure** - Your data stays private
    """)
    
    st.divider()
    
    st.header("🏆 Hackathon")
    st.write("**AI for Bharat 2025**")
    st.write("Built with AWS")
    st.image("https://img.shields.io/badge/AWS-Bedrock-orange", width=120)
    
    st.divider()
    
    st.header("👥 Team")
    st.write("**InvoiceAI Innovators**")
    st.write("Vihang Joshi (Lead)")

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["📝 Validate Invoice", "🤖 AI Assistant", "📊 Sample Data", "ℹ️ Help"])

with tab1:
    st.header("Upload Your GST Invoice")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # File uploader
        uploaded_file = st.file_uploader(
            "Upload Excel invoice (.xlsx)",
            type=['xlsx'],
            help="Upload your GST invoice in Excel format with required columns"
        )
    
    with col2:
        st.info("""
        **Required Columns:**
        - Invoice Number
        - Invoice Date
        - GSTIN Seller
        - GSTIN Buyer
        - Item Name
        - HSN Code
        - Quantity
        - Unit Price
        - GST Rate
        """)
    
    if uploaded_file:
        # Save uploaded file temporarily
        temp_file = "temp_invoice.xlsx"
        with open(temp_file, "wb") as f:
            f.write(uploaded_file.getvalue())
        
        # Parse invoice
        with st.spinner("📄 Parsing invoice..."):
            parse_result = parser.parse(temp_file)
        
        if not parse_result["success"]:
            st.error(f"❌ Error parsing invoice: {parse_result['error']}")
            st.stop()
        
        invoice_data = parse_result["data"]
        
        # Show success
        st.success("✅ Invoice parsed successfully!")
        
        # Invoice preview
        with st.expander("📄 Invoice Preview", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Invoice Number", invoice_data['invoice_number'])
                st.metric("Invoice Date", invoice_data['invoice_date'])
            
            with col2:
                st.metric("Total Amount", f"₹{invoice_data['total_amount']:,.2f}")
                st.metric("Total GST", f"₹{invoice_data['total_gst']:,.2f}")
            
            with col3:
                st.metric("Seller GSTIN", invoice_data['gstin_seller'])
                st.metric("Buyer GSTIN", invoice_data['gstin_buyer'])
            
            # Items table
            st.subheader("Invoice Items")
            items_df = pd.DataFrame(invoice_data['items'])
            st.dataframe(
                items_df[['item_name', 'hsn_code', 'quantity', 'unit_price', 'gst_rate', 'total_amount']],
                use_container_width=True
            )
        
        st.divider()
        
        # Validate button
        if st.button("🔍 Validate Against GST Rules", type="primary", use_container_width=True):
            with st.spinner("🔍 Validating invoice against GST compliance rules..."):
                validation_result = validator.validate(invoice_data)
            
            st.divider()
            st.header("📋 Validation Results")
            
            if validation_result["valid"]:
                st.success("### ✅ Invoice is GST Compliant!")
                st.balloons()
                
                st.markdown("""
                **Your invoice passed all validation checks:**
                - ✅ All mandatory fields present
                - ✅ GSTIN format correct
                - ✅ HSN codes valid
                - ✅ GST rates correct
                
                **Next Steps:**
                1. Download the validated invoice
                2. Submit to GST portal
                3. Keep copy for records
                """)
            
            else:
                # Show error summary
                col1, col2 = st.columns(2)
                with col1:
                    st.error(f"### ❌ Found {validation_result['error_count']} Errors")
                with col2:
                    if validation_result['warning_count'] > 0:
                        st.warning(f"### ⚠️ {validation_result['warning_count']} Warnings")
                
                st.markdown("---")
                
                # Show each error with AI explanation
                st.subheader("🔍 Errors to Fix:")
                
                for idx, error in enumerate(validation_result['errors'], 1):
                    with st.container():
                        # Error header
                        col1, col2 = st.columns([4, 1])
                        
                        with col1:
                            severity_emoji = {
                                "high": "🔴",
                                "medium": "🟡",
                                "low": "🟢"
                            }
                            st.markdown(f"## {severity_emoji.get(error['severity'], '⚪')} Error {idx}: {error['field']}")
                        
                        with col2:
                            st.write(f"**Severity**")
                            st.write(f"{error['severity'].upper()}")
                        
                        # Error details
                        st.write(f"**Issue:** {error['message']}")
                        
                        if 'current_value' in error:
                            st.write(f"**Current Value:** `{error['current_value']}`")
                        
                        if 'expected_value' in error:
                            st.write(f"**Expected Value:** `{error['expected_value']}`")
                        
                        # AI Explanation
                        if ai_explainer.enabled:
                            with st.spinner("🤖 AI is generating explanation..."):
                                ai_explanation = ai_explainer.explain_error(error)
                            
                            st.info(f"**🤖 AI Explanation:**\n\n{ai_explanation}")
                            
                            # Quick fix
                            fix_suggestion = ai_explainer.suggest_fix(error)
                            st.success(f"💡 **Quick Fix:** {fix_suggestion}")
                        else:
                            st.warning("⚠️ AI explanations require AWS Bedrock configuration")
                        
                        st.markdown("---")
            
            # Show warnings if any
            if validation_result['warnings']:
                st.subheader("⚠️ Warnings")
                
                for warning in validation_result['warnings']:
                    st.warning(f"• {warning['message']}")
        
        # Clean up temp file
        if os.path.exists(temp_file):
            os.remove(temp_file)

with tab2:
    st.header("🤖 GST Compliance Assistant")
    st.write("Ask any question about GST, HSN codes, or invoice compliance!")
    
    # Check if AI is enabled
    if not ai_chat.enabled:
        st.error("""
        **⚠️ AI Assistant requires AWS Bedrock configuration**
        
        To enable the AI assistant:
        1. Set up AWS credentials in `.env` file
        2. Request Amazon Bedrock model access
        3. Restart the application
        """)
    else:
        # Chat interface
        question = st.text_input(
            "Your question:",
            placeholder="e.g., What HSN code should I use for rice?",
            key="chat_question"
        )
        
        if question:
            with st.spinner("🤖 AI is thinking..."):
                answer = ai_chat.ask(question)
            
            st.markdown("### Answer:")
            st.info(answer)
        
        st.divider()
        
        # Sample questions
        st.subheader("💡 Common Questions:")
        
        sample_questions = [
            "What is the GST rate for mobile phones?",
            "What HSN code should I use for dairy products?",
            "What are the mandatory fields in a GST invoice?",
            "How do I calculate IGST for interstate sales?",
            "What is the difference between B2B and B2C invoices?",
        ]
        
        for q in sample_questions:
            if st.button(q, key=f"sample_{q}"):
                with st.spinner("🤖 AI is thinking..."):
                    answer = ai_chat.ask(q)
                st.info(answer)

with tab3:
    st.header("📊 Sample Invoice Data")
    st.write("Download this sample invoice to test the validator:")
    
    # Create sample data
    sample_data = {
        'Invoice Number': ['INV/2025/001', 'INV/2025/001'],
        'Invoice Date': ['2025-02-13', '2025-02-13'],
        'GSTIN Seller': ['29AABCU9603R1ZV', '29AABCU9603R1ZV'],
        'GSTIN Buyer': ['27AABCU9603R1ZX', '27AABCU9603R1ZX'],
        'Place of Supply': ['27', '27'],
        'Item Name': ['Rice', 'Mobile Phone'],
        'HSN Code': ['1006', '8517'],
        'Quantity': [100, 1],
        'Unit Price': [50, 20000],
        'GST Rate': [5, 18]
    }
    
    sample_df = pd.DataFrame(sample_data)
    
    st.dataframe(sample_df, use_container_width=True)
    
    # Download button
    csv = sample_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Sample Invoice (CSV)",
        data=csv,
        file_name='sample_invoice.csv',
        mime='text/csv',
    )
    
    st.info("""
    **How to use:**
    1. Download the sample CSV
    2. Open in Excel
    3. Save as .xlsx format
    4. Upload to validate
    """)

with tab4:
    st.header("📚 How to Use InvoiceAI Pro")
    
    st.markdown("""
    ### 🚀 Quick Start Guide
    
    #### Step 1: Prepare Your Invoice
    Create an Excel file with these columns:
    - **Invoice Number**: Unique invoice number (e.g., INV/2025/001)
    - **Invoice Date**: Date of invoice (YYYY-MM-DD format)
    - **GSTIN Seller**: Your 15-digit GSTIN
    - **GSTIN Buyer**: Customer's 15-digit GSTIN
    - **Place of Supply**: 2-digit state code (e.g., 27 for Maharashtra)
    - **Item Name**: Product/service name
    - **HSN Code**: 4 or 8 digit HSN code
    - **Quantity**: Number of units
    - **Unit Price**: Price per unit
    - **GST Rate**: GST percentage (0, 5, 12, 18, or 28)
    
    #### Step 2: Upload & Validate
    1. Go to "Validate Invoice" tab
    2. Upload your Excel file
    3. Click "Validate Against GST Rules"
    4. Review results
    
    #### Step 3: Fix Errors
    - Read the error message
    - Check AI explanation for clarity
    - Apply the suggested fix
    - Re-validate
    
    #### Step 4: Submit to GST Portal
    Once validation passes, your invoice is ready for GST portal submission!
    
    ---
    
    ### 🤖 Using AI Assistant
    
    The AI assistant can help you with:
    - **HSN Code Lookup**: "What HSN code for rice?"
    - **GST Rate Queries**: "What's the GST rate for medicines?"
    - **Compliance Questions**: "What fields are mandatory?"
    - **General Help**: Any GST-related question
    
    ---
    
    ### ⚠️ Common Errors
    
    **1. Invalid GSTIN**
    - Must be exactly 15 characters
    - Format: 99AAAAA9999A9Z9
    
    **2. Wrong HSN Code**
    - Must be 4 or 8 digits
    - Check against GST HSN master list
    
    **3. Incorrect GST Rate**
    - Each HSN has specific GST rate
    - Use AI assistant to find correct rate
    
    **4. Missing Fields**
    - All mandatory fields required
    - Check your Excel file has all columns
    
    ---
    
    ### 🔧 Technical Support
    
    **For issues:**
    - Check if AWS credentials are configured
    - Verify Excel file format
    - Try sample invoice first
    - Contact: support@invoiceai.pro
    
    **AWS Configuration:**
    Create `.env` file with:
    ```
    AWS_ACCESS_KEY_ID=your_key
    AWS_SECRET_ACCESS_KEY=your_secret
    AWS_DEFAULT_REGION=us-east-1
    ```
    """)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; padding: 2rem;'>
    <p><strong>InvoiceAI Pro</strong> - AI-Powered E-Invoice & Compliance Platform</p>
    <p>Built for AI for Bharat Hackathon 2025 | Powered by AWS Bedrock</p>
    <p>© 2025 InvoiceAI Innovators | All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)
