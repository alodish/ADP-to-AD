const axios = require('axios').default;
const spawn = require('child_process').spawn;
const path = 'C:/Users/test.user.TEST/Documents/';
const fs = require('fs');
const readline = require('readline');
const question = 
`
Enter Selection:
GET: GET Next Notification
DEL: DELETE Most Recent Notification
QUIT:  
`;
const options = {'get': 'GET', 'del': 'DELETE'};

function askQuestion(query) {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
    });

    return new Promise(resolve => rl.question(query, ans => {
        rl.close();
        resolve(ans.toLowerCase());
    }))
}

function spawnChild(script, obj) {
    if(typeof obj === 'object') {
        child = spawn("powershell.exe",[`${script} -aoid ${obj[0]} -action ${obj[1]} -value ${obj[2]}`])
    } else {
        child = spawn("powershell.exe",[`${script} ${obj}`]);
    }
    child.stdout.on("data",function(data){
        console.log(String(data));
    });
    child.stderr.on("data",function(data){
        console.log(String(data));
    });
    child.on("exit",function(){
        console.log("Powershell script complete.");
    });
    child.stdin.end(); //end input
}

async function getNotification(MTHD) {
    const request = await axios({
        method: `${MTHD}`,
        url: 'http://192.168.1.252:5000/notifications'
    });
    return request.data
}

async function processNotification(notification, type) {
    var data = notification.data.output;
    switch(type) {
        case 'worker.legal-address.change':
            return {
                id: data.worker.associateOID,
                StreetAddress: data.worker. person. legalAddress. lineOne,
                City: data.worker.person.legalAddress.cityName,
                State: data.worker.person.legalAddress.countrySubdivisionLevel1.codeValue
            }
        case 'worker.legal-name.change':
            return {
                id: data.worker.associateOID,
                Surname: data.worker.person.legalName.familyName1
            }
        case 'worker.preferred-name.change':
            return {
                id: data.worker.associateOID,
                Name: data.worker.person.legalName.nickname
            }
        case 'worker.hire':
            return {
                newWorker: data
            }
        case 'worker.terminate':
            return {
                id: data.worker.associateOID,
                Terminate: null
            }
        case 'worker.reports-to.modify':
            return {
                id: data.worker.associateOID,
                Manager: data.worker.reportsTo.associateOID
            }
    }
}


async function main() {
    let ans = await askQuestion(question);
    if(ans !== 'quit') {
        var notification = await getNotification(options[ans]);
        console.log(notification);
    }
    if(typeof notification === 'object') {
        var data = await processNotification(notification, notification.eventNameCode.codeValue);
        for (const key of Object.keys(data)) {
            if(key === 'newWorker') {
                fs.writeFileSync(
                    `${path}new_notification.json`, 
                    JSON.stringify(data[key], indent=4)
                );
                try {
                    spawnChild(`${path}process_newhire.ps1`, `-file ${path}new_notification.json`);
                } catch (err) {
                    console.log("error adding new employee");
                    console.log(err);
                }
            } else if(key === 'id') {
                var aoid = data[key];
            } else {
                console.log(`
                    Initializing AD User Modification
                        -AssociateOID: ${aoid}
                        -Action: ${key}
                        -Parameter: ${data[key]}
                `);
                try {
                    spawnChild(`${path}modify_ad_user.ps1`, `-aoid ${aoid} -action ${key} -value ${data[key]}`)
                } catch(err) {
                    console.log(`error modifying employee with aoid: ${aoid}`);
                    console.log(err);
                }
            }
            if(key === Object.keys(data)[Object.keys(data).length -1]){
                await main();
            }
        }
    } else {
        console.log('Goodbye');
    }   
}

main();

