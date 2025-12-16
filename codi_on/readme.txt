가상환경 접속
.\.venv\Scripts\activate

pip install -r requirements.txt.

pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

generate_dataset -> csv 생성
split_dataset -> train/validation/test 분리

train.py = train + validation
evaluate.py = test