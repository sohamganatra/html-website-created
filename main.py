import streamlit as st
from get_data_from_exa import search_ai_startups
from structure_data_using_claude import structure_data_using_claude
from convert_structured_data_into_webpage import convert_structured_data_into_webpage
import shutil
import sys
import time

def main():
    st.set_page_config(page_title="Website Generator", page_icon="🌐")
    st.title("Website Generator")

    # Copy backup file
    shutil.copy('backup_index.html', 'index.html')

    # Input field for query
    query = st.text_input("Enter a query:")

    if st.button("Generate Website"):
        if query:
            with st.spinner("Generating website..."):
                try:
                    crew_run = convert_structured_data_into_webpage(query)
                    st.success("Website modification completed!")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a query.")

if __name__ == "__main__":
    main()
