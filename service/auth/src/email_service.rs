// email_service.rs
use crate::errors::ServiceError;
use crate::models::Invitation;
use sparkpost::transmission::{
    EmailAddress, Message, Options, Recipient, Transmission, TransmissionResponse,
};

lazy_static::lazy_static! {
static ref API_KEY: String = std::env::var("SPARKPOST_API_KEY").expect("SPARKPOST_API_KEY must be set");
}

pub fn send_invitation(invitation: &Invitation) -> Result<(), ServiceError> {
    let tm = Transmission::new_eu(API_KEY.as_str());
    let sending_email =
        std::env::var("SENDING_EMAIL_ADDRESS").expect("SENDING_EMAIL_ADDRESS must be set");
    // new email message with sender name and email
    let mut email = Message::new(EmailAddress::new(sending_email, "Register on chillpaper.fr"));

    let options = Options {
        open_tracking: false,
        click_tracking: false,
        transactional: true,
        sandbox: false,
        inline_css: false,
        start_time: None,
    };

    // recipient from the invitation email
    let recipient: Recipient = invitation.email.as_str().into();

    let email_body = format!(

        "
<!DOCTYPE html>
<html>
<head>
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  <title>Registration Confirmation</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      padding: 20px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 20px;
    }}
    td {{
      padding: 10px 20px;
    }}
    td, th {{
      border: 1px solid #ddd;
      text-align: left;
    }}
    th {{
      background-color: #f2f2f2;
    }}
    h1 {{
      color: #333;
    }}
    .container {{
      background-color: #f2f2f2;
      padding: 20px;
      border-radius: 5px;
      text-align: center;
    }}
    /* Add some border radius */
    .btn {{
      background-color: #4CAF50;
      color: white;
      padding: 12px 20px;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      margin-top: 10px;
      text-decoration: none;
    }}
    /* Add some text color */
    .btn:hover {{
      background-color: #45a049;
    }}
  </style>
</head>
<body>
<h1>Registration Confirmation</h1>
<div class=\"container\">
  <p>Thank you for registering with our site! Your account has been created and you can now log in.</p>
  <a href=\"https://chillpaper.fr/register/{}?email={}\" class=\"btn\">Log In</a>
    your Invitation expires on <strong>{}</strong>

</div>
</body>
</html>
         ",
        invitation.id,
        invitation.email,
        invitation
            .expires_at
            .format("%I:%M %p %A, %-d %B, %C%y")
            .to_string()
    );

    // complete the email message with details
    email
        .add_recipient(recipient)
        .options(options)
        .subject("You have been invited to register on chillpaper.fr")
        .html(email_body);

    let result = tm.send(&email);

    // Note that we only print out the error response from email api
    match result {
        Ok(res) => match res {
            TransmissionResponse::ApiResponse(api_res) => {
                println!("API Response: \n {:#?}", api_res);
                Ok(())
            }
            TransmissionResponse::ApiError(errors) => {
                println!("Response Errors: \n {:#?}", &errors);
                Err(ServiceError::InternalServerError)
            }
        },
        Err(error) => {
            println!("Send Email Error: \n {:#?}", error);
            Err(ServiceError::InternalServerError)
        }
    }
}
