# Automation of Interactive Tests

## Developing Tests

I'm trying to minimize the amount of work one has to do to create and run test cases.
So, there are three main steps in automating tests using this framework. Note that 
I assume that the feature being tested works at least once, the time when the user
did their first tests.

1. **Manual Run**: Run tests manually. Do not use any such command that you would rather not if everything were to go as planned.
2. **Test config creation**:Copy the entire CLI sequences to a file. Filter and annotate the commands and responses and save the config file (.conf extension). Run scripts to convert the conf file into a JSON file for use in the framework.
3. **Create and run tests**: Write a test case method/new test suite.


### Script creation
The step #1 is a no-brainer. So, good luck with that. I'll briefly outline the other two steps with a small example:
Suppose the script to run is the following (this is a test for bug id 3602):

```
config
fru slot 1 sub-slot RTM expected-type XGBE-RTM
commit
top

router mpls ip ipv4 10.10.1.1
commit
top

interface physical 1/1/1 admin-status up
mac-address 00:16:3e:b5:18:4c
ipv4 address 10.10.1.1 prefix 24 address-advertise enable
commit
exit
mpls ip enable
mtu 1500
commit
top
do show mpls | nomore

router mpls static binding-ip ipv4 10.10.3.2 32 nexthop 10.10.2.2 out-interface phy-1-1-1 out-label 5002
commit
top

do show mpls | nomore
```

Here, we are configuring a static Ingress LSP and want to verify that everything goes on fine 
(and no binary crashes, which used to happen).
The bug was being seen after executing the last `do show mpls | nomore` command. So, what we want to test for is
_not getting a 'killed' message_.
Also, just for demonstration, we want to test it some time after configuring.

So, annotate the commands and responses as `command` and `success`:

>Please note that the paths inside parentheses for `[success]` are due to markdown rendering.

```
[command]config
[success]Entering configuration mode terminal

[command]fru slot 1 sub-slot RTM expected-type XGBE-RTM
[success] (config-fru-1/RTM)#

[command]commit
[success]Commit complete.

[command]top
[success] (config)#

[command]do show mpls | nomore
[success]MPLS Running Status: n/a

[command]router mpls ip ipv4 10.10.1.1
[success] (config)#

[command]commit
[success]Commit complete.

[command]top
[success] (config)#

[command]interface physical 1/1/1 admin-status up
[success] (config-if-phy-1-1-1)#

[command]mac-address 00:16:3e:b5:18:4c
[success] (config-if-phy-1-1-1)#

[command]ipv4 address 10.10.1.1 prefix 24 address-advertise enable
[success] (config-address-10.10.1.1)#

[command]commit
[success]Commit complete.

[command]exit
[success] (config-if-phy-1-1-1)#

[command]mpls ip enable
[success] (config-if-phy-1-1-1)#

[command]mtu 1500
[success] (config-if-phy-1-1-1)#

[command]commit
[success]Commit complete.

[command]top
[success] (config)#

[command]router mpls static binding-ip ipv4 10.10.3.2 32 nexthop 10.10.2.2 out-interface phy-1-1-1 out-label 5002
[success] (config)#

[command]commit
[success]Commit complete.

[command]top
[success] (config)#

{sleep=3}

[command]do show mpls | nomore
[success {regex=1}] (?!killed)
```

While most of it is literal string or string-fragment matching, regex is supported in the responses. To tell the framework not to literally interpret the response as string, use the additional flag `{regex=1}` in the annotation as in the last command `[success {regex=1}] (?!killed)`.

Commands wrapped inside curly braces will be interpreted by the framework and consumed locally. But only if they are not within a literal test command (things following `[command]` and `[success]`). So, `{sleep=3}` tells the framework to delay the execution of the next command by 3 seconds. Also, `sleep` is the only command we support for now. Adding support is not a big task, but we'd like to keep track of what the framework can do and what it cannot do.

The last statement `[success {regex=1}] (?!killed)` contains a _negative match_ regex pattern. It says, success is _not seeing 'killed'_ in the output stream. Regex will be more useful when putting up text fragments from multiline outputs, since we cannot put multiline outputs as expected responses here (yet).

So, say one expects to see static LSP programming and wants to validate that label programmed is correct and the LSP is operationally up, one might write something like:

`[success {regex=1}].*Label stack\s+: 4200.*Operational status : operStatusUp`

Finally, it may be required to manage more than one test sessions and execute commands
on them sequentially or pseudo-parallelly. For example, when configuring the interface above using
`interface physical 1/1/1 admin-status up` and `commit`, one might want to test if the
interface is indeed up in linux before proceeding further. In that case, the user may:

1. Exit the CLI, test in linux and enter CLI again.
2. Have a parallel session running.

I prefer the second option. To enable the use of multiple sessions to do many things (say, manage multiple DUTs in complex functional tests), add the session identifier in the command config as:

```
[command {tty=1}]interface physical 1/1/1 admin-status up
[success] (config-if-phy-1-1-1)#

[command {tty=1}]commit
[success]Commit complete.

[command {tty=2}]ifconfig phy-1-1-1
[success {regex=1}]phy-1-1-1:.*<UP,.*
```
Of course, this assumes that you've logged into the system on the session 2 as well. 
Since the initial steps on more than one session may be the same, one can specify
in the command to execute them on more than one session as:

```
[command {tty=1,2}]ssh root@192.168.111.82
[success]Are you sure you want to continue connecting (yes/no)?
[command {tty=1,2}]yes
...
```

>Note that if your raw scripts are one liners only, that is, the inputs and outputs are single line outputs, you could save some time by using `python ${SRC}/utils/annotate_script.py <file_name.txt>` which will annotate the odd numbered lines with `[command {tty=1}]` and even lines with `[success]`.

Finally, it is possible that some commands take a lot of time to execute. In those cases, one needs to explicitly specify that we expect a large timeout. For example, running `start_setup` on the target takes at least 8-9 minutse before we see the CLI and declare that the command execution was successful.
In such cases, one must specify in the command itself that a large timeout is expected as:

```
[command {tty=1}{timeout=600}]start_setup clean
```
This will tell the framework to wait for at 600 seconds before timing out and deeming the operation to be a failure.

### Script conversion
Lets say, your source is at location ${LOC} and file name is `test.conf`. Convert your `conf` to `json` with:

```
python ${LOC}/lib/utils/config_to_csv.py <path to conf file>/test.conf
python ${LOC}/lib/utils/csv_reader.py <path to conf file>/test.csv
```

This will produce an intermediate `test.csv` file and a final `test.json` file in the same path as your `test.conf` file.

I am following the file structure of keeping these files in 'conf', 'csv' and 'json' folders respectively.

## Writing Tests

You can augment an existing test suite or create a new one. That is mostly copy paste. For a barebones code, refer to

`${LOC}/tests/ssh_target/tests.py`

In case you are adding to an existing test suite, the skeletal code looks like:

```
    def test_a_new_test_case(self):
        #Set path to your script
        setup_file = "/path/to/json/file/"
        
        #Feed it to a test runner
        runner = Runner(files= [setup_file+"ssh_to_target.json"], 
                        logpath=self.folder)

        #Prepare the runner for testing the code
        runner.prepare()
        
        #Let it run
        runner.run()
        
        #Shutdown the runner
        runner.shutdown()
```

But, some work may need to be done in the `setUp` and `tearDown` methods too.
This could include SSHing into the target machine (or starting up an LXC) and
calling the startup scripts `start_setup clean` in `setUp` and `start_setup stop`
in `tearDown`. 

When any python unittest test case runs, `setUp` is called first, then the test 
case is executed, and `tearDown` is called finally. This happens for each test
case. So, every test case essentially runs from a clean slate as much as possible
unless the failing test case has left the system in a broken state that couldn't 
be cleaned up.

## Executing a set of tests:

In the folder where `test.py` is, run:

```
python test.py
```

This is suite specific.

If you want to run all of them from one place, then from the outermost folder, call:

```
python -m unittest discover
```

This will find all the python files that start with `test` and run them. Currently, this might not run very nicely due to system path settings. I'll fix it in due time.
