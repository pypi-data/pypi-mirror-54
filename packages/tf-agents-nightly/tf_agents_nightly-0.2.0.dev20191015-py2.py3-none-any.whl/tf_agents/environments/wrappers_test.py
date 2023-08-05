# coding=utf-8
# Copyright 2018 The TF-Agents Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Test for tf_agents.environments.wrappers."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import cProfile
import math
import pstats

from absl.testing import parameterized
from absl.testing.absltest import mock

import gym
import gym.spaces
import numpy as np

from tf_agents.environments import gym_wrapper
from tf_agents.environments import py_environment
from tf_agents.environments import random_py_environment
from tf_agents.environments import wrappers
from tf_agents.specs import array_spec
from tf_agents.trajectories import time_step as ts
from tf_agents.utils import test_utils


class PyEnvironmentBaseWrapperTest(parameterized.TestCase):

  @parameterized.named_parameters(
      {
          'testcase_name': 'scalar',
          'batch_size': None
      },
      {
          'testcase_name': 'batched',
          'batch_size': 2
      },
  )
  def test_batch_properties(self, batch_size):
    obs_spec = array_spec.BoundedArraySpec((2, 3), np.int32, -10, 10)
    action_spec = array_spec.BoundedArraySpec((1,), np.int32, -10, 10)
    env = random_py_environment.RandomPyEnvironment(
        obs_spec,
        action_spec,
        reward_fn=lambda *_: np.array([1.0]),
        batch_size=batch_size)
    wrap_env = wrappers.PyEnvironmentBaseWrapper(env)
    self.assertEqual(wrap_env.batched, env.batched)
    self.assertEqual(wrap_env.batch_size, env.batch_size)

  def test_default_batch_properties(self):
    cartpole_env = gym.spec('CartPole-v1').make()
    env = gym_wrapper.GymWrapper(cartpole_env)
    self.assertFalse(env.batched)
    self.assertEqual(env.batch_size, None)
    wrap_env = wrappers.PyEnvironmentBaseWrapper(env)
    self.assertEqual(wrap_env.batched, env.batched)
    self.assertEqual(wrap_env.batch_size, env.batch_size)

  def test_wrapped_method_propagation(self):
    mock_env = mock.MagicMock()
    env = wrappers.PyEnvironmentBaseWrapper(mock_env)
    env.reset()
    self.assertEqual(1, mock_env.reset.call_count)
    env.step(0)
    self.assertEqual(1, mock_env.step.call_count)
    mock_env.step.assert_called_with(0)
    env.seed(0)
    self.assertEqual(1, mock_env.seed.call_count)
    mock_env.seed.assert_called_with(0)
    env.render()
    self.assertEqual(1, mock_env.render.call_count)
    env.close()
    self.assertEqual(1, mock_env.close.call_count)


class TimeLimitWrapperTest(test_utils.TestCase):

  def test_limit_duration_wrapped_env_forwards_calls(self):
    cartpole_env = gym.spec('CartPole-v1').make()
    env = gym_wrapper.GymWrapper(cartpole_env)
    env = wrappers.TimeLimit(env, 10)

    action_spec = env.action_spec()
    self.assertEqual((), action_spec.shape)
    self.assertEqual(0, action_spec.minimum)
    self.assertEqual(1, action_spec.maximum)

    observation_spec = env.observation_spec()
    self.assertEqual((4,), observation_spec.shape)
    high = np.array([
        4.8,
        np.finfo(np.float32).max, 2 / 15.0 * math.pi,
        np.finfo(np.float32).max
    ])
    np.testing.assert_array_almost_equal(-high, observation_spec.minimum)
    np.testing.assert_array_almost_equal(high, observation_spec.maximum)

  def test_limit_duration_stops_after_duration(self):
    cartpole_env = gym.make('CartPole-v1')
    env = gym_wrapper.GymWrapper(cartpole_env)
    env = wrappers.TimeLimit(env, 2)

    env.reset()
    env.step(0)
    time_step = env.step(0)

    self.assertTrue(time_step.is_last())
    self.assertNotEqual(None, time_step.discount)
    self.assertNotEqual(0.0, time_step.discount)

  def test_extra_env_methods_work(self):
    cartpole_env = gym.make('CartPole-v1')
    env = gym_wrapper.GymWrapper(cartpole_env)
    env = wrappers.TimeLimit(env, 2)

    self.assertEqual(None, env.get_info())
    env.reset()
    env.step(0)
    self.assertEqual({}, env.get_info())

  def test_automatic_reset(self):
    cartpole_env = gym.make('CartPole-v1')
    env = gym_wrapper.GymWrapper(cartpole_env)
    env = wrappers.TimeLimit(env, 2)

    # Episode 1
    first_time_step = env.step(0)
    self.assertTrue(first_time_step.is_first())
    mid_time_step = env.step(0)
    self.assertTrue(mid_time_step.is_mid())
    last_time_step = env.step(0)
    self.assertTrue(last_time_step.is_last())

    # Episode 2
    first_time_step = env.step(0)
    self.assertTrue(first_time_step.is_first())
    mid_time_step = env.step(0)
    self.assertTrue(mid_time_step.is_mid())
    last_time_step = env.step(0)
    self.assertTrue(last_time_step.is_last())

  def test_duration_applied_after_episode_terminates_early(self):
    cartpole_env = gym.make('CartPole-v1')
    env = gym_wrapper.GymWrapper(cartpole_env)
    env = wrappers.TimeLimit(env, 10000)

    # Episode 1 stepped until termination occurs.
    time_step = env.step(1)
    while not time_step.is_last():
      time_step = env.step(1)

    self.assertTrue(time_step.is_last())
    env._duration = 2

    # Episode 2 short duration hits step limit.
    first_time_step = env.step(0)
    self.assertTrue(first_time_step.is_first())
    mid_time_step = env.step(0)
    self.assertTrue(mid_time_step.is_mid())
    last_time_step = env.step(0)
    self.assertTrue(last_time_step.is_last())


class ActionRepeatWrapperTest(test_utils.TestCase):

  def _get_mock_env_episode(self):
    mock_env = mock.MagicMock()
    mock_env.step.side_effect = [
        # In practice, the first reward would be 0, but test with a reward of 1.
        ts.TimeStep(ts.StepType.FIRST, 1, 1, [0]),
        ts.TimeStep(ts.StepType.MID, 2, 1, [1]),
        ts.TimeStep(ts.StepType.MID, 3, 1, [2]),
        ts.TimeStep(ts.StepType.MID, 5, 1, [3]),
        ts.TimeStep(ts.StepType.LAST, 7, 1, [4]),
    ]
    return mock_env

  def test_action_stops_on_first(self):
    mock_env = self._get_mock_env_episode()
    env = wrappers.ActionRepeat(mock_env, 3)
    env.reset()

    time_step = env.step([2])
    mock_env.step.assert_has_calls([mock.call([2])])

    self.assertEqual(1, time_step.reward)
    self.assertEqual([0], time_step.observation)

  def test_action_repeated(self):
    mock_env = self._get_mock_env_episode()
    env = wrappers.ActionRepeat(mock_env, 3)
    env.reset()

    env.step([2])
    env.step([3])
    mock_env.step.assert_has_calls([mock.call([2])] +
                                   [mock.call([3])] * 3)

  def test_action_stops_on_last(self):
    mock_env = self._get_mock_env_episode()
    env = wrappers.ActionRepeat(mock_env, 3)
    env.reset()

    env.step([2])
    env.step([3])
    time_step = env.step([4])
    mock_env.step.assert_has_calls([mock.call([2])] +
                                   [mock.call([3])] * 3 +
                                   [mock.call([4])])

    self.assertEqual(7, time_step.reward)
    self.assertEqual([4], time_step.observation)

  def test_checks_times_param(self):
    mock_env = mock.MagicMock()
    with self.assertRaises(ValueError):
      wrappers.ActionRepeat(mock_env, 1)

  def test_accumulates_reward(self):
    mock_env = self._get_mock_env_episode()
    env = wrappers.ActionRepeat(mock_env, 3)
    env.reset()

    env.step(0)
    time_step = env.step(0)

    mock_env.step.assert_called_with(0)
    self.assertEqual(10, time_step.reward)
    self.assertEqual([3], time_step.observation)


class RunStatsWrapperTest(test_utils.TestCase):

  def test_episode_count(self):
    cartpole_env = gym.make('CartPole-v1')
    env = gym_wrapper.GymWrapper(cartpole_env)
    env = wrappers.RunStats(env)

    self.assertEqual(0, env.episodes)
    time_step = env.reset()
    self.assertEqual(0, env.episodes)

    for episode_num in range(1, 4):
      while not time_step.is_last():
        time_step = env.step(1)
      self.assertEqual(episode_num, env.episodes)
      time_step = env.step(1)

  def test_episode_count_with_time_limit(self):
    cartpole_env = gym.make('CartPole-v1')
    env = gym_wrapper.GymWrapper(cartpole_env)
    env = wrappers.TimeLimit(env, 2)
    env = wrappers.RunStats(env)

    env.reset()
    self.assertEqual(0, env.episodes)

    env.step(0)
    time_step = env.step(0)

    self.assertTrue(time_step.is_last())
    self.assertEqual(1, env.episodes)

  def test_step_count(self):
    cartpole_env = gym.make('CartPole-v1')
    env = gym_wrapper.GymWrapper(cartpole_env)
    env = wrappers.RunStats(env)

    self.assertEqual(0, env.episodes)
    time_step = env.reset()
    self.assertEqual(0, env.episodes)

    steps = 0
    for _ in range(0, 4):
      while not time_step.is_last():
        self.assertEqual(steps, env.total_steps)
        time_step = env.step(1)
        steps += 1
      time_step = env.step(1)

  def test_resets_count(self):
    cartpole_env = gym.make('CartPole-v1')
    env = gym_wrapper.GymWrapper(cartpole_env)
    env = wrappers.RunStats(env)

    self.assertEqual(0, env.resets)
    time_step = env.reset()
    self.assertEqual(1, env.resets)

    resets = 1
    for _ in range(0, 4):
      while not time_step.is_last():
        self.assertEqual(resets, env.resets)
        time_step = env.step(1)
      time_step = env.step(1)
      resets += 1


class ActionDiscretizeWrapper(test_utils.TestCase):

  def test_discrete_spec_scalar_limit(self):
    obs_spec = array_spec.BoundedArraySpec((2, 3), np.int32, -10, 10)
    action_spec = array_spec.BoundedArraySpec((), np.float32, -10, 10)
    limits = 3

    env = random_py_environment.RandomPyEnvironment(
        obs_spec, action_spec=action_spec)
    env = wrappers.ActionDiscretizeWrapper(env, limits)

    expected_spec = array_spec.BoundedArraySpec((), np.int32, 0,
                                                np.asarray(limits) - 1)
    self.assertEqual(expected_spec, env.action_spec())

  def test_discrete_spec_1d(self):
    obs_spec = array_spec.BoundedArraySpec((2, 3), np.int32, -10, 10)
    action_spec = array_spec.BoundedArraySpec((2,), np.float32, -10, 10)
    limits = [5, 3]

    env = random_py_environment.RandomPyEnvironment(
        obs_spec, action_spec=action_spec)
    env = wrappers.ActionDiscretizeWrapper(env, limits)

    expected_spec = array_spec.BoundedArraySpec((2,), np.int32, 0,
                                                np.asarray(limits) - 1)
    self.assertEqual(expected_spec, env.action_spec())

  def test_discrete_spec_nd(self):
    obs_spec = array_spec.BoundedArraySpec((2, 3), np.int32, -10, 10)
    action_spec = array_spec.BoundedArraySpec((2, 2), np.float32, -10, 10)
    limits = np.array([[2, 4], [3, 2]])

    env = random_py_environment.RandomPyEnvironment(
        obs_spec, action_spec=action_spec)
    env = wrappers.ActionDiscretizeWrapper(env, limits)

    expected_spec = array_spec.BoundedArraySpec((2, 2), np.int32, 0, limits - 1)
    self.assertEqual(expected_spec, env.action_spec())

  def test_action_mapping_1d(self):
    obs_spec = array_spec.BoundedArraySpec((2, 3), np.int32, -10, 10)
    action_spec = array_spec.BoundedArraySpec((), np.float32, -10, 10)
    limits = np.array(5)

    def mock_step(_, action):
      return action

    with mock.patch.object(
        random_py_environment.RandomPyEnvironment,
        '_step',
        side_effect=mock_step,
        autospec=True,
    ):
      env = random_py_environment.RandomPyEnvironment(
          obs_spec, action_spec=action_spec)
      env = wrappers.ActionDiscretizeWrapper(env, limits)
      env.reset()

      action = env.step(2)
      np.testing.assert_array_almost_equal(0.0, action)
      action = env.step(4)
      np.testing.assert_array_almost_equal(10.0, action)

  def test_action_mapping_nd(self):
    obs_spec = array_spec.BoundedArraySpec((2, 3), np.int32, -10, 10)
    action_spec = array_spec.BoundedArraySpec((2, 2), np.float32, -10, 10)
    limits = np.array([[2, 5], [3, 2]])

    def mock_step(_, action):
      return action

    with mock.patch.object(
        random_py_environment.RandomPyEnvironment,
        '_step',
        side_effect=mock_step,
        autospec=True,
    ):
      env = random_py_environment.RandomPyEnvironment(
          obs_spec, action_spec=action_spec)
      env = wrappers.ActionDiscretizeWrapper(env, limits)
      env.reset()

      action = env.step([[0, 2], [1, 1]])
      np.testing.assert_array_almost_equal([[-10.0, 0.0], [0.0, 10.0]], action)

  def test_shapes_broadcast(self):
    obs_spec = array_spec.BoundedArraySpec((2, 3), np.int32, -10, 10)
    action_spec = array_spec.BoundedArraySpec((2, 2), np.float32, -10, 10)
    limits = np.array([[2, 5]])

    def mock_step(_, action):
      return action

    with mock.patch.object(
        random_py_environment.RandomPyEnvironment,
        '_step',
        side_effect=mock_step,
        autospec=True,
    ):
      env = random_py_environment.RandomPyEnvironment(
          obs_spec, action_spec=action_spec)
      env = wrappers.ActionDiscretizeWrapper(env, limits)
      env.reset()

      action = env.step([[0, 2], [1, 4]])
      np.testing.assert_array_almost_equal([[-10.0, 0.0], [10.0, 10.0]], action)

  def test_check_limits(self):
    obs_spec = array_spec.BoundedArraySpec((2, 3), np.int32, -10, 10)
    action_spec = array_spec.BoundedArraySpec((2, 2), np.float32, -10, 10)
    limits = np.array([[1, 5], [2, 2]])

    with self.assertRaisesRegexp(ValueError, '.*size 2.'):
      env = random_py_environment.RandomPyEnvironment(
          obs_spec, action_spec=action_spec)
      env = wrappers.ActionDiscretizeWrapper(env, limits)

  def test_check_action_shape(self):
    obs_spec = array_spec.BoundedArraySpec((2, 3), np.int32, -10, 10)
    action_spec = array_spec.BoundedArraySpec((2, 2), np.float32, -10, 10)
    limits = np.array([[2, 5], [2, 2]])

    with self.assertRaisesRegexp(ValueError, '.*incorrect shape.*'):
      env = random_py_environment.RandomPyEnvironment(
          obs_spec, action_spec=action_spec)
      env = wrappers.ActionDiscretizeWrapper(env, limits)
      env.reset()
      env.step([0, 0])

  def test_check_array_bounds(self):
    obs_spec = array_spec.BoundedArraySpec((2, 3), np.int32, -10, 10)
    action_spec = array_spec.BoundedArraySpec((2,), np.float32, [-10, 0], 10)
    limits = np.array([2, 5])

    def mock_step(_, action):
      return action

    with mock.patch.object(
        random_py_environment.RandomPyEnvironment,
        '_step',
        side_effect=mock_step,
        autospec=True,
    ):
      env = random_py_environment.RandomPyEnvironment(
          obs_spec, action_spec=action_spec)
      env = wrappers.ActionDiscretizeWrapper(env, limits)
      env.reset()

      action = env.step([0, 0])
      np.testing.assert_array_almost_equal([-10.0, 0.0], action)

      action = env.step([1, 4])
      np.testing.assert_array_almost_equal([10.0, 10.0], action)

      action = env.step([0, 2])
      np.testing.assert_array_almost_equal([-10.0, 5.0], action)

  def test_action_nest(self):
    obs_spec = array_spec.BoundedArraySpec((2, 3), np.int32, -10, 10)
    action_spec = {
        'action1': array_spec.BoundedArraySpec((2, 2), np.float32, -10, 10)
    }
    limits = np.array([[2, 5]])

    def mock_step(_, action):
      return action

    with mock.patch.object(
        random_py_environment.RandomPyEnvironment,
        '_step',
        side_effect=mock_step,
        autospec=True,
    ):
      env = random_py_environment.RandomPyEnvironment(
          obs_spec, action_spec=action_spec)
      env = wrappers.ActionDiscretizeWrapper(env, limits)
      env.reset()

      action = env.step(np.array([[0, 2], [1, 4]]))
      np.testing.assert_array_almost_equal([[-10.0, 0.0], [10.0, 10.0]],
                                           action['action1'])


class ActionClipWrapper(test_utils.TestCase):

  def test_clip(self):
    obs_spec = array_spec.BoundedArraySpec((2, 3), np.int32, -10, 10)
    action_spec = array_spec.BoundedArraySpec((2,), np.float32, [-1, 0], 1)

    def mock_step(_, action):
      return action

    with mock.patch.object(
        random_py_environment.RandomPyEnvironment,
        '_step',
        side_effect=mock_step,
        autospec=True,
    ):
      env = random_py_environment.RandomPyEnvironment(
          obs_spec, action_spec=action_spec)
      env = wrappers.ActionClipWrapper(env)
      env.reset()

      # actions within bounds, use NumPy action
      action = env.step(np.array([0, 0]))
      np.testing.assert_array_almost_equal([0.0, 0.0], action)

      # action 1 outside bounds, use list action
      action = env.step([-4, 0])
      np.testing.assert_array_almost_equal([-1.0, 0.0], action)

      # action 2 outside bounds, use NumPy action
      action = env.step(np.array([0, -4]))
      np.testing.assert_array_almost_equal([0.0, 0.0], action)

      # actions outside bounds, use list action
      action = env.step([4, 4])
      action = env.step(np.array([4, 4]))
      np.testing.assert_array_almost_equal([1.0, 1.0], action)

  def test_nested(self):
    obs_spec = array_spec.BoundedArraySpec((2, 3), np.int32, -10, 10)
    action_spec = [
        array_spec.BoundedArraySpec((2,), np.float32, -1, 1), [
            array_spec.BoundedArraySpec((2,), np.float32, -2, 2),
            array_spec.BoundedArraySpec((2,), np.float32, -3, 3)
        ]
    ]

    def mock_step(_, action):
      return action

    with mock.patch.object(
        random_py_environment.RandomPyEnvironment,
        '_step',
        side_effect=mock_step,
        autospec=True,
    ):
      env = random_py_environment.RandomPyEnvironment(
          obs_spec, action_spec=action_spec)
      env = wrappers.ActionClipWrapper(env)
      env.reset()

      # use NumPy action
      action = [np.array([10, -10]), [np.array([10, -10]), np.array([10, -10])]]
      action = env.step(action)
      np.testing.assert_array_almost_equal([1, -1], action[0])
      np.testing.assert_array_almost_equal([2, -2], action[1][0])
      np.testing.assert_array_almost_equal([3, -3], action[1][1])

      # use list action
      action = [[10, -10], [[10, -10], [10, -10]]]
      action = env.step(action)
      np.testing.assert_array_almost_equal([1, -1], action[0])
      np.testing.assert_array_almost_equal([2, -2], action[1][0])
      np.testing.assert_array_almost_equal([3, -3], action[1][1])


class ActionOffsetWrapperTest(test_utils.TestCase):

  def test_nested(self):
    obs_spec = array_spec.BoundedArraySpec((2, 3), np.int32, -10, 10)
    action_spec = [
        array_spec.BoundedArraySpec((2,), np.int32, -1, 1), [
            array_spec.BoundedArraySpec((2,), np.int32, -2, 2),
            array_spec.BoundedArraySpec((2,), np.int32, -3, 3)
        ]
    ]
    with self.assertRaisesRegexp(ValueError, 'single-array action specs'):
      env = random_py_environment.RandomPyEnvironment(obs_spec, action_spec)
      env = wrappers.ActionOffsetWrapper(env)

  def test_unbounded(self):
    obs_spec = array_spec.BoundedArraySpec((2, 3), np.int32, -10, 10)
    action_spec = array_spec.ArraySpec((2,), np.int32)
    with self.assertRaisesRegexp(ValueError, 'bounded action specs'):
      env = random_py_environment.RandomPyEnvironment(obs_spec, action_spec)
      env = wrappers.ActionOffsetWrapper(env)

  def test_continuous(self):
    obs_spec = array_spec.BoundedArraySpec((2, 3), np.int32, -10, 10)
    action_spec = array_spec.BoundedArraySpec((2,), np.float32, -1, 1)
    with self.assertRaisesRegexp(ValueError, 'discrete action specs'):
      env = random_py_environment.RandomPyEnvironment(obs_spec, action_spec)
      env = wrappers.ActionOffsetWrapper(env)

  def test_action_spec(self):
    obs_spec = array_spec.BoundedArraySpec((2, 3), np.int32, -10, 10)
    action_spec = array_spec.BoundedArraySpec((3,), np.int32, -1, 1)
    env = random_py_environment.RandomPyEnvironment(obs_spec, action_spec)
    env = wrappers.ActionOffsetWrapper(env)
    self.assertEqual(array_spec.BoundedArraySpec((3,), np.int32, 0, 2),
                     env.action_spec())

  def test_step(self):
    obs_spec = array_spec.BoundedArraySpec((2, 3), np.int32, -10, 10)
    action_spec = array_spec.BoundedArraySpec((3,), np.int32, -1, 1)
    mock_env = mock.Mock(
        wraps=random_py_environment.RandomPyEnvironment(obs_spec, action_spec))
    env = wrappers.ActionOffsetWrapper(mock_env)
    env.reset()

    env.step(np.array([0, 1, 2]))
    self.assertTrue(mock_env.step.called)
    np.testing.assert_array_equal(np.array([-1, 0, 1]),
                                  mock_env.step.call_args[0][0])


class FlattenObservationsWrapper(parameterized.TestCase):

  @parameterized.parameters((['obs1', 'obs2'], [(4,), (5,)], np.int32),
                            (['obs1', 'obs2', 'obs3'], [(1,), (1,),
                                                        (4,)], np.float32),
                            ((['obs1', 'obs2'], [(5, 2), (3, 3)], np.float32)))
  def test_with_varying_observation_specs(
      self, observation_keys, observation_shapes, observation_dtypes):
    """Vary the observation spec and step the environment."""
    obs_spec = collections.OrderedDict()
    for idx, key in enumerate(observation_keys):
      obs_spec[key] = array_spec.ArraySpec(observation_shapes[idx],
                                           observation_dtypes)
    action_spec = array_spec.BoundedArraySpec((), np.int32, -10, 10)

    env = random_py_environment.RandomPyEnvironment(
        obs_spec, action_spec=action_spec)
    env = wrappers.FlattenObservationsWrapper(env)
    time_step = env.step(
        array_spec.sample_bounded_spec(action_spec, np.random.RandomState()))
    # Check that all observations returned from environment is packed into one
    # dimension.
    expected_shape = self._get_expected_shape(obs_spec, obs_spec.keys())
    self.assertEqual(time_step.observation.shape, expected_shape)
    self.assertEqual(
        env.observation_spec(),
        array_spec.ArraySpec(
            shape=expected_shape,
            dtype=observation_dtypes,
            name='packed_observations'))

  @parameterized.parameters((('obs1'),), (('obs1', 'obs3'),))
  def test_with_varying_observation_filters(self, observations_to_keep):
    """Vary the observations to save from the environment."""
    obs_spec = collections.OrderedDict({
        'obs1': array_spec.ArraySpec((1,), np.int32),
        'obs2': array_spec.ArraySpec((2,), np.int32),
        'obs3': array_spec.ArraySpec((3,), np.int32)
    })

    observations_to_keep = np.array([observations_to_keep]).flatten()
    action_spec = array_spec.BoundedArraySpec((), np.int32, -10, 10)

    env = random_py_environment.RandomPyEnvironment(
        obs_spec, action_spec=action_spec)
    # Create the wrapper with list of observations to keep before packing it
    # into one dimension.
    env = wrappers.FlattenObservationsWrapper(
        env, observations_whitelist=observations_to_keep)
    time_step = env.step(
        array_spec.sample_bounded_spec(action_spec, np.random.RandomState()))
    # The expected shape is the sum of observation lengths in the observation
    # spec that has been filtered by the observations_to_keep list.
    expected_shape = self._get_expected_shape(obs_spec, observations_to_keep)
    # Test the expected shape of observations returned from stepping the
    # environment and additionally, check the environment spec.
    self.assertEqual(time_step.observation.shape, expected_shape)
    self.assertEqual(
        env.observation_spec(),
        array_spec.ArraySpec(
            shape=expected_shape, dtype=np.int32, name='packed_observations'))

  def test_env_reset(self):
    """Test the observations returned after an environment reset."""
    obs_spec = collections.OrderedDict({
        'obs1': array_spec.ArraySpec((1,), np.int32),
        'obs2': array_spec.ArraySpec((2,), np.int32),
        'obs3': array_spec.ArraySpec((3,), np.int32)
    })

    action_spec = array_spec.BoundedArraySpec((), np.int32, -10, 10)

    env = random_py_environment.RandomPyEnvironment(
        obs_spec, action_spec=action_spec)
    # Create the wrapper with list of observations to keep before packing it
    # into one dimension.
    env = wrappers.FlattenObservationsWrapper(env)
    time_step = env.reset()
    expected_shape = self._get_expected_shape(obs_spec, obs_spec.keys())
    self.assertEqual(time_step.observation.shape, expected_shape)
    self.assertEqual(
        env.observation_spec(),
        array_spec.ArraySpec(
            shape=expected_shape, dtype=np.int32, name='packed_observations'))

  @parameterized.parameters(([array_spec.ArraySpec((1,), np.int32)],),
                            array_spec.ArraySpec((1,), np.int32))
  def test_observations_wrong_spec_for_whitelist(self, observation_spec):
    """Test the Wrapper has ValueError if the observation spec is invalid."""
    action_spec = array_spec.BoundedArraySpec((), np.int32, -10, 10)

    env = random_py_environment.RandomPyEnvironment(
        observation_spec, action_spec=action_spec)
    # Create the wrapper with list of observations to keep before packing it
    # into one dimension.
    with self.assertRaises(ValueError):
      env = wrappers.FlattenObservationsWrapper(
          env, observations_whitelist=['obs1'])

  def test_observations_unknown_whitelist(self):
    """Test the Wrapper has ValueError if given unknown keys."""
    action_spec = array_spec.BoundedArraySpec((), np.int32, -10, 10)

    obs_spec = collections.OrderedDict({
        'obs1': array_spec.ArraySpec((1,), np.int32),
        'obs2': array_spec.ArraySpec((2,), np.int32),
        'obs3': array_spec.ArraySpec((3,), np.int32)
    })

    env = random_py_environment.RandomPyEnvironment(
        obs_spec, action_spec=action_spec)

    whitelist_unknown_keys = ['obs1', 'obs4']

    with self.assertRaises(ValueError):
      env = wrappers.FlattenObservationsWrapper(
          env, observations_whitelist=whitelist_unknown_keys)

  def test_observations_multiple_dtypes(self):
    """Test the Wrapper has ValueError if given unknown keys."""
    action_spec = array_spec.BoundedArraySpec((), np.int32, -10, 10)

    obs_spec = collections.OrderedDict({
        'obs1': array_spec.ArraySpec((1,), np.int32),
        'obs2': array_spec.ArraySpec((2,), np.float32),
    })

    env = random_py_environment.RandomPyEnvironment(
        obs_spec, action_spec=action_spec)

    with self.assertRaises(ValueError):
      env = wrappers.FlattenObservationsWrapper(env)

  def test_batch_env(self):
    """Vary the observation spec and step the environment."""
    obs_spec = collections.OrderedDict({
        'obs1': array_spec.ArraySpec((1,), np.int32),
        'obs2': array_spec.ArraySpec((2,), np.int32),
    })

    action_spec = array_spec.BoundedArraySpec((), np.int32, -10, 10)

    # Generate a randomy py environment with batch size.
    batch_size = 4
    env = random_py_environment.RandomPyEnvironment(
        obs_spec, action_spec=action_spec, batch_size=batch_size)

    env = wrappers.FlattenObservationsWrapper(env)
    time_step = env.step(
        array_spec.sample_bounded_spec(action_spec, np.random.RandomState()))

    expected_shape = self._get_expected_shape(obs_spec, obs_spec.keys())
    self.assertEqual(time_step.observation.shape,
                     (batch_size, expected_shape[0]))
    self.assertEqual(
        env.observation_spec(),
        array_spec.ArraySpec(
            shape=expected_shape, dtype=np.int32, name='packed_observations'))

  def _get_expected_shape(self, observation, observations_to_keep):
    """Gets the expected shape of a flattened observation nest."""
    # The expected shape is the sum of observation lengths in the observation
    # spec.  For a multi-dimensional observation, it is flattened, thus the
    # length is the product of its shape, i.e. Two arrays ([3, 3], [2, 3])
    # result in a len-9 and len-6 observation, with total length of 15.
    expected_shape = 0
    for obs in observations_to_keep:
      expected_shape += np.prod(observation[obs].shape)
    return (expected_shape,)


class MockGoalReplayEnvWrapper(wrappers.GoalReplayEnvWrapper):
  """Mock environment specific implementation of GoalReplayEnvWrapper."""

  def get_trajectory_with_goal(self, trajectory, goal):
    # In this mock environment, 'obs1' is the goal
    trajectory.observation.update({'obs1': goal})
    return trajectory

  def get_goal_from_trajectory(self, trajectory):
    return trajectory.observation['obs1']


class GoalReplayEnvWrapperTest(parameterized.TestCase):

  @parameterized.parameters((['obs1', 'obs2'], [(4,), (5,)], np.int32),
                            (['obs1', 'obs2', 'obs3'], [(1,), (1,),
                                                        (4,)], np.float32),
                            ((['obs1', 'obs2'], [(5, 2), (3, 3)], np.float32)))
  def test_with_varying_observation_specs(
      self, observation_keys, observation_shapes, observation_dtypes):
    """Vary the observation spec and step the environment."""
    obs_spec = collections.OrderedDict()
    for idx, key in enumerate(observation_keys):
      obs_spec[key] = array_spec.ArraySpec(observation_shapes[idx],
                                           observation_dtypes)
    action_spec = array_spec.BoundedArraySpec((), np.int32, -10, 10)

    env = random_py_environment.RandomPyEnvironment(
        obs_spec, action_spec=action_spec)
    env = MockGoalReplayEnvWrapper(env)
    random_action = array_spec.sample_bounded_spec(action_spec,
                                                   np.random.RandomState())
    time_step = env.step(random_action)
    self.assertIsInstance(time_step.observation, dict)
    self.assertEqual(time_step.observation.keys(),
                     env.observation_spec().keys())
    time_step = env.reset()
    self.assertIsInstance(time_step.observation, dict)
    self.assertEqual(time_step.observation.keys(),
                     env.observation_spec().keys())

  def test_not_implemented_functions(self):
    """Wrapper contains functions which need to be implemented in child."""
    obs_spec = collections.OrderedDict({
        'obs1': array_spec.ArraySpec((1,), np.int32),
        'obs2': array_spec.ArraySpec((2,), np.int32),
    })
    action_spec = array_spec.BoundedArraySpec((), np.int32, -10, 10)

    env = random_py_environment.RandomPyEnvironment(
        obs_spec, action_spec=action_spec)
    with self.assertRaises(TypeError):
      env = wrappers.GoalReplayEnvWrapper(env)

  def test_batch_env(self):
    """Test batched version of the environment."""
    obs_spec = collections.OrderedDict({
        'obs1': array_spec.ArraySpec((1,), np.int32),
        'obs2': array_spec.ArraySpec((2,), np.int32),
    })
    action_spec = array_spec.BoundedArraySpec((), np.int32, -10, 10)

    # Generate a randomy py environment with batch size.
    batch_size = 4
    env = random_py_environment.RandomPyEnvironment(
        obs_spec, action_spec=action_spec, batch_size=batch_size)
    env = MockGoalReplayEnvWrapper(env)
    random_action = array_spec.sample_bounded_spec(action_spec,
                                                   np.random.RandomState())

    time_step = env.step(random_action)
    self.assertIsInstance(time_step.observation, dict)
    self.assertEqual(time_step.observation.keys(),
                     env.observation_spec().keys())
    time_step = env.reset()
    self.assertIsInstance(time_step.observation, dict)
    self.assertEqual(time_step.observation.keys(),
                     env.observation_spec().keys())


class CountingEnv(py_environment.PyEnvironment):

  def __init__(self):
    self._count = np.array(0, dtype=np.int32)

  def _reset(self):
    self._count = np.array(0, dtype=np.int32)
    return ts.restart(self._count.copy())

  def observation_spec(self):
    return array_spec.ArraySpec((), np.int32)

  def action_spec(self):
    return array_spec.ArraySpec((), np.int32)

  def _step(self, action):
    self._count += 1
    if self._count < 4:
      return ts.transition(self._count.copy(), 1)
    return ts.termination(self._count.copy(), 1)


class HistoryWrapperTest(test_utils.TestCase):

  def test_observation_spec_changed(self):
    cartpole_env = gym.spec('CartPole-v1').make()
    env = gym_wrapper.GymWrapper(cartpole_env)
    obs_shape = env.observation_spec().shape

    history_env = wrappers.HistoryWrapper(env, 3)
    self.assertEqual((3,) + obs_shape, history_env.observation_spec().shape)

  def test_observation_spec_changed_with_action(self):
    cartpole_env = gym.spec('CartPole-v1').make()
    env = gym_wrapper.GymWrapper(cartpole_env)
    obs_shape = env.observation_spec().shape
    action_shape = env.action_spec().shape

    history_env = wrappers.HistoryWrapper(env, 3, include_actions=True)
    self.assertEqual((3,) + obs_shape,
                     history_env.observation_spec()['observation'].shape)
    self.assertEqual((3,) + action_shape,
                     history_env.observation_spec()['action'].shape)

  def test_observation_stacked(self):
    env = CountingEnv()
    history_env = wrappers.HistoryWrapper(env, 3)
    time_step = history_env.reset()
    self.assertEqual([0, 0, 0], time_step.observation.tolist())

    time_step = history_env.step(0)
    self.assertEqual([0, 0, 1], time_step.observation.tolist())

    time_step = history_env.step(0)
    self.assertEqual([0, 1, 2], time_step.observation.tolist())

    time_step = history_env.step(0)
    self.assertEqual([1, 2, 3], time_step.observation.tolist())

  def test_observation_and_action_stacked(self):
    env = CountingEnv()
    history_env = wrappers.HistoryWrapper(env, 3, include_actions=True)
    time_step = history_env.reset()
    self.assertEqual([0, 0, 0], time_step.observation['observation'].tolist())
    self.assertEqual([0, 0, 0], time_step.observation['action'].tolist())

    time_step = history_env.step(5)
    self.assertEqual([0, 0, 1], time_step.observation['observation'].tolist())
    self.assertEqual([0, 0, 5], time_step.observation['action'].tolist())

    time_step = history_env.step(6)
    self.assertEqual([0, 1, 2], time_step.observation['observation'].tolist())
    self.assertEqual([0, 5, 6], time_step.observation['action'].tolist())

    time_step = history_env.step(7)
    self.assertEqual([1, 2, 3], time_step.observation['observation'].tolist())
    self.assertEqual([5, 6, 7], time_step.observation['action'].tolist())


class PerformanceProfilerWrapperTest(test_utils.TestCase):

  def test_profiling(self):
    cartpole_env = gym.make('CartPole-v1')
    env = gym_wrapper.GymWrapper(cartpole_env)
    profile = [None]
    def profile_fn(p):
      self.assertIsInstance(p, cProfile.Profile)
      profile[0] = p

    env = wrappers.PerformanceProfiler(
        env, process_profile_fn=profile_fn,
        process_steps=2)

    env.reset()

    # Resets are also profiled.
    s = pstats.Stats(env._profile)
    self.assertGreater(s.total_calls, 0)

    for _ in range(2):
      env.step(1)

    self.assertIsNotNone(profile[0])
    previous_profile = profile[0]

    updated_s = pstats.Stats(profile[0])
    self.assertGreater(updated_s.total_calls, s.total_calls)

    for _ in range(2):
      env.step(1)

    self.assertIsNotNone(profile[0])
    # We saw a new profile.
    self.assertNotEqual(profile[0], previous_profile)


class OneHotActionWrapperTest(test_utils.TestCase):

  def testActionSpec(self):
    cartpole_env = gym.spec('CartPole-v1').make()
    env = gym_wrapper.GymWrapper(cartpole_env)
    one_hot_action_wrapper = wrappers.OneHotActionWrapper(env)
    expected_spec = array_spec.BoundedArraySpec(
        shape=(2,),
        dtype=np.int64,
        minimum=0,
        maximum=1,
        name='one_hot_action_spec')
    self.assertEqual(one_hot_action_wrapper.action_spec(), expected_spec)

  def testStep(self):
    obs_spec = array_spec.BoundedArraySpec((2, 3), np.int32, -10, 10)
    action_spec = array_spec.BoundedArraySpec((1,), np.int32, 0, 2)
    mock_env = mock.Mock(
        wraps=random_py_environment.RandomPyEnvironment(obs_spec, action_spec))
    one_hot_action_wrapper = wrappers.OneHotActionWrapper(mock_env)
    one_hot_action_wrapper.reset()

    one_hot_action_wrapper.step(np.array([0.5, 0.4, 0.1]))
    self.assertTrue(mock_env.step.called)
    np.testing.assert_array_equal(0, mock_env.step.call_args[0][0])


if __name__ == '__main__':
  test_utils.main()
