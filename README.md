# Volmex Snooper

The point of this script is to read the data from publicly available APIs to figure out how far the volmex token prices are from their index values.

## Set up a virtual environment

This has not been tested, if something is wrong here just file an issue.

```shell
python3 -m venv venv
source venv/bin/activate 
pip install -r requirements.txt
```

To collect a single data point, when your virtual environment is activated run

```shell
python main.py
```

To view the canned charts

```shell
python view.py
```

## Contributing 

I will take PRs to this and review them when I can.