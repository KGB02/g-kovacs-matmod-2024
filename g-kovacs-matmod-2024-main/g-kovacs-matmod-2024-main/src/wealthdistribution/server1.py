import mesa
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

import src.wealthdistribution as wd


def bsr_model_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is wd.GrainAgent: # a gabona vizualizálása
        portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
        (x, y) = agent.pos
        portrayal["x"] = x
        portrayal["y"] = y
        if agent.grain_here > 30:
            portrayal["Color"] = "#FFFF00"
        else:
            portrayal["Color"] = "#FFFFAD"

    elif type(agent) is wd.PersonAgent: # a társadalmi osztályokat meghatározó ábra vizualizálása
        if agent.state == 0:
            portrayal["Shape"] = "pics/inf.png"
            portrayal["scale"] = 0.9
            portrayal["Layer"] = 3
        elif agent.state == 1:
            portrayal["Shape"] = "pics/rec.png"
            portrayal["scale"] = 0.9
            portrayal["Layer"] = 2
        elif agent.state == 2:
            portrayal["Shape"] = "pics/susc.png"
            portrayal["scale"] = 0.9
            portrayal["Layer"] = 1
    return portrayal


canvas_element = CanvasGrid(bsr_model_portrayal, 50, 50, 500, 500)

chart1 = mesa.visualization.ChartModule([{"Label": "Low", "Color": "Red"}, {"Label": "Medium", "Color": "Blue"},
                                         {"Label": "High", "Color": "Green"}],
                                        data_collector_name='datacollector')

model_params = { # a megadott paraméterek mentén meghatározzuk a rács tulajdonságait és csúszkát hozunk létre minden megfelelő elemhez
    "height": 50,
    "width": 50,
    "max_grain": 50,
    "percent_best_land": mesa.visualization.Slider(name="percent_best_land", value=0.5, min_value=0, max_value=1, step=0.1),
    "num_people": mesa.visualization.Slider(name="num_people", value=500, min_value=10, max_value=900, step=1),
    "life_expectancy_max": mesa.visualization.Slider(name="life_expectancy_max", value=30, min_value=1, max_value=100, step=1),
    "life_expectancy_min": mesa.visualization.Slider(name="life_expectancy_min", value=5, min_value=1, max_value=100, step=1),
    "metabolism_max": mesa.visualization.Slider(name="metabolism_max", value=5, min_value=1, max_value=25, step=1),
    "num_grain_grow": mesa.visualization.Slider(name="num_grain_grow", value=5, min_value=1, max_value=10, step=1)
}

server = ModularServer(
    wd.WealthModel, [canvas_element, chart1], "Wealth Distribution", model_params
)
