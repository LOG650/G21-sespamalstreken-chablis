$here = Split-Path -Parent $MyInvocation.MyCommand.Path
python (Join-Path $here "generate_status.py")
