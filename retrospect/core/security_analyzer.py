from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from fpdf import FPDF
import json
import os
from dotenv import load_dotenv
from retrospect.utils.logger import appLogger

class SensitiveDataAnalyzer:
    """
    SensitiveDataAnalyzer is a class designed to analyze unstructured text for potentially leaked sensitive information
    and identify possible attack vectors based on publicly available data.

    Attributes:
        model (ChatGroq): A Groq language model instance for generating insights and analysis of sensitive data.
        embeddings (HuggingFaceEmbeddings): Embedding model used for text representation in document retrieval.
    """
    
    def __init__(self):
        """
        Initializes the SensitiveDataAnalyzer class by loading the Groq API key and model ID from environment variables
        and configuring the necessary components (Groq model and HuggingFace embeddings) for sensitive data analysis.

        Raises:
            ValueError: If the Groq API key or model ID is not found in the environment variables.
        """
        load_dotenv()

        groq_api_key = os.getenv("GROQ_API_KEY")
        model_id = os.getenv("MODEL_ID")

        if not groq_api_key or not model_id:
            raise ValueError("GROQ API key and Model ID are required. Ensure they are defined in the .env file.")

        self.model = ChatGroq(model=model_id, temperature=1, api_key=groq_api_key)
        self.embeddings = HuggingFaceEmbeddings()
        appLogger.info("🔥 Groq model initialized successfully! Ready to roll. 💻")

    def analyze_sensitive_data(self, unified_file_path: str, pdf_path="sensitive_data_report.pdf", json_path="sensitive_data_report.json"):
        """
        Analyzes the unified text file for sensitive data and generates a detailed report highlighting potential attack vectors.
        The report will include actionable insights, possible data leaks (email addresses, API keys, etc.), and recommendations.

        Args:
            unified_file_path (str): Path to the unified file containing unprocessed HTML snapshot text.
            pdf_path (str, optional): Path where the generated PDF report will be saved. Defaults to "sensitive_data_report.pdf".
            json_path (str, optional): Path where the generated JSON report will be saved. Defaults to "sensitive_data_report.json".

        Returns:
            str: A message indicating whether the report generation was successful or if an error occurred.
        """
        try:
            appLogger.info("🔍 Reading and processing unified data from file...")

            with open(unified_file_path, "r", encoding="utf-8") as file:
                scan_results = file.read()

            appLogger.info("📚 Creating FAISS index for document retrieval...")
            chunks = self._split_log_into_chunks(scan_results)

            vector_store = FAISS.from_documents(chunks, self.embeddings)
            retriever = vector_store.as_retriever()
            chain = RetrievalQA.from_chain_type(self.model, retriever=retriever)

            report = self._generate_analysis_prompt()

            appLogger.info("🤖 Running the analysis with retrieval chain...")
            result = chain.invoke(report)

            self._generate_pdf_report(result, pdf_path)
            self._generate_json_report(result, json_path)

            appLogger.info("✅ Report generation complete! Files saved successfully. 🛡️")
            return "Report generation complete. PDF and JSON reports have been saved."

        except Exception as e:
            appLogger.error(f"🚨 Error during report generation: {e}")
            return f"Error during report generation: {e}"

    def _split_log_into_chunks(self, scan_results):
        """
        Splits the unified scan results into smaller chunks to facilitate better processing.

        Args:
            scan_results (str): The unified scan results (extracted HTML text).

        Returns:
            list: A list of text chunks created from the scan results.
        """
        appLogger.info(f"🔪 Splitting log into chunks ...")
        text_splitter = CharacterTextSplitter(chunk_size=4500, chunk_overlap=0)
        return text_splitter.create_documents([scan_results])

    def _generate_analysis_prompt(self):
        """
        Generates a prompt to instruct the Groq model to analyze the unified scan results for sensitive data leaks
        and identify potential security risks, such as exposed email addresses, API keys, passwords, and other
        critical data that could pose an attack vector.

        The model is instructed to act as a cybersecurity expert focused on identifying and reporting data leaks.
        """
        return (
            "You are an advanced AI-powered cybersecurity expert, tasked with identifying **sensitive data leaks** "
            "and **security vulnerabilities** from a series of publicly accessible documents and web data. "
            "Your mission is to conduct a **thorough and structured analysis** to detect any leaked or exposed information "
            "that could be exploited in a cyberattack. This includes any data that could lead to unauthorized access or compromise security.\n\n"
            
            "In your analysis, you must focus only on the most **relevant** and **critical** information that directly impacts security. "
            "Do not consider information that does not present a clear risk or cannot be exploited. Only include data that poses a direct "
            "threat to the system's integrity or confidentiality.\n\n"

            "The focus of your analysis should be on identifying the following types of sensitive data:\n\n"
            
            "   - **Email addresses** (e.g., personal or corporate email addresses that may be used in phishing attacks).\n"
            "   - **API keys and tokens** (e.g., keys for accessing cloud services, databases, or other critical infrastructure).\n"
            "   - **Passwords and other credentials** (e.g., plaintext passwords, username and password pairs, authentication tokens).\n"
            "   - **Sensitive URLs** (e.g., database connection strings, private repositories, internal service endpoints, or access URLs that could be misused).\n"
            "   - **Personal information** (e.g., addresses, phone numbers, social security numbers, or anything that can be used for identity theft).\n"
            "   - **Encryption keys and private keys** (e.g., cloud credentials, API signing keys, private certificates).\n"
            "   - **System configuration data** (e.g., configurations that may reveal system architecture, internal endpoints, or vulnerabilities).\n"
            "   - **Other critical data** that may expose attack vectors (e.g., backup files, administrative credentials, cloud service keys, etc.).\n\n"
            
            "For each potential leak or sensitive data found, focus on providing the most relevant and actionable analysis with the following components:\n\n"
            
            "   1. **Description**: A concise, clear description of the leaked or exposed information. Include the type of data and its relevance in the context of security.\n"
            "   2. **Impact Assessment**: An analysis of the potential **security impact** of the leak, including the risks it poses to the system, network, or organization. "
            "Highlight the likelihood of exploitation and the severity of the issue.\n"
            "   3. **Risk Level**: Assign a risk level (e.g., High, Medium, Low) based on the criticality of the data and its potential for exploitation.\n"
            "   4. **Immediate Mitigation Actions**: Provide specific, **actionable** steps to **mitigate** the risk. Focus on practical, prioritized actions for security teams to follow. "
            "These steps should address the most critical vulnerabilities first. Explain the urgency and importance of these actions.\n"
            "   5. **Long-term Recommendations**: If applicable, offer longer-term recommendations for preventing such leaks, such as improved security protocols or better data management practices.\n\n"
            
            "Your analysis should prioritize **high-risk** findings and focus on **immediate, actionable solutions** to resolve the most critical vulnerabilities. "
            "Your goal is to protect the system from potential exploitation due to any sensitive data leaks.\n\n"
            
            "Ensure that your analysis is concise, with a focus on the most **relevant** findings. Do not include irrelevant data or anything that does not pose a direct security risk. "
            "Your findings must be **actionable**, clearly communicated, and tailored for system administrators or security professionals to act swiftly.\n\n"
            
            "Also, provide the **context** of where each leak or vulnerability was found (e.g., file names, document sections) to help security teams locate the exposed data in the original source."
        )


    def _generate_pdf_report(self, analysis, file_path="sensitive_data_report.pdf"):
        """
        Generates a PDF report based on the analysis results and saves it to the specified file path.

        Args:
            analysis (dict): The analysis results containing actionable insights and findings.
            file_path (str, optional): Path where the PDF report will be saved. Defaults to "sensitive_data_report.pdf".
        """
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", style='B', size=16)
            pdf.cell(200, 10, txt="Sensitive Data Leak Report", ln=True, align='C')
            pdf.ln(10)
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, txt=analysis.get("result", ""))
            pdf.output(file_path)
            appLogger.info(f"📄 PDF report generated: {file_path}")
        except Exception as e:
            appLogger.error(f"⚠️ Error generating PDF report: {e}")

    def _generate_json_report(self, analysis, file_path="sensitive_data_report.json"):
        """
        Generates a JSON report based on the analysis results and saves it to the specified file path.

        Args:
            analysis (dict): The analysis results containing actionable insights and findings.
            file_path (str, optional): Path where the JSON report will be saved. Defaults to "sensitive_data_report.json".
        """
        try:
            report_data = {"analysis": analysis.get("result", "")}
            with open(file_path, 'w') as json_file:
                json.dump(report_data, json_file, indent=4)
            appLogger.info(f"📂 JSON report generated: {file_path}")
        except Exception as e:
            appLogger.error(f"⚠️ Error generating JSON report: {e}")