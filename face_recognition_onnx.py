import cv2
import numpy as np
from pathlib import Path
import torch
import torch.nn.functional as F
from boxmot.appearance.reid_multibackend import ReIDDetectMultiBackend
import face_recognition

TARGET_SIZE = (112, 112)
THRESH = 0.35
DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
FACE_RECOG = ReIDDetectMultiBackend(weights=Path("backbone_90000_vggface2.onnx"), device=DEVICE, fp16=True)
global COSINE_DIST

def load_image_file(path):
    # Read the image using OpenCV
    image = cv2.imread(path)
    
    # Assertion
    assert image is not None, f'Cannot load {path}'
    
    # resize image to desired img shape        
    image = cv2.resize(image, TARGET_SIZE)
    
    # # convert BRG to RGB
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # no need, reid_multibackend will do
    
    return image

def face_locations(frame):
    face_locations = face_recognition.face_locations(frame)
    return face_locations

def face_encodings(query_image, face_locations):
    encodings = []
    for face_location in face_locations:
        # unpack face location following dlib format
        top, right, bottom, left = face_location
        
        # crop image
        crop = query_image[top:bottom,left:right,:]
        
        # get encoding
        xyxys = np.array([[0, 0, crop.shape[1], crop.shape[0]]])
        encoding = FACE_RECOG.get_features(xyxys, crop)
        
        # append
        encoding = torch.from_numpy(encoding)
        encodings.append(encoding)
    
    if len(encodings) > 0:    
        # convert from a list of N (1, E) arrays into (N, E), where e is encoding size
        encodings = torch.cat(encodings, dim=0)  
        
        # normalize
        encodings = F.normalize(encodings, dim=1) 
    
    return encodings 

def compare_faces(known_face_encodings, face_encoding):
    '''
    Given that:
        known_face_encodings is a M x 512 matrix
        face_encodings is a 1 x 512 matrix
    '''
    # reshape just in case is (512, )
    #face_encoding = face_encoding.reshape(1, 512)
    face_encoding = face_encoding[None,:]
    
    # normalize face_encoding    
    face_encoding = F.normalize(face_encoding, dim=1) 
    
    # convert known_face_encodings to tensor
    known_face_encodings = np.stack(known_face_encodings)
    known_face_encodings = torch.tensor(known_face_encodings)

    # cosine similarity
    cosine_sim = torch.mm(known_face_encodings, face_encoding.transpose(0, 1))
    match_ids        = torch.argmax(cosine_sim, dim=0).cpu().tolist()
    match_thresholds = torch.any(cosine_sim > THRESH, dim=0).cpu().tolist()
    
    matches          = cosine_sim > THRESH
    cosine_dist      = 1 - cosine_sim
    
    global COSINE_DIST
    COSINE_DIST     = cosine_dist
    
    return matches

def face_distance(known_face_encodings, face_encoding):
    global COSINE_DIST
    return COSINE_DIST
