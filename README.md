# Glimmer
Current version: 1.7.3

***A poc framework base on python***

## Requirements
- rich
- func_timeout
- requests
- click
- shodan
- zoomeye

## Install
### common
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
### docker
```bash
# start a glimmer docker
docker run --name glimmer -itd longlone/glimmer
# exec bash from docker 
docker exec -it glimmer bash
# in docker, run glimmer
glimmer --help

# or just use glimmer directly
docker run --rm -it longlone/glimmer:cli --help
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

## poc repository


## pocs
default offical pocs save into [gitee/glimmer_pocs](https://gitee.com/guuest/glimmer_pocs)
### write yourself poc
poc template in glimmer/pocs/_demo/demo.py

you can write yourself poc into glimmer/pocs/new_folder/demo_poc.py and load it by new_folder/demo_poc

or you can write yourself poc into anywhere the Internet can access, and load it by url parser

or you can write yourself poc into anywhere and load it by yourself parser

## plugin:parser
parser plugin used to parse the protocol to provide pocs or targets.

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

load pocs / targets from python, it will be executed in python and get stdout as pocs / targets

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

### repo
example: `repo://rce/netentsec/ngfw_rce`, `repo://rce/`(will load pocs from rce directory in offical repository)

you can load poc(s) from offical poc repository in gitee

## write yourself parser plugin
copy this template, edit and move it into glimmer/plugins/parser directory, rename it as you like.
```python
from glimmer.api import PluginParserBase, register_plugin, is_valid_pathname, base64_decode, check_if_base64


class Plugin(PluginParserBase):
    protocols = ["myfile", "myfiles"]

    def rule_check(self, module_path):
        """check if module_path start with protocols"""
        # self.protocol_check: check if protocol start with Plugin.protocols
        # is_valid_pathname: check if module_path is valid pathname
        return self.protocol_check(module_path) and is_valid_pathname(self.remove_protocol(module_path))

    def get_data(self, module_path):
        """get poc from module_path"""
        # get protocol from module_path
        protocol = self.get_protocol(module_path)
        try:
            # remove protocol
            module_path = self.remove_protocol(module_path)

            # open file 
            with open(module_path, "r") as f:
                result = f.read()
            
            # if protocols is myfiles
            if protocol == "myfiles":
                # split result by line
                result = result.split()
                # base64 decode result if is base64 encode
                result = [base64_decode(r) if check_if_base64(
                    r) else r for r in result]
                return result
            else:
                # return a result list
                return (result, )
        except Exception:
            return ()

# register plugin for glimmer
register_plugin(Plugin)
```

## plugin:output
output plugin used to show poc result.

Exist plugins
- console
- pure_text
- table
- text
### console
print result to console with color

### pure_text
write pure hit urls to ./pure_result.txt

### table
print result as table to console with color

### text

write pure result to ./text.txt

### result parameter
```python
result = {
            "url": url,       # target url
            "status": status, # spoc tatus, 0 if success else failed
            "msg": msg,       # poc message
            "hit_urls": [],   # hit urls
            "extra": {        # extra data, store as key-value dict
            }
        }
```

### write yourself output plugin
copy this template, edit and move it into glimmer/plugins/output directory, rename it as you like.
```python
from glimmer.api import PluginOutputBase, register_plugin, cprint, header
from threading import Lock

LOCK = Lock()

class Plugin(PluginOutputBase):
    def construct(self):
      """plugin construct, if you want to save as file, you can init file handler in this function."""
      ...
      # self._handler = open("result.txt", "w+")

    def handle(self, poc, result, **kwargs):
        """plugin handler, you can handle poc result in this function."""
        status = result.get('status', -1)
        text = result.get("url") + " "
        text += "success" if status == 0 else "failed"

        if not status:
            LOCK.acquire()
            self._handler.write(text)
            self._handler.flush()
            LOCK.release()

    def destruct(self):
        """plugin destruct, if you want to save as file, you can close file handler and print message in this function."""
        ...
        # self._handler.close()
        # del self._handler
        # cprint(header("Poc", "*", "Result save in ./result.txt"))


register_plugin(Plugin)
```

