# Sample videos

### Video_1.mp4
- Western faces.
- Slightly blurrish.
- Faces are moderate distance away from camera.

### Video_2.mp4
- Asian faces
- Faces are moderate distance away from camera.

### Video_3.mp4
- A close up interview video.
- Faces are close to the camera.


## Remarks
1. Since the training dataset comprised of mostly western faces, the matching accuracy for non-western may be slightly less accurate. This can be improved by adding more copies of the same person faces with slightly different angle.
2. Face detection works well when face is closer to the camera, because we are not using SOTA face detection model. We purposely do not upgrade the face detection model, because we want to make sure that the face can only be detected in good conditions (lighting, angle, etc) to improve face recognition accuracy.
