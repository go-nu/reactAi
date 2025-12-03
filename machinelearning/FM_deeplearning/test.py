import torch


def test_cuda_test():
    # 1. GPU 사용 가능 여부 확인
    print("CUDA Available:", torch.cuda.is_available())

    # 2. 사용 중인 GPU 이름 확인
    if torch.cuda.is_available():
        print("GPU Name:", torch.cuda.get_device_name(0))
    elif torch.backends.mps.is_available():
        print("MPS GPU Name:", torch.cuda.get_device_name(0))
    else:
        print("GPU를 사용할 수 없습니다.")

    # 3. 간단한 텐서 연산을 GPU에서 실행해보기
    try:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        x = torch.rand(3, 3).to(device)
        y = torch.rand(3, 3).to(device)
        z = x + y
        print("Tensor device:", z.device)
        print("GPU 연산 성공!")
    except Exception as e:
        print("GPU 연산 실패:", e)


def model_test():
    from train.FM_recommend import MatrixFactorization

    checkpoint = torch.load("./model/fm_model.pt", map_location="cpu")

    n_users = checkpoint["n_users"]
    n_items = checkpoint["n_items"]
    embedding_dim = checkpoint["embedding_dim"]

    user_idx = checkpoint["user_idx"]
    item_idx = checkpoint["item_idx"]

    model = MatrixFactorization(n_users, n_items, embedding_dim)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    print("=== 모델 로드 완료 ===")
    print("총 사용자 수:", n_users)
    print("총 아이템(영화) 수:", n_items)
    print("임베딩 차원:", embedding_dim)
    print()

    # -----------------------------------------
    # 🔥 실제 사용자 테스트
    # -----------------------------------------
    real_user_id = 69716   # user_id
    print(user_idx)
    # exit()

    if real_user_id not in user_idx:
        print(f"❌ 유저 {real_user_id} 는 학습 데이터에 없습니다.")
        return

    u = user_idx[real_user_id]

    u_tensor = torch.LongTensor([u])

    # 예: 첫 번째 영화(인덱스 0)에 대한 예측 출력
    item_example_idx = 1000 # item_idx
    i_tensor = torch.LongTensor([item_example_idx])

    pred = model(u_tensor, i_tensor).item()

    print("=== 실제 사용자 테스트 ===")
    print(f"실제 user_id: {real_user_id}")
    print(f"모델에서의 user_idx: {u}")
    print(f"테스트 예시 영화 item_idx = {item_example_idx}")
    print(f"예측 평점 = {pred:.4f}")

    return model, user_idx, item_idx



if __name__ == "__main__":
    model_test()
