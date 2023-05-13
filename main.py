# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`
#firebase emulators:start --only functions
#firebase deploy --only functions

#from firebase_functions import firebase_function, https_fn
from firebase_admin import initialize_app
import face_recognition
import pickle
import cv2
import os
import csv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
from datetime import datetime
import uuid
from flask import Flask, render_template
import io
import pickle
import numpy as np
from PIL import Image, ImageOps

app1 = Flask(__name__)
key = {
    "type": "service_account",
    "project_id": "facecounter-7bdad",
    "private_key_id": "7c233c617d6066e5e2016f7f5fac1fa8e81c50c5",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCxJV3TcgtpIyz8\nrw+1u7+VObid8RRf90Ti0SbE9wI1/9okm365XHqka5anZDOKa0JilTBbnCcM+Say\nZk3BgTDGE2QR9rOR3+iFi/MI5j0PoRLgzUTZDMl2W7C6cGi8eoIzWHsnjFrdExSb\nSiQp0rV02z2rs4ro/IP6YQIYmp4hlrxxwlkTxRiSyZqLs3l8hHNwtcdFo75m2KGl\n7FFjm0YfmoBojQMKO5VP9eLovEqXDK0uRagd4PKjU53xNuHmIURHCsbtzNZHfMSC\n+CZ5nQuSFOoBfBX9+mlbcho6ikMprLDMODz5Ne88evRQDOSZEhQy9Re3bjnS7UjK\nnuh/Dz+RAgMBAAECggEABU1KgR0dNVDdtFRjAnvzkHpRSbzg8LxcXfOHlwaTlN0r\nAMR8pvybGRe1Qx5PIpnyOzQe5ecHDi7Y1ycTtbJxrMQAzz7Ugg2zDmgxZndJpZGb\nGIpcQKjO0NGOuQ3LPLTn97RyvyzGvW4oRDuUWIIbdztmnaB6jF2eb5x+rRDXocat\n03vd+omgQLnrFMxRkR2zPqSd0VTnbrnzNF9sP3fVXcilD4i9BpgI+4WiAw22JPLT\nJaME4M+WN9Lg132Up9m+KEptBxXwdpIqmvd5BhOCMm08JQoWvApoXVqdJGYShOu6\nd3Uh/byukoHsR3BCVY1FJ9gv42zuO5ZgJHo4GUQw7wKBgQDyYFiHUA0Fn6+zy/IX\n+YI7UgOoDQdtF5Cf1nH5h2jOPheA2HTdu/0uqlDNhi/e1dzGh0+ZroVEJa2pWDUH\nFfRCUt23oJnWOYHFc9zGMDtqTxCQLqsDjZcPg756bKkqAtDyFqSgoBRrftGHqCWM\n9V0sMCVP7QwCUuAV7POoBT5OiwKBgQC7GmS7+z0HOQiRfwjJ7h/dG6WZD6qCTNEe\ni9saNRDAoFHAC5XSQaQwzaHARD2QzJxo1+GxyxzmwNl8emmHGTXyWmvs2EOzDQzJ\nyudu9oB13/eNJPGZXzUICt2E6sKA+as1hDreeDxLZmo4E9UZq7g1EEZiwmF6c2Cy\nVJVyRKjp0wKBgBH0jzpe9MgA32xLZIDgLASm+7xcUruDLmSY51Kb9Giq8uTJpEa0\n4XmuhlPjZ/JzF2rhpUT2R8sXm3jbHvqKZtDvAJvU2vCiy/lLrwRDmHM0rj5wJp0Z\nxSISGW9KU3HYSZBVmxaHJVwdRfptu3JozuEyI+F65xPY/d7B8f71fHsnAoGAPswA\n+0a7mOz/fzXP0VZmw2NAFTs40zrNBR+Tjhw5Xy1vwrEgu8zkOq0JmOpOb4b9CANM\n8MtnC9u2Ix1CxeEkRg8rIfcD4diDbkb3njqFqwpcn7bCj+NwfR6IctAIMBmb6P5U\nc86PDg91nxSo9VC5JrYrqYHsDZkj3zacYhnBR5kCgYEAkoUsrYuetMoT/lC7yAa8\nNAxJme3XyhqKwyYwwz2d9t5af71vADOqSutQY1yk7dQczJXppo1szNB1RGk0neSv\n/JGaH+rH8PcO1RivZbOLKB3oU7EFmmI0ZCsaDoKCJ4hRkXaqB31rmLYbvNODwYw4\n+ob7HqkjGql/bUIbEtSb768=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-zdctb@facecounter-7bdad.iam.gserviceaccount.com",
    "client_id": "103057494865791731303",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-zdctb%40facecounter-7bdad.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
    }

    # Inicializar la app de Firebase
cred = credentials.Certificate(key)
firebase_admin.initialize_app(cred, {'storageBucket': 'facecounter-7bdad.appspot.com'})

@app1.route("/")
def face_counter_api():
    

    app = firebase_admin.get_app()
    print(app.name)

    # Get a reference to the Firestore database
    db = firestore.client()

    # Get a reference to the storage bucket
    bucket = storage.bucket()

    # Define el nombre de la carpeta en el Storage de Firebase que deseas descargar
    folder_name = 'Fotos Subidas/'

    # Obtener la lista de nombres de los archivos en la carpeta
    blobs = bucket.list_blobs(prefix=folder_name)

    TOLERANCE = 0.5
    FRAME_THICKNESS = 3
    FONT_THICKNESS = 2
    MODEL = "cnn"

    # Establecer el código del curso
    c_codigo_curso = "6OnWmcvdlM27usk2U68Q"

    def marcar_ausente_todos():
        alumnos_ref = db.collection('curso_alumno').where("c_codigo_curso", "==", c_codigo_curso)
        alumnos = alumnos_ref.get()
        for alumno in alumnos:
            alumno_ref = db.collection('curso_alumno').document(alumno.id)
            alumno_ref.update({'d_asistencia': 'Ausente'})
            alumno_ref.update({'d_modificacion': 'Automatico'})


    print("Cargando caras conocidas desde el archivo 'faces.dat'")
    # Descarga el archivo faces.dat como bytes desde Firebase Storage
    blob_dat = bucket.blob('faces.dat')
    faces_data = blob_dat.download_as_string()

    # Carga el contenido del archivo en memoria usando io.BytesIO
    in_memory_file = io.BytesIO(faces_data)

    # Usa pickle para cargar los datos del archivo en un diccionario
    data = pickle.load(in_memory_file)
    known_faces = data['known_faces']
    known_names = data['known_names']

    print("Procesando caras desconocidas")
    correct_recognitions = 0
    total_recognitions = 0

    marcar_ausente_todos()
    # Recorrer los blobs en la carpeta y cargar las imágenes en memoria
    for blob in blobs:
        # Obtener los datos binarios del blob
        img_data = blob.download_as_bytes()
        if img_data:
            # Convertir los datos binarios en un objeto Image de PIL
            image = Image.open(io.BytesIO(img_data))

            # Redimensionar la imagen proporcionalmente usando ImageOps.fit()
            image = ImageOps.fit(image, (int(image.size[0]*0.15), int(image.size[1]*0.15)))
            image = np.asarray(image)
            # Detectar las caras en la imagen
            locations = face_recognition.face_locations(image, model=MODEL)
            encoding = face_recognition.face_encodings(image, locations)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        else:
            continue
        # Dibujar los cuadros y los nombres en la imagen
        for face_encoding, face_location in zip(encoding, locations):
            results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)
            match = None
            if True in results:
                match = known_names[results.index(True)]
                print(f"Match Found: {match}")
                # Actualizar la base de datos
                correct_recognitions += 1

                top_left = (face_location[3], face_location[0])
                bottom_right = (face_location[1], face_location[2])
                color = [0, 255, 0]
                cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)

                top_left = (face_location[3], face_location[2])
                bottom_right = (face_location[1], face_location[2] + 22)
                cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)
                cv2.putText(image, match, (face_location[3] + 10, face_location[2] + 15), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,200), FONT_THICKNESS)
                
                
                # Actualizar la columna d_asistencia en la tabla asistencia
                            
                alumnos_ref = db.collection('curso_alumno').where("c_codigo_curso", "==", c_codigo_curso).stream()

                for alumno in alumnos_ref:
                    if alumno.get('d_nombre') == match:
                        alumno_ref = db.collection('curso_alumno').document(alumno.id)
                        alumno_ref.update({
                            'd_asistencia': 'Presente',
                            'd_fecha': datetime.now().strftime("%d de %B de %Y, %H:%M:%S UTC-5")
                        })
                                    
                    else:
                        alumno_ref = db.collection('curso_alumno').document(alumno.id)
                        alumno_ref.update({
                            'd_fecha': datetime.now().strftime("%d de %B de %Y, %H:%M:%S UTC-5")
                        })

            
            total_recognitions += 1

        # Sube la imagen a Firebase Storage
        blob = bucket.blob('Registro de fotografias/' + str(uuid.uuid4()) + '.jpg')
        _, buffer = cv2.imencode('.jpg', image)
        blob.upload_from_string(buffer.tobytes(), content_type='image/jpeg')

        print(f"Imagen subida exitosamente a Firebase Storage")

        cv2.imshow(blob.name, image)
        cv2.waitKey(5000)
        #cv2.destroyWindow(filename)


    accuracy = correct_recognitions / total_recognitions * 100
    print(f"Accuracy: {accuracy:.2f}%")

    # Obtener los registros de asistencia para el curso
    results = []
    alumnos_ref = db.collection('curso_alumno').where("c_codigo_curso", "==", c_codigo_curso).stream()
    for alumno in alumnos_ref:
        nombre = alumno.get('d_nombre')
        asistencia = alumno.get('d_asistencia')
        fecha = alumno.get('d_fecha')
        modificacion = alumno.get('d_modificacion')
        results.append((nombre, asistencia, fecha, modificacion))
        
    # Definir los nombres de los archivos y su ruta en Firebase Storage
    filename_txt = 'archivos de asistencia/asistencia.txt'
    filename_csv = 'archivos de asistencia/asistencia.csv'

    # Crear el contenido del archivo TXT
    content_txt = ''
    for row in results:
        content_txt += f"{row[0]}: {row[1]} | {row[2] } | {row[3]}\n"

    # Subir el archivo TXT a Firebase Storage
    blob_txt = bucket.blob(filename_txt)
    blob_txt.upload_from_string(content_txt)

    # Crear el contenido del archivo CSV
    content_csv = 'Nombre,Asistencia,Fecha,Modificacion\n'
    for row in results:
        content_csv += f"{row[0]},{row[1]},{row[2]},{row[3]}\n"

    # Subir el archivo CSV a Firebase Storage
    blob_csv = bucket.blob(filename_csv)
    blob_csv.upload_from_string(content_csv)

    print(f"Archivos de asistencia subidos exitosamente a Firebase Storage")
    return "Reconocimiento realizado"

if __name__ == "__main__":
    app1.run()
