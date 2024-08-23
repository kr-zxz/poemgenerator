import os
import streamlit as st
import google.generativeai as genai

def main():
    # Set your Gemini API key directly here
    api_key = 'AIzaSyA7z51_2Wvy6ZDn8OA-eF55rQDsKoURUZc'  
    genai.configure(api_key=api_key)

    # Set up the Streamlit interface
    st.title("Poem Generator")

    # User input for poem theme or topic
    user_input = st.text_area(
        "Please describe the theme or topic of the poem below (e.g., 'A poem about the beauty of nature')",
        height=200
    )

    # Button to generate poem
    if st.button("Generate Poem"):
        if user_input.strip():
            # Create a prompt for generating the poem
            prompt = f"""
            Based on the following description, please generate a creative poem:

            "{user_input}"

            The poem should be engaging, thematic, and adhere to the theme described.
            """

            try:
                # Use the Gemini generative model to generate the poem
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                poem_body = response.text

                # Store the generated poem in the session state to keep it persistent
                st.session_state.generated_poem = poem_body
                st.session_state.copy_status = "Copy Poem to Clipboard"  # Reset the copy button text

            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.warning("We couldn't generate the poem. Please try again later.")
        else:
            st.warning("Please provide a description of the poem theme or topic.")

    # Check if the generated poem is in session state
    if 'generated_poem' in st.session_state:
        st.subheader("Your Generated Poem:")
        poem_text_area = st.text_area("Generated Poem:", st.session_state.generated_poem, height=400, key="poem_content")

        # Button to copy poem to clipboard
        copy_button = st.button(st.session_state.get('copy_status', "Copy Poem to Clipboard"), key="copy_button")

        if copy_button:
            # JavaScript code to copy the text and change button text
            st.write(f"""
                <script>
                function copyToClipboard() {{
                    var poemContent = document.querySelector('#poem_content');
                    var range = document.createRange();
                    range.selectNode(poemContent);
                    window.getSelection().removeAllRanges();  // Clear current selection
                    window.getSelection().addRange(range);  // Select the content
                    document.execCommand('copy');  // Copy the selected content
                    window.getSelection().removeAllRanges();  // Clear selection
                    document.getElementById('copy_button').innerText = 'COPIED';
                }}
                copyToClipboard();
                </script>
                """, unsafe_allow_html=True)
            st.session_state.copy_status = "COPIED"  # Update the button text to "COPIED"

if __name__ == "__main__":
    main()
