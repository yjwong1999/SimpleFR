# SimpleFR
This is a very simple face recognition code based on [face recognition api](https://github.com/ageitgey/face_recognition).

## Setup
Create conda environment
```bash
conda create --name ws python=3.11 -y
conda activate ws
```

Install dlib on macos and Ubuntu
```bash
git clone https://github.com/davisking/dlib.git
cd dlib
sudo apt  install cmake
mkdir build; cd build; cmake ..; cmake --build .
cd ..
python3 setup.py install
cd ../
```

Install the face recognition api
```bash
pip install face-recognition==1.3.0
pip install opencv-python==4.10.0.84
```

## Known errors and solutions related to face_recognition and opencv api
1. How to install dlib on different OS: [(Refer this link)](https://gist.github.com/ageitgey/629d75c1baac34dfa5ca2a1928a7aeaf)
2. How to solve imshow function not implemented error: [(Refer this link)](https://github.com/opencv/opencv-python/issues/17#issuecomment-877649472)
3. How to solve "Invoked with: <_dlib_pybind11.face_recognition_model_v1 object at 0x1046d73f0>, array([[[ 8, 4, 1], error" error: [(Refer this link)](https://github.com/ageitgey/face_recognition/issues/1516#issuecomment-1615931065)

## Acknowledgement
1. [Face recognition api](https://github.com/ageitgey/face_recognition)
