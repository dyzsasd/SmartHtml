# Smart HTML Generator API

Welcome to the Smart HTML Generator API! This tool is designed to help you effortlessly create web pages based on specific requirements.

## Getting Started

To use this API, you can follow these simple steps:

### Step 1: Generate a Web Page

First, you'll need to send your requirements to the API. Here's an example of how to do this using `curl`:

```bash
curl --location 'https://smart-html-37k3xbcrqq-od.a.run.app/api/session' \
--header 'Content-Type: application/json' \
--data '{
    "requirements": "我希望设计一个个人主页，在上面以照片墙的形式展示分享我的照片"
}'
```

In this example, the requirement is to design a personal homepage displaying photos in a photo wall format. You can replace the `requirements` field with your specific webpage needs.

### Step 2: Demonstrate Generated Webpage

After your webpage is generated, you can view it using the following `curl` command:

```bash
curl --location 'https://smart-html-37k3xbcrqq-od.a.run.app/api/session/df973f49-ec58-464a-a080-a824ff054178'
```

This command retrieves the webpage created in Step 1. Note that you should replace the session ID at the end of the URL with the ID of your generated session.

## Conclusion

With these simple steps, you can quickly generate custom web pages to meet your specific needs. Enjoy creating with the Smart HTML Generator API!
