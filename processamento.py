import cv2
import pytesseract

def encontrarRoiPlaca(source):
    img = cv2.imread(source)
    #cv2.imshow('placa', img)
    cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('placa cinza', cinza)
    _, bin = cv2.threshold(cinza, 90, 255, cv2.THRESH_BINARY)
    #cv2.imshow('placa binarizada', bin)
    desfoque = cv2.GaussianBlur(bin, (5, 5), 0)
    #cv2.imshow('placa desfocada', desfoque)
    contornos, hier = cv2.findContours(bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    #cv2.drawContours(img, contornos, -1, (0, 255, 0), 3)
    #cv2.imshow('contornos', img)

    for c in contornos:
        perimetro = cv2.arcLength(c, True)
        if perimetro < 200:
            continue            

        aprox = cv2.approxPolyDP(c, 0.02 * perimetro, True)
        if len(aprox) == 4:
            #cv2.drawContours(img, [aprox], -1, (0, 255, 0), 3)
            x, y, w, h = cv2.boundingRect(aprox)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

            roi = img[y:y+h, x:x+w]

            cv2.imwrite('assets/placa-detectada.jpg', roi)
            #break

    cv2.imshow('contornos', img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def preProcessamentoRoi():
    img_roi = cv2.imread('assets/placa-detectada.jpg')
    if img_roi is None:
        return

    #resized = cv2.resize(img_roi, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    cinza = cv2.cvtColor(img_roi, cv2.COLOR_BGR2GRAY)
    _, bin = cv2.threshold(cinza, 70, 255, cv2.THRESH_BINARY)

    cv2.imwrite("assets/roi-ocr.jpg", bin)

    cv2.imshow("roi", bin)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def ocrImagemRoiPlaca():
    img_roi = cv2.imread('assets/roi-ocr.jpg')
    if img_roi is None:
        return

    config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 6'

    saida = pytesseract.image_to_string(img_roi, lang='eng', config=config)
    print(saida)

if __name__ == "__main__":
    source = 'assets/carro1.jpeg'
    #encontrarRoiPlaca(source)
    #preProcessamentoRoi()
    ocrImagemRoiPlaca()