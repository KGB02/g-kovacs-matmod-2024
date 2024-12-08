import matplotlib.pyplot as plt

import src.wealthdistribution as wd


def main(): # rács definiálása
    width = 50  # szélesség
    height = 50 # magasság
    max_grain = 50 # egy mezőre jutó legtöbb gabona
    percent_best_land = 0.5 # a legjobb termőnégyzetek
    num_people = 500 # emberek száma
    life_expectancy_max = 15 # max élettartam
    life_expectancy_min = 3 # min élettartam
    metabolism_max = 5 # anyagcsere
    num_grain_grow = 10 # egy időpont alatt növő gabona mennyisége
    model = wd.WealthModel(width=width, height=height, max_grain=max_grain, percent_best_land=percent_best_land,
                           num_people=num_people, life_expectancy_max=life_expectancy_max,
                           life_expectancy_min=life_expectancy_min, metabolism_max=metabolism_max,
                           num_grain_grow=num_grain_grow) # a fenti paraméterekkel létrehozzuk a modellt
    time = 5
    for t in range(time): # lépésszám
        model.step()
    model_data = model.datacollector.get_model_vars_dataframe() # az adatok lekérése


if __name__ == "__main__":
    main() # futtatás
