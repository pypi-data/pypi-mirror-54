# What does this package do
Tail log files on your server and report by email if error occurs.

By default, the regex pattern was set for default uwsgi logs.

# Install
```
pip install tail_uwsgi_log
```

# Usage
```
tail_uwsgi_log -c your_config_filepath.ini
```

# Configs
The config file provides infomations needed to send an email and log-files to tail.

For example:
```ini
; section name startswith 'log' would be interpreted as logfile config
[log-myapp1]

; log file path
filepath = your_log_filepath

; wait_time for tail command, the thread will sleep and wait
; the wait_time should be small if the server is busy and generates log lines quickly
wait_time = 0.5

; the regex pattern to read the log line, the line doesn't match this regex will be recorded as innormal
pattern = 

; mail settings
mail_recipients = example1@example.com, example2@example.com

mail_host = smtp.qq.com
mail_port = 465
mail_sender = your_email_address
mail_password = your_password
```

To tail several log files at the same time, we could set several sections on config files, the section name should start with 'log'.

For mail settings, we could use a section named 'mail' to set default value. The default value will be used if there is no keyword in log section.

For example:
```ini
[log-myapp1]
filepath = your_log_filepath1
wait_time = 0.5
pattern = 
mail_recipients = example1@example.com, example2@example.com

[log-myapp2]
filepath = your_log_filepath2
wait_time = 1
pattern = 
mail_recipients = example3@example.com, example4@example.com

[mail]
mail_host = smtp.qq.com
mail_port = 465
mail_sender = your_email_address
mail_password = your_password
```

The default regex pattern to match the logline was for default uwsgi logs, which is:
```python
pattern = r'''\]\ (?P<ip>.*?)\ (.*)\ {.*?}\ \[(?P<datetime>.*?)\]\ (?P<request_method>POST|GET|DELETE|PUT|PATCH)\s
            (?P<request_uri>[^ ]*?)\ =>\ generated\ (?:.*?)\ in\ (?P<resp_msecs>\d+)\ msecs\s
            \(HTTP/[\d.]+\ (?P<resp_status>\d+)\)'''
```

The '**resp_status**' in the pattern is important, which will be used as a signal.

When the resp_status is **500**, an email will be sent with all innormal log lines recorded before.
