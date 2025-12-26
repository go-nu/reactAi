TRAIN_CONFIG = {
    "input_dim": 11,
    "hidden_dims": [32, 16],
    "activation": "tanh",
    "dropout": 0.1,

    "batch_size": 32,
    "epochs": 100,

    "optimizer": "adam",
    "learning_rate": 1e-3,

    "loss": "mse",

    # early stopping
    "early_stopping": True,
    "es_patience": 20, # epoch 기준
    "es_min_delta": 1e-4, # 최소 변화량
    "es_monitor": "loss", # loss | acc
}
