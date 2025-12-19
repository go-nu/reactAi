가상환경 접속
.\.venv\Scripts\activate

pip install -r requirements.txt

cuda 사용
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
