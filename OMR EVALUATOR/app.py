# Import necessary libraries
from flask import Flask, render_template, request
import cv2
import numpy as np
import imutils
from imutils import contours
import four_point

# Initialize Flask app
app = Flask(__name__)

# Default answer key
Answer_key = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get answer key from the form
        answer_key_str = request.form['answer_key']
        # Convert answer key string to dictionary
        global Answer_key
        Answer_key = {int(pair.split(':')[0]): int(pair.split(':')[1]) for pair in answer_key_str.split(',')}

        # Get uploaded image files
        image_files = request.files.getlist('images')
        
        # Process each image
        results = []
        for image_file in image_files:
            # Save the image to a temporary file
            image_path = f"temp_image.png"
            image_file.save(image_path)

            # Process the image
            correct_answers = process_image(image_path)
            results.append({'filename': image_file.filename, 'correct_answers': correct_answers})

        # Render the results on the HTML page
        return render_template('result_multiple.html', results=results)

    return render_template('index_multiple.html')

def process_image(image_path):
    # Your existing code for image processing
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)
    cnts = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    docCnt = None

    if len(cnts) > 0:
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            if len(approx) == 4:
                docCnt = approx
                break

    if docCnt is not None:
        paper = four_point.four_point_transform(image, docCnt.reshape(4, 2))
        warped = four_point.four_point_transform(gray, docCnt.reshape(4, 2))
        thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        questionCnts = []

        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            ar = w / float(h)
            if w >= 20 and h >= 20 and ar >= 0.9 and ar <= 1.1:
                questionCnts.append(c)

        # sorting the contours from top to bottom
        questionCnts = contours.sort_contours(questionCnts, method="top-to-bottom")[0]
        correct = 0

        for (q, i) in enumerate(np.arange(0, len(questionCnts), 5)):
            cnts = contours.sort_contours(questionCnts[i: i + 5])[0]
            bubbled = None

            for (j, c) in enumerate(cnts):
                mask = np.zeros(thresh.shape, dtype="uint8")
                cv2.drawContours(mask, [c], -1, 255, -1)
                mask = cv2.bitwise_and(thresh, thresh, mask=mask)
                total = cv2.countNonZero(mask)

                if bubbled is None or total > bubbled[0]:
                    bubbled = (total, j)

            color = (0, 0, 255)
            k = Answer_key[q]
            if k == bubbled[1]:
                correct = correct + 1

        return correct

    return 0

if __name__ == '__main__':
    app.run(debug=True)
