$root = Split-Path -Parent $MyInvocation.MyCommand.Path
python (Join-Path $root "012 fase 2 - plan\generate_status.py")
