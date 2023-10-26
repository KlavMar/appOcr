import os
import pytesseract
from flask import Flask, request, jsonify,render_template,Response
#import cv2
from PIL import Image, ImageDraw
# Configurez l'emplacement du programme Tesseract OCR (il peut être nécessaire de le modifier en fonction de votre installation)
#pytesseract.pytesseract.tesseract_cmd ='/usr/bin/tesseract'
pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'

app = Flask(__name__)

def img_to_string(string_img):
    
    return pytesseract.image_to_string(string_img,config="-c tessedit_char_whitelist=0123456789")


def recup_roi(image,roi):
    #return image[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
    return image.crop((int(roi[0]), int(roi[1]), int(roi[0] + roi[2]), int(roi[1] + roi[3])))


# Définissez l'URL de la page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Définissez l'URL pour le traitement de l'OCR
@app.route('/process_image', methods=['POST'])
def hall_of_fame_process():
    try:

        if 'image' not in request.files:
            return jsonify({'error': "Upload is down"}), 400

        # Récupérez le fichier image depuis le formulaire
        image = request.files['image']
        img = Image.open(image)

        # Redimensionnez l'image
        width = 1600
        height = 900
        img = img.resize((width, height))
        
        # Appliquez l'OCR à l'image redimensionnée
        texte_ocr = ocr(img)


        # Retournez les résultats au format JSON
        response = jsonify({'data': texte_ocr})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response


    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Définissez l'URL pour le traitement de l'OCR
@app.route('/process_image_troops', methods=['POST'])
def troops_process():
    try:

        if 'image' not in request.files:
            return jsonify({'error': "Upload is down"}), 400

        # Récupérez le fichier image depuis le formulaire
        image = request.files['image']
        img = Image.open(image)
       
        # Redimensionnez l'image
        width = 1600
        height = 900
        img = img.resize((width, height))
        
        # Appliquez l'OCR à l'image redimensionnée
        texte_ocr = troops(img)
        print(texte_ocr)

        # Retournez les résultats au format JSON
        response = jsonify({'data': texte_ocr})
        print(jsonify({'data': texte_ocr}))
        allowed_origins='http://192.168.1.17:8080'
        response.headers.add('Access-Control-Allow-Origin', allowed_origins)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST , OPTIONS')
        print(response)
        return response


    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def resized_img(image):
    width=1600
    height=900
    image = Image.open(image)
   # resized_image = Image.resize(image, (width, height))
    resized_image = image.resize((width, height))
    # Enregistrer l'image redimensionnée
    resized_image.save("resized.png")
    #cv2.imwrite('resized.jpg', resized_image)

def ocr(image):
    try:

        text=list()

        x0=440
        y0=510
        space_x=240
        space_y=80
        
        w=121
        h=60
        
        ### calibration 
        ### Calibrer les x0 et y0 des deux premières lignes 
        ### Quelques pixels d'écart sur les 30 images testées 
        ### Chaque ligne et chaque espace sont identiques 
        ### pas de boucle suite à l'inconvénient des pixels de départ x0 et y0 
        ### ligne 0 = référence


        
        ####
        # ligne -1
        ## items 1
        roi = (x0,y0-space_y*2,w,h)
        data = img_to_string(recup_roi(image,roi))
        if len(data)==0:
            y0=y0*0.9
            roi = (x0,y0-space_y*2,w,h)
            data = img_to_string(recup_roi(image,roi))
            if len(data) ==0:
                y0=510
                roi = (x0,y0-space_y*2,w,h)
                data = img_to_string(recup_roi(image,roi))
    
        text.append(data)
        ## items 2 
        roi=(x0+space_x,y0-space_y*2,w,h)
        text.append(img_to_string(recup_roi(image,roi)))
        
        ## items 3 
        roi=(x0+space_x*2,y0-space_y*2,w,h)
        text.append(img_to_string(recup_roi(image,roi)))
        
        
        # ligne 0
        ## items 1
        roi = (x0,y0-space_y,w,h)
        data = img_to_string(recup_roi(image,roi))
        if len(data)<=6:
            x0=round(x0*0.97)
            space_x=round(space_x*0.97)-2
            roi = (x0,y0-space_y,w,h)
            data = img_to_string(recup_roi(image,roi))
            if len(data)==0:
                y0=y0*0.95
                roi = (x0,y0-space_y,w,h)
                data = img_to_string(recup_roi(image,roi))
                
                
                if len(data) == 0:
                    x0=440
                    y0=510
                    roi = (x0,y0-space_y,w,h)
                    data = img_to_string(recup_roi(image,roi))
        text.append(data)
        ## items 2 
        
        roi=(x0+space_x,y0-space_y,w,h)
        text.append(img_to_string(recup_roi(image,roi)))
       
        ## items 3 
        roi=(x0+space_x*2,y0-space_y,w,h)
        text.append(img_to_string(recup_roi(image,roi)))
        
        
        
    
        # ligne 1 référence
        ## items 1
        roi = (x0,y0,w,h)
        data = img_to_string(recup_roi(image,roi))
        if len(data)==0:
            y0=round(y0*0.97)
            roi = (x0,y0,w,h)
            data = img_to_string(recup_roi(image,roi))

            if len(data) ==0:
                y0=510
                roi = (x0,y0,w,h)
                data = img_to_string(recup_roi(image,roi))
    
        text.append(data)
        ## items 2 
        roi=(x0+space_x,y0,w,h)
        text.append(img_to_string(recup_roi(image,roi)))
        
        ## items 3 
        roi=(x0+space_x*2,y0,w,h)
        text.append(img_to_string(recup_roi(image,roi)))
        


        # ligne 2 
        ## items 1 
        roi=(x0,y0+space_y,w,h)
        data = img_to_string(recup_roi(image,roi))
        if len(data)==0:
            y0=round(y0*0.92)
            roi = (x0,y0+space_y,w,h)
            data = img_to_string(recup_roi(image,roi))

            if len(data) ==0:
                y0=510
                roi = (x0,y0+space_y,w,h)
                data = img_to_string(recup_roi(image,roi))
    
        text.append(data)
        
        ## items 2 
        roi=(x0+space_x,y0+space_y,w,h)
        text.append(img_to_string(recup_roi(image,roi)))
        
        ## items 3
        roi=(x0+space_x*2,y0+space_y,w,h)
        text.append(img_to_string(recup_roi(image,roi)))
        
                    
        # ligne 3 
        ## items 1
        roi=(x0,y0+space_y*2,w,h)
        text.append(img_to_string(recup_roi(image,roi)))
        
        ## items 2
        roi=(x0+space_x,y0+space_y*2,w,h)
        text.append(img_to_string(recup_roi(image,roi)))
        
        ## items 3
        roi=(x0+space_x*2,y0+space_y*2,w,h)
        text.append(img_to_string(recup_roi(image,roi)))
        return text
    except :
        pass



def troops(img_):
    try:
        text=list()

        x0=490
        y0=410
        space_x=222
        space_y=130
        roi=(x0,410,110,50) #T5 inf 
        text.append(img_to_string(recup_roi(img_,roi)))
        roi=(x0+222,410,110,50)#T5 cav
        text.append(img_to_string(recup_roi(img_,roi)))
        roi=(x0+222*2,410,110,50)#T5 arch
        text.append(img_to_string(recup_roi(img_,roi)))
        roi=(x0+222*3,410,110,50)#T5 sieges
        text.append(img_to_string(recup_roi(img_,roi)))
        
        roi=(x0,410+130,110,50) #T4 inf 
        text.append(img_to_string(recup_roi(img_,roi)))
        roi=(x0+222,410+130,110,50)#T4 cav
        text.append(img_to_string(recup_roi(img_,roi)))
        roi=(x0+222*2,410+130,110,50)#T4 arch
        text.append(img_to_string(recup_roi(img_,roi)))
        roi=(x0+222*3,410+130,110,50)#T4 sieges
        text.append(img_to_string(recup_roi(img_,roi)))

        return text
       # return Img.show()
    except Exception as e:
        print(e)