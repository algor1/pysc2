from pysc2.agents import base_agent
from pysc2.lib import actions,features


import time

# Functions
_BUILD_SUPPLYDEPOT = actions.FUNCTIONS.Build_SupplyDepot_screen.id
_NOOP = actions.FUNCTIONS.no_op.id
_SELECT_POINT = actions.FUNCTIONS.select_point.id
_SELECT_RECT = actions.FUNCTIONS.select_rect.id


# Features
_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index

# Unit IDs
_TERRAN_COMMANDCENTER = 18
_TERRAN_SCV = 45

# Parameters
_PLAYER_SELF = 1
_NOT_QUEUED = [0]
_QUEUED = [1]

class SimpleAgent(base_agent.BaseAgent):
    base_top_left = None
    supply_depot_built = False
    scv_selected = False
    stop_scv= False
    def step(self, obs):
        super(SimpleAgent, self).step(obs)

        time.sleep(0.5)
        if not self.stop_scv:
            target=[[0,0],[84,84]]
            self.stop_scv=True
            return actions.FunctionCall(_SELECT_RECT, [_NOT_QUEUED, target])

        if self.base_top_left is None:
            player_y, player_x = (obs.observation["minimap"][_PLAYER_RELATIVE] == _PLAYER_SELF).nonzero()
            self.base_top_left = player_y.mean() <= 31

        if not self.supply_depot_built:
            if not self.scv_selected:
                unit_type = obs.observation["screen"][_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _TERRAN_SCV).nonzero()

                target = [unit_x[0], unit_y[0]]

                self.scv_selected = True

                return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])
            elif _BUILD_SUPPLYDEPOT in obs.observation["available_actions"]:
                unit_type = obs.observation["screen"][_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _TERRAN_COMMANDCENTER).nonzero()

                target = self.transformLocation(int(unit_x.mean()), 0, int(unit_y.mean()), 20)

                self.supply_depot_built = True

                return actions.FunctionCall(_BUILD_SUPPLYDEPOT, [_NOT_QUEUED, target])


        return actions.FunctionCall(actions.FUNCTIONS.no_op.id, [])
    def _build_model_predict(self):
        #
        # input_dim = (self.state_size+self.action_size)*self.num_of_previous_turns
        # model = Sequential()
        # model.add(Dense(input_dim*2,input_shape=(input_dim,),activation='relu'))
        # # model.add(Dropout(0.4))
        # model.add(Dense(input_dim*2, activation='relu'))
        # # model.add(Dropout(0.4))
        # model.add(Dense(1, activation='tanh'))
        # print(model.summary())
        # model.compile(loss='mean_squared_error',
        #               optimizer='adam')
        # print(model.output_shape)
        # print(model.input_shape)
        # return model
        pass

    def transformLocation(self, x, x_distance, y, y_distance):
        if not self.base_top_left:
            return [x - x_distance, y - y_distance]

        return [x + x_distance, y + y_distance]