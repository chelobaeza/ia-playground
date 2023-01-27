import time
import traceback

from mazeEnvExtended import MazeEnvExtended
from agent import Agent
from modelExample import ModelExample
from search_agents import AgentA, AgentUCS


envs = [
    (MazeEnvExtended, "MazeEnv10x10_1"),
    (MazeEnvExtended, "MazeEnv10x10_2")
]

agents = [
    # (Agent, "InputAgent")
    (AgentUCS, "UCS"),
    (AgentA, "A"),
    #(AgentLRTA, "LRTA"),
]

models = [
    (ModelExample, "GoalModel")
]


def main():

    for env, e_name in envs:
        for agent, a_name in agents:
            for model, m_name in models:
                print(e_name, a_name, m_name)
                try:
                    # si queremos que se vea con interfaz grafica
                    run(env(maze_file=e_name + ".npy", mode="human"),
                        agent(model(model_file=e_name + ".txt")))
                    # run(env(maze_file=e_name + ".npy"),
                    #     agent(model(model_file=e_name + ".txt")))
                except Exception as e:
                    print(str(e))
                    print(traceback.format_exc())
                print("------------")
            print("-----------------------")
        print("-----------------------------------")


def run(env, agent):
    try:
        _prepare_env(env)

        start_time = time.time()
        print("Starting:", start_time)
        wins, step_counter = agent.run(env)
        print("--- %s seconds ---" % (time.time() - start_time))
        print("Catched:", wins, "Steps:", step_counter)
    finally:
        print("deleting env")
        del env


def _prepare_env(env):
    env.reset()
    env.should_trace_location(True)


if __name__ == "__main__":
    main()
