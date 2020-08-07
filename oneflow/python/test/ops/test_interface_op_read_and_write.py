"""
Copyright 2020 The OneFlow Authors. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import oneflow as flow
import numpy as np


def test(test_case):
    flow.config.gpu_device_num(2)
    @flow.global_function()
    def add():
        with flow.scope.placement("gpu", "0:0-1"):
            x = flow.get_variable(
                name="x", shape=(2, 3), initializer=flow.random_uniform_initializer(),
            )
            y = flow.get_variable(
                name="y", shape=(2, 3), initializer=flow.random_uniform_initializer(),
            )
            return flow.math.add_n([x, y])

    check_point = flow.train.CheckPoint()
    check_point.init()
    x_value = np.random.random((2, 3)).astype(np.float32)
    y_value = np.random.random((2, 3)).astype(np.float32)
    flow.experimental.set_interface_blob_value("x", x_value)
    flow.experimental.set_interface_blob_value("y", y_value)
    test_case.assertTrue(
        np.array_equal(x_value, flow.experimental.get_interface_blob_value("x"))
    )
    test_case.assertTrue(
        np.array_equal(y_value, flow.experimental.get_interface_blob_value("y"))
    )
    test_case.assertTrue(np.array_equal(add().get().numpy(), x_value + y_value))
