#!/usr/bin/env python

import flask
from flask import Flask, render_template, url_for, abort, request
import plotly
import plotly.graph_objs as go
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
import json
from flowshop import Flowshop
import datetime

def create_plot():
    n = 30
    x = np.linspace(0, 1, n)
    y = np.random.randn(n)
    df = pd.DataFrame({'x': x, 'y': y})

    data = [
        go.Bar(
            x = df["x"],
            y = df["y"]
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


app = Flask(__name__)

@app.route('/solve', methods=["POST"])
def solve():
    if request.method == "POST":
        prob = request.get_json()
        pfsp_algorithm = prob["algorithm"]
        data = prob["data"]
        print(data)
        print("algorithm {}".format(pfsp_algorithm))

@app.route('/')
def index():
    nb_m = 2
    nb_j = 6
    data = [[6, 2, 10, 4, 5, 3], [5, 4, 3, 8, 2, 4]]
    pfsp = Flowshop(data, nb_m, nb_j)
    seq, jobs_m1, jobs_m2 = pfsp.solve_johnson()

    df = []
    curr_date = datetime.datetime.now()
    for i, j in zip(jobs_m1, jobs_m2):
        Start =  (datetime.timedelta(seconds=i["start_time"]) + curr_date).strftime("%Y-%m-%d %H:%M:%S")
        Finish = (datetime.timedelta(seconds=i["end_time"]) + curr_date).strftime("%Y-%m-%d %H:%M:%S")
        task = {"Task": "M1", "Start": Start, "Finish": Finish, "Resource": i["name"]}
        df.append(task)
        Start =  (datetime.timedelta(seconds=j["start_time"]) + curr_date).strftime("%Y-%m-%d %H:%M:%S")
        Finish = (datetime.timedelta(seconds=j["end_time"]) + curr_date).strftime("%Y-%m-%d %H:%M:%S")
        task = {"Task": "M2", "Start": Start, "Finish": Finish, "Resource": j["name"]}
        df.append(task)
    fig = ff.create_gantt(df, group_tasks=True, index_col="Resource", show_colorbar=True, showgrid_x=True, showgrid_y=True, width=500, height=600, bar_width=0.1)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('index.html', plot=graphJSON)

if __name__ == "__main__":
    app.run(debug=True, port=1337)

