# Copyright 2017 LasLabs Inc.
# License Apache 2.0 (https://www.apache.org/licenses/LICENSE-2.0.html)

Import-Module ActiveDirectory


$SSH_KEY_ATTR = Read-Host 'SSH Key Attribute'
$upn = whoami /UPN
$username, $dn = $upn.split('@')
$user = Get-ADUser -Identity $username -Properties $SSH_KEY_ATTR
$keys = @();

foreach($k in $user.$SSH_KEY_ATTR){
    if($k -notlike '127.0.0.1*'){
        $keys += $k
    }
}

$ssh_host = Read-Host 'SSH Key Host (or * for global)'
$ssh_key = Read-Host 'SSH Public Key'
$keys += "$($ssh_host):$($ssh_key)"

Set-ADUser -Identity $username -replace @{$SSH_KEY_ATTR=$keys}
Write-Host "Successfully added SSH Public Key for host $ssh_host"
