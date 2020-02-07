from rasa.core.featurizers import (
    TrackerFeaturizer,
    # BinarySingleStateFeaturizer,
    # LabelTokenizerSingleStateFeaturizer,
    BOWSingleStateFeaturizer,
)
from rasa.core.domain import Domain
import numpy as np
import scipy


def test_fail_to_load_non_existent_featurizer():
    assert TrackerFeaturizer.load("non_existent_class") is None


def test_binary_featurizer_handles_on_non_existing_features():
    f = BinarySingleStateFeaturizer()
    f.input_state_map = {"a": 0, "b": 3, "c": 2, "d": 1}
    f.num_features = len(f.input_state_map)
    encoded = f.encode({"a": 1.0, "b": 1.0, "c": 0.0, "e": 1.0})
    assert (encoded == np.array([1, 0, 0, 1])).all()


def test_binary_featurizer_uses_correct_dtype_int():
    f = BinarySingleStateFeaturizer()
    f.input_state_map = {"a": 0, "b": 3, "c": 2, "d": 1}
    f.num_features = len(f.input_state_map)
    encoded = f.encode({"a": 1.0, "b": 1.0, "c": 0.0})
    assert encoded.dtype == np.int32


def test_binary_featurizer_uses_correct_dtype_float():
    f = BinarySingleStateFeaturizer()
    f.input_state_map = {"a": 0, "b": 3, "c": 2, "d": 1}
    f.num_features = len(f.input_state_map)
    encoded = f.encode({"a": 1.0, "b": 0.2, "c": 0.0})
    assert encoded.dtype == np.float64


def test_binary_featurizer_handles_on_non_existing_probabilistic_features():
    f = BinarySingleStateFeaturizer()
    f.input_state_map = {"a": 0, "b": 3, "c": 2, "d": 1}
    f.num_features = len(f.input_state_map)
    encoded = f.encode({"a": 1.0, "b": 0.2, "c": 0.0, "e": 1.0})
    assert (encoded == np.array([1, 0, 0, 0.2])).all()


def test_binary_featurizer_handles_probabilistic_intents():
    f = BinarySingleStateFeaturizer()
    f.input_state_map = {"intent_a": 0, "b": 3, "intent_c": 2, "d": 1}
    f.num_features = len(f.input_state_map)
    encoded = f.encode({"intent_a": 0.5, "b": 0.2, "intent_c": 1.0})
    assert (encoded == np.array([0.5, 0, 1.0, 0.2])).all()


def test_label_tokenizer_featurizer_handles_on_non_existing_features():
    f = LabelTokenizerSingleStateFeaturizer()
    f.user_labels = ["a_d"]
    f.bot_labels = ["c_b"]
    f.user_vocab = {"a": 0, "d": 1}
    f.bot_vocab = {"b": 1, "c": 0}
    f.num_features = len(f.user_vocab) + len(f.slot_labels) + len(f.bot_vocab)
    encoded = f.encode(
        {"a_d": 1.0, "prev_c_b": 0.0, "e": 1.0, "prev_action_listen": 1.0}
    )
    assert (encoded == np.array([1, 1, 0, 0])).all()


def test_label_tokenizer_featurizer_uses_correct_dtype_int():
    f = LabelTokenizerSingleStateFeaturizer()
    f.user_labels = ["a_d"]
    f.bot_labels = ["c_b"]
    f.user_vocab = {"a": 0, "d": 1}
    f.bot_vocab = {"b": 1, "c": 0}
    f.num_features = len(f.user_vocab) + len(f.slot_labels) + len(f.bot_vocab)
    encoded = f.encode({"a_d": 1.0, "prev_c_b": 0.0, "prev_action_listen": 1.0})
    assert encoded.dtype == np.int32


def test_label_tokenizer_featurizer_uses_correct_dtype_float():
    f = LabelTokenizerSingleStateFeaturizer()
    f.user_labels = ["a_d"]
    f.bot_labels = ["c_b"]
    f.user_vocab = {"a": 0, "d": 1}
    f.bot_vocab = {"b": 1, "c": 0}
    f.num_features = len(f.user_vocab) + len(f.slot_labels) + len(f.bot_vocab)
    encoded = f.encode({"a_d": 0.2, "prev_c_b": 0.0, "prev_action_listen": 1.0})
    assert encoded.dtype == np.float64


def test_label_tokenizer_featurizer_handles_on_non_existing_probabilistic():
    f = LabelTokenizerSingleStateFeaturizer()
    f.user_labels = ["a_d"]
    f.bot_labels = ["c_b"]
    f.user_vocab = {"a": 0, "d": 1}
    f.bot_vocab = {"b": 1, "c": 0}
    f.num_features = len(f.user_vocab) + len(f.slot_labels) + len(f.bot_vocab)
    encoded = f.encode(
        {"a_d": 0.2, "prev_c_b": 1.0, "c": 0.0, "e": 1.0, "prev_action_listen": 1.0}
    )
    assert (encoded == np.array([0.2, 0.2, 1.0, 1.0])).all()


def test_label_tokenizer_featurizer_handles_probabilistic_intents():
    f = LabelTokenizerSingleStateFeaturizer()
    f.user_labels = ["intent_a", "intent_d"]
    f.bot_labels = ["c", "b"]
    f.user_vocab = {"intent": 2, "a": 0, "d": 1}
    f.bot_vocab = {"b": 1, "c": 0}
    f.num_features = len(f.user_vocab) + len(f.slot_labels) + len(f.bot_vocab)
    encoded = f.encode(
        {"intent_a": 0.5, "prev_b": 0.2, "intent_d": 1.0, "prev_action_listen": 1.0}
    )
    assert (encoded == np.array([0.5, 1.0, 1.5, 0.0, 0.2])).all()

def test_bow_tokenizer_featurizer_handles_on_non_existing_features():
    f = BOWSingleStateFeaturizer()
    d = Domain
    d.input_states = ['ab_cd', 'ef_gh_kl']
    f.prepare_from_domain(d)
    encoded = f.encode({"ab_cd": 1.0, "prev_cd_ab": 0.0, "kl": 1.0, "prev_action_listen": 1.0}
        )
    assert (encoded == np.array([2, 2, 0, 0, 1])).all()

def test_bow_tokenizer_featurizer_uses_correct_dtype_int():
    f = BOWSingleStateFeaturizer()
    d = Domain
    d.input_states = ['ab_cd', 'ef_gh_kl']
    f.prepare_from_domain(d)
    encoded = f.encode({"ab_cd": 1.0, "prev_cd_ab": 0.0, "kl": 1.0, "prev_action_listen": 1.0})
    assert encoded.dtype == np.int32

def test_bow_tokenizer_featurizer_outputs_numpy_as_required():
    f = BOWSingleStateFeaturizer()
    d = Domain
    d.input_states = ['ab_cd', 'ef_gh_kl']
    f.prepare_from_domain(d)
    encoded = f.encode({"ab_cd": 1.0, "prev_cd_ab": 0.0, "kl": 1.0, "prev_action_listen": 1.0})
    assert type(encoded) == np.ndarray

def test_bow_tokenizer_featurizer_outputs_sparse_matrix_as_required():
    f = BOWSingleStateFeaturizer()
    d = Domain
    d.input_states = ['ab_cd', 'ef_gh_kl']
    f.prepare_from_domain(d)
    encoded = f.encode({"ab_cd": 1.0, "prev_cd_ab": 0.0, "kl": 1.0, "prev_action_listen": 1.0}, type_output="sparse")
    assert type(encoded) == scipy.sparse.csr.csr_matrix

def test_bow_tokenizer_featurizer_none_input_sparse():
    f = BOWSingleStateFeaturizer()
    d = Domain
    d.input_states = ['ab_cd', 'ef_gh_kl']
    f.prepare_from_domain(d)
    encoded = f.encode(None, type_output="sparse")
    assert type(encoded) == scipy.sparse.csr.csr_matrix

def test_bow_tokenizer_featurizer_none_input_dense():
    f = BOWSingleStateFeaturizer()
    d = Domain
    d.input_states = ['ab_cd', 'ef_gh_kl']
    f.prepare_from_domain(d)
    encoded = f.encode(None, type_output="dense")
    assert type(encoded) == np.ndarray and encoded.dtype == np.int32

def main():
    test_bow_tokenizer_featurizer_handles_on_non_existing_features()
    test_bow_tokenizer_featurizer_uses_correct_dtype_int()
    test_bow_tokenizer_featurizer_outputs_numpy_as_required()
    test_bow_tokenizer_featurizer_outputs_sparse_matrix_as_required()
    test_bow_tokenizer_featurizer_none_input_sparse()
    test_bow_tokenizer_featurizer_none_input_dense()


main()




