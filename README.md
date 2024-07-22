# SimpleFR

conda create --name ws python=3.11 -y
conda activate ws

# install dlib on macos and Ubuntu
# https://gist.github.com/ageitgey/629d75c1baac34dfa5ca2a1928a7aeaf
```bash
git clone https://github.com/davisking/dlib.git
cd dlib
sudo apt  install cmake
mkdir build; cd build; cmake ..; cmake --build .
cd ..
python3 setup.py install
cd ../
```

# install the face recognition api
```
pip install face-recognition==1.3.0
pip install opencv-python==4.10.0.84
```
