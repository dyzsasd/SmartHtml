# Smart HTML Generator API

## Introduction
Welcome to the Smart HTML Generator API! This tool is designed to help you effortlessly create web pages based on specific requirements.

## Installation
Please use Python >= 3.11
Please use Node.Js >= 18

```bash
git clone git@github.com:dyzsasd/SmartHtml.git
cd SmartHtml
pip install -r requirements.txt
cp .env.tempalte .env
# create and migrate db schema
bin/migrate.sh
bin/run_dev.sh
```

## Startup
Step 1: Run npm run install-all
Step 2: Run npm run dev

In this example, the requirement is to design a personal homepage displaying photos in a photo wall format. You can replace the `requirements` field with your specific webpage needs.

### Step 2: Demonstrate Generated Webpage

After your webpage is generated, you can view it using the following `curl` command, and the link can be found in previous request response:

```bash
curl --location 'https://smart-html-37k3xbcrqq-od.a.run.app/api/session/df973f49-ec58-464a-a080-a824ff054178'
```

## API Reference
API reference can be found in swagger.yaml
