# Contribute to the Owner
# print text file
$contributionPath = './data/contribution'
$srcPath1 = './data/*.pak'
$srcPath2 = './data/*.sig'
$pathFile = './path.txt'

$vngFile1 = 'VNGLogo-WindowsClient.sig'
$vngFile2 = 'VNGLogo-WindowsClient.pak'

function ContributionPrint {
    param(
        [string]$path
    )
    if (!(Test-Path $path)){
        Write-Error "Introduction file not found"
    } else {
        Get-Content $path
        ForEach-Object {
            Write-Output $_
        }
    }
    Write-Output "Do you wish to continue? (Y/N - Y is default)"
    $signal = Read-Host
    while ($signal -ne 'Y' -and $signal -ne 'N' -and $signal -ne 'y' -and $signal -ne 'n' -and $signal -ne '') {
        Write-Output "Invalid input, please enter Y or N"
        $signal = Read-Host
    }
    if ($signal -eq 'N' -or $signal -eq 'n'){
        Write-Output "Thank you for using the script. L11tled1no."
        exit
    }
}

function isDataExist {
    param(
        [string]$Path1, 
        [string]$Path2
    )
    if (!(Test-Path $Path1) -or !(Test-Path $srcPath2)){
        Write-Error "Data is missing, please download the zip again"
    }
}

function isPathExist {
    param(
        [string]$path
    )
    # Check if the path.txt file exists
    if (!(Test-Path $path)) {
        Write-Error "Path file not found"
    } else {
        # Read the path.txt file and get the path
        $destinationPath = Get-Content $path | ForEach-Object { $_.Trim() }
        
        # Check if the destination path exists
        if (!(Test-Path $destinationPath)) {
            Write-Error "Destination path not found, please check the path.txt file"
        } else {
            # Write-Output "Destination path: $destinationPath"
            $concatPath1 = $destinationPath + '\' + $vngFile1
            $concatPath2 = $destinationPath + '\' + $vngFile2
            return @($destinationPath, $concatPath1, $concatPath2)
        }
    }
}

function copyFiles {
    param(
        [string]$srcPath1,
        [string]$srcPath2,
        [string]$destinationPath
    )
    Copy-Item -Path $srcPath1 -Destination $destinationPath
    Copy-Item -Path $srcPath2 -Destination $destinationPath
    Write-Output "Copy files successfully"

}

function removeFiles {
    param(
        [string]$concatPath1,
        [string]$concatPath2
    )
    if (Test-Path $concatPath1) {
        Remove-Item $concatPath1
        Write-Output "Remove $vngFile1 successfully"
    } else {
        Write-Output "File $vngFile1 not found, does not need to remove"
    }
    if (Test-Path $concatPath2) {
        Remove-Item $concatPath2
        Write-Output "Remove $vngFile2 successfully"
    }
    else {
        Write-Output "File $vngFile2 not found, does not need to remove"
    }
}
function main {
    ContributionPrint $contributionPath
    isDataExist $srcPath1 $srcPath2
    $paths = isPathExist $pathFile
    
    copyFiles $srcPath1 $srcPath2 $paths[0]
    removeFiles $paths[1] $paths[2]
    Pause
}

main
