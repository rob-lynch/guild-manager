<#
    Synopsis: A quick powershell script for converting Monolith DKP output to a csv Django import_export can work with. 
    (https://www.curseforge.com/wow/addons/monolith-dkp)
    Example: .\ConvertData.ps1 -InputFile import.csv -RaidDate "2020-03-01"
#>

param (
    [parameter(mandatory)] [string] $InputFile, 
    [string] $OutputFile="raid_data.csv",
    [parameter(mandatory)] [ValidatePattern("\d{4}-\d{2}-\d{2}")] [string] $RaidDate
)


#Import the csv
$CsvImportObjectArray = Import-Csv -Path $InputFile

#Using a custom object array, collect and modify the data we plan to export
#The property names will be the headers in the file
$CsvExportObjectArray = @()
$CsvImportObjectArray | ForEach-Object $_ {
    $RecordObject = [PSCustomObject]@{
        raid_character = $_.player
        raid = $RaidDate
        id = ""
    }

    $CsvExportObjectArray += $recordObject
} 
Write-Output $CsvExportObjectArray

#Export the data to csv
$CsvExportObjectArray | Export-Csv -Path $OutputFile -NoTypeInformation -Encoding ASCII