import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(
    page_title="AI Mock Interview Assistant",
    page_icon="🎤",
    layout="centered"
)

# Application Heading
st.title("🎤 AI Mock Interview Assistant")

st.write(
    "Prepare for your interviews with AI-generated questions "
    "and personalized feedback."
)

st.divider()

# API Configuration
api_key = st.secrets.get("GROQ_API_KEY", "")

# Interview Setup
st.subheader("Interview Setup")

name = st.text_input(
    "Your Name",
    placeholder="Enter your name"
)

job_role = st.selectbox(
    "Select Your Job Role",
    [
        "Python Developer",
        "Web Developer",
        "Data Analyst",
        "Software Engineer",
        "AI/ML Engineer",
        "Other"
    ]
)

if job_role == "Other":
    job_role = st.text_input("Enter Your Job Role")

interview_type = st.selectbox(
    "Interview Type",
    ["Technical", "HR", "General"]
)

difficulty = st.selectbox(
    "Difficulty Level",
    ["Beginner", "Intermediate", "Advanced"]
)

st.divider()

# Generate Interview Question
st.subheader("Mock Interview")

if st.button("Generate Interview Question"):

    if not api_key:
        st.error("Please configure your Groq API key.")

    elif not name or not job_role:
        st.warning("Please enter your name and job role.")

    else:
        try:
            client = Groq(api_key=api_key)

            prompt = f"""
            Act as a professional interviewer.

            Candidate Name: {name}
            Job Role: {job_role}
            Interview Type: {interview_type}
            Difficulty: {difficulty}

            Generate ONE relevant interview question.

            Do not provide the answer.
            Keep the question clear and appropriate
            for the selected difficulty level.
            """

            with st.spinner("Preparing your interview question..."):

                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

            st.session_state.question = (
                response.choices[0].message.content
            )

            st.session_state.answer = ""
            st.session_state.feedback = ""

        except Exception as e:
            st.error(f"Error generating question: {e}")


# Display Generated Question
if "question" in st.session_state:

    st.success("Your Interview Question")

    st.info(st.session_state.question)

    # Answer Section
    st.subheader("Your Answer")

    answer = st.text_area(
        "Type your answer below:",
        key="answer",
        height=180,
        placeholder="Write your interview answer here..."
    )

    # Submit Answer
    if st.button("Submit Answer"):

        if not answer.strip():
            st.warning("Please enter your answer first.")

        elif not api_key:
            st.error("Groq API key is missing.")

        else:
            try:
                client = Groq(api_key=api_key)

                evaluation_prompt = f"""
                Act as a professional interview evaluator.

                Job Role: {job_role}
                Interview Type: {interview_type}
                Difficulty: {difficulty}

                Interview Question:
                {st.session_state.question}

                Candidate Answer:
                {answer}

                Evaluate the answer and provide:

                1. Score out of 10.
                2. Strengths of the answer.
                3. Areas that need improvement.
                4. A suggested improved answer.

                Be constructive, clear and encouraging.
                Evaluate only the content of the answer.
                Do not assume facts that the candidate has
                not provided.
                """

                with st.spinner("Evaluating your answer..."):

                    response = client.chat.completions.create(
                        model="openai/gpt-oss-20b",
                        messages=[
                            {
                                "role": "user",
                                "content": evaluation_prompt
                            }
                        ]
                    )

                st.session_state.feedback = (
                    response.choices[0].message.content
                )

            except Exception as e:
                st.error(f"Error evaluating answer: {e}")


# Display AI Feedback
if st.session_state.get("feedback"):

    st.divider()

    st.subheader("📊 Interview Performance")

    st.markdown(st.session_state.feedback)

    st.success("Interview evaluation completed!")

    if st.button("Try Another Question"):

        del st.session_state.question
        del st.session_state.feedback
        st.session_state.answer = ""

        st.rerun()


# Footer
st.divider()

st.caption(
    "AI Mock Interview Assistant | "
    "Developed using Python, Streamlit and Groq GPT-OSS"
)
