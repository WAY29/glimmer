# Glimmer
Current version: 1.4.0
***A poc framework base on python***

## Requirements
- rich
- func_timeout
- requests
- click
- shodan
- zoomeye

## Install
```bash
pip3 install -U python-glimmer
glimmer --help
```
or
```bash
git clone https://github.com/WAY29/glimmer.git
cd glimmer
python3 -m pip install -r requirements.txt
python3 glimmer/main.py --help
```

## Usage
```
Usage: main.py [OPTIONS] COMMAND [ARGS]...

  A poc framework base on python.

  Tips: {parser} are plugins in plugins/parser which parse
  user input by protocol and get data for poc and target, you
  can write yourself parser.

Options:
  -u, --url TEXT         Load targets from {parser}.
  -f, --file TEXT        Load targets from file and parse each
                         line with {parser}.

  -p, --poc TEXT         Load pocs from {parser}.
  -pf, --poc-file TEXT   Load pocs from file and parse each
                         line with {parser}.

  --pocs_path TEXT       User custom poc dir.
  -o, --out TEXT         Use output plugins. default is console
  --plugins_path TEXT    User custom output plugin dir.
  --threads INTEGER
  -c, --config TEXT      Load config from a configuration toml
                         file.

  -t, --timeout INTEGER  Max program runtime.
  -v, --verbose          display verbose information.
  -vv                    display more verbose information.
  --debug                setup debug mode.
  --help                 Show this message and exit.

Commands:
  show-poc-info
```

## config
You can use the `-c` option to specify the configuration file, if not set, glimmer will use default config in glimmer/data/default_config.ini, you can copy it and change by yourself.

## parser
Support parsers
- file
- url
- python
- shodan
- zoomeye
- fofa
### file
example: `file://./url.txt`, `files://./poc.txt`
**if protocol is files, the result will be split by line and decode if encoded by base64, so you can generate multi targets / pocs.**
### url
example: `http://localhost`, `https://baidu.com`
### python
example: `python://./poc.py`, `pythons://./targets.py`
**if protocol is pythons, the result will be split by line and decode if encoded by base64, so you can generate multi targets / pocs.**
### shodan
example: `shodan://[key@]shodan.io/?q={query_str}[&max_page=1&limit=0]`

you can set shodan key in config
```
[shodan]
key = 
``` 
### zoomeye
example: `zoomeye://[key@]zoomeye.org/?q={query_str}[&max_page=1&resource=host]`

you can set zoomeye key in config
```
[zoomeye]
key = 
``` 
### fofa
example: `fofa://[email:key@]fofa.so/?q={query_str}[&max_page=1]`

you can set fofa email and key in config
```
[fofa]
email = 
key = 
``` 
## References
[pocsuite3](https://github.com/knownsec/pocsuite3)