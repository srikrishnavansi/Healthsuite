# AI Health Suite

## Overview
AI Health Suite is a comprehensive application that integrates both medical imaging diagnosis and personalized health & fitness planning. The application leverages the Gemini API to analyze medical images and provide personalized dietary and fitness plans tailored to individual user profiles.

## Features
- **Medical Imaging Diagnosis**: Upload medical images for professional analysis using advanced computer vision and radiological expertise.
- **AI Health & Fitness Planner**: Get personalized dietary and fitness plans based on user profiles, including age, weight, height, activity level, dietary preferences, and fitness goals.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ai-health-suite.git
   cd ai-health-suite
   ```

2. **Create a virtual environment and activate it:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the Streamlit application:**
   ```bash
   streamlit run ai_health_suite.py
   ```

2. **Configure your Gemini API Key:**
   - Enter your Gemini API Key in the sidebar to access the service.
   - If you don't have a key, you can get one from [Google AI Studio](https://aistudio.google.com/apikey).

3. **Select a Feature:**
   - Choose between "Medical Imaging Diagnosis" and "AI Health & Fitness Planner" from the sidebar.

### Medical Imaging Diagnosis
- Upload a medical image in JPG, JPEG, PNG, or DICOM format.
- The application will analyze the image and provide a detailed diagnostic report.

### AI Health & Fitness Planner
- Enter your profile details including age, weight, height, sex, activity level, dietary preferences, and fitness goals.
- Generate personalized dietary and fitness plans.
- Ask questions about your plan and get answers based on the generated content.

## Contributing
Contributions are welcome! Please create an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements
- Thanks to [Google Gemini](https://ai.google.dev/gemini-api/docs/vision?lang=python) for providing the API for image analysis.
- Thanks to the Streamlit team for their amazing framework.
