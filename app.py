import streamlit as st

from agent import (
    extract_pdf_text,
    generate_study_guide,
    create_pdf,
    answer_question
)


st.set_page_config(
    page_title="Study Guide Agent",
    page_icon="📚",
    layout="wide"
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("📚 Study Guide Agent")

st.write(
    "Upload course material, generate a personalized study guide, "
    "and ask questions based only on the uploaded document."
)

st.divider()


# --------------------------------------------------
# Upload PDF
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload a course PDF",
    type=["pdf"]
)


if uploaded_file:

    # Check if a new document was uploaded
    if (
        "current_file" not in st.session_state
        or st.session_state.current_file != uploaded_file.name
    ):
        st.session_state.current_file = uploaded_file.name
        st.session_state.study_guide = None
        st.session_state.answer = None

        try:
            st.session_state.pages = extract_pdf_text(uploaded_file)

        except Exception as e:
            st.error("Could not read the uploaded PDF.")
            st.exception(e)
            st.stop()


    pages = st.session_state.pages


    # --------------------------------------------------
    # Validate PDF
    # --------------------------------------------------

    if not pages:

        st.error(
            "No readable text was found in this PDF."
        )

        st.info(
            "The PDF may contain scanned images instead of selectable text."
        )

        st.stop()


    # --------------------------------------------------
    # Document information
    # --------------------------------------------------

    st.success("PDF uploaded successfully.")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Readable Pages",
            len(pages)
        )

    with col2:
        st.metric(
            "Document",
            uploaded_file.name
        )


    st.divider()


    # --------------------------------------------------
    # Main Tabs
    # --------------------------------------------------

    tab1, tab2 = st.tabs(
        [
            "📄 Generate Study Guide",
            "💬 Ask Questions"
        ]
    )


    # ==================================================
    # TAB 1 - Study Guide
    # ==================================================

    with tab1:

        st.subheader(
            "Generate Personalized Study Guide"
        )

        st.write(
            "The agent reads the uploaded document and follows "
            "the instructions defined in SKILL.md."
        )


        if st.button(
            "✨ Generate Study Guide",
            type="primary",
            use_container_width=True
        ):

            try:

                with st.spinner(
                    "The agent is analyzing the document and applying the Skill..."
                ):

                    study_guide = generate_study_guide(
                        pages
                    )

                    st.session_state.study_guide = study_guide

            except Exception as e:

                st.error(
                    "An error occurred while generating the study guide."
                )

                st.exception(e)


        # Show generated guide
        if st.session_state.get("study_guide"):

            st.success(
                "Study guide generated successfully!"
            )

            st.divider()

            st.markdown(
                st.session_state.study_guide
            )

            st.divider()


            # Create PDF
            try:

                pdf_path = create_pdf(
                    st.session_state.study_guide
                )

                with open(
                    pdf_path,
                    "rb"
                ) as pdf_file:

                    st.download_button(
                        label="📥 Download Study Guide PDF",
                        data=pdf_file.read(),
                        file_name="study_guide.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

            except Exception as e:

                st.error(
                    "The study guide was created, "
                    "but the PDF could not be generated."
                )

                st.exception(e)


    # ==================================================
    # TAB 2 - Questions
    # ==================================================

    with tab2:

        st.subheader(
            "Ask Questions About the Document"
        )

        st.write(
            "The agent answers using only information found "
            "in the uploaded PDF."
        )


        question = st.text_input(
            "Enter your question",
            placeholder="Example: What is the difference between Process and Thread?"
        )


        if st.button(
            "🔎 Ask",
            use_container_width=True
        ):

            if not question.strip():

                st.warning(
                    "Please enter a question."
                )

            else:

                try:

                    with st.spinner(
                        "Searching the document..."
                    ):

                        answer = answer_question(
                            pages,
                            question
                        )

                        st.session_state.answer = answer

                except Exception as e:

                    st.error(
                        "An error occurred while answering the question."
                    )

                    st.exception(e)


        if st.session_state.get("answer"):

            st.divider()

            st.markdown("### Answer")

            st.write(
                st.session_state.answer
            )


else:

    st.info(
        "Upload a PDF document to start."
    )