
import streamlit as st
import pickle

from auth import register_user, login_user
from history import save_history, get_history


# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="Fake News Detection",
    page_icon="📰",
    layout="centered"
)


# -----------------------------------
# LOAD TRAINED MODEL
# -----------------------------------

with open("fake_news_model.pkl", "rb") as file:
    model = pickle.load(file)


# -----------------------------------
# SESSION STATE
# -----------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""


# -----------------------------------
# CUSTOM DESIGN
# -----------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #f4f7fb;
}

.main-title {
    text-align: center;
    color: #1e3a8a;
    font-size: 38px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    color: #555555;
    font-size: 17px;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------------
# LOGIN AND REGISTER PAGE
# -----------------------------------

if not st.session_state.logged_in:

    st.markdown(
        '<p class="main-title">📰 Fake News Detection</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">Machine Learning Based News Detection</p>',
        unsafe_allow_html=True
    )

    st.write("---")

    st.write("Welcome! Please register or login to continue.")

    option = st.radio(
        "Choose an option",
        ["Login", "Register"],
        horizontal=True
    )


    # -----------------------------------
    # REGISTER
    # -----------------------------------

    if option == "Register":

        st.subheader("Create Your Account")

        new_username = st.text_input(
            "Username",
            key="register_username"
        )

        new_password = st.text_input(
            "Password",
            type="password",
            key="register_password"
        )

        if st.button("Register", use_container_width=True):

            if not new_username.strip() or not new_password:

                st.warning("Please enter username and password.")

            elif len(new_password) < 8:

                st.warning(
                    "Password must contain at least 8 characters."
                )

            else:

                success, message = register_user(
                    new_username.strip(),
                    new_password
                )

                if success:

                    st.success(message)

                    st.info(
                        "Registration completed. "
                        "Select Login to enter your account."
                    )

                else:

                    st.error(message)


    # -----------------------------------
    # LOGIN
    # -----------------------------------

    else:

        st.subheader("Login to Your Account")

        username = st.text_input(
            "Username",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Login", use_container_width=True):

            if not username.strip() or not password:

                st.warning("Please enter username and password.")

            elif login_user(username.strip(), password):

                st.session_state.logged_in = True

                st.session_state.username = username.strip()

                st.rerun()

            else:

                st.error("Invalid username or password.")


# -----------------------------------
# NEWS DETECTION PAGE
# -----------------------------------

else:

    st.markdown(
        '<p class="main-title">📰 Fake News Detector</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">Analyze news using Machine Learning</p>',
        unsafe_allow_html=True
    )

    st.write("---")

    st.write(
        f"Welcome, **{st.session_state.username}**!"
    )


    # -----------------------------------
    # LOGOUT
    # -----------------------------------

    if st.button("Logout"):

        st.session_state.logged_in = False

        st.session_state.username = ""

        st.rerun()


    st.write("---")


    # -----------------------------------
    # NEWS INPUT
    # -----------------------------------

    st.subheader("🔍 Analyze a News Article")

    st.write(
        "Enter a news title and article to get a prediction."
    )

    news_title = st.text_input(
        "News Title",
        placeholder="Enter the news headline..."
    )

    news = st.text_area(
        "News Article",
        height=220,
        placeholder="Paste the news article here..."
    )


    # -----------------------------------
    # DETECT NEWS
    # -----------------------------------

    if st.button("🔎 Detect News", use_container_width=True):

        if not news.strip() and not news_title.strip():

            st.warning(
                "Please enter a news title or article."
            )

        else:

            # Match training format
            combined_news = (
                news_title.strip() + " " + news.strip()
            )

            # Predict
            prediction = model.predict(
                [combined_news]
            )[0]

            probabilities = model.predict_proba(
                [combined_news]
            )[0]

            confidence = float(
                max(probabilities) * 100
            )


            # Prediction label
            if prediction == 0:

                prediction_label = "FAKE"

            else:

                prediction_label = "REAL"


            # Save prediction history
            save_history(
                st.session_state.username,
                combined_news,
                prediction_label,
                confidence
            )


            # Display result
            st.write("---")

            st.subheader("📊 Detection Result")

            if prediction_label == "FAKE":

                st.error(
                    "⚠️ Model Prediction: FAKE NEWS"
                )

            else:

                st.success(
                    "✅ Model Prediction: REAL NEWS"
                )


            # Confidence
            st.metric(
                label="Model Confidence",
                value=f"{confidence:.2f}%"
            )

            st.progress(
                confidence / 100
            )

            st.info(
                "This is a machine learning prediction based "
                "on the training dataset. It does not verify "
                "current facts."
            )


    # -----------------------------------
    # DETECTION HISTORY
    # -----------------------------------

    st.write("---")

    st.subheader("📜 Your Detection History")

    records = get_history(
        st.session_state.username
    )

    if records:

        for record in records:

            news_text, prediction, confidence, date = record

            with st.expander(
                f"{prediction} | {date}"
            ):

                st.write("**News Article:**")

                st.write(news_text)

                st.write(
                    "**Prediction:**",
                    prediction
                )

                st.write(
                    f"**Confidence:** {confidence:.2f}%"
                )

                st.write(
                    "**Date:**",
                    date
                )

    else:

        st.info(
            "You have not checked any news articles yet."
        )


    # -----------------------------------
    # FOOTER
    # -----------------------------------

    st.write("---")

    st.caption(
        " Fake News Detection "
        "using NLP and Machine Learning"
    )
