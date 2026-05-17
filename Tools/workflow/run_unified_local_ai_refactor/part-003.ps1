# This file is dot-sourced by its parent launcher and delegates to split sections.
# Original content moved to part-003_sections to keep maintained scripts below the line budget.
$__IaCarminePartRoot = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
. (Join-Path $__IaCarminePartRoot "part-003_sections/section-001.ps1")
. (Join-Path $__IaCarminePartRoot "part-003_sections/section-002.ps1")
Remove-Variable -Name __IaCarminePartRoot -ErrorAction SilentlyContinue
