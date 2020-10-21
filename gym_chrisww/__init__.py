from gym.envs.registration import register

register(
    id='chrisww-v0',
    entry_point='gym_chrisww.envs:Chrisww_gym',
    kwargs={'dim': 5,'res':240,'mines':0, 'r_mines':0, 'r_dist':-1, 'r_door':0 }, 
)

register(
    id='chrisww-v1',
    entry_point='gym_chrisww.envs:Chrisww_gym',
    kwargs={'dim': 10,'res':480,'mines':0, 'r_mines':0, 'r_dist':-1, 'r_door':0}, 
)

register(
    id='chrisww-v2',
    entry_point='gym_chrisww.envs:Chrisww_gym',
    kwargs={'dim': 10,'res':480,'mines':10, 'r_mines':-3, 'r_dist':-1, 'r_door':0}, 
)