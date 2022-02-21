# Document Knowledge Engine Solution Accelerator
https://github.com/eda-ayan/knowledge-engine-solution-accelerator/blob/main/invoice_demo.mp4
## About this accelerator
The Document Knowledge Engine solution accelerator aims to provides a quick way of creating an intelligent search engine, that enables searching and filtering through invoice and receipt documents. It leverages Knowledge Mining and Cognitive Services technologies, to extract all the valuable information and insights from the incoive documents, like company names, total, serial number, date, ..etc. It also creates an intuitive, easy-to-navigate user interface, that allows for a full search experience with capabilities like searching with search terms, customized filters, and informative result cards. Moreover, the extracted information can also be exported to Power BI and used to create informative dashboards, to give a high level overview of the information extracted. 

### Resources and Architecture 
- Storage Account 
- Cognitive Search 
- Cognitive Services
- Azure Function 
- App Service

![Architecture](https://user-images.githubusercontent.com/88718044/139073235-eb6b8b2c-3577-405e-b974-82bc951676dc.png)

### Sample Documents 
The sample documents used to demo this accelerator are 10 invoice documents that are manually created and can be found [here](https://github.com/eda-ayan/knowledge-engine-solution-accelerator/tree/main/assets/Sample%20Documents). The folder contains 2 different types of invoices each containing 5 documents.

### Extracted Information
The information and isights extracted from the invoice documents are: 

- Receiver name 
- Company name
- Date
- Serial number 
- General total 

### Web App Interface
The first interface created to display the extracted insights is a website interface, that can be used to search and filter through the invoice documents.

#### Home Page
![Home Page](https://user-images.githubusercontent.com/88718044/139071306-6595000e-a33c-4dca-85eb-ed6c475d66cf.jpeg)


#### Search Results
![Search Results](https://user-images.githubusercontent.com/25666677/148658186-57a8614b-2a34-4efe-8f49-bd454fd0077c.png)

### PowerBI Dashboard
COMING SOON

## Deployemnt Process
Deploying the accelerator can be done in seven simple steps, that cover every aspect from deploying the resources, creating the search service elements, and conecting to the web interface. 

### Prerequisites
In order to deploy the accelerator, clone or download this repository, and make sure the following requirements are met:
- Azure Subscription 
- Visual Studio 2019 or later
- VS Code with Azure Functions extension
- Sample documents

### Step 0: Set up the Resources

Initially set up a Storage Account and a Cognitive Search resource in Azure portal.

### Step 1: Setup the Environemnt 
After resources are deployed successfully, navigate to the newly created Storage Account in Azure, and upload the sample documents in a new blob container. The sample documents can be found in [Assets/Sample Documents](https://github.com/eda-ayan/knowledge-engine-solution-accelerator/tree/main/assets/Sample%20Documents) folder. Sample documents should be in the same container to be able to use a single SAS URI for them.

### Step 2: Build a Custom Model
From Azure Form Recognizer Studio, train different custom models for different types of documents. To train a custom model, select the fields you want to extract from the document and label them.
![FormRecognizer](https://user-images.githubusercontent.com/25666677/148658436-86c08c49-cfcb-40fb-9186-73c889402cf3.png)

After 2 models are built, compose them and save the model id of the composed model.

![image](https://user-images.githubusercontent.com/25666677/148658472-df230a87-d719-44d5-9bce-f7ea50a58899.png)

### Step 3: Create the Custom Skill 

In this step we will create an HTTP Trigger Azure Function in Python that consumes the composed model we built. In VS Code, create an HTTP Trigger Azure Function in Python, and replace the code in the "init" file with the code provided in [Assets/Function Script](https://github.com/eda-ayan/knowledge-engine-solution-accelerator/blob/main/assets/extract_info.py). 

In the init file, make sure to add the values for the Form Recognizer Services Key, Endpoint and model id in the script.
You also need to obtain a SAS URL for the container you hold the documents. Instructions on how to generate SAS URLs: [Generate SAS tokens for storage containers](https://www.google.com/search?q=how+to+obtain+azure+blob+storage+container+sas+url&rlz=1C1GCEU_trTR970TR970&oq=how+to+obtain+azure+blob+storage+container+sas+url&aqs=chrome..69i57.14028j0j4&sourceid=chrome&ie=UTF-8)

To deploy the function, you can follow the instructions provided in here: [Develop Azure Functions by using Visual Studio Code](https://docs.microsoft.com/en-us/azure/azure-functions/functions-develop-vs-code?tabs=python).

After deploying both custom skill functions, we can procceed to create the Skillset. 

### Step 4: Create Skillset, Index & Indexer
In the Cognitive Search resource created before, click on "import data". Chose the location of your documents as the data source. Then click on "Add Cognitive Skills". Attach a Cognitive Services Resource. Then in the "add enrichments" section, specify a name for your skillset. In the next tab, specify the name of your index. Add the features you extracted from the document as new fields. Select the appropriate types for the fields. 

![image](https://user-images.githubusercontent.com/25666677/148659506-d1ed5665-175d-4e9e-9b23-7cb59517bbd9.png)

This will create an Index in the Search Service for the information to be extracted from the documents as mentioned earlier. Switch to the next tab to name the indexer, then submit. This will create an Indexer in the Search Service that will exctract the defined information from the invoices.

### Step 5: Add the Custom Skill

After your index and indexer are created, we need to modify the skillset to add the custom skill we created. In the Search Service page, move to the Skillsets tab and choose the skillset you created. Add the json object in [skills.txt](https://github.com/eda-ayan/knowledge-engine-solution-accelerator/blob/main/assets/Custom%20Skill%20Script/skill.txt) to the skillset definition as described in the [tutorial](https://docs.microsoft.com/en-us/azure/search/cognitive-search-custom-skill-interface). Don't forget to update the function uri with the name of your function and trigger.

### Step 6: Update the Indexer

The skillset we created takes the name of the file as the input and outputs the desired values. But these outputs should also be added to the indexer. Navigate to the indexer tab and choose the indexer you created. Open the indexer definition json file and your output labels to the outputFieldMappings as below.

![image](https://user-images.githubusercontent.com/25666677/148660047-55e215ef-8c7b-473b-96d6-05f54d6984fe.png)

Then save, reset and run the indexer. 

### Step 6: Create the Web App Interface
In [Assets/Website Template](https://github.com/eda-ayan/knowledge-engine-solution-accelerator/tree/main/assets/Website%20Template), open the solution file "CognitiveSearch.Template.sln" in Visual Studio. 

Navigate to the "appsettings.json" file, and change the values according to the following table:

| Placeholder Value | Value to replace |
| ------ | ------ |
| <SEARCH_SERVICE_NAME> | Name of Cognitive Search Service |
| <SEARCH_SERVICE_KEY> | Admin Key of Cognitive Search Service |
| <INDEX_NAME> | Index Name in Search Service |
| <INDEXER_NAME> | Indexer Name in Search Service |
| <STORAGE_ACCOUNT_NAME> | Storage Account Name that stores the documents |
| <STORAGE_ACCOUNT_KEY> | Storage Account Key |
| <CONTAINER_NAME> | Container Name in Storage Account that stores the documents |

You can test the website locally by running the solution in Visual Studio, or publish the website to Azure by following the instructions found here: [Quickstart: Publish an ASP.NET web app](https://docs.microsoft.com/en-US/visualstudio/deployment/quickstart-deploy-aspnet-web-app?view=vs-2019&tabs=azure).

### Step 7: Create the PowerBI Dashboard
COMING SOON

## References 
This accelerator was inspired by the [Knowledge Mining Solution Accelerator](https://github.com/Azure-Samples/azure-search-knowledge-mining) and [CV Knowledge Engine Solution Accelerator](https://github.com/AhmedAlmu/cv-knowledge-engine-accelerator).

## License
Copyright (c) Microsoft Corporation. All rights reserved.

Licensed under [MIT License](https://github.com/eda-ayan/knowledge-engine-solution-accelerator/blob/main/LICENSE).
