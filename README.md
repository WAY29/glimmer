# Glimmer
Current version: 1.7.1

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

  Tips: {parser} are plugins in plugins/parser which parse user input by
  protocol and get data for poc and target, you can write yourself parser.

Options:
  -u, --url TEXT         Load targets from {parser}.
  -f, --file TEXT        Load targets from file and parse each line with
                         {parser}.

  -p, --poc TEXT         Load pocs from {parser}.
  -pf, --poc-file TEXT   Load pocs from file and parse each line with
                         {parser}.

  --pocs_path TEXT       User custom poc dir.
  --attack               set poc mode to attack mode, default is check mode.
  -o, --out TEXT         Use output plugins. default is console
  --plugins_path TEXT    User custom output plugin dir.
  --threads INTEGER      Number of threads
  -c, --config TEXT      Load config from a configuration toml file.
  -t, --timeout INTEGER  Max program runtime.
  -v, --verbose          display verbose information.
  -vv                    display more verbose information.
  --debug                setup debug mode.
  --help                 Show this message and exit.

Commands:
  search-poc     Search pocs by poc type / poc name / poc filename.
  show-poc-info  Show poc information by poc filename.
```

## config
You can use the `-c` option to specify the configuration file, if not set, glimmer will use default config in glimmer/data/default_config.ini, you can copy it and change by yourself.
```ini
[request.headers]
User-Agent = Glimmer

;[request.cookies]
;PHPSESSID = 

;[request.proxies]
; http_proxy = 
; https_proxy = 

[shodan]
key = 

[fofa]
email = 
key = 


[zoomeye]
key = 

[option]
# verbose is 1 / 0
verbose = 0
# very_verbose is 1 / 0
vv = 0
# attack is 1 / 0
attack = 0
# threads is int
threads = 10
# timeout is int
timeout = 300
# url is str and split by ,
; url = http://example.com
# file is str and split by ,
; file = url.txt,url2.txt
# poc is str and split by ,
; poc = demo/demo,demo/demo2
# poc_file is str and split by ,
; poc_file = poc.txt,poc2.txt
# pocs_path is str
; pocs_path = /home/user/glimmer/pocs
# plugins_path is str
; plugins_path = /home/user/glimmer/plugins
# out is str and split by ,
; out = console,table
```

## parser
Support parsers
- file
- url
- python
- shodan
- zoomeye
- fofa
- repo
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

### zoomeye
example: `zoomeye://[key@]zoomeye.org/?q={query_str}[&max_page=1&resource=host]`

### fofa
example: `fofa://[email:key@]fofa.so/?q={query_str}[&max_page=1]`


### repo
example: `repo://rce/netentsec/ngfw_rce`, `repo://rce/`(will load pocs from rce directory in offical repository)

you can load poc(s) from offical poc repository in gitee


## poc repository
[gitee/glimmer_pocs](https://gitee.com/guuest/glimmer_pocs)

## References
[pocsuite3](https://github.com/knownsec/pocsuite3)