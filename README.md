# Inspiced a Chef Transformer Backend

This application allows you to pass through an array of ingredients and it will return a list of recipes that you can make with those ingredients.

**Input**

``` 
 [
    "chicken",
    "onion",
    "garlic",
    "ginger",
    "soy sauce",
    "sesame oil",
    "rice",
    "salt",
    "pepper"
]

```

**Output**

```
[TITLE]: Chicken wings
[INGREDIENTS]:
 - 1: 3 lb. chicken wings
 - 2: 4 tbsp. mazola
 - 3: 2 tbsp. mazola
[DIRECTIONS]:
 - 1: Preheat oven to 350.
 - 2: Arrange wings in single layer on baking pan. bake for 40 minutes or until brown, turning once.
  - 3: Spray cookie sheet with pam and spread chicken wings on pan.
  - 4: Pour 1 teaspoon mazola on each wing and bake for an additional 20 minutes, until chicken is done.
  - 5: Put fried wings on cookie sheet and bake for 2 to 3 minutes.
----------------------------------------------------------------------------------------------------------------------------------
```




Using this [Deployment Guide](https://www.eliasbrange.dev/posts/deploy-fastapi-on-aws-part-2-fargate-alb/) I was able to create this repository that will allow you to deploy Chef Transformer on AWS.

## Missing Features

At the moment the recipes are not stored in a database. They will just be printed to the console. **As I do not have access to a database or the resources to host one** so I will not be able to implement this feature. If you would like to contribute to this project, please feel free to do so. 

## Prerequisites for Local Development

- Python 3.8
- Docker

## Prerequisites for Deployment

- AWS Account
- AWS CLI
- AWS CDK


## Deploying Locally with Docker

run the following command to build the docker image:

``` docker-compose up --build```

You can then access the application at ```localhost:3000/docs```

## Deploying to AWS

You would need to do the following steps:


1. Create a virtual environment:

``` python3 -m venv .env ```

2. Activate virtual environment:

``` source .env/bin/activate ```

3. Install the requirements:

``` pip install -r requirements.txt ```

4. Ensure you have the AWS CLI installed and configured with your credentials. You can find the instructions [here](https://docs.aws.amazon.com/cdk/v2/guide/work-with.html#work-with-prerequisites).

5. cd into the cdk directory and run the following command:

``` cdk deploy ```

The application will be deployed to AWS and you can access the application at the URL provided in the output.

# Possible Issues

Chef Transformer is a compute intensive task. You may want to scale the application to handle more requests. This can be modified in the ```inspiced/cdk/fastapi.py``` file. You can change the number of tasks and the memory allocated to each task. 
