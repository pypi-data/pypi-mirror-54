from keras.layers import Dense
from keras import Sequential
import numpy as np
import pytest

import optuna
from optuna.integration import KerasPruningCallback
from optuna.testing.integration import create_running_trial
from optuna.testing.integration import DeterministicPruner


def test_keras_pruning_callback():
    # type: () -> None

    def objective(trial):
        # type: (optuna.trial.Trial) -> float

        model = Sequential()
        model.add(Dense(1, activation='sigmoid', input_dim=20))
        model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])
        model.fit(
            np.zeros((16, 20), np.float32),
            np.zeros((16, ), np.int32),
            batch_size=1,
            epochs=1,
            callbacks=[KerasPruningCallback(trial, 'accuracy')],
            verbose=0)

        return 1.0

    study = optuna.create_study(pruner=DeterministicPruner(True))
    study.optimize(objective, n_trials=1)
    assert study.trials[0].state == optuna.structs.TrialState.PRUNED

    study = optuna.create_study(pruner=DeterministicPruner(False))
    study.optimize(objective, n_trials=1)
    assert study.trials[0].state == optuna.structs.TrialState.COMPLETE
    assert study.trials[0].value == 1.0


def test_keras_pruning_callback_observation_isnan():
    # type: () -> None

    study = optuna.create_study(pruner=DeterministicPruner(True))
    trial = create_running_trial(study, 1.0)
    callback = KerasPruningCallback(trial, 'loss')

    with pytest.raises(optuna.structs.TrialPruned):
        callback.on_epoch_end(0, {'loss': 1.0})

    with pytest.raises(optuna.structs.TrialPruned):
        callback.on_epoch_end(0, {'loss': float('nan')})
