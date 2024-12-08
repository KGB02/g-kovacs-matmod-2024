# megfelelő csomagok behívása

import numpy as np

from mesa.agent import Agent

import src.wealthdistribution as wd

# gabona mint osztály definiálása
class GrainAgent(Agent):
    def __init__(self, pos: tuple, model: wd.WealthModel):
        super().__init__(pos, model)
        self.pos = pos # a cella pozíciója
        self.grain_here = None # a cellában lévő gabona mennyisége

    def step(self):
        self.grow_grain() # ezzel növeljük lépésenként a gabona mennyiségét

    def grow_grain(self): # a gabona növekedésének pontos meghatározása
        self.model: wd.WealthModel
        agents_in_cell = self.model.grid.get_cell_list_contents([self.pos])
        agents_in_cell.remove(self)
        if len(agents_in_cell) == 0:
            self.grain_here += self.model.num_grain_grow # gabona mennyiségének növelése
        else:
            self.grain_here = self.model.num_grain_grow # gabona újratelepítése


class PersonAgent(Agent): # a résztvevő személyek(ágensek) definiálása
    def __init__(self, unique_id: int, model: wd.WealthModel):
        super().__init__(unique_id=unique_id, model=model)
        self.age = None # a személy kora
        self.metabolism = None # a személy metabolizmusa (anyagcseréje)
        self.wealth = None # a személy vagyona
        self.life_expectancy = None # a személy várható élettartama
        self.state = None # a személy osztályba sorolása (alsó,közép,felső)

    def step(self):
        self.move() # a személy mozgása
        self.harvest() # aratás definiálása
        self.eat_age_die() # az ágens ezen kívül még eszik,öregszik és meghal

    def move(self):
        self.model: wd.WealthModel
        cell_to_move = self.model.grid.get_neighborhood(
            pos=self.pos,
            moore=True,
            include_center=False,
            radius=6) # a lehetséges mozgás meghatározása, a "max-vision" itt változtatható,nem csúszkával
        dest_cell = self.model.random.choice(cell_to_move) # egy cella kiválasztása
        self.model.grid.move_agent(agent=self, pos=dest_cell) # az ágens kiválasztott cellába helyezése

    def harvest(self): # a begyűjtés definiálása
        self.model: wd.WealthModel
        agents_in_cell = self.model.grid.get_cell_list_contents([self.pos])
        if len(agents_in_cell) == 1:
            pass
        else:
            grain = None # ha az ágens egyedül van a cellában, gabona nélkül, akkor nem történik semmi
            for agent in agents_in_cell:
                if type(agent) == wd.GrainAgent:
                    grain = agent.grain_here # van gabona
            if grain is not None:
                self.wealth += (grain / (len(agents_in_cell)-1)) # elfogyasztják és megnöveli a vagyont

    def eat_age_die(self):
        self.model: wd.WealthModel
        self.wealth -= self.metabolism # gabonafogyasztás
        self.age += 1 # öregedés,lépésenként 1-el
        pos = self.pos
        if self.wealth > self.model.max_wealth:
            self.model.max_wealth = self.wealth
        if self.wealth <= (self.model.max_wealth / 3):
            self.state = 0 # a személy az alsó osztályba tartozik
        elif (self.model.max_wealth / 3) < self.wealth <= (self.model.max_wealth * 2 / 3):
            self.state = 1 # a személy középosztálybeli
        else:
            self.state = 2 # a személy gazdag
        if self.wealth < 0 or self.age > self.life_expectancy:
            self.model.grid.remove_agent(self) # ágens halála
            self.model.schedule.remove(self) # ágens eltávolítása a további lépésekből
            g = wd.PersonAgent(unique_id=self.model.next_id(), model=self.model)
            self.model.schedule.add(agent=g) # létrehoz egy új ágenst
            self.model.grid.place_agent(agent=g, pos=pos) # elhelyezésre kerül, random élettartam,vagyon és metabolizmus értékekkel
            g.life_expectancy = (self.model.life_expectancy_min +
                                 np.random.randint(self.model.life_expectancy_max - self.model.life_expectancy_min + 1))
            g.metabolism = 1 + np.random.randint(self.model.metabolism_max)
            g.wealth = g.metabolism + np.random.randint(50)
            g.age = np.random.randint(g.life_expectancy)
            if g.wealth <= (self.model.max_wealth / 3): # az új ágens vagyonbéli besorolása
                g.state = 0
            elif (self.model.max_wealth / 3) < g.wealth <= (self.model.max_wealth * 2 / 3):
                g.state = 1
            else:
                g.state = 2


