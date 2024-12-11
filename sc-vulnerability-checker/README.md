# Smart Contract Vulnerability Checker

## NEWS!

- This project got 2018 Korea Computer Congress Best Undergraduate Paper Award!
- The paper is written in Korean : http://www.dbpia.co.kr/Journal/ArticleDetail/NODE07503549

## Why do we make this project?

Where code is written in a blockchain such as eiderium, a smart contract is called a smart contract, where errors in the code that is written there can create a number of vulnerabilities. To avoid this vulnerability, tools such as Oyente, Securify, Mythrill, MAIAN, Gasper have been developed, but most of them need source code to detect vulnerability which users cannot have. The project implemented smart contract Kookmin Security Token, which serves as interface and data store, and an analysis server linked to it, making it easy for anyone to send addresses to and receive results from smart contracts.

## Architecture

![architecture](https://github.com/learnitdeep/sc-vulnerability-checker/blob/master/architecture.PNG)  

We created a Kookmin Security Token (KST) smart agreement that complies with the ERC20 standard, which makes it easy for anyone to send addresses of smart contracts that want analysis. Above picture shows the structure of the vulnerability detection service. If the user's account sends the address of the smart contract to KST contract, the vulnerability analysis server checks the status of the KST in real time and takes the vulnerability analysis tool's byte code from the smart contract. The analysis results are sent to the KST contract and the user checks the analysis results through the interface of the KST contract. Communication between the ethereum network and the vulnerability analysis server was implemented using web3.js.

## Result

![result](https://github.com/learnitdeep/sc-vulnerability-checker/blob/master/result.PNG)  

We tested 19 vulnerable smart contract. This dataset is from Ardit Dika, “Ethereum Smart Contracts: Security Vulnerabilities and Security Tools”, NTNU master’s thesis, Dec. 2017
