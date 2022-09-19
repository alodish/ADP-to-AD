Import-Module SimplySql

# Connect to DB
Open-MySqlConnection  -User "austin" -Password "password" -Database "employees"

#
$first = 'Valerie'
$last = 'Mckain'

# Store generic admin password
$password = ConvertTo-SecureString -String "Button99" -AsPlainText -Force

# Select necessary fields from patients table
# Unable to Select '*' due to conflict with datetime.
# Will fix in the future
$newEmp = Invoke-SqlQuery -Query ("SELECT pat_id, gurantor_id, extern_id1, first_name, last_name, middle_name, preferred_first_name, `
title, address1, address2, address3, city, state, zip_code, country, home_phone, work_phone, cell_phone, alternate_phone, email, universal_id `
FROM patients WHERE first_name = '{0}' AND last_name = '{1}'" -f $first, $last) 

# Find the row from patient_admin with a matching pat_id
$admin = Invoke-SqlQuery -Query ("SELECT employee_group, company_code, job_code, cost_center_code, supervisor_id `
FROM patient_admin WHERE pat_id = {0}" -f $newEmp.pat_id)

# Fix phone number formatting
$phFix = $newEmp.home_phone, $newEmp.work_phone, $newEmp.cell_phone, $newEmp.alternate_phone | Convert-String -Example "7178261069=(717)826-1069"

Write-Host $phFix

# Org placement happens after user creation. 
# Determine correct domain for new user based on company_code from patients table
# Comapny Codes
# 9JT = MIE
# 3EJ = NoMoreClipboard
# ZZ9 = Contractors
$org = `
if ($admin.company_code -eq "9JT") `
{ `
    "MIE" `
} `
elseif ($admin.company_code -eq "3EJ") `
{ `
    "NMC" `
} `
elseif ($admin.company_code -eq "ZZ9") `
{ `
    "Contractors" `
} 

Write-Host $org

# Use supervisor_id from patient_admin table to Select matching name from patients table
$mgr = Invoke-sqlQuery -Query ("SELECT first_name, last_name FROM patients WHERE pat_id = {0}" -f $admin.supervisor_id)

# Create New AD User with query data
# Note: -Path Indicates the organizational unit in which to create the new user
# -UserPrincipalName  ("{0}{1}@test.local" -f $newEmp.first_name[0].toLower(), $newEmp.last_name.toLower()) `
New-ADUser `
-Name ("{0} {1}" -f $newEmp.first_name, $newEmp.last_name) `
-UserPrincipalName $newEmp.gurantor_id `
-AccountPassword $password `
-ChangePasswordAtLogon $false `
-City $newEmp.city `
-Company $org `
-Country $newEmp.country `
-DisplayName $newEmp.gurantor_id `
-Description $admin.employee_group `
-Department $admin.employee_group `
-EmailAddress $newEmp.email `
-EmployeeNumber $newEmp.pat_id `
-GivenName $newEmp.first_name `
-HomePhone $phFix[0] `
-OfficePhone $phFix[1] `
-MobilePhone $phFix[2] `
-PostalCode $newEmp.zip_code `
-State $newEmp.state `
-StreetAddress ("{0}{1}{2}" -f $newEmp.address1, $newEmp.address2, $newEmp.address3) `
-Surname $newEmp.last_name `
-Title $newEmp.title `
-Path ("OU={0},DC=Test,DC=Local" -f $org)
