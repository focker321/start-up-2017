var helper = require('sendgrid').mail;
var sg = require('sendgrid')("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");

function Mail_Sender(from, to) {
  this.from = from;
  this.to = to;
  this.subject = "Hello World from the SendGrid Node.js Library!";
  this.content = "Hello, Email!";
}

module.exports = Mail_Sender;


Mail_Sender.prototype.createMail = function () {
  var from_email = new helper.Email(this.from);
  var to_email = new helper.Email(this.to);
  var subject = this.subject;
  var content = new helper.Content('text/plain', this.content);

  var mail = new helper.Mail(from_email, subject, to_email, content);

  return mail;
};

Mail_Sender.prototype.sendMail = function (mail) {

  var request = sg.emptyRequest({
    method: 'POST',
    path: '/v3/mail/send',
    body: mail.toJSON(),
  });

  sg.API(request, function (error, response) {
    console.log(response.statusCode);
    console.log(response.body);
    console.log(response.headers);
  });


};