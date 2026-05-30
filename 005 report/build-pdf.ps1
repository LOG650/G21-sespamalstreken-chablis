# Bygger rapport.pdf fra rapport.md og slaar sammen med PDF-vedleggene.
# - Konverterer HTML figurblokker til native pandoc bilder med caption
# - Konverterer HTML tabelltekster til markdown tabell-captions
# - Bruker xelatex via pandoc med skriftstorrelse 12, linjeavstand 1.5, sidetall
# - Genererer auto-TOC med sidetall, ekskluderer forsiden fra TOC
# - Beregner totalt antall sider (rapport + vedlegg) og setter det paa forsiden
# - Bygger Vedlegg D (modellkode) som egen PDF, paa lik linje med Vedlegg A og B
# - Bygger Vedlegg F (konfidensialitetsavtaler) ved aa slaa sammen to bilder og en PDF
# - Merger til endelig rapport.pdf med pdfunite

$ErrorActionPreference = "Stop"

$reportDir = $PSScriptRoot
if (-not $reportDir) { $reportDir = (Get-Location).Path }

$src       = Join-Path $reportDir "rapport.md"
$work      = Join-Path $reportDir "rapport_processed.md"
$tex       = Join-Path $reportDir "rapport_processed.tex"
$pdf       = Join-Path $reportDir "rapport.pdf"
$hdr       = Join-Path $reportDir "rapport-header.tex"
$vedleggA   = Join-Path $reportDir "Vedlegg A - Everything You Need To Know About Marine Fuels.pdf"
$vedleggB   = Join-Path $reportDir "Vedlegg B - FuelEU Guidance Document for Shipping Companies.pdf"
$vedleggDmd = Join-Path $reportDir "Vedlegg D - Modellkode.md"
$vedleggD   = Join-Path $reportDir "Vedlegg D - Modellkode.pdf"
$vedleggE   = Join-Path $reportDir "Vedlegg E - ki-erklering-norsk---himolde.pdf"
$vedleggF   = Join-Path $reportDir "Vedlegg F - Konfidensialitetsavtaler.pdf"

function Get-PdfPageCount {
  param([string]$Path)
  $info = & pdfinfo $Path 2>$null
  $line = ($info | Select-String '^Pages:').ToString()
  return [int]($line.Split(':')[1].Trim())
}

function Invoke-RapportBuild {
  param([int]$TotalPages = 0, [int]$MergedPages = 0)

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

  # 2) Konverter HTML tabelltekster til en sentrert, liten kursiv linje UNDER
  #    tabellen (LOG650-praksis, jf. kompendiet 6.2), i stedet for en pandoc
  #    tabell-caption som xelatex ellers plasserer paa toppen av tabellen.
  $tabRegex = [System.Text.RegularExpressions.Regex]::new(
    '<p\s+align="center"[^>]*><small><i>(Tabell[^<]+)</i></small></p>',
    [System.Text.RegularExpressions.RegexOptions]::Singleline
  )
  $content = $tabRegex.Replace($content, '\begin{center}{\small\itshape $1}\end{center}')

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

  # 5) Fyll inn sidetall paa forsiden via plassholdere i titlepage-blokken.
  #    ZZBODYPAGESZZ  = sidetall for rapportkroppen (forside + kapitler)
  #    ZZTOTALPAGESZZ = sidetall for hele dokumentet inkludert vedlegg
  #    Plassholderne er understrek-frie slik at de ikke trigger LaTeX-mattemodus
  #    dersom de naar xelatex urort i pass 1 (foer tallene er kjent).
  if ($TotalPages -gt 0) {
    $content = $content -replace 'ZZBODYPAGESZZ', $TotalPages
  }
  if ($MergedPages -gt 0) {
    $content = $content -replace 'ZZTOTALPAGESZZ', $MergedPages
  }

  Set-Content -Path $work -Value $content -Encoding UTF8 -NoNewline

  Write-Output "  Pandoc: markdown -> LaTeX"
  $pandocArgs = @(
    $work,
    "--from=markdown+autolink_bare_uris",
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

  # Sett xcolor sin table-opsjon FOER pandoc-malen laster xcolor, slik at
  # \rowcolors (lysegraa annenhver tabellrad, jf. rapport-header.tex) er
  # definert. Settes rett etter \documentclass i den genererte .tex-filen.
  $texSrc = Get-Content -Path $tex -Raw -Encoding UTF8
  $texSrc = $texSrc -replace '(\\documentclass(?:\[[^\]]*\])?\{[^}]*\})', "`$1`n\PassOptionsToPackage{table}{xcolor}"
  Set-Content -Path $tex -Value $texSrc -Encoding UTF8 -NoNewline

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

function Invoke-VedleggDBuild {
  # Bygger Vedlegg D (modellkode) som egen PDF paa lik linje med Vedlegg A og B.
  # Holdes utenfor rapportkroppen og merges paa slutten. Bruker samme skrift,
  # marg og header (fvextra for linjebryting av kodeblokker) som rapporten.
  if (-not (Test-Path $vedleggDmd)) { throw "Fant ikke $vedleggDmd" }

  Write-Output "  Pandoc: Vedlegg D markdown -> PDF"
  $vdArgs = @(
    $vedleggDmd,
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
    "--pdf-engine=xelatex",
    "--standalone",
    "-o", $vedleggD
  )
  & pandoc @vdArgs
  if ($LASTEXITCODE -ne 0) { throw "pandoc (Vedlegg D) avsluttet med feilkode $LASTEXITCODE" }
}

function Invoke-VedleggFBuild {
  # Slaar sammen de tre konfidensialitetsavtalene til ett PDF-vedlegg (Vedlegg F):
  #   1) HiMolde (jpg)  2) Odfjell_E (png)  3) Odfjell_K (allerede PDF)
  # De to bildene legges sentrert paa hver sin fulle A4-side via xelatex, og
  # K-avtalen (PDF) merges bakerst. Begge bildene er staaende uten EXIF-rotasjon.
  $imgHiMolde  = Join-Path $reportDir "Confidentiality agreement, HiMolde.jpg"
  $imgOdfjellE = Join-Path $reportDir "Confidentiality agreement, Odfjell_E.png"
  $pdfOdfjellK = Join-Path $reportDir "confidentiality agreement, odfjell, K.pdf"
  foreach ($f in @($imgHiMolde, $imgOdfjellE, $pdfOdfjellK)) {
    if (-not (Test-Path $f)) { throw "Fant ikke $f" }
  }

  # Kopier bildene til trygge midlertidige filnavn (uten mellomrom/komma) som
  # \includegraphics handterer problemfritt.
  $tmpImg1 = Join-Path $reportDir "vf_img1.jpg"
  $tmpImg2 = Join-Path $reportDir "vf_img2.png"
  Copy-Item $imgHiMolde  $tmpImg1 -Force
  Copy-Item $imgOdfjellE $tmpImg2 -Force

  $vfTex = Join-Path $reportDir "vf_images.tex"
  $texContent = @'
\documentclass[a4paper,12pt]{article}
\usepackage[margin=1.5cm]{geometry}
\usepackage{graphicx}
\pagestyle{empty}
\setlength{\parindent}{0pt}
\begin{document}
\begin{center}
\includegraphics[width=\textwidth,height=\textheight,keepaspectratio]{vf_img1.jpg}
\end{center}
\clearpage
\begin{center}
\includegraphics[width=\textwidth,height=\textheight,keepaspectratio]{vf_img2.png}
\end{center}
\end{document}
'@
  Set-Content -Path $vfTex -Value $texContent -Encoding UTF8

  Write-Output "  xelatex: Vedlegg F bilder -> PDF"
  Push-Location $reportDir
  try {
    cmd /c "xelatex -interaction=nonstopmode -halt-on-error `"vf_images.tex`" > nul 2>&1"
    if ($LASTEXITCODE -ne 0) { throw "xelatex (Vedlegg F bilder) feilet med kode $LASTEXITCODE" }
  } finally {
    Pop-Location
  }

  $vfImagesPdf = Join-Path $reportDir "vf_images.pdf"
  Write-Output "  pdfunite: bilder + Odfjell K -> Vedlegg F"
  cmd /c "pdfunite `"$vfImagesPdf`" `"$pdfOdfjellK`" `"$vedleggF`" > nul 2>&1"
  if ($LASTEXITCODE -ne 0) { throw "pdfunite (Vedlegg F) feilet med kode $LASTEXITCODE" }

  foreach ($ext in @(".aux", ".log", ".tex", ".pdf")) {
    $aux = Join-Path $reportDir ("vf_images" + $ext)
    if (Test-Path $aux) { Remove-Item $aux -Force }
  }
  Remove-Item $tmpImg1 -Force -ErrorAction SilentlyContinue
  Remove-Item $tmpImg2 -Force -ErrorAction SilentlyContinue
}

# === Pass 1: bygg rapporten uten total for aa maale body-sidetallet ===
# Sidetallet paa forsiden gjelder kun selve rapporten (forside + kapitler),
# IKKE de vedlagte PDF-ene som merges paa slutten.
Write-Output "[1/3] Bygger rapportkjernen (uten total paa forsiden) + Vedlegg D + Vedlegg F"
Invoke-RapportBuild
Invoke-VedleggDBuild
# Vedlegg F bygges fra konfidensielle kildebilder som ikke alltid er sjekket ut.
# Mangler bildene, men finnes den ferdige PDF-en, gjenbrukes den i stedet for aa feile.
if (Test-Path (Join-Path $reportDir "Confidentiality agreement, HiMolde.jpg")) {
  Invoke-VedleggFBuild
} elseif (Test-Path $vedleggF) {
  Write-Output "  Hopper over Vedlegg F-bygg (kildebilder mangler); bruker eksisterende $vedleggF"
} else {
  throw "Mangler bade kildebilder og ferdig Vedlegg F-PDF"
}
$bodyPages = Get-PdfPageCount $pdf
$pagesA    = Get-PdfPageCount $vedleggA
$pagesB    = Get-PdfPageCount $vedleggB
$pagesD    = Get-PdfPageCount $vedleggD
$pagesE    = Get-PdfPageCount $vedleggE
$pagesF    = Get-PdfPageCount $vedleggF
$mergedPages = $bodyPages + $pagesA + $pagesB + $pagesD + $pagesE + $pagesF
Write-Output ("       body={0}  vedleggA={1}  vedleggB={2}  vedleggD={3}  vedleggE={4}  vedleggF={5}  merged-total={6}" -f $bodyPages,$pagesA,$pagesB,$pagesD,$pagesE,$pagesF,$mergedPages)

# === Pass 2: bygg paa nytt med body-sidetall (rapporten alene) paa forsiden ===
Write-Output "[2/3] Bygger paa nytt med 'Totalt antall sider'=$bodyPages paa forsiden"
Invoke-RapportBuild -TotalPages $bodyPages -MergedPages $mergedPages
$newBody = Get-PdfPageCount $pdf
if ($newBody -ne $bodyPages) {
  Write-Warning "Body-sidetall endret seg fra $bodyPages til $newBody. Justerer og bygger igjen."
  $bodyPages = $newBody
  $mergedPages = $bodyPages + $pagesA + $pagesB + $pagesD + $pagesE + $pagesF
  Invoke-RapportBuild -TotalPages $bodyPages -MergedPages $mergedPages
}

# === Pass 3: merge rapport + vedlegg A + vedlegg B + vedlegg D + vedlegg E + vedlegg F ===
Write-Output "[3/3] Merger rapport.pdf + Vedlegg A + Vedlegg B + Vedlegg D + Vedlegg E + Vedlegg F"
$merged = Join-Path $reportDir "rapport_merged.pdf"
# Kjor pdfunite via cmd for aa unngaa at PowerShell pakker stderr som
# ErrorRecord (pdfunite skriver harmlose "Syntax Warning"-meldinger til stderr).
cmd /c "pdfunite `"$pdf`" `"$vedleggA`" `"$vedleggB`" `"$vedleggD`" `"$vedleggE`" `"$vedleggF`" `"$merged`" > nul 2>&1"
if ($LASTEXITCODE -ne 0) { throw "pdfunite feilet med kode $LASTEXITCODE" }
if (-not (Test-Path $merged)) { throw "pdfunite produserte ingen fil paa $merged" }
Move-Item -Path $merged -Destination $pdf -Force

# Opprydding
Remove-Item $work -Force -ErrorAction SilentlyContinue

$finalPages = Get-PdfPageCount $pdf
Write-Output ""
Write-Output "PDF generert: $pdf"
Write-Output ("Endelig sidetall (merget): {0}  (rapport={1} + vedleggA={2} + vedleggB={3} + vedleggD={4} + vedleggE={5} + vedleggF={6})" -f $finalPages,$bodyPages,$pagesA,$pagesB,$pagesD,$pagesE,$pagesF)
Write-Output ("Forsiden viser 'Totalt antall sider inkludert forsiden: {0}' (kun rapportkroppen)" -f $bodyPages)
Write-Output ("Storrelse: {0:N0} bytes" -f (Get-Item $pdf).Length)
