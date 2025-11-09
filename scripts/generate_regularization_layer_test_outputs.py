import argparse
import os
import numpy as np
import sys
from pathlib import Path

# 修改这个路径为你的 mlpractical 根目录
BASE = Path(r"D:\mlpractical").resolve()

os.environ["MLP_DATA_DIR"] = str(BASE / "data")

# 确保 mlp package 可以被 import
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from mlp.layers import DropoutLayer
from mlp.penalties import L1Penalty, L2Penalty
parser = argparse.ArgumentParser(description='Welcome to regularization test script')

parser.add_argument('--student_id', nargs="?", type=str, help='Your student id in the format "Sxxxxxxx"')

args = parser.parse_args()

student_id = args.student_id

def fprop_bprop_layer(inputs, dropout_layer, grads_wrt_outputs, weights, params=False):
    if params:
        dropout_layer.params = [weights]

    fprop = dropout_layer.fprop(inputs)
    bprop = dropout_layer.bprop(inputs, fprop, grads_wrt_outputs)

    outputs = [fprop, bprop]
    if params:
        grads_wrt_weights = dropout_layer.grads_wrt_params(
            inputs, grads_wrt_outputs)
        outputs.append(grads_wrt_weights)

    return outputs


def call_grad_layer(inputs, penalty_layer, grads_wrt_outputs, weights, params=False):
    if params:
        penalty_layer.params = [weights]

    call = penalty_layer(inputs)
    grad = penalty_layer.grad(inputs)

    outputs = [call, grad]
    if params:
        grads_wrt_weights = penalty_layer.grads_wrt_params(
            inputs, grads_wrt_outputs)
        outputs.append(grads_wrt_weights)

    return outputs

def get_student_seed(student_id):
    student_seed_number = int(student_id[1:])
    return student_seed_number


seed = get_student_seed(student_id)
rng = np.random.RandomState(seed)

reg_output_dict = dict()

inputs = rng.normal(loc=0.0, scale=1.0, size=(32, 3, 8, 8))
grads_wrt_outputs = rng.normal(loc=0.0, scale=1.0, size=(32, 3, 8, 8))
weights = rng.normal(loc=0.0, scale=1.0, size=(1))

reg_output_dict['inputs'] = inputs
reg_output_dict['weights'] = weights
reg_output_dict['grads_wrt_outputs'] = grads_wrt_outputs

for dropout_layer, params_flag in zip(
        [DropoutLayer],
        [False]):
    if isinstance(dropout_layer(), DropoutLayer):
        rng = np.random.RandomState(92019)
        print(True)
        outputs = fprop_bprop_layer(inputs, dropout_layer(
            rng=rng), grads_wrt_outputs, weights, params_flag)
    else:
        outputs = fprop_bprop_layer(
            inputs, dropout_layer(), grads_wrt_outputs, weights, params_flag)
    reg_output_dict['{}_{}'.format(
        dropout_layer.__name__, 'fprop')] = outputs[0]
    reg_output_dict['{}_{}'.format(
        dropout_layer.__name__, 'bprop')] = outputs[1]
    if params_flag:
        reg_output_dict['{}_{}'.format(
            dropout_layer.__name__, 'grads_wrt_outputs')] = outputs[2]

for penalty_layer, params_flag in zip(
        [L1Penalty, L2Penalty], [False, False]):
    outputs = call_grad_layer(inputs, penalty_layer(
        1e-4), grads_wrt_outputs, weights, params_flag)
    reg_output_dict['{}_{}'.format(
        penalty_layer.__name__, '__call__correct')] = outputs[0]
    reg_output_dict['{}_{}'.format(
        penalty_layer.__name__, 'grad_correct')] = outputs[1]
    if params_flag:
        reg_output_dict['{}_{}'.format(
            penalty_layer.__name__, 'grads_wrt_outputs')] = outputs[2]

np.save(os.path.join(os.environ['MLP_DATA_DIR'],
        '{}_regularization_test_pack.npy'.format(seed)), reg_output_dict)

test_data = np.load(os.path.join(
    os.environ['MLP_DATA_DIR'], '{}_regularization_test_pack.npy'.format(seed)), allow_pickle=True)

for key, value in test_data.item().items():
    print(key, value)
