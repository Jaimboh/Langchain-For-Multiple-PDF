import streamlit as st
import os
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI

# Add a web title
st.title("PDF Search App")

# Access the OpenAI API key from the secrets manager
openai_api_key = st.secrets["openai"]["api_key"]

# Function to save uploaded files to a directory
def save_uploaded_files(uploaded_files, save_directory):
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    for file in uploaded_files:
        with open(os.path.join(save_directory, file.name), "wb") as f:
            f.write(file.getvalue())

    return save_directory

# Upload PDF files
uploaded_files = st.file_uploader("Upload PDF Files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    save_directory = "uploaded_files"
    save_uploaded_files(uploaded_files, save_directory)

# Cache the results to improve performance
@st.cache
def query_model(query, selected_files):
    ...
    # Load PDF files and query model
    ...
    return results

# Display uploaded files and allow user to select specific files to search
uploaded_files = os.listdir("uploaded_files") if os.path.exists("uploaded_files") else []
selected_files = st.multiselect("Select PDF files to search", uploaded_files)

# Get query from user input
query = st.text_input("Enter your query")

# Add a search button
if st.button("Search"):

    # Show loading indicator
    with st.spinner('Searching...'):

        # Query the model only if a query is entered
        if query:

            # If selected files, only search those files
            if selected_files:
                loader = PyPDFDirectoryLoader([os.path.join("uploaded_files", file) for file in selected_files])
            else:
                loader = PyPDFDirectoryLoader("uploaded_files")

            docs = loader.load()
            results = query_model(query, selected_files)

    # Display results
    st.markdown(results)

# Allow user to rephrase query
rephrase = st.button("Rephrase Query")
if rephrase:
    st.text_input("Enter rephrased query", query)

# Add FAQ section
st.subheader("Frequently Asked Questions")
st.markdown("""
- How do I upload PDF files? Use the "Upload PDF Files" file uploader.
- How do I search the PDF files? Enter a query in the "Enter your query" text input and click "Search".
- What if I don't get good results? Click "Rephrase Query" to enter a new query.
- How do I select specific PDF files to search? Use the "Select PDF files to search" multiselect.
""")

# Add a sidebar for file management
st.sidebar.title("File Management")
uploaded_files = os.listdir("uploaded_files") if os.path.exists("uploaded_files") else []
file_to_delete = st.sidebar.selectbox("Select a file to delete", uploaded_files)
if st.sidebar.button("Delete File"):
    os.remove(os.path.join("uploaded_files", file_to_delete))
    st.sidebar.success(f"File '{file_to_delete}' deleted.")
