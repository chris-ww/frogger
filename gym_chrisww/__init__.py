from gym.envs.registration import register

register(
    id='chrisww-v0',
    entry_point='gym_chrisww.envs:Chrisww_gym',
    kwargs={'dim': 5,'res':240}, 
)

register(
    id='chrisww-v1',
    entry_point='gym_chrisww.envs:Chrisww_gym',
    kwargs={'dim': 10,'res':480}, 
)



