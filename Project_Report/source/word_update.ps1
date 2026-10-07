param([string]$In, [string]$Out, [string]$Pdf)
$ErrorActionPreference = "Stop"
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open($In, $false, $false)
    $doc.Fields.Update() | Out-Null
    foreach ($t in $doc.TablesOfContents) { $t.Update() | Out-Null }
    $doc.Repaginate()
    foreach ($t in $doc.TablesOfContents) { $t.UpdatePageNumbers() | Out-Null }
    "TOC count: " + $doc.TablesOfContents.Count
    "Pages: " + $doc.ComputeStatistics(2)
    "Words: " + $doc.ComputeStatistics(0)
    $doc.SaveAs2($Out, 16)
    $doc.ExportAsFixedFormat($Pdf, 17)
    $doc.Close($false)
} finally {
    $word.Quit()
}
