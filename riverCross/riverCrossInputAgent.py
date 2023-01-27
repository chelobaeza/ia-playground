from riverCrossEnv import RiverCrossEnv
from riverCrossUtils import finish, ask_input, parse_action, input_action


def run():

    env = RiverCrossEnv()

    hasFinished = False
    observation = env.reset()

    while (not(hasFinished)):
        env.render()
        action = input_action()

        observation, reward, hasFinished, debug = env.step(action)

    env.render()
    finish(observation)
