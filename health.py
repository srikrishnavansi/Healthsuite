import os
import PIL
import requests
from PIL import Image
import streamlit as st
from google import genai
from google.genai import types

def analyze_image(api_key, image_path):
    client = genai.Client(api_key=api_key)
    image = PIL.Image.open(image_path)
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=[
            """
            You are a highly skilled medical imaging expert with extensive knowledge in radiology and diagnostic imaging. Analyze the patient's medical image and structure your response as follows:

            ### 1. Image Type & Region
            - Specify imaging modality (X-ray/MRI/CT/Ultrasound/etc.)
            - Identify the patient's anatomical region and positioning
            - Comment on image quality and technical adequacy

            ### 2. Key Findings
            - List primary observations systematically
            - Note any abnormalities in the patient's imaging with precise descriptions
            - Include measurements and densities where relevant
            - Describe location, size, shape, and characteristics
            - Rate severity: Normal/Mild/Moderate/Severe

            ### 3. Diagnostic Assessment
            - Provide primary diagnosis with confidence level
            - List differential diagnoses in order of likelihood
            - Support each diagnosis with observed evidence from the patient's imaging
            - Note any critical or urgent findings

            ### 4. Patient-Friendly Explanation
            - Explain the findings in simple, clear language that the patient can understand
            - Avoid medical jargon or provide clear definitions
            - Include visual analogies if helpful
            - Address common patient concerns related to these findings

            ### 5. Research Context
            IMPORTANT: Use the DuckDuckGo search tool to:
            - Find recent medical literature about similar cases
            - Search for standard treatment protocols
            - Provide a list of relevant medical links of them too
            - Research any relevant technological advances
            - Include 2-3 key references to support your analysis

            Format your response using clear markdown headers and bullet points. Be concise yet thorough.
            """,
            image
        ]
    )
    return response.text

def display_dietary_plan(plan_content):
    with st.expander("📋 Your Personalized Dietary Plan", expanded=True):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 🎯 Why this plan works")
            st.info(plan_content.get("why_this_plan_works", "Information not available"))
            st.markdown("### 🍽️ Meal Plan")
            st.write(plan_content.get("meal_plan", "Plan not available"))
        
        with col2:
            st.markdown("### ⚠️ Important Considerations")
            considerations = plan_content.get("important_considerations", "").split('\n')
            for consideration in considerations:
                if consideration.strip():
                    st.warning(consideration)

def display_fitness_plan(plan_content):
    with st.expander("💪 Your Personalized Fitness Plan", expanded=True):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 🎯 Goals")
            st.success(plan_content.get("goals", "Goals not specified"))
            st.markdown("### 🏋️‍♂️ Exercise Routine")
            st.write(plan_content.get("routine", "Routine not available"))
        
        with col2:
            st.markdown("### 💡 Pro Tips")
            tips = plan_content.get("tips", "").split('\n')
            for tip in tips:
                if tip.strip():
                    st.info(tip)

def main():
    st.set_page_config(
        page_title="AI Health Suite",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stButton>button {
            width: 100%;
            border-radius: 5px;
            height: 3em;
        }
        .success-box {
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: #f0fff4;
            border: 1px solid #9ae6b4;
        }
        .warning-box {
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: #fffaf0;
            border: 1px solid #fbd38d;
        }
        div[data-testid="stExpander"] div[role="button"] p {
            font-size: 1.1rem;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🏥 AI Health Suite")

    # Initialize session state
    if 'dietary_plan' not in st.session_state:
        st.session_state.dietary_plan = {}
        st.session_state.fitness_plan = {}
        st.session_state.qa_pairs = []
        st.session_state.plans_generated = False

    # Sidebar for API key configuration and feature selection
    with st.sidebar:
        st.header("🔑 API Configuration")
        gemini_api_key = st.text_input(
            "Gemini API Key",
            type="password",
            help="Enter your Gemini API key to access the service"
        )
        
        if not gemini_api_key:
            st.warning("⚠️ Please enter your Gemini API Key to proceed")
            st.markdown("[Get your API key here](https://aistudio.google.com/apikey)")
            return
        
        st.success("API Key accepted!")

        feature = st.selectbox("Select Feature", ["🏥 Medical Imaging Diagnosis", "🏋️‍♂️ AI Health & Fitness Planner"])

    if gemini_api_key:
        try:
            gemini_model = genai.Client(api_key=gemini_api_key)
        except Exception as e:
            st.error(f"❌ Error initializing Gemini model: {e}")
            return

        if feature == "🏥 Medical Imaging Diagnosis":
            st.header("🏥 Medical Imaging Diagnosis Agent")
            st.write("Upload a medical image for professional analysis")

            upload_container = st.container()
            image_container = st.container()
            analysis_container = st.container()

            with upload_container:
                uploaded_file = st.file_uploader(
                    "Upload Medical Image",
                    type=["jpg", "jpeg", "png", "dicom"],
                    help="Supported formats: JPG, JPEG, PNG, DICOM"
                )

            if uploaded_file is not None:
                with image_container:
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        image = Image.open(uploaded_file)
                        width, height = image.size
                        aspect_ratio = width / height
                        new_width = 500
                        new_height = int(new_width / aspect_ratio)
                        resized_image = image.resize((new_width, new_height))
                        
                        st.image(
                            resized_image,
                            caption="Uploaded Medical Image",
                            use_container_width=True
                        )
                        
                        analyze_button = st.button(
                            "🔍 Analyze Image",
                            type="primary",
                            use_container_width=True
                        )
                
                with analysis_container:
                    if analyze_button:
                        image_path = "temp_medical_image.png"
                        with open(image_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        with st.spinner("🔄 Analyzing image... Please wait."):
                            try:
                                response = analyze_image(gemini_api_key, image_path)
                                st.markdown("### 📋 Analysis Results")
                                st.markdown("---")
                                st.markdown(response)
                                st.markdown("---")
                                st.caption(
                                    "Note: This analysis is generated by AI and should be reviewed by "
                                    "a qualified healthcare professional."
                                )
                            except Exception as e:
                                st.error(f"Analysis error: {e}")
                            finally:
                                if os.path.exists(image_path):
                                    os.remove(image_path)
            else:
                st.info("👆 Please upload a medical image to begin analysis")

        elif feature == "🏋️‍♂️ AI Health & Fitness Planner":
            st.header("🏋️‍♂️ AI Health & Fitness Planner")
            st.markdown("""
                <div style='background-color: #00008B; padding: 1rem; border-radius: 0.5rem; margin-bottom: 2rem;'>
                Get personalized dietary and fitness plans tailored to your goals and preferences.
                Our AI-powered system considers your unique profile to create the perfect plan for you.
                </div>
            """, unsafe_allow_html=True)

            st.header("👤 Your Profile")
            
            col1, col2 = st.columns(2)
            
            with col1:
                age = st.number_input("Age", min_value=10, max_value=100, step=1, help="Enter your age")
                height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, step=0.1)
                activity_level = st.selectbox(
                    "Activity Level",
                    options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"],
                    help="Choose your typical activity level"
                )
                dietary_preferences = st.selectbox(
                    "Dietary Preferences",
                    options=["Vegetarian", "Keto", "Gluten Free", "Low Carb", "Dairy Free"],
                    help="Select your dietary preference"
                )

            with col2:
                weight = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0, step=0.1)
                sex = st.selectbox("Sex", options=["Male", "Female", "Other"])
                fitness_goals = st.selectbox(
                    "Fitness Goals",
                    options=["Lose Weight", "Gain Muscle", "Endurance", "Stay Fit", "Strength Training"],
                    help="What do you want to achieve?"
                )

            if st.button("🎯 Generate My Personalized Plan", use_container_width=True):
                with st.spinner("Creating your perfect health and fitness routine..."):
                    try:
                        dietary_response = gemini_model.models.generate_content(
                            model="gemini-2.0-flash-exp",
                            contents=[f"Create a personalized dietary plan for a user with the following profile:\n\nAge: {age}\nWeight: {weight}kg\nHeight: {height}cm\nSex: {sex}\nActivity Level: {activity_level}\nDietary Preferences: {dietary_preferences}\nFitness Goals: {fitness_goals}"]
                        )
                        dietary_plan = {
                            "why_this_plan_works": "High Protein, Healthy Fats, Moderate Carbohydrates, and Caloric Balance",
                            "meal_plan": dietary_response.text,
                            "important_considerations": """
                            - Hydration: Drink plenty of water throughout the day
                            - Electrolytes: Monitor sodium, potassium, and magnesium levels
                            - Fiber: Ensure adequate intake through vegetables and fruits
                            - Listen to your body: Adjust portion sizes as needed
                            """
                        }

                        fitness_response = gemini_model.models.generate_content(
                            model="gemini-2.0-flash-exp",
                            contents=[f"Create a personalized fitness plan for a user with the following profile:\n\nAge: {age}\nWeight: {weight}kg\nHeight: {height}cm\nSex: {sex}\nActivity Level: {activity_level}\nDietary Preferences: {dietary_preferences}\nFitness Goals: {fitness_goals}"]
                        )
                        fitness_plan = {
                            "goals": "Build strength, improve endurance, and maintain overall fitness",
                            "routine": fitness_response.text,
                            "tips": """
                            - Track your progress regularly
                            - Allow proper rest between workouts
                            - Focus on proper form
                            - Stay consistent with your routine
                            """
                        }

                        st.session_state.dietary_plan = dietary_plan
                        st.session_state.fitness_plan = fitness_plan
                        st.session_state.plans_generated = True
                        st.session_state.qa_pairs = []

                        display_dietary_plan(dietary_plan)
                        display_fitness_plan(fitness_plan)

                    except Exception as e:
                        st.error(f"❌ An error occurred: {e}")

            if st.session_state.plans_generated:
                st.header("❓ Questions about your plan?")
                question_input = st.text_input("What would you like to know?")

                if st.button("Get Answer"):
                    if question_input:
                        with st.spinner("Finding the best answer for you..."):
                            dietary_plan = st.session_state.dietary_plan
                            fitness_plan = st.session_state.fitness_plan

                            context = f"Dietary Plan: {dietary_plan.get('meal_plan', '')}\n\nFitness Plan: {fitness_plan.get('routine', '')}"
                            full_context = f"{context}\nUser Question: {question_input}"

                            try:
                                run_response = gemini_model.models.generate_content(
                                    model="gemini-2.0-flash-exp",
                                    contents=[full_context]
                                )

                                if hasattr(run_response, 'text'):
                                    answer = run_response.text
                                else:
                                    answer = "Sorry, I couldn't generate a response at this time."

                                st.session_state.qa_pairs.append((question_input, answer))
                            except Exception as e:
                                st.error(f"❌ An error occurred while getting the answer: {e}")

                if st.session_state.qa_pairs:
                    st.header("💬 Q&A History")
                    for question, answer in st.session_state.qa_pairs:
                        st.markdown(f"**Q:** {question}")
                        st.markdown(f"**A:** {answer}")

if __name__ == "__main__":
    main()