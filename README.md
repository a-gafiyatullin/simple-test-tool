# Simple Test Tool
A simple multi-stage multi-module testing tool.

[![Build Status](https://travis-ci.com/gafiyatullin-a/simple-test-tool.svg?branch=master)](https://travis-ci.com/gafiyatullin-a/simple-test-tool)
[![codecov](https://codecov.io/gh/gafiyatullin-a/simple-test-tool/branch/master/graph/badge.svg?token=OZEQC34LII)](https://codecov.io/gh/gafiyatullin-a/simple-test-tool)
## About:
Simple Test Tool (STT) is a high-level tool for building and testing of  multi-module projects.
STT requires user-defined scripts for some stages. It simply performs them in the right order
by taking into account dependencies between modules.

## How to use:

### Modules
<strong>Module</strong> is a container for Stages, Outputs and Dependencies.<br>
<strong>Outputs</strong> are files that are results of Module's Stages execution.<br>
<strong>Dependencies</strong> are files that are needed for Module's Stages execution and are produced by other Modules.<br>
<strong>Stages</strong> are processes of building and testing of the Module.


Attributes:
<ul>
<li><strong>Name</strong> - Module name.</li>
</ul>

Subtag:

<ul>
<li><strong>Outputs</strong></li>
Subtag:
<ul>
<li><strong>Output</strong> - output file info:</li>
Attributes:
<ul>
<li><strong>Name</strong> - output file name;</li>
<li><strong>Path</strong> - output file path.</li>
</ul>
</ul>

<li><strong>Dependencies</strong></li>
Subtag:
<ul>
<li><strong>Dependency</strong> - dependency file info:</li>
Attributes:
<ul>
<li><strong>Name</strong> - dependency file name;</li>
<li><strong>Path</strong> - dependency file path.</li>
</ul>
</ul>

<li><strong>Stages</strong></li>

</ul>

### Stages
There are 5 stages:
<ul>

<li><strong>Build</strong> - build source code;</li>
Attributes:
<ul>
<li><strong>Type</strong> - build system type:</li>
Possible values:
<ul>
<li><strong>Make;</strong></li>
<li><strong>CMake.</strong></li>
</ul>

<li><strong>Path</strong> - build system root directory.</li>
</ul>
Subtag:
<ul>
<li><strong>Target</strong> - build targets:</li>
<ul>
Attributes:
<li><strong>Name</strong> - build target name.</li>
</ul>
</ul>


<li><strong>VCS</strong> - update source code from remote repository;</li>
Attributes:
<ul>
<li><strong>Type</strong> - version control system type:</li>
Possible values:
<ul>
<li><strong>SVN;</strong></li>
<li><strong>Git.</strong></li>
</ul>
</ul>
Subtag:
<ul>
<li><strong>Path</strong> - version control system directories:</li>
Attributes:
<ul>
<li><strong>Path</strong> - path name.</li>
</ul>
</ul>


<li><strong>Test</strong> - test application using scripts;</li>
Subtag:
<ul>
<li><strong>Path</strong> - test script paths:</li>
Attributes:
<ul>
<li><strong>Path</strong> - path name.</li>
</ul>
</ul>


<li><strong>Commit</strong> - commit and push Outputs and Dependencies to remote repository;</li>
Attributes:
<ul>
<li><strong>Type</strong> - version control system type:</li>
Possible values:
<ul>
<li><strong>SVN;</strong></li>
<li><strong>Git.</strong></li>
</ul>
<li><strong>AutoCommitAndPush</strong> - perform auto commit and push.</li>
</ul>
Subtag:
<ul>
<li><strong>Path</strong> - version control system directories:</li>
Attributes:
<ul>
<li><strong>Path</strong> - path name.</li>
</ul>
</ul>


<li><strong>Notification</strong> - notify about STT execution process. Uses all logs from other Stages.</li>
Attributes:
<ul>
<li><strong>Type</strong> - service for notification:</li>
Possible values:
<ul>
<li><strong>Email;</strong></li>
<li><strong>Telegram.</strong></li>
</ul>
</ul>
if Email was chosen:
<ul>
<li><strong>EmailTo</strong> - destination Email address;</li>
<li><strong>EmailFrom</strong> - STT Email address;</li>
<li><strong>SmtpServerAddress</strong> - STT Email SMTP address;</li>
<li><strong>SmtpServerPort</strong> - STT Email SMTP port;</li>
<li><strong>Password</strong> - STT Email address password.</li>
</ul>
if Telegram was chosen:
<ul>
<li><strong>Token</strong> - bot token;</li>
<li><strong>ChatID</strong> - chat id.</li>
</ul>

</ul>

Also, all stages have attributes:
<ul>
<li><strong>LogEnable</strong> - write all execute statuses into log file;</li>
<li><strong>LogPath</strong> - path for log file;</li>
<li><strong>InterruptOnFail</strong> - interrupt execution of all stages if something went wrong(except Notification stage).</li>
</ul>
Log file name consists of current date, Module name and Stage name.


### Execution order
1. <strong>VCS;</strong>
2. <strong>Build;</strong>
3. <strong>Test;</strong>
4. <strong>Commit;</strong>
5. <strong>Notification.</strong>

None of Stages is necessarily.

### Input file example
```
<STT>
    <Module Name="A">
        <Dependencies>
            <Dependency Name = "B_file_or_dir" Path = "A/" />
            <Dependency Name = "C_file_or_dir" Path = "A/" />
        </Dependencies>

        <Outputs>
            <Output Name = "A_file_or_dir" Path = "A/" />
        </Outputs>

        <Stages>
            <Build Type = "CMake" Path = "A/" LogEnable = "On" LogPath = "A/" InterruptOnFail = "On" />

            <VCS Type = "Git" LogEnable = "On" LogPath = "A/" InterruptOnFail = "On">
                <Path Path = "A/" />
            </VCS>

            <Test LogEnable = "On" LogPath = "A" InterruptOnFail = "On">
                <Path Path = "A/tests/A_test_tool_1.sh" />
                <Path Path = "A/tests/A_test_tool_2.sh" />
            </Test>

            <Notification Type = "Email" EmailTo = "to@mail.com" EmailFrom = "from@mail.com"
                          SmtpServerAddress="smtp.mail.com" SmtpServerPort="587" Password="password"/>
        </Stages>
    </Module>

    <Module Name="B">
        <Dependencies>
            <Dependency Name = "C_file_or_dir" Path = "B/" />
        </Dependencies>

        <Outputs>
            <Output Name = "B_file_or_dir" Path = "B/" />
        </Outputs>

        <Stages>
            <Build Type = "Make" Path = "B/" LogEnable = "Off" InterruptOnFail = "On" />

            <VCS Type = "SVN" LogEnable = "On" LogPath = "B/" InterruptOnFail = "Off">
                <Path Path = "B/" />
            </VCS>

            <Test LogEnable = "Off" InterruptOnFail = "On">
                <Path Path = "B/tests/B_test_tool_1.sh" />
                <Path Path = "b/tests/B_test_tool_2.sh" />
            </Test>

            <Notification Type = "Telegram" Token = "token_string" ChatID = "12345678"/>
        </Stages>
    </Module>

    <Module Name="C">
        <Outputs>
            <Output Name = "C_file_or_dir" Path = "C/" />
        </Outputs>

        <Stages>
            <Build Type = "Make" Path = "C/" LogEnable = "Off" InterruptOnFail = "On" />
        </Stages>

        <Commit Type = "Git" LogEnable = "On" LogPath = "C/" InterruptOnFail = "Off" AutoCommitAndPush="Off">
                <Path Path="C/" />
        </Commit>
    </Module>
</STT>
```