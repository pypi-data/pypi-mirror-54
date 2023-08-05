<img src="https://www.activeledger.io/wp-content/uploads/2018/09/Asset-23.png" alt="Activeledger" width="500"/>


# Activeledger Python SDK

Welcome to Python SDK for Activeledger. This SDK facilitates the user in sending the transactions to the ledger against a smart contract.

## Prerequisites

- Currently only python 3.5+ version is suported


## Installing

- Simply download the sdk with the following command:

```
pip install activeLedger-sdk
```

## Usage

The SDK currently supports the following functionality

- Connection handling
- Key generation
- Key onboarding
- Transaction building


 ### Initialization and Connection Handlilng 
 ```
conn=Connection.Connection()
conn.setConnection(<protocol>,<host>,<port>)

 ```       

### Generating KeyPair
```
  keyObject = key.Key('rsa')
  keyObject.generate_key()

```

### Key onboarding
```
  user_object = user.User()
  user_object.add_key(keyObject)
  id = user_object.onboard_key(<keyName>, conn.getConnectionURL())

```
    
### Transaction Building    
 Transaction class has 2 functions which you can use for building the Transaction.



 Build the TxObject and send it to either
 1) createTransaction(selfsign,Territoriality,streamID,keyObject,keyName,keyType) - creates the Transaction Object
 	- You can update the sigs object if needed in the returned Transaction Object.
	- To use the territoriality, pass the nodeID. Otherwise None.
	- If transaction is self signed , send true otherwise false
	- Use sendTransaction(Transaction,conn) to send the transaction to activeledger
 2) createAndSendTransation(conn,selfsign,Territoriality,streamID,keyObject,keyName,keyType) - creates and sends the transaction to Activeledger. 
 	- You will get a Response object in return which will give you either the streamID or error.
 
```
tx=transaction.baseTransaction()
tx.set_contract('user')
tx.set_namespace("healthtestnet")
tx.set_entry("update")

i={<streamId>:{}} #dict
tt.set_i(i)
o={} #dict
tt.set_o(o) 

# Creating complete transaction
txResp=tx.createTransaction(selfsign,Territoriality,streamID,keyObject,keyName,keyType)
# Sending Transaction
tx.sendTransaction(txResp,conn)

or

# Creates and Send the tRansaction to Activeledger. Returns Response object.
tx.createAndSendTransaction(conn,selfsign,Territoriality,streamID,keyObject,keyName,keyType);

```

## Events Subscription

SDK contains different helper functions in Events Package for the purpose of subscribing to different events.

- subscribe(host,port)host=http://ip:port
- subscribeStream(host,port,stream)
- contractEventSubscribe(host,port,contract,event)
- contractSubscribe(host,port,contract)
- eventsubscribe(host,port)

They all return events which can then be used by developers.

## ActivityStreams

SDK also contains helper functions in ActivityStreams package to get and search streams from Activeledger.
- getActivityStreams(host,ids) //multiple streams.host=http://ip:port
- getActivityStream(host, id) //single stream
- getActivityStreamVolatile(host, id)
- setActivityStreamVolatile(host,id,body) // Anything in the bdy will be written to that location for that stream id.
- getActivityStreamChanges(host)
- searchActivityStreamPost(host,query)//post request
- searchActivityStreamGet(host,query)//get Request
- findTransaction(host,umid)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details