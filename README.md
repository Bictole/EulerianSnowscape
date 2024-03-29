<img align="right" src="https://visitor-badge.laobi.icu/badge?page_id=bictole.appero&right_color=pink">

# Eulerian Snowscape [![Profile][title-img]][profile]

[title-img]:https://img.shields.io/badge/-Bictole-pink
[profile]:https://github.com/bictole

## Authors

[Bictole](https://github.com/Bictole)\
[Alex-Leme](https://github.com/Alex-Leme)\
[Adrien Anton Ludwig](https://github.com/Adrien-ANTON-LUDWIG)\
[jeannemorin](https://github.com/jeannemorin)

---

## Architecture

The `theory` folder contains files related to the algorithms used to retrieve Eulerian cycles from a graph:
- drone.py: functions related to creating the drone's route
- eulerian.py: functions related to the Eulerian cycle (verification, search, creation, etc.)
- graph.py: functions related to graphs
- main.py: main function executing various algorithms to retrieve snowplow itineraries
- oriented_edge.py: functions related to graph orientation
- print_tools.py: functions related to graph display
- test.py: unit tests for the theoretical part
- tools.py: useful functions

The `application` folder contains files related to the application of our algorithms from the "theory" tree to cities:
- city_test.py: tests for the application of algorithms to a city
- city_tools.py: functions useful for transforming city data for our algorithms

---

## Usage

Install Python3 and pip, then create a virtual python environment:

```bash
pip install virtualenv
python -m venv venv
source venv/bin/activate
```

Install the required packages:

```bash
- python3 install -r requirements.txt
```

To run the demonstration on the city of Montréal (France):

```bash
python demonstration.py
```


To run the generic demonstration (allows for modification of the parameters used):
```bash
python generic_demonstration.py
```

<img src="https://github.com/Bictole/Appero/blob/master/theory/neige-tempete-deneigeuse.jpg" alt="Appero logo">
