# Anonymous by Love, USP
Anonymous was created to create a safe space for USP students to hold meaningful conversations about mental health.
This simulates a group chat where students can share experience or advice, while remaining completely anonymous



## Features
When registered, any message that you sent to the bot will be sent to all other students that are also registered on the bot.
Your message would be accompanied by your username, allowing others to identify messages that are sent.
No other personal information would be shared with anyone in the group.



## General Commands
Below are a list of available commands for users that can be used in the Telegram bot.

### `/start`
Returns a general welcome message.

### `/register <matric number> <password>`
Registers the student into the Anonymous system.
After being registered, students will receive messages that are sent.
The password is specific to each matric number, and will be provided by Love, USP admin.

### `/username`
Shows the student's username.

### `/leave`
Unregisters the student from the Anonymous system.
Afterwards, students will no longer be able to receive messages that are sent.
All details of the student that are stored in the Anonymous system would also be deleted.



## Admin Commands
These commands should only be made known to the admin to prevent misuse.

### `/delete <matric number> <password>`
Unregisters the user with a certain matric number.
This is to ensure that admins can easily remove any user that may be causing distress in the chat.
The password used here is different from the password used in `/register`, and should only be known by the admin.



## FAQs
1) ???

## AWS and Serverless Deployment

### Installing
```
# Open the command window in the bot file location

# Install the Serverless Framework
$ npm install serverless -g

# Install the necessary plugins
$ npm install
```

### Deploying
```
# Update AWS CLI in .aws/credentials

# Deploy it!
$ serverless deploy

# With the URL returned in the output, configure the Webhook
$ curl -X POST https://<your_url>.amazonaws.com/dev/set_webhook
```

### AWS Configurations
1. From the AWS Console, select AWS Lambda.
2. In AWS Lambda, select "anon-group-bot-dev-webhook".
3. Select "Permissions" and select the Lambda role under "Execution role"
4. In AWS IAM, select "Attach policies" under "Permissions" and "Permissions policies"
5. Search for and select "AmazonDynamoDBFullAccess" and "Attach policy"
6. Run the Telegram bot with `/start` and register with `/register`
7. The first attempt at registration should return an error.
8. From the AWS Console, select AWS DynamoDB.
9. Under "Tables", ensure that the "AnonChatTable" table has been created.
10. Re-register with `/register`, and registration should be successful.
