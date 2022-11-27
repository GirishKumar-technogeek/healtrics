var nodemailer = require('nodemailer');
var express = require('express');
const bodyParser = require('body-parser');
var app = express();
var port = process.env.PORT || 5050;

app.use(bodyParser.urlencoded({ extended: true }));

app.get('/send_mail', (req,res) => {

    var transporter = nodemailer.createTransport({
        service: 'gmail',
        auth: {
          user: 'voidmain0101@gmail.com',
          pass: 'jmstflysyvizxubl'
        }
    });

    var mailOptions = {
        from: req.query.email_from,
        to: req.query.to_email,
        subject: req.query.subject,
        text: req.query.message
    };

    console.log(mailOptions)
      
    transporter.sendMail(mailOptions, function(error, info){
        if (error) {
            res.send({"message":error})
        } else {
            res.send({"message":info.response})
        }
    });
})

var server = app.listen(port, console.log("API listening at " + port))