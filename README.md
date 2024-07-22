# SimpleFR

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
