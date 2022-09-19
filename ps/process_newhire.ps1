param ($file='C:\Users\test.user.TEST\Documents\new_notification.json')
$user = Get-Content $file -Raw | ConvertFrom-Json
$user = $user.worker

$password = ConvertTo-SecureString -String "Button99" -AsPlainText -Force

$name = if($user.person.legalName.nickName){
    $user.person.legalName.nickName + " " + $user.person.legalName.familyName1
}else{
    $user.person.legalName.givenName + " " + $user.person.legalName.familyName1
};

$testUser = Get-ADUser -Filter "Name -like '$name'"
$unp = $name.split(' ')[0][0].toString().toLower() + $name.split(' ')[1].toString().toLower()


if($testUser){
    Write-Host "User $name already exists"
} else {
    Write-Host "Creating new AD profile for $name"
    $group = $user.workAssignments[0].payrollGroupCode

    $org = if ($group -eq "9JT") {"MIE"} `
    elseif ($group -eq "3EJ") {"NMC"} `
    elseif ($group -eq "ZZ9") {"Contractors"}
    
    $phNum = $user.person.communication.mobiles.areaDialing.ToString() + $user.person.communication.mobiles.dialNumber.ToString()
    $phNum = $phNum | Convert-String -Example "7178261069=(717)826-1069" 

    New-ADUser `
    -Name $name `
    -UserPrincipalName ("{0}{1}" -f $unp, "@test.local") `
    -AccountPassword $password `
    -ChangePasswordAtLogon $false `
    -City $user.person.legalAddress.cityName `
    -Company $org `
    -Country $user.person.legalAddress.countryCode `
    -DisplayName $unp `
    -Description $user.workAssignments[0].homeOrganizationalUnits[0].nameCode.shortName `
    -Department $user.workAssignments[0].homeOrganizationalUnits[0].nameCode.shortName `
    -EmailAddress ("{0}{1}" -f $unp, "@mieweb.com") `
    -EmployeeNumber $user.associateOID `
    -GivenName $user.person.legalName.givenName `
    -OfficePhone $phNum `
    -PostalCode $user.person.legalAddress.postalCode `
    -State $user.person.legalAddress.countrySubdivisionLevel1.codeValue `
    -StreetAddress $user.person.legalAddress.lineOne `
    -Surname $user.person.legalName.familyName1 `
    -Title $user.workAssignments[0].jobTitle `
    -Path ("OU={0},DC=Test,DC=Local" -f $org) `
    -Manager ("{0} {1}" -f $user.workAssignments[0].reportsTo.reportsToWorkerName.givenName, $user.workAssignments[0].reportsTo.reportsToWorkerName.familyName1)
        
    Enable-ADAccount -Identity $name
}