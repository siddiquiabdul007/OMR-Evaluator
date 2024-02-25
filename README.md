# OMR-Evaluator
GitHub repository for Python text analysis script, analyzing sentiment, readability, and word frequencies from a list of URLs
Automatic Multiple-Choice Grading System using Flask and OpenCV

This repository contains a Flask web application for automatically grading multiple-choice answer sheets. The system utilizes computer vision techniques from the OpenCV library to process scanned or photographed answer sheets, identify and extract the regions of interest, and determine the correctness of the selected answers.

Key Features:

Web Interface: Built using Flask, the web interface allows users to upload answer sheets and specify the answer key.
Image Processing: OpenCV is employed for image processing tasks such as contour detection, perspective transformation, and thresholding to isolate answer bubbles.
Answer Grading: The application compares the identified bubbles against a user-provided answer key, tallying correct responses.
Dynamic Result Display: Results are dynamically presented on the web page, indicating the correctness of each answer sheet.
How to Use:

Clone the repository.
Install the required libraries using pip install -r requirements.txt.
Run the Flask application with python app.py.
Access the web interface, upload answer sheets, and provide the answer key for automated grading.
Dependencies:

Flask
OpenCV
NumPy
Imutils
Contributing:
Contributions, issues, and feature requests are welcome! Feel free to open an issue or create a pull request.

License:
No License

Acknowledgments:
The code structure and initial implementation are based on four_point.py for perspective transformation and contour sorting. Credits to the authors for their contributions.

Disclaimer:
This project is developed for educational and experimental purposes. Use it responsibly and ensure compliance with academic integrity policies.




