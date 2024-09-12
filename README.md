# SimpleFR
This is a very simple face recognition code based on [face recognition api](https://github.com/ageitgey/face_recognition). The face recognition is built using [dlib's](https://github.com/davisking/dlib) state-of-the-art face recognition built with deep learning. The model has an accuracy of 99.38% on the Labeled Faces in the Wild benchmark. The Graphic User Interface (GUI) is based on tkinter for simplicty's sake.

Face detector
- HOG + Linear SVM (prefered for fast inference speed on resource constrained device)
- CNNs

Face recognition model
- based on ResNet-34 from [this work](https://arxiv.org/abs/1512.03385)

Face database
- All faces should be stored in ```SimpleFR/database```

## Files organization
```
SimpleFR
├── database
│   ├── <4 digit>_<name 1>.jpg/png
│   ├── <4 digit>_<name 2>.jpg/png
├── dlib
├── ask.py
```

## Setup
Create conda environment
```bash
conda create --name ws python=3.8 -y
conda activate ws
```

## Clone the repo
```bash
git clone https://github.com/yjwong1999/SimpleFR.git
cd SimpleFR
```

## Install dependencies

Install Pytorch (always refer [the official installation code](https://pytorch.org/get-started/locally/))
```bash
# for GPU
pip install torch==2.0.0 torchvision==0.15.1 torchaudio==2.0.1 --index-url https://download.pytorch.org/whl/cu118

# for CPU only
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cpu
```

If you prefer to use YOLO (just install regardless)
```
pip install ultralytics==8.1.24
```


Install dlib on macos and Ubuntu (for windows refer [this guide](https://github.com/sachadee/Dlib) or [that guide](https://github.com/z-mahmud22/Dlib_Windows_Python3.x))
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

## Find port number connected to camera
```bash
python3 find_port.py
```

## Run one camera/source
```bash
# without YOLO
python3 run.py --source <video/stream source>

# with YOLO
python3 run.py --use-yolo --source <video/stream source>
```

## Run multiple camera(s)/source(s)
```bash
# configure source.streams
<list down all video/streaming source in source.streams>

# without YOLO
python3 multi_run.py 

# with YOLO
python3 multi_run.py --use-yolo
```

## Experiment
If you want to use onnxruntime-based face recognition instead of C++ (dlib), you can try the following:
```bash
pip install scikit-learn
pip install loguru
pip install gdown
pip install ftfy
pip install regex
pip install filterpy

pip install onnxruntime
# pip install onnxruntime-gpu==1.17.0 --index-url=https://pkgs.dev.azure.com/onnxruntime/onnxruntime/_packaging/onnxruntime-cuda-12/pypi/simple
pip install onnxruntime-gpu --extra-index-url https://aiinfra.pkgs.visualstudio.com/PublicPackages/_packaging/onnxruntime-cuda-12/pypi/simple/
```

After installation, replace the following codes in `run.py` and `run_grid.py`
```python
# import face_recognition
import face_recognition_onnx as import face_recognition
```

## Known errors and solutions related to face_recognition and opencv api
1. How to install dlib on different OS: [(Refer this link)](https://gist.github.com/ageitgey/629d75c1baac34dfa5ca2a1928a7aeaf)
2. How to solve imshow function not implemented error: [(Refer this link)](https://github.com/opencv/opencv-python/issues/17#issuecomment-877649472)
3. How to solve "Invoked with: <_dlib_pybind11.face_recognition_model_v1 object at 0x1046d73f0>, array([[[ 8, 4, 1], error" error: [(Refer this link)](https://github.com/ageitgey/face_recognition/issues/1516#issuecomment-1615931065)
4. You might face difficulties installing lap. Please use python 3.8 version to avoid this issue. I directly commented `import lap` in `boxmot/utils/matching.py` to prevent using lap entirely, since the main function of this repo do not uses lap dependencies.

## Acknowledgement
1. [Face recognition api](https://github.com/ageitgey/face_recognition)
2. [dlib](https://github.com/davisking/dlib)
