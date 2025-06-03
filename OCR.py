import cv2
import pytesseract
from PIL import Image
import io
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog

# Tesseract 실행 파일 경로 지정 (Windows 사용자의 경우)
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'


def extract_text_from_image(img):
    """
    이미지에서 텍스트를 추출하는 함수입니다.
    Args:
        img: OpenCV 이미지 객체
    Returns:
        추출된 텍스트
    """
    # 이미지 전처리
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # Tesseract OCR 실행, 환경 변수 및 config 적용
    os.environ['TESSDATA_PREFIX'] = '/usr/share/tesseract-ocr/4.00/tessdata'
    config = ('-l kor+eng --oem 3 --psm 6')
    text = pytesseract.image_to_string(Image.fromarray(gray), config=config)

    return text

# Tkinter로 파일 선택창 열기
root = tk.Tk()
root.withdraw()  # Tkinter 창 숨기기

file_paths = filedialog.askopenfilenames(
    title="이미지 파일을 선택하세요",
    filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff;*.tif")]
)

if not file_paths:
    print("선택된 파일이 없습니다.")
else:
    for file_path in file_paths:
        with open(file_path, 'rb') as f:
            file_content = f.read()
        image_bytes = io.BytesIO(file_content)
        image = Image.open(image_bytes)
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        extracted_text = extract_text_from_image(img)
        print(f"파일: {file_path}\n텍스트: {extracted_text}\n{'-'*40}")