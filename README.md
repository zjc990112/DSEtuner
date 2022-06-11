# DSEtuner
A DSEtuner for spatial architecture 

## prerequisites

```shell
conda create --name dsetuner python=3.8
conda install --file requirements.txt
```

## Usage

```shell
# for all the parameters
./dsetuner.py --help
```


```shell
# with simulator executable and setting file, and stop after 100 seconds

./dsetuner.py --stop-after 100 --setting ./setting.json --simulator ./simulator.py
```
