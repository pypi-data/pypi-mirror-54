# Help Scout API Wrapper
This package provide wrapper for Help Scout API 2.0. It gives access to all mailbox endpoints.

## Instalation
You can install it from pypi: `pip install helpscout`

## Authentication
To use API you need to create app and get `app_id` and `app_secret`.
Instructions [here](https://developer.helpscout.com/mailbox-api/overview/authentication/)

## Usage
All endpoint commands and coresponding parameters you can find in [documentation](https://developer.helpscout.com/mailbox-api/)

**Conversations**

| API Endpoint | Wrapper command |
| ------------ | --------------- |
| List conversation | `client.conversation.list(kwargs)` |
| Get conversation | `client.conversation.get(conv_id, kwargs)` |
| Create conversation | `client.conversation.create(kwargs)` |
| Update conversation | `client.conversation.update(conv_id, op, path, value)` |
| Delete conversation | `client.conversation.delete(conv_id)` |
| Get attachemnt data | `client.conversation.attachment.get(conv_id, attach_id)` |
| Upload attachment | `client.conversation.attachment.upload(conv_id, thread_id, file_name, mime_type, data)` |
| Delete attachment | `client.conversation.attachment.delete(conv_id, attach_id)` |
| Update custom fields | `client.conversation.custom_field.update(conv_id, fields)` |
| Update tags | `client.conversation.tag.update(conv_id, tags)` |
| List threads | `client.conversation.thread.list(conv_id)` |
| Update thread | `client.conversation.thread.update(conv_id, thread_id, op, path, value)` |
| Create reply thread | `client.conversation.thread.create_reply_thread(conv_id, kwargs)` |
| Create phone thread | `client.conversation.thread.create_phone_thread(conv_id, kwargs)` |
| Create note | `client.conversation.thread.create_note(conv_id, kwargs)` |
| Create customer thread | `client.conversation.thread.create_customer_thread(conv_id, kwargs)` |
| Create chat thread | `client.conversation.thread.create_chat_thread(conv_id, kwargs)` |

**Customers**

| API Endpoint | Wrapper command |
| ------------ | --------------- |
| List customers | `client.customer.list(kwargs)` |
| Get customer | `client.customer.get(cust_id, kwargs)` |
| Create customer | `client.customer.create(first_name, kwargs)` |
| Update customers | `client.customer.update(cust_id, first_name, kwargs)` |
| Get address | `client.customer.address.get(cust_id)` |
| Create address | `client.customer.address.create(cust_id, city, state, postal_code, country, lines)` |
| Update address | `client.customer.address.update(cust_id, city, state, postal_code, country, lines)` |
| Delete address | `client.customer.address.delete(cust_id)` |
| List chat handler | `client.customer.chat_handler.list(cust_id)` |
| Create chat handler | `client.customer.chat_handler.create(cust_id, type_, value)` |
| Update chat handler | `client.customer.chat_handler.update(cust_id, chat_id, type_, value)` |
| Delete chat handler | `client.customer.chat_handler.delete(cust_id, chat_id)` |
| List email | `client.customer.email.list(cust_id)` |
| Create email | `client.customer.email.create(cust_id, type_, value)` |
| Update email | `client.customer.email.update(cust_id, email_id, type_, value)` |
| Delete email | `client.customer.email.delete(cust_id, email_id)` |
| List phone | `client.customer.phone.list(cust_id)` |
| Create phone | `client.customer.phone.create(cust_id, type_, value)` |
| Update phone | `client.customer.phone.update(cust_id, phone_id, type_, value)` |
| Delete phone | `client.customer.phone.delete(cust_id, phone_id)` |
| List social profile | `client.customer.social_profile.list(cust_id)` |
| Create social profile | `client.customer.social_profile.create(cust_id, type_, value)` |
| Update social profile | `client.customer.social_profile.update(cust_id, profile_id, type_, value)` |
| Delete social profile | `client.customer.social_profile.delete(cust_id, profile_id)` |
| List website | `client.customer.website.list(cust_id)` |
| Create website | `client.customer.website.create(cust_id, type_, value)` |
| Update website | `client.customer.website.update(cust_id, website_id, type_, value)` |
| Delete website | `client.customer.website.delete(cust_id, website_id)` |

**Mailboxes**

| API Endpoint | Wrapper command |
| ------------ | --------------- |
| List mailboxes | `client.mailbox.list()` |
| Get mailbox | `client.mailbox.get(mailbox_id)` |
| List mailbox custom fields | `client.mailbox.mailbox_fields(mailbox_id)` |
| List mailbox folders | `client.mailbox.mailbox_folders(mailbox_id)` |

**Reports**

| API Endpoint | Wrapper command |
| ------------ | --------------- |
| Chat report | `client.report.chat_report(start, end, kwargs)` |
| Email report | `client.report.email_report(start, end, kwargs)` |
| Phone report | `client.report.phone_report(start, end, kwargs)` |
| Company overall report | `client.report.company.overall_report(start, end, kwargs)` |
| Company customers helped | `client.report.company.customers_helped(start, end, kwargs)` |
| Company drilldown | `client.report.company.drilldown(start, end, range_, kwargs)` |
| Conversation overall report | `client.report.conversation.overall_report(start, end, kwargs)` |
| Conversation volumes by channel | `client.report.conversation.volumes_by_channel(start, end, kwargs)` |
| Conversation busiest time of day | `client.report.conversation.busiest_time_of_day(start, end, kwargs)` |
| Conversation drilldown | `client.report.conversation.drilldown(start, end, range_, kwargs)` |
| Conversation drilldown by field | `client.report.conversation.drilldown_by_field(start, end, field, fieldid, kwargs)` |
| Conversation new drilldown | `client.report.conversation.new(start, end, kwargs)` |
| Conversation received messages statistics | `client.report.conversation.received_messages(start, end, kwargs)` |
| Doc overall report | `client.report.doc.overall_report(start, end, kwargs)` |
| Happiness overall report | `client.report.happiness.overall_report(start, end, kwargs)` |
| Happiness ratings report | `client.report.happiness.ratings(start, end, kwargs)` |
| Productivity overall report | `client.report.productivity.overall_report(start, end, kwargs)` |
| Productivity first response time | `client.report.productivity.first_response_time(start, end, kwargs)` |
| Productivity replies sent | `client.report.productivity.replies_sent(start, end, kwargs)` |
| Productivity resolution time | `client.report.productivity.resolution_time(start, end, kwargs)` |
| Productivity resolved | `client.report.productivity.resolved(start, end, kwargs)` |
| Productivity response time | `client.report.productivity.response_time(start, end, kwargs)` |
| User overall report | `client.report.user.overall_report(user, start, end, kwargs)` |
| User conversation history | `client.report.user.conversation_history(user, start, end, kwargs)` |
| User customers helped | `client.report.user.customers_helped(user, start, end, kwargs)` |
| User drilldown | `client.report.user.drilldown(user, start, end, kwargs)` |
| User happiness | `client.report.user.happiness(user, start, end, kwargs)` |
| User happiness drilldown | `client.report.user.happiness_drilldown(user, start, end, kwargs)` |
| User replies | `client.report.user.replies(user, start, end, kwargs)` |
| User resolution | `client.report.user.resolution(user, start, end, kwargs)` |

**Tags**

| API Endpoint | Wrapper command |
| ------------ | --------------- |
| List tags | `client.tag.list(kwargs)` |

**Teams**

| API Endpoint | Wrapper command |
| ------------ | --------------- |
| List teams | `client.team.list(kwargs)` |
| List team members | `client.team.members(team_id, kwargs)` |

**Tags**

| API Endpoint | Wrapper command |
| ------------ | --------------- |
| List tags | `client.tag.list(kwargs)` |

**Tags**

| API Endpoint | Wrapper command |
| ------------ | --------------- |
| List users | `client.user.list(kwargs)` |
| Get user | `client.user.user(user_id)` |
| Get resource owner | `client.user.resource_owner()` |

**Webhook**

| API Endpoint | Wrapper command |
| ------------ | --------------- |
| List webhooks | `client.webhook.list()` |
| Get webhook | `client.webhook.get(webhook_id)` |
| Create webhook | `client.webhook.create(url, events, secret, notification)` |
| Update webhook | `client.webhook.update(webhook_id, url, events, secret, notification)` |
| Delete webhook | `client.webhook.delete(webhook_id)` |

**Workflow**

| API Endpoint | Wrapper command |
| ------------ | --------------- |
| List workflows | `client.workflow.list(kwargs)` |
| Update workflow status | `client.workflow.update_status(workflow_id, op, value, path)` |
| Run manual workflow | `client.workflow.run_manual(workflow_id, conversation_ids)` |

## Examples

**List all conversations**
```python
>>> from helpscout import Client
>>> client = Client('<YOUR_APP_ID>', '<YOUR_APP_SECRET>')
>>> client.conversation.list()
{
  "_embedded" : {
    "conversations" : [ {
      "id" : 10,
      "number" : 12,
      "threads" : 2,
      "type" : "email",
      "folderId" : 11,
      "status" : "closed",
      "state" : "published",
      "subject" : "Help",
      "preview" : "Preview",
      "mailboxId" : 13,
      ...
```
