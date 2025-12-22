가상환경 접속
설정 -> 인터프리터 로컬 가상환경(.venv) 생성
.\.venv\Scripts\activate

pip install -r requirements.txt

cuda 설치
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

실행 순서
ml/pipeline/generate_dataset.py
ml/pipeline/split_dataset.py
m1/pipeline/train.py

서버 실행
python -m uvicorn api.main:app --reload