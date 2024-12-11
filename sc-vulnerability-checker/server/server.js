var Web3 = require('web3');
var util = require('ethereumjs-util');
var tx = require('ethereumjs-tx');
var lightwallet = require('eth-lightwallet');
var fs = require('fs');
var shell = require('shelljs');
var txutils = lightwallet.txutils;


var web3 = new Web3(
    new Web3.providers.HttpProvider('https://rinkeby.infura.io')
);
var address = '0xD1327ffe8765732Ff675d7B533f7AAD93053739b';
var key = '609378169defc198fd60738d298e69840b78e721e8b4a15cc45e95e142bc2a9b';

var bytecode = '606060405234156200001057600080fd5b620f4240600360003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002081905550620f42406000819055506040805190810160405280601681526020017f4b6f6f6b6d696e20536563757269747920546f6b656e0000000000000000000081525060079080519060200190620000ae92919062000170565b506012600860006101000a81548160ff021916908360ff1602179055506040805190810160405280600381526020017f4b53540000000000000000000000000000000000000000000000000000000000815250600990805190602001906200011892919062000170565b5033600a60006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550600060018190555060006002819055506200021f565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f10620001b357805160ff1916838001178555620001e4565b82800160010185558215620001e4579182015b82811115620001e3578251825591602001919060010190620001c6565b5b509050620001f39190620001f7565b5090565b6200021c91905b8082111562000218576000816000905550600101620001fe565b5090565b90565b6116bf806200022f6000396000f30060606040526004361061013e576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff168063044215c61461014857806306fdde03146101ab578063095ea7b31461023957806316f66e551461029357806318160ddd146102bc57806323b872dd146102e557806327e235e31461035e5780632a2a3284146103ab578063313ce567146103d4578063446a37e0146104035780635c65816514610458578063664e9704146104c457806370a08231146104ed57806378a895671461053a5780638da5cb5b14610563578063933e16af146105b857806395d89b41146106095780639f181b5e14610697578063a9059cbb146106c0578063b44272631461071a578063baf8b45914610724578063c948e47b14610779578063dc369a66146107d7578063dd62ed3e1461083a575b6101466108a6565b005b341561015357600080fd5b61016960048080359060200190919050506109e2565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b34156101b657600080fd5b6101be610a15565b6040518080602001828103825283818151815260200191508051906020019080838360005b838110156101fe5780820151818401526020810190506101e3565b50505050905090810190601f16801561022b5780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b341561024457600080fd5b610279600480803573ffffffffffffffffffffffffffffffffffffffff16906020019091908035906020019091905050610ab3565b604051808215151515815260200191505060405180910390f35b341561029e57600080fd5b6102a6610ba5565b6040518082815260200191505060405180910390f35b34156102c757600080fd5b6102cf610bab565b6040518082815260200191505060405180910390f35b34156102f057600080fd5b610344600480803573ffffffffffffffffffffffffffffffffffffffff1690602001909190803573ffffffffffffffffffffffffffffffffffffffff16906020019091908035906020019091905050610bb1565b604051808215151515815260200191505060405180910390f35b341561036957600080fd5b610395600480803573ffffffffffffffffffffffffffffffffffffffff16906020019091905050610f6c565b6040518082815260200191505060405180910390f35b34156103b657600080fd5b6103be610f84565b6040518082815260200191505060405180910390f35b34156103df57600080fd5b6103e7610f8e565b604051808260ff1660ff16815260200191505060405180910390f35b341561040e57600080fd5b61043a600480803573ffffffffffffffffffffffffffffffffffffffff16906020019091905050610fa1565b60405180826000191660001916815260200191505060405180910390f35b341561046357600080fd5b6104ae600480803573ffffffffffffffffffffffffffffffffffffffff1690602001909190803573ffffffffffffffffffffffffffffffffffffffff16906020019091905050610fea565b6040518082815260200191505060405180910390f35b34156104cf57600080fd5b6104d761100f565b6040518082815260200191505060405180910390f35b34156104f857600080fd5b610524600480803573ffffffffffffffffffffffffffffffffffffffff16906020019091905050611015565b6040518082815260200191505060405180910390f35b341561054557600080fd5b61054d61105e565b6040518082815260200191505060405180910390f35b341561056e57600080fd5b610576611068565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b34156105c357600080fd5b6105ef600480803573ffffffffffffffffffffffffffffffffffffffff1690602001909190505061108e565b604051808215151515815260200191505060405180910390f35b341561061457600080fd5b61061c6111e5565b6040518080602001828103825283818151815260200191508051906020019080838360005b8381101561065c578082015181840152602081019050610641565b50505050905090810190601f1680156106895780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b34156106a257600080fd5b6106aa611283565b6040518082815260200191505060405180910390f35b34156106cb57600080fd5b610700600480803573ffffffffffffffffffffffffffffffffffffffff16906020019091908035906020019091905050611289565b604051808215151515815260200191505060405180910390f35b6107226108a6565b005b341561072f57600080fd5b61075b600480803573ffffffffffffffffffffffffffffffffffffffff1690602001909190505061147e565b60405180826000191660001916815260200191505060405180910390f35b341561078457600080fd5b6107bd600480803573ffffffffffffffffffffffffffffffffffffffff1690602001909190803560001916906020019091905050611496565b604051808215151515815260200191505060405180910390f35b34156107e257600080fd5b6107f86004808035906020019091905050611562565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b341561084557600080fd5b610890600480803573ffffffffffffffffffffffffffffffffffffffff1690602001909190803573ffffffffffffffffffffffffffffffffffffffff1690602001909190505061159f565b6040518082815260200191505060405180910390f35b600080341115156108b657600080fd5b6108cb61c3503461162690919063ffffffff16565b905061091f81600360003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205461165e90919063ffffffff16565b600360003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055506109778160005461165e90919063ffffffff16565b600081905550600a60009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff166108fc349081150290604051600060405180830381858888f1935050505015156109df57600080fd5b50565b60056020528060005260406000206000915054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b60078054600181600116156101000203166002900480601f016020809104026020016040519081016040528092919081815260200182805460018160011615610100020316600290048015610aab5780601f10610a8057610100808354040283529160200191610aab565b820191906000526020600020905b815481529060010190602001808311610a8e57829003601f168201915b505050505081565b600081600460003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055508273ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925846040518082815260200191505060405180910390a36001905092915050565b60025481565b60005481565b600080600460008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054905082600360008773ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205410158015610c825750828110155b8015610c8e5750600083115b1515610c9957600080fd5b610ceb83600360008773ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205461165e90919063ffffffff16565b600360008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002081905550610d8083600360008873ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205461167a90919063ffffffff16565b600360008773ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055507fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff811015610efb57610e7a83600460008873ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205461167a90919063ffffffff16565b600460008773ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055505b8373ffffffffffffffffffffffffffffffffffffffff168573ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef856040518082815260200191505060405180910390a360019150509392505050565b60036020528060005260406000206000915090505481565b6000600254905090565b600860009054906101000a900460ff1681565b6000600660008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020549050919050565b6004602052816000526040600020602052806000526040600020600091509150505481565b61c35081565b6000600360008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020549050919050565b6000600154905090565b600a60009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b6000806110ba6002546110ac6001805461165e90919063ffffffff16565b61167a90919063ffffffff16565b90506110d16001805461165e90919063ffffffff16565b6001819055508260056000600154815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555061117d81600360003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205461165e90919063ffffffff16565b600360003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055506111d58160005461165e90919063ffffffff16565b6000819055506001915050919050565b60098054600181600116156101000203166002900480601f01602080910402602001604051908101604052809291908181526020018280546001816001161561010002031660029004801561127b5780601f106112505761010080835404028352916020019161127b565b820191906000526020600020905b81548152906001019060200180831161125e57829003601f168201915b505050505081565b60015481565b600081600360003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054101580156112da5750600082115b15156112e557600080fd5b61133782600360003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205461167a90919063ffffffff16565b600360003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055506113cc82600360008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205461165e90919063ffffffff16565b600360008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055508273ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef846040518082815260200191505060405180910390a36001905092915050565b60066020528060005260406000206000915090505481565b6000600a60009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff161415156114f457600080fd5b81600660008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000208160001916905550611552600160025461165e90919063ffffffff16565b6002819055506001905092915050565b60006005600083815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff169050919050565b6000600460008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054905092915050565b6000808314156116395760009050611658565b818302905081838281151561164a57fe5b0414151561165457fe5b8090505b92915050565b6000818301905082811015151561167157fe5b80905092915050565b600082821115151561168857fe5b8183039050929150505600a165627a7a72305820f9400e70c5d55232490f8a03d50d6560226d93e8c7d40e363a5f835b4f18a76b0029';
var interface = [{"anonymous":false,"inputs":[{"indexed":true,"name":"_owner","type":"address"},{"indexed":true,"name":"_spender","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Approval","type":"event"},{"constant":false,"inputs":[{"name":"_token","type":"address"}],"name":"analysis","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"createTokens","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_from","type":"address"},{"indexed":true,"name":"_to","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":false,"inputs":[{"name":"_token","type":"address"},{"name":"_result","type":"bytes32"}],"name":"setResult","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"allowed","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balances","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_token","type":"address"}],"name":"getResult","outputs":[{"name":"_token_result","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"num","type":"uint256"}],"name":"getSmartContract","outputs":[{"name":"token_address","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getTokenCount","outputs":[{"name":"token_count","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getTokenDoneCount","outputs":[{"name":"token_done_count","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"RATE","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"token","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"token_result","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"tokenCount","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"tokenDone","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}];

var myContract = web3.eth.contract(interface);
var contractAddress = '0x34799d1600179a4f56c7074bbc15382a27f8d160';
var myContractInstance = myContract.at(contractAddress);

function sendRaw(rawTx) {
    var privateKey = new Buffer(key, 'hex');
    var transaction = new tx(rawTx);
    transaction.sign(privateKey);
    var serializedTx = transaction.serialize().toString('hex');
    web3.eth.sendRawTransaction(
    '0x' + serializedTx, function(err, result) {
        if(err) {
            console.log(err);
        } else {
            console.log(result);
        }
    });
}

var txOptions = {
    nonce: web3.toHex(web3.eth.getTransactionCount(address)),
    gasLimit: web3.toHex(800000),
    gasPrice: web3.toHex(20000000000),
    to: contractAddress
}

// Web3 examples
// var rawTx = txutils.functionTx(interface, 'analysis', ['0x005'], txOptions);
// sendRaw(rawTx);
// var result = myContractInstance.getTokenCount();
// console.log(result)

var getTokenCount = parseInt(myContractInstance.getTokenCount());
var getTokenDoneCount = parseInt(myContractInstance.getTokenDoneCount());

while((getTokenCount-getTokenDoneCount) != 0) {
    getTokenDoneCount = getTokenDoneCount + 1;
    var result_string = '';
    var contract_address = myContractInstance.token(getTokenDoneCount);

    try{
        var code = String(web3.eth.getCode(contract_address));
    }
    catch(err){
        var output = "WrongAddress";
        fs.writeFileSync('./output'+String(getTokenDoneCount)+'.txt', output, function(err){
            if(err) {
                return console.log(err);
            }
        });
        continue;
    }
    fs.writeFileSync('./test.bin', code.substring(2), function(err){
        if(err) {
            return console.log(err);
        }
    });

    try{
        var _output = shell.exec('sudo docker run -v /home/learnitdeep/smartcontract-security-checker/server:/server --name test luongnguyen/oyente /bin/bash -c "cd oyente; python oyente.py -s /server/test.bin -b"', {async:false});
        var output = _output.stderr;

        if (shell.exec('sudo docker rm test').code !== 0) {
            shell.echo('Error: Git commit failed');
            shell.exit(1);
        }
    }
    catch(err){
        var _output = "error1";
        var output = _output;
    }

    try{
        _output = shell.exec('sudo docker run --name test mythril /bin/bash -c "myth -x -a '+String(contract_address)+' --rpc infura-rinkeby --max-depth 4"', {async:false});
        output = output + _output.stdout;
        console.log(output);

        if (shell.exec('sudo docker rm test').code !== 0) {
            shell.echo('Error: Git commit failed');
            shell.exit(1);
        }
    }
    catch(err){
        output = output + "error2";
    }
    fs.writeFileSync('./output'+String(getTokenDoneCount)+'.txt', output, function(err){
        if(err) {
            return console.log(err);
        }
    });
    if(output.indexOf('Callstack Depth Attack Vulnerability:  True') >= 0) {
        result_string = result_string + "Exception.";
    }
    if(output.indexOf('Timestamp Dependency:                  True') >= 0) {
        result_string = result_string + "Timestamp."
    }
    if(output.indexOf('Re-Entrancy Vulnerability:             True') >= 0) {
        result_string = result_string + "re-entrancy.";
    }
    if(output.indexOf('Transaction-Ordering Dependence (TOD): True') >= 0) {
        result_string = result_string + "TOD.";
    }
    if(output.indexOf('==== Ether send ====') >= 0) {
        result_string = result_string + "Access control.";
    }
    if(output.indexOf('tx.origin') >= 0) {
        result_string = result_string + "tx.origin.";
    }

    var rawTx = txutils.functionTx(interface, 'setResult', [result_string], txOptions);
    sendRaw(rawTx);
}
