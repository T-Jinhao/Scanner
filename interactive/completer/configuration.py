usemodule = [
    'burp',
    'scan',
    'domain',
    'port',
    'worker'
]

Workbench = {
    'main': ['help', 'usemodule', 'exit', 'main', 'set', 'info'],
    'burp': ['main', 'help', 'info', 'set', 'run', 'exit', 'usemodule', 'execute'],
    'domain': ['main', 'help', 'info', 'set', 'usemodule', 'exit', 'run', 'execute'],
    'scan': ['main', 'help', 'info', 'set', 'usemodule', 'exit', 'run', 'execute'],
    'port': ['main', 'help', 'info', 'set', 'usemodule', 'exit', 'run', 'execute'],
    'search': ['main', 'help', 'info', 'reset', 'set', 'usemodule', 'exit'],
    'worker': ['main', 'help', 'info', 'set', 'run', 'exit', 'usemodule']
}