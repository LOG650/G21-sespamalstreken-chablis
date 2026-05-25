# Bygger rapport.pdf fra rapport.md og slaar sammen med PDF-vedleggene.
# - Konverterer HTML figurblokker til native pandoc bilder med caption
# - Konverterer HTML tabelltekster til markdown tabell-captions
# - Bruker xelatex via pandoc med skriftstorrelse 12, linjeavstand 1.5, sidetall
# - Genererer auto-TOC med sidetall, ekskluderer forsiden fra TOC
# - Beregner totalt antall sider (rapport + vedlegg) og setter det paa forsiden
# - Merger til endelig rapport.pdf med pdfunite

$ErrorActionPreference = "Stop"

$reportDir = $PSScriptRoot
if (-not $reportDir) { $reportDir = (Get-Location).Path }

$src       = Join-Path $reportDir "rapport.md"
$work      = Join-Path $reportDir "rapport_processed.md"
$tex       = Join-Path $reportDir "rapport_processed.tex"
$pdf       = Join-Path $reportDir "rapport.pdf"
$hdr       = Join-Path $reportDir "rapport-header.tex"
$vedleggA  = Join-Path $reportDir "Vedlegg A - Everything You Need To Know About Marine Fuels.pdf"
$vedleggB  = Join-Path $reportDir "Vedlegg B - FuelEU Guidance Document for Shipping Companies.pdf"

function Get-PdfPageCount {
  param([string]$Path)
  $info = & pdfinfo $Path 2>$null
  $line = ($info | Select-String '^Pages:').ToString()
  return [int]($line.Split(':')[1].Trim())
}

function Invoke-RapportBuild {
  param([int]$TotalPages = 0)

  $content = Get-Content -Path $src -Raw -Encoding UTF8

  # 1) Konverter HTML figurblokker til native markdown bilder med caption
  $figRegex = [System.Text.RegularExpressions.Regex]::new(
    '<div\s+align="center">\s*<img\s+src="([^"]+)"\s+alt="([^"]*)"\s+width="([^"]+)">\s*<p\s+align="center"[^>]*><small><i>([^<]+)</i></small></p>\s*</div>',
    [System.Text.RegularExpressions.RegexOptions]::Singleline
  )
  $figEval = [System.Text.RegularExpressions.MatchEvaluator]{
    param($m)
    $imgsrc = [System.Uri]::UnescapeDataString($m.Groups[1].Value)
    $caption = $m.Groups[4].Value
    $width = $m.Groups[3].Value
    return "![{0}](<{1}>){{width={2}}}" -f $caption, $imgsrc, $width
  }
  $content = $figRegex.Replace($content, $figEval)

  # 2) Konverter HTML tabelltekster til pandoc tabell-captions
  $tabRegex = [System.Text.RegularExpressions.Regex]::new(
    '<p\s+align="center"[^>]*><small><i>(Tabell[^<]+)</i></small></p>',
    [System.Text.RegularExpressions.RegexOptions]::Singleline
  )
  $content = $tabRegex.Replace($content, ': $1')

  # 3) Bytt ut manuell TOC-bullet-liste med LaTeX \tocnotitle
  $nl = "`n"
  $tocRegex = [System.Text.RegularExpressions.Regex]::new(
    '(## Innholdsfortegnelse\s*\r?\n\r?\n)(?:- [^\r\n]+\r?\n)+',
    [System.Text.RegularExpressions.RegexOptions]::Singleline
  )
  $tocReplacement = '$1' + '\tocnotitle' + $nl + $nl
  $content = $tocRegex.Replace($content, $tocReplacement)

  # 4) Marker alle headinger foer "## 1.0 Innledning" som .unnumbered .unlisted
  $splitMarker = '## 1.0 Innledning'
  $splitIdx = $content.IndexOf($splitMarker)
  if ($splitIdx -lt 0) { throw "Fant ikke '$splitMarker' i rapport.md" }
  $frontMatter = $content.Substring(0, $splitIdx)
  $body = $content.Substring($splitIdx)
  $frontMatter = [System.Text.RegularExpressions.Regex]::Replace(
    $frontMatter,
    '(?m)^(#{1,3}\s+\S[^\r\n]*?)\s*$',
    '$1 {.unnumbered .unlisted}'
  )
  $content = $frontMatter + $body

  # 5) Fyll inn totalt antall sider paa forsiden naar TotalPages er angitt.
  #    Bruk [ \t]* (ikke \s*) for aa unngaa aa spise opp den blanke linjen
  #    mellom denne og "Molde, Innleveringsdato".
  if ($TotalPages -gt 0) {
    $content = [System.Text.RegularExpressions.Regex]::Replace(
      $content,
      '(\*\*Totalt antall sider inkludert forsiden:\*\*)[ \t]*(\r?\n)',
      ('$1 {0}$2' -f $TotalPages)
    )
  }

  Set-Content -Path $work -Value $content -Encoding UTF8 -NoNewline

  Write-Output "  Pandoc: markdown -> LaTeX"
  $pandocArgs = @(
    $work,
    "-V", "geometry:margin=2.5cm",
    "-V", "fontsize=12pt",
    "-V", "linestretch=1.5",
    "-V", "papersize=a4",
    "-V", "lang=nb-NO",
    "-V", "mainfont=Calibri",
    "-V", "monofont=Consolas",
    "-V", "colorlinks=true",
    "-V", "linkcolor=black",
    "-V", "urlcolor=blue",
    "-H", $hdr,
    "--standalone",
    "-o", $tex
  )
  & pandoc @pandocArgs
  if ($LASTEXITCODE -ne 0) { throw "pandoc avsluttet med feilkode $LASTEXITCODE" }

  $texName = [System.IO.Path]::GetFileName($tex)
  $texBase = [System.IO.Path]::GetFileNameWithoutExtension($tex)

  Push-Location $reportDir
  try {
    foreach ($pass in 1..3) {
      Write-Output "  xelatex pass $pass/3"
      cmd /c "xelatex -interaction=nonstopmode -halt-on-error `"$texName`" > nul 2>&1"
      if ($LASTEXITCODE -ne 0) {
        $log = Join-Path $reportDir ($texBase + ".log")
        if (Test-Path $log) {
          Write-Output "--- siste 30 linjer av $log ---"
          Get-Content $log -Tail 30
        }
        throw "xelatex pass $pass feilet med kode $LASTEXITCODE"
      }
    }
  } finally {
    Pop-Location
  }

  $generatedPdf = Join-Path $reportDir ($texBase + ".pdf")
  if (Test-Path $pdf) { Remove-Item $pdf -Force }
  Move-Item -Path $generatedPdf -Destination $pdf -Force

  foreach ($ext in @(".aux", ".log", ".out", ".toc", ".tex")) {
    $aux = Join-Path $reportDir ($texBase + $ext)
    if (Test-Path $aux) { Remove-Item $aux -Force }
  }
}

# === Pass 1: bygg rapporten uten total for aa maale body-sidetallet ===
# Sidetallet paa forsiden gjelder kun selve rapporten (forside + kapitler),
# IKKE de vedlagte PDF-ene som merges paa slutten.
Write-Output "[1/3] Bygger rapportkjernen (uten total paa forsiden)"
Invoke-RapportBuild
$bodyPages = Get-PdfPageCount $pdf
$pagesA    = Get-PdfPageCount $vedleggA
$pagesB    = Get-PdfPageCount $vedleggB
$mergedPages = $bodyPages + $pagesA + $pagesB
Write-Output ("       body={0}  vedleggA={1}  vedleggB={2}  merged-total={3}" -f $bodyPages,$pagesA,$pagesB,$mergedPages)

# === Pass 2: bygg paa nytt med body-sidetall (rapporten alene) paa forsiden ===
Write-Output "[2/3] Bygger paa nytt med 'Totalt antall sider'=$bodyPages paa forsiden"
Invoke-RapportBuild -TotalPages $bodyPages
$newBody = Get-PdfPageCount $pdf
if ($newBody -ne $bodyPages) {
  Write-Warning "Body-sidetall endret seg fra $bodyPages til $newBody. Justerer og bygger igjen."
  $bodyPages = $newBody
  $mergedPages = $bodyPages + $pagesA + $pagesB
  Invoke-RapportBuild -TotalPages $bodyPages
}

# === Pass 3: merge rapport + vedlegg A + vedlegg B ===
Write-Output "[3/3] Merger rapport.pdf + Vedlegg A + Vedlegg B"
$merged = Join-Path $reportDir "rapport_merged.pdf"
# Kjor pdfunite via cmd for aa unngaa at PowerShell pakker stderr som
# ErrorRecord (pdfunite skriver harmlose "Syntax Warning"-meldinger til stderr).
cmd /c "pdfunite `"$pdf`" `"$vedleggA`" `"$vedleggB`" `"$merged`" > nul 2>&1"
if ($LASTEXITCODE -ne 0) { throw "pdfunite feilet med kode $LASTEXITCODE" }
if (-not (Test-Path $merged)) { throw "pdfunite produserte ingen fil paa $merged" }
Move-Item -Path $merged -Destination $pdf -Force

# Opprydding
Remove-Item $work -Force -ErrorAction SilentlyContinue

$finalPages = Get-PdfPageCount $pdf
Write-Output ""
Write-Output "PDF generert: $pdf"
Write-Output ("Endelig sidetall (merget): {0}  (rapport={1} + vedleggA={2} + vedleggB={3})" -f $finalPages,$bodyPages,$pagesA,$pagesB)
Write-Output ("Forsiden viser 'Totalt antall sider inkludert forsiden: {0}' (kun rapportkroppen)" -f $bodyPages)
Write-Output ("Storrelse: {0:N0} bytes" -f (Get-Item $pdf).Length)
