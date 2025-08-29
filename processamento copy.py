import cv2
import pytesseract

def encontrarRoiPlaca(img):
    cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, bin = cv2.threshold(cinza, 90, 255, cv2.THRESH_BINARY)
    desfoque = cv2.GaussianBlur(bin, (5, 5), 0)
    contornos, hier = cv2.findContours(bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    roi = None
    for c in contornos:
        perimetro = cv2.arcLength(c, True)
        if perimetro < 200:
            continue            
        aprox = cv2.approxPolyDP(c, 0.02 * perimetro, True)
        if len(aprox) == 4:
            x, y, w, h = cv2.boundingRect(aprox)
            roi = img[y:y+h, x:x+w]
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
            break  # Stop at first found plate

    return img, roi

def preProcessamentoRoi(roi):
    cinza = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, bin = cv2.threshold(cinza, 70, 255, cv2.THRESH_BINARY)
    return bin

def ocrImagemRoiPlaca(roi_img):
    config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 6'
    saida = pytesseract.image_to_string(roi_img, lang='eng', config=config)
    print("Placa detectada:", saida.strip())

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Não foi possível acessar a webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        img_contornos, roi = encontrarRoiPlaca(frame.copy())
        cv2.imshow('Webcam - Pressione Q para sair', img_contornos)

        if roi is not None:
            roi_proc = preProcessamentoRoi(roi)
            cv2.imshow('ROI', roi_proc)
            ocrImagemRoiPlaca(roi_proc)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
