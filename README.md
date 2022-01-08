# Document Knowledge Engine Solution Accelerator

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
The sample documents used to demo this accelerator are 10 invoice documents that are manually created and can be found [here](https://github.com/eda-ayan/knowledge-engine-solution-accelerator/tree/main/invoice_images). The folder contains 2 different types of invoices each containing 5 documents.

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
- Sample CV documents

### Step 0: Set up the Resources

Initially set up a storage account and a cognitive search resource in Azure portal.

### Step 1: Setup the Environemnt 
After resources are deployed successfully, navigate to the newly created Storage Account in Azure, and upload the sample documents in a new blob container.

The sample documents can be found in [Assets/Sample Documents](https://github.com/AhmedAlmu/cv-knowledge-engine-accelerator/tree/main/Assets/Sample%20Documents) folder. 

Sample documents should be in the same container to be able to use a single SAS URI for them.

### Step 2: Build a Custom Model
From Azure Form Recognizer Studio, train different custom models for different types of documents. To train a custom model, select the fields you want to extract from the document and label them.
![FormRecognizer](https://user-images.githubusercontent.com/25666677/148658436-86c08c49-cfcb-40fb-9186-73c889402cf3.png)

After 2 models are built, compose them and save the model id of the composed model.

![image](https://user-images.githubusercontent.com/25666677/148658472-df230a87-d719-44d5-9bce-f7ea50a58899.png)

### Step 3: Create the Skillset 
#### Step 3a: Custom Skill

In this step we will create an HTTP Trigger Azure Function in Python that consumes the composed model we built. 

In VS Code, create an HTTP Trigger Azure Function in Python, and replace the code in the "init" file with the code provided in [Assets/Function Script](https://github.com/eda-ayan/knowledge-engine-solution-accelerator/blob/main/assets/extract_info.py). 


In Text Extraction, make sure to add the values for the Cognitive Services Key and Endpoint in the script, and add "requests" in the requirments file.

To deploy the function, you can follow the instructions provided in here: [Develop Azure Functions by using Visual Studio Code](https://docs.microsoft.com/en-us/azure/azure-functions/functions-develop-vs-code?tabs=python).

After deploying both custom skill functions, we can procceed to create the Skillset. 

#### Step 3b: Built-in Skills
In Postman, navigate to Create Skillset request. 

For the "Custom Entity Lookup" skills, we need to provide the URL for the CSV lookup tables. You can upload the two files in [Assets/Lookup Tables](https://github.com/AhmedAlmu/cv-knowledge-engine-accelerator/tree/main/Assets/Lookup%20Tables) to the Storage Account, and get their SAS URL to be used in the skill definition. After both URLs are provided, run the request.  

This will create a Skillstet in the Search Service that identifies all the information to be extracted from the CVs.

### Step 4: Create the Index
In Postman, navigate to Create Index and run the request. 

This will create an Index in the Search Service for the information to be extracted from the CVs as mentioned earlier.

### Step 5: Create the Indexer
In Postman, navigate to Create Indexer and run the request. 

This will create an Indexer in the Search Service that will exctract the defined information from the CVs.

### Step 6: Create the Web App Interface
In [Assets/Website Template](https://github.com/AhmedAlmu/cv-knowledge-engine-accelerator/tree/main/Assets/Website%20Template), open the solution file "CognitiveSearch.Template.sln" in Visual Studio. 

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
This accelerator was inspired by the [Knowledge Mining Solution Accelerator](https://github.com/Azure-Samples/azure-search-knowledge-mining).

## License
For all licensing information refer to [LICENSE](https://github.com/AhmedAlmu/cv-knowledge-engine-accelerator/blob/main/LICENSE).
