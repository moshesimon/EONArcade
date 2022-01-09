from gym.envs.registration import register

register(
    id='ArcadeGame-v2',
    entry_point ='gym_game.envs:CustomEnv',
    max_episode_steps=2000,
)