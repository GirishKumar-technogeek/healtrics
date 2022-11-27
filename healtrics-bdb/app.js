var express = require('express');
var app = express();
var port = process.env.PORT || 6000;
const driver = require('bigchaindb-driver');
const API_PATH = 'https://test.ipdb.io/api/v1/';
const axios = require('axios')

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

/*
{
  "request_id": 1234,
  "donor_type": "Donor",
  "blood_bank_id": "None",
  "donor_id": 7894,
  "donation_date_time": 09-10-2022 18:44,
  "donation_type":"Whole Blood",
  "blood_type":"O+",
  "donated_quantity":1200,
}
*/

app.get('/bdb_write', function(req,res){

    const key_pair = new driver.Ed25519Keypair();
    const privateKey = key_pair.privateKey;
    const publicKey = key_pair.publicKey;
    const request_id = req.query.request_id;
    const donor_type = req.query.donor_type;
    const blood_bank_id = req.query.blood_bank_id;
    const donor_id = req.query.donor_id;
    const donation_date_time = req.query.donation_date_time;
    const donation_type = req.query.donation_type;
    const blood_type = req.query.blood_type;
    const donated_quantity = req.query.donated_quantity;

    const conn = new driver.Connection(API_PATH);
    const assetdata = {
        'donation': {
            'request_id': request_id,
            'donor_type': donor_type,
            'blood_bank_id': blood_bank_id,
            'donor_id': donor_id,
            'donation_date_time': donation_date_time,
            'donation_type': donation_type,
            'blood_type': blood_type,
            'donated_quantity': donated_quantity
        }
    }
    const assetCreateTx = driver.Transaction.makeCreateTransaction(
        assetdata,
        null,
        [ 
            driver.Transaction.makeOutput( driver.Transaction.makeEd25519Condition('' + publicKey))
        ],
        publicKey
    )
    const assetCreateTxSigned = driver.Transaction.signTransaction(assetCreateTx, privateKey)
    conn.postTransactionCommit(assetCreateTxSigned)
    txid = assetCreateTxSigned.id
    res.send({
        'transaction_id' : txid
    })

})

app.get('/bdb_read', (req,res) => {
    axios.get("https://test.ipdb.io/api/v1/transactions/" + req.query.transaction_id)
  .then(resp => {
    console.log(resp); 
    res.send(resp.data)
  })
  .catch(err => res.send(err))
})

var server = app.listen(port, console.log("API listening at " + port))