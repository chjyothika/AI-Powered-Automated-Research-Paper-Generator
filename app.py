"""
Streamlit Web Interface for AI-Powered Research Paper Generator
Provides user-friendly interface for generating academic papers
"""
import streamlit as st
import os
import time
import zipfile
import io
import glob as _glob
from datetime import datetime
import logging

from paper_generator import ResearchPaperGenerator
from config import SUPPORTED_PUBLISHERS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="AI Research Paper Generator",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.disclaimer-box {
    background-color: #fff3cd;
    border: 1px solid #ffeaa7;
    border-radius: 5px;
    padding: 1rem;
    margin: 1rem 0;
}
.success-box {
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    border-radius: 5px;
    padding: 1rem;
    margin: 1rem 0;
}
.error-box {
    background-color: #f8d7da;
    border: 1px solid #f5c6cb;
    border-radius: 5px;
    padding: 1rem;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'generator' not in st.session_state:
        st.session_state.generator = None
    if 'generation_result' not in st.session_state:
        st.session_state.generation_result = None
    if 'generation_time' not in st.session_state:
        st.session_state.generation_time = 0
    if 'system_initialized' not in st.session_state:
        st.session_state.system_initialized = False
    if 'num_authors' not in st.session_state:
        st.session_state.num_authors = 1

def load_generator():
    """Load the paper generator with caching"""
    if st.session_state.generator is None:
        with st.spinner("Initializing AI models and components..."):
            try:
                st.session_state.generator = ResearchPaperGenerator()
                st.session_state.system_initialized = True
                st.success("System initialized successfully!")
            except Exception as e:
                st.error(f"Failed to initialize system: {e}")
                st.session_state.system_initialized = False
                return None
    
    return st.session_state.generator

def display_disclaimer():
    """Display important disclaimer"""
    st.markdown("""
    <div class="disclaimer-box">
    <h3>⚠️ IMPORTANT DISCLAIMER</h3>
    <p><strong>This tool assists in preparing submission-ready manuscripts.</strong></p>
    <ul>
        <li>Human review and validation are REQUIRED before any submission</li>
        <li>Plagiarism checks must be performed</li>
        <li>All citations and references must be verified</li>
        <li>Peer review process is still necessary</li>
        <li>This tool does NOT guarantee publication acceptance</li>
    </ul>
    <p><em>Use this tool responsibly and in accordance with academic ethics.</em></p>
    </div>
    """, unsafe_allow_html=True)

def display_system_status(generator):
    """Display system status in sidebar"""
    st.sidebar.subheader("System Status")
    
    try:
        status = generator.get_system_status()
        
        if "error" in status:
            st.sidebar.error(f"System Error: {status['error']}")
        else:
            st.sidebar.success("✅ arXiv Fetcher Ready")
            
            # RAG Engine Status
            rag_stats = status.get("rag_engine", {})
            if rag_stats:
                st.sidebar.info(f"📚 RAG Database: {rag_stats.get('total_papers', 0)} papers")
            
            # AI Generator Status
            ai_info = status.get("ai_generator", {})
            if ai_info:
                st.sidebar.info(f"🤖 AI Model: {ai_info.get('model_name', 'Unknown')}")
                st.sidebar.info(f"💻 Device: {ai_info.get('device', 'Unknown')}")
            
            # Supported Publishers
            publishers = status.get("supported_publishers", [])
            st.sidebar.info(f"📖 Publishers: {len(publishers)} supported")
    
    except Exception as e:
        st.sidebar.error(f"Status check failed: {e}")

def main():
    """Main Streamlit application"""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">📄 AI-Powered Research Paper Generator</h1>', unsafe_allow_html=True)
    
    # Disclaimer
    display_disclaimer()
    
    # Load generator
    generator = load_generator()
    
    if not st.session_state.system_initialized or generator is None:
        st.error("System not initialized. Please refresh the page.")
        return
    
    # Display system status in sidebar
    display_system_status(generator)
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Paper Generation Settings")

        # ── Author Details (OUTSIDE the form so num_authors rerenders immediately) ──
        with st.expander("Author Details", expanded=True):
            num_authors = st.number_input(
                "Number of Authors",
                min_value=1, max_value=6,
                value=st.session_state.num_authors,
                step=1,
                key="num_authors_input",
                help="How many authors to include in the paper"
            )
            st.session_state.num_authors = int(num_authors)

            authors_data = []
            for idx in range(st.session_state.num_authors):
                st.markdown(f"**Author {idx + 1}**")
                c1, c2, c3 = st.columns(3)
                with c1:
                    a_name = st.text_input("Name", value="Research Author" if idx == 0 else f"Co-Author {idx + 1}", key=f"a_name_{idx}")
                    a_dept = st.text_input("Department", value="Department", key=f"a_dept_{idx}")
                with c2:
                    a_inst = st.text_input("Institution", value="Research Institution", key=f"a_inst_{idx}")
                    a_city = st.text_input("City", value="City", key=f"a_city_{idx}")
                with c3:
                    a_country = st.text_input("Country", value="India", key=f"a_country_{idx}")
                    a_email = st.text_input("Email", value=f"author{idx+1}@institution.edu", key=f"a_email_{idx}")
                authors_data.append({
                    "name": a_name, "institution": a_inst,
                    "department": a_dept, "city": a_city,
                    "country": a_country, "email": a_email,
                })
                if idx < st.session_state.num_authors - 1:
                    st.divider()

        # Backward-compat variables used in result display
        author_name = authors_data[0]["name"] if authors_data else "Research Author"
        author_email = authors_data[0]["email"] if authors_data else "author@institution.edu"

        # Input form (topic, abstract, settings only)
        with st.form("paper_generation_form"):
            # Research topic
            topic = st.text_input(
                "Research Topic/Title",
                placeholder="e.g., Road Accident Safety Prediction using Machine Learning",
                help="Enter the main research topic/title for your paper"
            )

            # User-provided abstract (CRITICAL)
            user_abstract = st.text_area(
                "Research Abstract (Required)",
                placeholder="Enter your research abstract here. This will be the semantic anchor for all generated content...",
                height=150,
                help="Your abstract defines the research scope. All sections will be consistent with this abstract."
            )

            # Publisher selection
            publisher = st.selectbox(
                "Target Publisher",
                options=list(SUPPORTED_PUBLISHERS.keys()),
                format_func=lambda x: f"{x.upper()} - {SUPPORTED_PUBLISHERS[x]['citation_style']} citations",
                help="Select the target publisher for template and citation style"
            )

            # Paper type
            paper_type = st.selectbox(
                "Paper Type",
                options=["research", "review", "survey"],
                help="Select the type of paper to generate"
            )

            # Advanced settings
            with st.expander("Advanced Settings"):
                max_references = st.slider(
                    "Maximum References",
                    min_value=5,
                    max_value=50,
                    value=20,
                    help="Maximum number of references to fetch"
                )

            # Generate button
            generate_button = st.form_submit_button(
                "🚀 Generate Research Paper",
                type="primary",
                use_container_width=True
            )
        
        # Generation process — only runs when form is submitted
        if generate_button:
            if not topic.strip():
                st.error("Please enter a research topic/title.")
                return

            if not user_abstract.strip():
                st.error("Please provide a research abstract. This is required as the semantic anchor.")
                return

            # Clear previous result so stale data isn't shown while generating
            st.session_state.generation_result = None
            st.session_state.generation_time = 0

            progress_bar = st.progress(0)
            status_text = st.empty()

            _should_rerun = False
            try:
                status_text.text("Generating paper — this may take a minute...")
                progress_bar.progress(10)

                start_time = time.time()

                result = generator.generate_paper(
                    topic=topic,
                    user_abstract=user_abstract,
                    publisher=publisher,
                    paper_type=paper_type,
                    max_references=max_references,
                    author_name=author_name,
                    author_email=author_email,
                    authors=authors_data,
                )

                progress_bar.progress(100)
                generation_time = time.time() - start_time

                # Persist result and time — display happens BELOW (outside this block)
                st.session_state.generation_result = result
                st.session_state.generation_time = generation_time

                status_text.empty()
                progress_bar.empty()

                if not result.get("success"):
                    st.error(f"Generation failed: {result.get('error', 'Unknown error')}")
                else:
                    _should_rerun = True

            except Exception as e:
                st.error(f"Generation failed: {e}")
                logger.error(f"Generation error: {e}")

            if _should_rerun:
                st.rerun()  # rerun so the results block below renders cleanly

        # ── Results block ── always shown when session state has a successful result.
        # This persists across all reruns triggered by download / convert buttons.
        result = st.session_state.generation_result
        if result and result.get("success"):
            st.markdown("""
            <div class="success-box">
            <h3>✅ Paper Generated Successfully!</h3>
            </div>
            """, unsafe_allow_html=True)
            display_generation_results(result, st.session_state.generation_time)
    
    with col2:
        st.subheader("Publisher Information")
        
        # Display publisher details
        if publisher in SUPPORTED_PUBLISHERS:
            pub_info = SUPPORTED_PUBLISHERS[publisher]
            st.info(f"""
            **Template:** {pub_info['template']}
            
            **Citation Style:** {pub_info['citation_style']}
            
            **Template URL:** [Official Template]({pub_info['url']})
            """)
        
        # Recent generation result
        if st.session_state.generation_result:
            st.subheader("Last Generation")
            result = st.session_state.generation_result
            
            if result.get("success"):
                st.success(f"Topic: {result['topic']}")
                st.info(f"References: {result['references_used']}")
                st.info(f"Sections: {result['sections_generated']}")
            else:
                st.error("Last generation failed")

def display_generation_results(result, generation_time):
    """Display the results of paper generation"""
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Generation Time", f"{generation_time:.1f}s" if generation_time else "—")
    
    with col2:
        st.metric("Sections Generated", result['sections_generated'])
    
    with col3:
        st.metric("References Found", result['references_found'])
    
    with col4:
        st.metric("References Used", result['references_used'])
    
    # Paper details
    st.subheader("Generated Paper Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Title:** {result['title']}")
        st.write(f"**Author:** {result['author']}")
        st.write(f"**Publisher:** {result['publisher'].upper()}")
        st.write(f"**Type:** {result['paper_type'].title()}")
    
    with col2:
        st.write(f"**Topic:** {result['topic']}")
        st.write(f"**Generated:** {result['generation_time'][:19]}")
        
        # Citation stats
        citation_stats = result.get('citations', {})
        st.write(f"**Citation Style:** {citation_stats.get('citation_style', 'Unknown')}")
    
    # File downloads
    st.subheader("Download Generated Files")
    
    files = result.get('files', {})
    
    # PDF file download (if available)
    pdf_file = files.get('pdf_file')
    if pdf_file and os.path.exists(pdf_file):
        with open(pdf_file, 'rb') as f:
            pdf_content = f.read()
        
        st.download_button(
            label="📄 Download PDF File (.pdf)",
            data=pdf_content,
            file_name=os.path.basename(pdf_file),
            mime="application/pdf",
            use_container_width=True,
            key="dl_pdf_local"
        )
    else:
        # Online PDF conversion option
        latex_file = files.get('latex_file')
        if latex_file and os.path.exists(latex_file):
            col1, col2 = st.columns(2)
            
            with col1:
                convert_key = f"convert_pdf_{result.get('generation_time', '')}"
                if st.button("🌐 Convert to PDF Online", key=convert_key, use_container_width=True):
                    st.session_state[f"converting_{convert_key}"] = True
                
                # Check if conversion is in progress
                if st.session_state.get(f"converting_{convert_key}", False):
                    with st.spinner("Converting LaTeX to PDF online..."):
                        try:
                            from online_pdf_converter import convert_latex_to_pdf_online
                            pdf_path = convert_latex_to_pdf_online(latex_file, "./output")
                            
                            if pdf_path and os.path.exists(pdf_path):
                                # Store PDF path in session state
                                st.session_state[f"pdf_path_{convert_key}"] = pdf_path
                                st.session_state[f"converting_{convert_key}"] = False
                                st.success("PDF converted successfully!")
                                st.rerun()
                            else:
                                st.error("PDF conversion failed. Try installing LaTeX locally.")
                                st.session_state[f"converting_{convert_key}"] = False
                        except Exception as e:
                            st.error(f"Online conversion error: {str(e)}")
                            st.session_state[f"converting_{convert_key}"] = False
                
                # Show download button if PDF exists
                pdf_path = st.session_state.get(f"pdf_path_{convert_key}")
                if pdf_path and os.path.exists(pdf_path):
                    with open(pdf_path, 'rb') as f:
                        pdf_content = f.read()
                    
                    st.download_button(
                        label="📄 Download Converted PDF",
                        data=pdf_content,
                        file_name=os.path.basename(pdf_path),
                        mime="application/pdf",
                        use_container_width=True,
                        key="dl_pdf_converted"
                    )
            
            with col2:
                st.info("💡 **Local PDF generation not available**")
        
        with st.expander("How to install LaTeX for local PDF generation"):
            st.markdown("""
            **Option 1: Install MiKTeX (Recommended)**
            1. Run: `install_latex.bat`
            2. Download from https://miktex.org/
            3. After installation, run: `python enable_pdf.py`
            
            **Option 2: Command Line**
            ```bash
            winget install MiKTeX.MiKTeX
            python enable_pdf.py
            ```
            """)
    
    # LaTeX file download
    latex_file = files.get('latex_file')
    if latex_file and os.path.exists(latex_file):
        with open(latex_file, 'r', encoding='utf-8') as f:
            latex_content = f.read()

        st.download_button(
            label="📝 Download LaTeX File (.tex)",
            data=latex_content,
            file_name=os.path.basename(latex_file),
            mime="text/plain",
            use_container_width=True,
            key="dl_latex"
        )

        # ZIP bundle: .tex + all PNG figures in the same output directory
        output_dir = os.path.dirname(latex_file)
        png_files = _glob.glob(os.path.join(output_dir, "*.png"))
        if png_files:
            zip_buf = io.BytesIO()
            with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
                zf.write(latex_file, os.path.basename(latex_file))
                for png in png_files:
                    zf.write(png, os.path.basename(png))
            zip_buf.seek(0)
            st.download_button(
                label="📦 Download ZIP (LaTeX + Figures)",
                data=zip_buf,
                file_name=os.path.basename(latex_file).replace(".tex", "_bundle.zip"),
                mime="application/zip",
                use_container_width=True,
                help="Download .tex file together with all generated figure PNG files",
                key="dl_zip"
            )
    
    # Bibliography file download
    bib_file = files.get('bibliography_file')
    if bib_file and os.path.exists(bib_file):
        with open(bib_file, 'r', encoding='utf-8') as f:
            bib_content = f.read()
        
        st.download_button(
            label="📚 Download Bibliography File (.bib)",
            data=bib_content,
            file_name=os.path.basename(bib_file),
            mime="text/plain",
            use_container_width=True,
            key="dl_bib"
        )
    
    # Preview sections
    st.subheader("Paper Content Preview")
    
    paper_content = result.get('paper_content', {})
    
    for section in ['abstract', 'introduction', 'literature_review', 'methodology', 'results', 'conclusion']:
        if section in paper_content:
            with st.expander(f"{section.replace('_', ' ').title()} Section"):
                content = paper_content[section]
                st.text_area(
                    f"{section}_content",
                    value=content,
                    height=200,
                    label_visibility="collapsed"
                )

if __name__ == "__main__":
    main()